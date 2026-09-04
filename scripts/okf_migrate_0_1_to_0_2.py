#!/usr/bin/env python3
"""Migrate an OKF v0.1 knowledge bundle to OKF v0.2.

    okf_migrate_0_1_to_0_2.py <bundle-root> [--actor ACTOR] [--dry-run]
                              [--git-fallback] [--strip-reserved]
                              [--no-quote-fix] [--verbose]

What it rewrites:

  timestamp: 2026-04-15   ->  generated:
                                by: <actor>
                                at: 2026-04-15T00:00:00Z
  status: <vault value>   ->  stage: <vault value>   (+ status: deprecated
                              when the value is `retired`)
  # Citations body list   ->  sources: frontmatter entries
  okf_version: "0.1"      ->  okf_version: "0.2"     (bundle-root index.md)

Only the leading `---` block is touched, by line position rather than by
parse-and-dump, so key order, quoting style and unknown extension keys all
survive untouched and a ```yaml example inside a document body is never
mistaken for frontmatter. The migration is idempotent: a second run reports
zero changes.

Stdlib only. Exit codes: 0 done, 1 a file's frontmatter could not be parsed,
2 usage or IO error.
"""

import argparse
import difflib
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

OKF_VERSION = '0.2'
DEFAULT_ACTOR = 'claude-code/kernel'

PRUNE_DIRS = {
    '.git', '.obsidian', '.claude', '.trash', '_dump',
    'node_modules', '.github', '.playwright-mcp',
}
RESERVED_FILES = {'index.md', 'log.md'}
OKF_STATUS_VALUES = {'draft', 'stable', 'deprecated'}

# A date, or a datetime, optionally quoted, optionally trailed by a comment.
DATE_VAL = re.compile(
    r"""^(?P<q>['"]?)(?P<date>\d{4}-\d{2}-\d{2})"""
    r"""(?:[T ](?P<time>\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?)(?P<tz>Z|[+-]\d{2}:\d{2})?)?"""
    r"""(?P=q)[ \t]*(?:\#.*)?$""",
    re.X,
)
CITATION_HEADING = re.compile(r'^#{1,6}[ \t]*citations[ \t]*$', re.I)
LIST_ITEM = re.compile(r'^[ \t]*(?:[-*+]|\d+[.)])[ \t]+(.*)$')
MD_LINK = re.compile(r'\[(?P<title>[^\]]*)\]\((?P<url>[^)\s]+)\)')
BARE_URL = re.compile(r'(?P<url>https?://\S+|/\S+\.md)')
FOOTNOTE_LABEL = re.compile(r'^\[\^?(?P<label>[^\]]+)\]:?[ \t]*')
POSITIONAL_REF = re.compile(r'\[\d+\]')

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

# ------------------------------------------------------------------ entries

class Entry:
    """One top-level frontmatter key and the raw lines that belong to it."""

    def __init__(self, key, lines):
        self.key = key
        self.lines = lines

    @property
    def raw_value(self):
        match = KEY_RE.match(self.lines[0])
        return (match.group(2) or '') if match else ''

    def value(self):
        return strip_comment(self.raw_value).strip()


def split_entries(lines):
    entries, current = [], Entry(None, [])
    for line in lines:
        match = KEY_RE.match(line) if line[:1] not in (' ', '\t') else None
        if match:
            if current.key is not None or current.lines:
                entries.append(current)
            current = Entry(match.group(1), [line])
        else:
            current.lines.append(line)
    if current.key is not None or current.lines:
        entries.append(current)
    return entries


def find(entries, key):
    for entry in entries:
        if entry.key == key:
            return entry
    return None


def to_datetime(raw):
    """Normalise a v0.1 date or datetime into an OKF v0.2 UTC datetime."""
    match = DATE_VAL.match(raw.strip())
    if not match:
        return None
    if not match.group('time'):
        return '%sT00:00:00Z' % match.group('date')
    time = match.group('time')
    if len(time) == 5:
        time += ':00'
    return '%sT%s%s' % (match.group('date'), time, match.group('tz') or 'Z')


def git_datetime(root, rel):
    try:
        result = subprocess.run(
            ['git', '-C', root, 'log', '-1', '--format=%cI', '--', rel],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    stamp = result.stdout.strip()
    if result.returncode != 0 or not stamp:
        return None
    try:
        parsed = datetime.fromisoformat(stamp)
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


# --------------------------------------------------------------- transforms

class Report:
    def __init__(self):
        self.counts = {}
        self.status_values = {}
        self.needs_review = []

    def bump(self, key, amount=1):
        self.counts[key] = self.counts.get(key, 0) + amount

    def review(self, rel, reason):
        self.needs_review.append('%s: %s' % (rel, reason))


def transform_frontmatter(entries, rel, root, opts, report):
    """Apply T1, T2, T4, T5 to the entry list. Returns True when changed."""
    changed = False
    generated = find(entries, 'generated')
    timestamp = find(entries, 'timestamp')

    # T1 - timestamp becomes generated {by, at}
    if timestamp is not None:
        if generated is not None:
            entries.remove(timestamp)
            report.bump('timestamp dropped (generated already present)')
            changed = True
        else:
            stamp = to_datetime(timestamp.raw_value)
            if stamp is None:
                report.review(rel, 'timestamp value is not a date: %r'
                              % timestamp.raw_value.strip())
            else:
                timestamp.key = 'generated'
                timestamp.lines = ['generated:',
                                   '  by: %s' % opts.actor,
                                   '  at: %s' % stamp]
                report.bump('timestamp -> generated')
                changed = True
    elif generated is None and entries:
        stamp = None
        created = find(entries, 'created')
        if created is not None:
            stamp = to_datetime(created.raw_value)
            if stamp:
                report.bump('at taken from created')
        if stamp is None and opts.git_fallback:
            stamp = git_datetime(root, rel)
            if stamp:
                report.bump('at taken from git')
        if stamp is None:
            if find(entries, 'type') is not None:
                report.bump('generated omitted (no date)')
        else:
            anchor = created
            if anchor is None:
                for key in ('tags', 'description', 'title', 'type'):
                    anchor = find(entries, key) or anchor
                    if anchor is not None and anchor.key == key:
                        break
            block = Entry('generated', ['generated:',
                                        '  by: %s' % opts.actor,
                                        '  at: %s' % stamp])
            index = entries.index(anchor) + 1 if anchor is not None else len(entries)
            entries.insert(index, block)
            changed = True

    # T2 - the vault lifecycle vocabulary moves to `stage`
    status = find(entries, 'status')
    if status is not None and status.value() not in OKF_STATUS_VALUES:
        if find(entries, 'stage') is not None:
            report.review(rel, 'both `status` and `stage` are present')
        else:
            value = status.value()
            report.status_values[value] = report.status_values.get(value, 0) + 1
            status.lines[0] = re.sub(r'^status:', 'stage:', status.lines[0], count=1)
            status.key = 'stage'
            report.bump('status -> stage')
            changed = True
            if value.lower() == 'retired':
                entries.insert(entries.index(status) + 1,
                               Entry('status', ['status: deprecated']))
                report.bump('status: deprecated added')

    # T4 - the bundle-root index.md declares the version
    if rel == 'index.md':
        version = find(entries, 'okf_version')
        if version is None:
            entries.append(Entry('okf_version', ['okf_version: "%s"' % OKF_VERSION]))
            report.bump('okf_version added')
            changed = True
        elif version.value().strip('\'"') != OKF_VERSION:
            quote = version.value()[:1] if version.value()[:1] in '\'"' else '"'
            version.lines[0] = 'okf_version: %s%s%s' % (quote, OKF_VERSION, quote)
            report.bump('okf_version bumped')
            changed = True

    # T5 - quote plain scalars that a strict YAML reader would misread
    if not opts.no_quote_fix:
        for entry in entries:
            if entry.key is None or len(entry.lines) != 1:
                continue
            raw = entry.raw_value.strip()
            if not raw or raw[0] in '\'"[{' or TEMPLATE_TOKEN_RE.match(raw):
                continue
            if ': ' in raw or raw.endswith(':') or ' #' in raw:
                entry.lines[0] = "%s: '%s'" % (entry.key, raw.replace("'", "''"))
                report.bump('quoted for strict YAML')
                changed = True
    return changed


def convert_citations(body, rel, report):
    """T3 - a `# Citations` body list becomes `sources:` frontmatter."""
    lines = body.split('\n')
    start = None
    for index, line in enumerate(lines):
        if CITATION_HEADING.match(line.strip()):
            start = index
            break
    if start is None:
        return None, body

    items, end = [], start + 1
    while end < len(lines):
        line = lines[end]
        if not line.strip():
            following = end + 1
            while following < len(lines) and not lines[following].strip():
                following += 1
            if following < len(lines) and LIST_ITEM.match(lines[following]):
                end = following
                continue
            break
        if line.lstrip().startswith('#'):
            break
        match = LIST_ITEM.match(line)
        if not match:
            report.review(rel, 'the Citations block is not a plain list')
            return None, body
        items.append(match.group(1).strip())
        end += 1

    if not items:
        return None, body
    if POSITIONAL_REF.search('\n'.join(lines[:start])):
        report.review(rel, 'the body uses positional [n] citation references')
        return None, body

    sources = []
    for position, item in enumerate(items, 1):
        label = None
        label_match = FOOTNOTE_LABEL.match(item)
        if label_match:
            label = label_match.group('label').lstrip('^')
            item = item[label_match.end():].strip()
        link = MD_LINK.search(item)
        if link:
            title, url = link.group('title').strip(), link.group('url')
        else:
            bare = BARE_URL.search(item)
            if not bare:
                report.review(rel, 'a citation has no resolvable resource: %r' % item)
                return None, body
            url = bare.group('url')
            title = (item[:bare.start()] + item[bare.end():]).strip(' -—:')
        identifier = label or (re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
                               if title else '') or 'src-%d' % position
        sources.append((identifier, url, title))

    block = ['sources:']
    for identifier, url, title in sources:
        block.append('  - id: %s' % identifier)
        block.append('    resource: %s' % url)
        if title:
            block.append('    title: %s' % yaml_scalar(title))
    while end < len(lines) and not lines[end].strip():
        end += 1
    report.bump('citations -> sources', len(sources))
    return block, '\n'.join(lines[:start] + lines[end:])


def yaml_scalar(text):
    if re.search(r'^[\s\-?:,\[\]{}#&*!|>\'"%@`]|: | #|:$', text):
        return "'%s'" % text.replace("'", "''")
    return text

# ------------------------------------------------------------------- driver

def migrate_file(root, rel, opts, report):
    path = os.path.join(root, rel)
    with open(path, encoding='utf-8') as handle:
        original = handle.read()

    newline = '\r\n' if '\r\n' in original[:4096] else '\n'
    name = os.path.basename(rel)
    is_root_index = rel == 'index.md'
    reserved = name in RESERVED_FILES

    try:
        split = split_frontmatter(original)
    except ParseError as exc:
        report.review(rel, exc.message)
        report.bump('unparseable')
        return None
    if split is None:
        report.bump('skipped (no frontmatter)')
        if not (is_root_index and opts.strip_reserved):
            return None
        block, body_offset = '', 0
    else:
        block, body_offset = split

    body = original[body_offset:]
    bom = '﻿' if original.startswith('﻿') else ''

    # T6 - reserved files carry no frontmatter (the root index.md keeps only
    # the version declaration).
    if reserved and opts.strip_reserved:
        if is_root_index:
            new_block = '%s---%s%s: "%s"%s---%s' % (
                bom, newline, 'okf_version', OKF_VERSION, newline, newline)
            if block != new_block:
                report.bump('root index.md reduced to okf_version')
                return write(path, new_block + body, original, rel, opts)
            return None
        if block:
            report.bump('reserved frontmatter stripped')
            return write(path, bom + body.lstrip('\n'), original, rel, opts)
        return None

    if not block:
        return None

    inner = block.split(newline, 1)[1] if newline in block else block
    inner = inner.rsplit('---', 1)[0]
    lines = [line for line in inner.split(newline)]
    if lines and lines[-1] == '':
        lines.pop()

    try:
        entries = split_entries(lines)
    except Exception as exc:                       # pragma: no cover - defensive
        report.review(rel, 'could not split frontmatter: %s' % exc)
        report.bump('unparseable')
        return None
    if not entries:
        report.bump('skipped (empty frontmatter)')
        return None

    changed = transform_frontmatter(entries, rel, root, opts, report)

    if not reserved:
        citations, new_body = convert_citations(body, rel, report)
        if citations is not None:
            entries.append(Entry('sources', citations))
            body = new_body
            changed = True

    if not changed:
        return None

    rebuilt = []
    for entry in entries:
        rebuilt.extend(entry.lines)
    new_block = '%s---%s%s%s---%s' % (
        bom, newline, newline.join(rebuilt) + newline, '', newline)
    return write(path, new_block + body, original, rel, opts)


def write(path, new_text, original, rel, opts):
    if new_text == original:
        return None
    if opts.dry_run or opts.verbose:
        diff = difflib.unified_diff(
            original.splitlines(True), new_text.splitlines(True),
            fromfile='a/' + rel, tofile='b/' + rel, n=2)
        sys.stdout.writelines(diff)
    if not opts.dry_run:
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(new_text)
    return rel


def iter_markdown(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in PRUNE_DIRS)
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = '' if rel_dir == '.' else rel_dir
        for name in sorted(filenames):
            if name.endswith('.md'):
                yield os.path.join(rel_dir, name).replace(os.sep, '/')


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='okf_migrate_0_1_to_0_2.py',
        description='Migrate an OKF v0.1 knowledge bundle to OKF v%s.' % OKF_VERSION)
    parser.add_argument('root', help='bundle root directory')
    parser.add_argument('--actor', default=DEFAULT_ACTOR,
                        help='actor recorded in generated.by (default: %s)' % DEFAULT_ACTOR)
    parser.add_argument('--dry-run', action='store_true',
                        help='print diffs, write nothing')
    parser.add_argument('--git-fallback', action='store_true',
                        help='date notes with no timestamp or created from their last commit')
    parser.add_argument('--strip-reserved', action='store_true',
                        help='remove frontmatter from index.md and log.md (OKF reserves them)')
    parser.add_argument('--no-quote-fix', action='store_true',
                        help='leave plain scalars a strict YAML reader would misread')
    parser.add_argument('--verbose', action='store_true', help='print diffs as it writes')
    opts = parser.parse_args(argv)

    root = os.path.abspath(opts.root)
    if not os.path.isdir(root):
        sys.stderr.write('okf_migrate_0_1_to_0_2.py: not a directory: %s\n' % opts.root)
        return 2

    report = Report()
    scanned = changed = 0
    for rel in iter_markdown(root):
        scanned += 1
        if migrate_file(root, rel, opts, report):
            changed += 1

    print('scanned %d markdown files | changed %d%s'
          % (scanned, changed, ' (dry run, nothing written)' if opts.dry_run else ''))
    for key in sorted(report.counts):
        print('  %-42s %d' % (key, report.counts[key]))
    if report.status_values:
        histogram = ', '.join('%s %d' % (value, count) for value, count
                              in sorted(report.status_values.items(),
                                        key=lambda item: (-item[1], item[0])))
        print('  status values moved to stage: %s' % histogram)
    if report.needs_review:
        print('needs review (%d):' % len(report.needs_review))
        for line in report.needs_review:
            print('  %s' % line)
    return 1 if report.counts.get('unparseable') else 0


if __name__ == '__main__':
    sys.exit(main())
