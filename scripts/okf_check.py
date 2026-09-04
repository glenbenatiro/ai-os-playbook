#!/usr/bin/env python3
"""Open Knowledge Format (OKF) v0.2 conformance checker.

Checks that a directory tree is a conformant OKF v0.2 knowledge bundle:

  1. every non-reserved `.md` file carries a parseable YAML frontmatter block;
  2. every frontmatter carries a non-empty `type`;
  3. the reserved files `index.md` and `log.md` hold no frontmatter, except the
     bundle-root `index.md`, which declares `okf_version` and nothing else.

It also lints the v0.2 field families (`generated`, `verified`, `status`,
`stale_after`, `sources`) and warns about leftovers from OKF v0.1.

    okf_check.py <bundle-root> [--strict] [--allow-placeholders]
                 [--exclude REL_PATH ...] [--quiet]

`--allow-placeholders` accepts `{{TOKENS}}` where a datetime, actor or version
is required, so an unfilled template scaffold can be checked. `--strict` adds a
second opinion from PyYAML when it is installed, catching frontmatter this
parser reads leniently but a strict YAML consumer would reject.

Stdlib only. Exit codes: 0 clean, 1 findings, 2 usage or IO error.
"""

import argparse
import os
import re
import sys
from datetime import datetime

OKF_VERSION = '0.2'

PRUNE_DIRS = {
    '.git', '.obsidian', '.claude', '.trash', '_dump',
    'node_modules', '.github', '.playwright-mcp',
}
# CLAUDE.md is a one-line `@AGENTS.md` import shim for Claude Code, not a
# concept document, so it cannot carry frontmatter and is not checked.
SHIM_FILES = {'CLAUDE.md'}
RESERVED_FILES = {'index.md', 'log.md'}
STATUS_VALUES = {'draft', 'stable', 'deprecated'}

DATETIME_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})$'
)
ACTOR_RE = re.compile(r'^(?:human:[^\s/]+|process:[^\s/]+|[A-Za-z0-9_.-]+/\S+)$')
PLACEHOLDER_RE = re.compile(r'^\{\{[A-Z_]+\}\}$')

# ---------------------------------------------------------------- frontmatter
# A deliberately small YAML-subset parser. OKF bundles are hand-written markdown
# and must stay readable with nothing installed, so this covers exactly the
# shapes that appear in frontmatter and refuses anything it cannot read rather
# than guessing. Values are returned as strings - no type coercion - which
# matches the OKF reference consumer (it disables the YAML 1.1 timestamp
# resolver so dates stay strings too).

BLOCK_RE = re.compile(
    r'^(?P<bom>﻿?)---[ \t]*\r?\n(?P<fm>.*?\r?\n)?---[ \t]*(?:\r?\n|\Z)',
    re.S,
)
KEY_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_.-]*):(?:[ \t]+(.*))?$')


class ParseError(Exception):
    def __init__(self, line, message):
        super().__init__(message)
        self.line = line          # 0-based, relative to the frontmatter body
        self.message = message


def split_frontmatter(text):
    """Return (block_text, body_offset) for a leading --- block, else None.

    Raises ParseError when the file opens a block it never closes.
    """
    if not text.startswith('﻿---') and not text.startswith('---'):
        return None
    match = BLOCK_RE.match(text)
    if match is None:
        raise ParseError(0, 'frontmatter opened but never closed')
    return match.group(0), match.end()


def strip_comment(raw):
    """Drop a trailing ` #comment` from a plain (unquoted) scalar."""
    out, quote, i = [], None, 0
    while i < len(raw):
        char = raw[i]
        if quote:
            out.append(char)
            if char == quote:
                quote = None
        elif char in '\'"' and not out:
            quote = char
            out.append(char)
        elif char == '#' and (i == 0 or raw[i - 1] in ' \t'):
            break
        else:
            out.append(char)
        i += 1
    return ''.join(out).rstrip()


def _unquote(raw):
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    return raw


def _split_items(raw):
    """Split a flow collection body on commas that sit outside quotes."""
    items, depth, quote, current = [], 0, None, []
    for char in raw:
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in '\'"':
            quote = char
        elif char in '[{':
            depth += 1
        elif char in ']}':
            depth -= 1
        elif char == ',' and depth == 0:
            items.append(''.join(current).strip())
            current = []
            continue
        current.append(char)
    tail = ''.join(current).strip()
    if tail:
        items.append(tail)
    return items


TEMPLATE_TOKEN_RE = re.compile(r'^\{\{[A-Za-z_][A-Za-z0-9_]*\}\}$')


def parse_value(raw, line):
    raw = raw.strip()
    if raw.startswith(('|', '>')):
        raise ParseError(line, 'block scalars are not supported in frontmatter')
    if TEMPLATE_TOKEN_RE.match(raw):
        # An unfilled scaffold placeholder, not a flow mapping.
        return raw
    if raw.startswith('['):
        if not raw.endswith(']'):
            raise ParseError(line, 'unterminated inline list')
        return [parse_value(item, line) for item in _split_items(raw[1:-1])]
    if raw.startswith('{'):
        if not raw.endswith('}'):
            raise ParseError(line, 'unterminated flow mapping')
        mapping = {}
        for item in _split_items(raw[1:-1]):
            match = KEY_RE.match(item) or re.match(r'^([A-Za-z_][\w.-]*):(.*)$', item)
            if not match:
                raise ParseError(line, 'expected key: value inside flow mapping')
            mapping[match.group(1)] = parse_value(match.group(2) or '', line)
        return mapping
    if raw.startswith(('\'', '"')):
        return _unquote(strip_comment(raw))
    raw = strip_comment(raw)
    if raw in ('', '~', 'null'):
        return None
    return raw


def _is_blank(line):
    return not line.strip() or line.lstrip().startswith('#')


def _indent(line):
    return len(line) - len(line.lstrip())


def parse_block(lines, base=0, depth=0):
    """Parse frontmatter lines (delimiters removed) into a dict."""
    if depth > 2:
        raise ParseError(base, 'frontmatter nested too deeply')
    out, i = {}, 0
    while i < len(lines):
        line = lines[i]
        if _is_blank(line):
            i += 1
            continue
        if _indent(line) != 0:
            raise ParseError(base + i, 'unexpected indent')
        match = KEY_RE.match(line)
        if not match:
            raise ParseError(base + i, 'expected "key: value"')
        key, raw = match.group(1), match.group(2)
        if key in out:
            raise ParseError(base + i, 'duplicate key %r' % key)
        if raw is None or not raw.strip():
            nested, consumed = _parse_nested(lines, i + 1, base, depth)
            if consumed:
                out[key] = nested
                i += 1 + consumed
                continue
            out[key] = None
        else:
            out[key] = parse_value(raw, base + i)
        i += 1
    return out


def _parse_nested(lines, start, base, depth):
    """Read an indented mapping or a block list following an empty key."""
    j = start
    while j < len(lines) and _is_blank(lines[j]):
        j += 1
    if j >= len(lines):
        return None, 0
    line = lines[j]
    is_list = line.lstrip().startswith('- ') or line.strip() == '-'
    if _indent(line) == 0 and not is_list:
        return None, 0

    block, k = [], j
    while k < len(lines):
        if _is_blank(lines[k]):
            block.append(lines[k])
            k += 1
            continue
        stripped = lines[k].lstrip()
        if _indent(lines[k]) == 0 and not (stripped.startswith('- ') or stripped == '-'):
            break
        block.append(lines[k])
        k += 1
    while block and _is_blank(block[-1]):
        block.pop()
        k -= 1

    if is_list:
        return _parse_list(block, base + j, depth), k - start
    inner = min(_indent(x) for x in block if not _is_blank(x))
    dedented = [x[inner:] if not _is_blank(x) else x for x in block]
    return parse_block(dedented, base + j, depth + 1), k - start


def _parse_list(block, base, depth):
    items, current, current_lines = [], None, None
    for offset, line in enumerate(block):
        if _is_blank(line):
            continue
        stripped = line.lstrip()
        if stripped.startswith('- ') or stripped == '-':
            if current_lines is not None:
                items.append(_finish_item(current, current_lines, base, depth))
            current = stripped[2:].strip() if stripped != '-' else ''
            current_lines = []
        else:
            if current_lines is None:
                raise ParseError(base + offset, 'expected a "- " list item')
            current_lines.append(stripped)
    if current_lines is not None:
        items.append(_finish_item(current, current_lines, base, depth))
    return items


def _finish_item(head, tail, base, depth):
    if not tail:
        return parse_value(head, base) if head else None
    mapping = {}
    for raw in ([head] if head else []) + tail:
        match = KEY_RE.match(raw)
        if not match:
            raise ParseError(base, 'expected "key: value" in list item')
        mapping[match.group(1)] = parse_value(match.group(2) or '', base)
    return mapping


def parse_frontmatter(text):
    """Return (frontmatter_dict_or_None, block_text_or_None)."""
    split = split_frontmatter(text)
    if split is None:
        return None, None
    block, _ = split
    inner = block.split('\n', 1)[1]
    inner = inner.rsplit('---', 1)[0]
    lines = inner.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return parse_block([line.rstrip('\r') for line in lines]), block

# ---------------------------------------------------------------------- rules

class Finding:
    def __init__(self, level, path, code, detail=''):
        self.level = level
        self.path = path
        self.code = code
        self.detail = detail

    def __str__(self):
        tail = ': %s' % self.detail if self.detail else ''
        return '%-6s %s: %s%s' % (self.level, self.path, self.code, tail)


def is_datetime(value, placeholders):
    if placeholders and isinstance(value, str) and PLACEHOLDER_RE.match(value):
        return True
    if not isinstance(value, str) or not DATETIME_RE.match(value):
        return False
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return False
    return True


def is_actor(value, placeholders):
    if placeholders and isinstance(value, str) and PLACEHOLDER_RE.match(value):
        return True
    return isinstance(value, str) and bool(ACTOR_RE.match(value))


def check_fields(rel, fm, placeholders):
    """Lint the OKF v0.2 field families. Returns a list of findings."""
    out = []
    add = lambda level, code, detail='': out.append(Finding(level, rel, code, detail))

    generated = fm.get('generated')
    if generated is not None:
        if not isinstance(generated, dict) or not generated.get('by'):
            add('FAIL', 'generated-shape', 'expected a mapping with a non-empty `by`')
        else:
            if not is_actor(generated['by'], placeholders):
                add('WARN', 'actor-format', 'generated.by = %r' % generated['by'])
            if not is_datetime(generated.get('at'), placeholders):
                add('FAIL', 'generated-at',
                    'expected an ISO 8601 datetime with offset, got %r'
                    % (generated.get('at'),))

    verified = fm.get('verified')
    if verified is not None:
        entries = verified if isinstance(verified, list) else [verified]
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get('by'):
                add('FAIL', 'verified-shape', 'each entry needs `by` and `at`')
                continue
            if not is_actor(entry['by'], placeholders):
                add('WARN', 'actor-format', 'verified.by = %r' % entry['by'])
            if not is_datetime(entry.get('at'), placeholders):
                add('FAIL', 'verified-at',
                    'expected an ISO 8601 datetime with offset, got %r'
                    % (entry.get('at'),))

    status = fm.get('status')
    if status is not None and status not in STATUS_VALUES:
        add('FAIL', 'status-vocab',
            'OKF reserves `status` for %s; vault lifecycle values belong in '
            '`stage`, got %r' % ('/'.join(sorted(STATUS_VALUES)), status))

    if fm.get('stale_after') is not None and not is_datetime(fm['stale_after'], placeholders):
        add('FAIL', 'stale-after',
            'expected an ISO 8601 datetime with offset, got %r' % (fm['stale_after'],))

    sources = fm.get('sources')
    if sources is not None:
        if not isinstance(sources, list):
            add('FAIL', 'sources-shape', 'expected a list of mappings')
        else:
            for entry in sources:
                if not isinstance(entry, dict) or not entry.get('resource'):
                    add('FAIL', 'sources-shape', 'each source needs a `resource`')

    if 'timestamp' in fm:
        add('WARN', 'legacy-timestamp',
            'OKF v0.1 field; use `generated: {by, at}`')
    if not fm.get('title'):
        add('WARN', 'missing-title')
    if not fm.get('description'):
        add('WARN', 'missing-description')
    if str(fm.get('stage', '')).lower() == 'retired' and fm.get('status') != 'deprecated':
        add('WARN', 'stage-retired-not-deprecated',
            'a retired note should also carry `status: deprecated`')
    return out


def check_file(root, rel, placeholders, strict):
    path = os.path.join(root, rel)
    findings = []
    try:
        with open(path, encoding='utf-8') as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        return [Finding('FAIL', rel, 'unreadable', str(exc))]

    name = os.path.basename(rel)
    is_root_index = rel == 'index.md'
    reserved = name in RESERVED_FILES

    try:
        fm, block = parse_frontmatter(text)
    except ParseError as exc:
        return [Finding('FAIL', rel, 'frontmatter-parse',
                        'line %d: %s' % (exc.line + 2, exc.message))]

    if reserved:
        if is_root_index:
            if fm is None:
                return [Finding('FAIL', rel, 'missing-okf-version',
                                'the bundle-root index.md must declare '
                                'okf_version: "%s"' % OKF_VERSION)]
            extra = sorted(key for key in fm if key != 'okf_version')
            if extra:
                findings.append(Finding(
                    'FAIL', rel, 'reserved-frontmatter',
                    'the root index.md carries only okf_version; remove %s'
                    % ', '.join(extra)))
            version = fm.get('okf_version')
            if version is None:
                findings.append(Finding('FAIL', rel, 'missing-okf-version'))
            elif not (placeholders and isinstance(version, str)
                      and PLACEHOLDER_RE.match(version)) and str(version) != OKF_VERSION:
                findings.append(Finding('FAIL', rel, 'okf-version',
                                        'expected %r, got %r' % (OKF_VERSION, version)))
        elif fm is not None:
            findings.append(Finding(
                'FAIL', rel, 'reserved-frontmatter',
                'OKF reserved files carry no frontmatter'))
        return findings

    if fm is None:
        return [Finding('FAIL', rel, 'no-frontmatter',
                        'every concept document opens with a --- block')]
    if not fm.get('type'):
        findings.append(Finding('FAIL', rel, 'missing-type',
                                '`type` is the one required OKF field'))
    findings.extend(check_fields(rel, fm, placeholders))
    if strict and block is not None:
        findings.extend(strict_findings(rel, block))
    return findings


def strict_findings(rel, block):
    """Second opinion from PyYAML, mirroring the OKF reference consumer."""
    try:
        import yaml
    except ImportError:
        return []
    loader = getattr(strict_findings, '_loader', None)
    if loader is None:
        class Loader(yaml.SafeLoader):
            pass
        Loader.yaml_implicit_resolvers = {
            key: [(tag, regexp) for tag, regexp in value
                  if tag != 'tag:yaml.org,2002:timestamp']
            for key, value in yaml.SafeLoader.yaml_implicit_resolvers.items()
        }
        loader = strict_findings._loader = Loader
    inner = block.split('\n', 1)[1].rsplit('---', 1)[0]
    try:
        yaml.load(inner, Loader=loader)
    except yaml.YAMLError as exc:
        detail = ' '.join(str(exc).split())
        return [Finding('STRICT', rel, 'yaml-parse', detail)]
    return []


def iter_markdown(root, excludes):
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = '' if rel_dir == '.' else rel_dir
        dirnames[:] = sorted(
            name for name in dirnames
            if name not in PRUNE_DIRS
            and os.path.join(rel_dir, name).replace(os.sep, '/') not in excludes
        )
        for name in sorted(filenames):
            if not name.endswith('.md') or name in SHIM_FILES:
                continue
            rel = os.path.join(rel_dir, name).replace(os.sep, '/')
            if rel not in excludes:
                yield rel


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='okf_check.py',
        description='Check an OKF v%s knowledge bundle for conformance.' % OKF_VERSION)
    parser.add_argument('root', help='bundle root directory')
    parser.add_argument('--strict', action='store_true',
                        help='promote warnings to failures and add a PyYAML parse check')
    parser.add_argument('--allow-placeholders', action='store_true',
                        help='accept {{TOKENS}} where a datetime, actor or version is required')
    parser.add_argument('--exclude', action='append', default=[], metavar='REL_PATH',
                        help='skip this file or directory (repeatable)')
    parser.add_argument('--quiet', action='store_true',
                        help='print the summary line only')
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.stderr.write('okf_check.py: not a directory: %s\n' % args.root)
        return 2
    excludes = {item.strip('/').replace(os.sep, '/') for item in args.exclude}

    findings, checked = [], 0
    for rel in iter_markdown(root, excludes):
        checked += 1
        findings.extend(check_file(root, rel, args.allow_placeholders, args.strict))

    order = {'FAIL': 0, 'STRICT': 1, 'WARN': 2, 'NOTE': 3}
    findings.sort(key=lambda f: (order.get(f.level, 9), f.path, f.code))
    if not args.quiet:
        for finding in findings:
            print(finding)

    counts = {level: 0 for level in order}
    for finding in findings:
        counts[finding.level] = counts.get(finding.level, 0) + 1
    print('checked %d files: %d failures, %d strict, %d warnings'
          % (checked, counts['FAIL'], counts['STRICT'], counts['WARN']))

    if counts['FAIL'] or (args.strict and (counts['WARN'] or counts['STRICT'])):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
