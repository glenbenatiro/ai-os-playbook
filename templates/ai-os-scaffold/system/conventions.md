---
type: system
title: Conventions
description: The note types, frontmatter schema, linking, naming, taxonomy, and lifecycle rules the kernel follows.
tags: [system, conventions]
generated:
  by: {{KERNEL_ACTOR}}
  at: {{CREATED_AT}}
created: {{CREATED}}
provenance: extracted
---

# Conventions

The rules the kernel (via [AGENTS.md](/AGENTS.md)) follows. Keep them simple.

This vault is an **[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
v0.2 knowledge bundle** — a directory of plain markdown files with YAML frontmatter. The rules below are
OKF's conventions made concrete for an Obsidian-viewed personal/work OS.

## Frontmatter

Every concept note starts with YAML frontmatter. OKF only *requires* a non-empty `type`; the rest are
strongly recommended here (order follows OKF's priority):

```yaml
---
type: person | organization | tool | project | epic | task | meeting | meeting-transcript | meeting-source | source | daily | system | moc | reference
title: Jane Doe                # human display name — the filename is a slug, so the name lives here
description:                   # one sentence — a cheap-to-scan preview so the kernel can skim without the body
tags: []                       # lowercase snake_case; must be registered in /_meta/taxonomy.md
generated:                     # who last wrote this note, and when
  by: {{KERNEL_ACTOR}}         # <tool>/<version> | human:<id> | process:<id>
  at: {{CREATED_AT}}           # ISO 8601 datetime with an explicit UTC offset
status:                        # OKF lifecycle, where it applies: draft | stable | deprecated (absent = stable)
verified:                      # optional — confirmation events, each { by: <actor>, at: <datetime> }
stale_after:                   # optional — ISO 8601 datetime after which the content should be re-checked
sources:                       # optional — provenance entries, each { id, resource, title }
# --- extension fields (OKF preserves these; they are not part of conformance) ---
created: {{CREATED}}           # ISO date first made; never changes
provenance: extracted          # extracted (from a source) | inferred (kernel synthesis) | to-confirm
stage:                         # this vault's own lifecycle: backlog | in-progress | blocked | done | retired
resource:                      # canonical URI, when the note maps to one (tool site, dashboard, repo)
---
```

- `type` is **required and non-empty** — the one hard OKF conformance rule. Everything else is optional
  to OKF and conventional here.
- `title` carries the human-readable name (the filename is a slug). `description` keeps the graph
  queryable cheaply — the kernel reads descriptions before opening bodies.
- `generated` records **who wrote the note and when**, replacing the old `timestamp`. `by` is an actor:
  `<tool>/<version>` for an agent, `human:<id>` for a person, `process:<id>` for an automated job. `at`
  is an ISO 8601 datetime with an explicit UTC offset (`2026-06-30T14:00:00Z`), not a bare date. Set both
  when you make a meaningful edit; `created` never changes.
- **`status` and `stage` are different fields.** OKF reserves `status` for `draft` / `stable` /
  `deprecated` (absent means stable), which is how any OKF-aware tool reads a note's lifecycle. This
  vault's own vocabulary — `backlog`, `in-progress`, `blocked`, `done`, `retired` — lives in `stage`. A
  note whose `stage` is `retired` also carries `status: deprecated`.
- `verified` is how trust is expressed: no `verified` key means unverified; entries by non-`human:`
  actors mean machine-confirmed; an entry by a `human:<id>` actor means human-reviewed. Never use the
  `human:` prefix for something a machine produced.
- `provenance` defaults to `extracted`. Use `inferred` for the kernel's own synthesis and `to-confirm`
  for anything unverified (also drop a `> ⚠️ **to confirm**` callout in the body).
- Producers may add any other keys; consumers must preserve unknown keys and never reject a note over
  them.
- **Raw records exempt:** verbatim files under `meetings/<slug>/raw/` (`type: meeting-transcript` /
  `meeting-source`) and standalone captures in `sources/` (`type: source`) are ground-truth sources —
  they may keep their original content with only minimal frontmatter (`type` + a `source:`/`from:` line).
  Every other note gets the full frontmatter.

## Filenames & folders

- **Filenames are `snake_case` slugs**, no spaces — `Jane Doe` → `people/jane_doe.md`. The
  readable name lives in the `title` field.
- **Folders are lowercase** — `people/`, `organizations/`, `tools/`, `projects/`, `meetings/`,
  `sources/`, `daily/`, `inbox/`, `system/`.
- **Kept verbatim** (external-tool or OKF-reserved names, not slugged): `AGENTS.md`, `CLAUDE.md`,
  `README.md`, `index.md`, `log.md`, and the `_meta/` and `.obsidian/` paths.

### Bundle tooling, not concepts

Some files in the bundle are plumbing rather than knowledge, and are excluded from conformance: `CLAUDE.md`
(the one-line `@AGENTS.md` import shim), `.obsidian/` (display config), and `.trash/` (local-only prune
quarantine, never committed). Everything else that ends in `.md` is a concept document and needs
frontmatter.

## Note types

| type | what it is | lives in |
|---|---|---|
| `moc` | a map-of-content / index hub (e.g. [home](/home.md)) | anywhere |
| `person` | a human | `people/` |
| `organization` | a company / client | `organizations/` |
| `tool` | a platform in the stack | `tools/` |
| `epic` | a large project with sub-tasks | `projects/<epic>/` (folder + MOC note) |
| `task` | a discrete unit of work | under a project, or `projects/` |
| `meeting` | a meeting summary (the folder note) | `meetings/<slug>/` |
| `meeting-transcript` | a verbatim speech-to-text transcript | `meetings/<slug>/raw/` |
| `meeting-source` | a verbatim pasted source (chat, notes, email) | `meetings/<slug>/raw/` |
| `source` | a standalone verbatim capture (chat/email/note), reusable context | `sources/` |
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
  list, each entry `- [Title](slug.md) — description`. OKF reserves it, so it carries **no frontmatter** —
  except the **root `index.md`**, whose frontmatter is the single line `okf_version: "0.2"` and nothing
  else. The [dream pass](/system/dream.md) keeps these in sync.
- **`log.md`** at the vault root is the change history: date-grouped (`## YYYY-MM-DD`, newest first),
  entries prefixed `**Update**` / `**Creation**` / `**Deprecation**`. It is reserved too, so it carries no
  frontmatter.

## Conventional headings

Use these OKF section headings when they apply: `# Overview`, `# Schema`, `# Examples`. External sources
backing a claim go in the `sources:` frontmatter list, not a `# Citations` body section; attribute an
individual claim with a markdown footnote whose label is a `sources[].id` (`Text.[^source-id]`).

## Tags & taxonomy

- Tags are lowercase `snake_case` and must be registered in [taxonomy](/_meta/taxonomy.md).
- Before inventing a tag, check the taxonomy for an existing one. If a genuinely new tag is needed, add
  it to the taxonomy with a one-line definition in the same edit.
- The [dream pass](/system/dream.md) flags off-taxonomy tags and proposes merges for near-duplicates.

## Naming & dates

- Dates are ISO (`YYYY-MM-DD`). Convert relative dates ("today", "this week") to absolute against
  {{OWNER_SHORT}}'s working window — see [{{OWNER}}](/people/{{OWNER_SLUG}}.md).
- Meetings are **foldered**: `meetings/<yyyy_mm_dd_who_what>/` with the summary as the slug-named folder
  note (`<slug>.md`) and raw sources under `raw/`. No `index.md` inside a meeting folder (the summary is
  the entry point). The readable form lives in `title`. See [AGENTS.md](/AGENTS.md) → "Meetings".

## Lifecycle (inbox → wiki → schema)

- **Inbox (raw):** unprocessed captures land in `inbox/`. Digest them into clean, linked notes in their
  proper home, then clear the item. Never silently rewrite source meaning.
- **Wiki (the vault):** the durable, linked knowledge graph. Merge-first — update an existing note rather
  than creating a near-duplicate.
- **Meetings (raw + summary):** never file a raw transcript/source without its paired summary in the same
  turn — see [AGENTS.md](/AGENTS.md) → "Meetings".
- **Raw context routing:** route any raw artifact by [AGENTS.md](/AGENTS.md) → "Raw context — routing" —
  meeting → `meetings/<slug>/raw/`; project working material → the project repo; standalone reusable →
  `sources/`.
- **Schema (`system/` + `_meta/`):** the rules and taxonomy that keep the wiki coherent. When the shape
  of the knowledge changes, the schema changes first, then notes follow.

## Housekeeping

- After any structural change, update the relevant `index.md` / MOC and append an entry to [log](/log.md).
- Keep `inbox/` empty over time — process captures into their real home.
- Flag unconfirmed facts with a `> ⚠️ **to confirm**` callout rather than asserting them.
- Run the [dream pass](/system/dream.md) periodically for the deep clean (re-link, dedup,
  prune-to-`.trash/`, rebuild indexes, validate conformance). Before any commit, verify its contents are
  already ingested into the vault; flag anything that isn't rather than committing or deleting it.
