---
type: system
title: Conventions
description: The note types, frontmatter schema, linking, naming, taxonomy, and lifecycle rules the kernel follows.
tags: [system, conventions]
timestamp: {{CREATED}}
created: {{CREATED}}
provenance: extracted
---

# Conventions

The rules the kernel ([Claude](/tools/claude.md) via `CLAUDE.md`) follows. Keep them simple.

This vault is an **[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
knowledge bundle** — a directory of plain markdown files with YAML frontmatter. The rules below are
OKF's conventions made concrete for an Obsidian-viewed personal/work OS.

## Frontmatter

Every concept note starts with YAML frontmatter. OKF only *requires* a non-empty `type`; the rest are
strongly recommended here (order follows OKF's priority):

```yaml
---
type: person | organization | tool | project | epic | task | meeting | daily | system | moc | reference
title: Jane Doe          # human display name — the filename is a slug, so the name lives here
description:                   # one sentence — a cheap-to-scan preview so the kernel can skim without the body
tags: []                       # lowercase snake_case; must be registered in /_meta/taxonomy.md
timestamp: {{CREATED}}         # ISO date of last meaningful change (OKF field)
# --- extension fields (OKF preserves these; they are not part of conformance) ---
created: {{CREATED}}           # ISO date first made; never changes
provenance: extracted          # extracted (from a source) | inferred (kernel synthesis) | to-confirm
status:                        # only for task/project/epic: backlog | in-progress | blocked | done
resource:                      # canonical URI, when the note maps to one (tool site, dashboard, repo)
---
```

- `type` is **required and non-empty** — the one hard OKF conformance rule. `status`/`resource` only
  where they apply.
- `title` carries the human-readable name (the filename is a slug). `description` (OKF; replaces the old
  `summary`) keeps the graph queryable cheaply — the kernel reads descriptions before opening bodies.
- `timestamp` (OKF; replaces the old `updated`) = last meaningful change. `created` never changes.
- `provenance` defaults to `extracted`. Use `inferred` for the kernel's own synthesis and `to-confirm`
  for anything unverified (also drop a `> ⚠️ **to confirm**` callout in the body).
- Producers may add any other keys; consumers must preserve unknown keys and never reject a note over
  them (OKF §4.1).

## Filenames & folders

- **Filenames are `snake_case` slugs**, no spaces — `Jane Doe` → `people/jane_doe.md`. The
  readable name lives in the `title` field.
- **Folders are lowercase** — `people/`, `organizations/`, `tools/`, `projects/`, `meetings/`,
  `daily/`, `inbox/`, `system/`.
- **Kept verbatim** (external-tool or OKF-reserved names, not slugged): `CLAUDE.md`, `AGENTS.md`,
  `README.md`, `index.md`, `log.md`, and the `_meta/`, `_dump/`, `.obsidian/` paths.

## Note types

| type | what it is | lives in |
|---|---|---|
| `moc` | a map-of-content / index hub (e.g. [home](/home.md)) | anywhere |
| `person` | a human | `people/` |
| `organization` | a company / client | `organizations/` |
| `tool` | a platform in the stack | `tools/` |
| `epic` | a large project with sub-tasks | `projects/<epic>/` (folder + MOC note) |
| `task` | a discrete unit of work | under a project, or `projects/` |
| `meeting` | a call / 1:1 / transcript | `meetings/` |
| `daily` | a daily log note | `daily/` |
| `reference` | a durable external pointer (repo, dashboard, link) | anywhere |
| `system` | meta-notes about the OS | `system/` |

## Linking (the important part)

- **Links are OKF bundle-relative markdown links** — `[Human Text](/folder/slug.md)`, an absolute path
  from the bundle (vault) root, beginning with `/`. (Verified: Obsidian resolves these into graph edges
  and renders ghost nodes, identically to the old wikilinks.)
- **Link the human name, target the slug** — `[Jane Doe](/people/jane_doe.md)`.
- **Stub on mention.** If you reference something that deserves a note but doesn't have one yet, link it
  to its intended slug path *and* create a stub (frontmatter + one line). OKF tolerates the
  not-yet-written target; Obsidian shows it as a ghost node so the gap stays visible.
- **Link up and across.** Each note links up to its parent `index.md` / MOC and across to related
  people/tools/orgs; hub notes link back down. The *kind* of relationship lives in the surrounding
  prose, not the link (OKF §5.3).

## Index & log (OKF reserved files)

- **`index.md`** in any folder is a progressive-disclosure listing of that folder — a grouped markdown
  list, each entry `- [Title](slug.md) — description`. It carries **no frontmatter**, except the **root
  `index.md`**, which declares `okf_version: "0.1"`. `/dream` keeps these in sync.
- **`log.md`** at the vault root is the change history: date-grouped (`## YYYY-MM-DD`, newest first),
  entries prefixed `**Update**` / `**Creation**` / `**Deprecation**`. (Replaces the old
  `System/Changelog.md`.)

## Conventional headings

Use these OKF section headings when they apply: `# Overview`, `# Schema`, `# Examples`, `# Citations`
(external sources backing claims, numbered).

## Tags & taxonomy

- Tags are lowercase `snake_case` and must be registered in [taxonomy](/_meta/taxonomy.md).
- Before inventing a tag, check the taxonomy for an existing one. If a genuinely new tag is needed, add
  it to the taxonomy with a one-line definition in the same edit.
- The `/dream` skill flags off-taxonomy tags and proposes merges for near-duplicates.

## Naming & dates

- Dates are ISO (`YYYY-MM-DD`). Convert relative dates ("today", "this week") to absolute against
  {{OWNER_SHORT}}'s working window — see [{{OWNER}}](/people/{{OWNER_SLUG}}.md).
- Meeting notes: `meetings/YYYY-MM-DD_<who>_<what>.md` (snake_case); the readable form lives in `title`.

## Lifecycle (inbox → wiki → schema)

- **Inbox (raw):** unprocessed captures land in `inbox/`. Digest them into clean, linked notes in their
  proper home, then clear the item. Never silently rewrite source meaning.
- **Wiki (the vault):** the durable, linked knowledge graph. Merge-first — update an existing note rather
  than creating a near-duplicate.
- **Schema (`system/` + `_meta/`):** the rules and taxonomy that keep the wiki coherent. When the shape
  of the knowledge changes, the schema changes first, then notes follow.

## Housekeeping

- After any structural change, update the relevant `index.md` / MOC and append an entry to [log](/log.md).
- Keep `inbox/` empty over time — process captures into their real home.
- Flag unconfirmed facts with a `> ⚠️ **to confirm**` callout rather than asserting them.
- Run `/dream` periodically for the deep clean (re-link, dedup, prune-to-`_dump/`, rebuild indexes).
- `_dump/` is local-only scratch (raw drops + prune quarantine): gitignored, never committed or pushed.
  Before any commit, verify its contents are already ingested into the vault; flag anything that isn't
  rather than committing or deleting it.
