---
type: system
tags: [system, conventions]
created: {{CREATED}}
updated: {{CREATED}}
summary: The note types, frontmatter schema, linking, naming, taxonomy, and lifecycle rules the kernel follows.
provenance: extracted
---

# Conventions

The rules the kernel ([[Claude]] via `CLAUDE.md`) follows. Keep them simple.

## Frontmatter

Every note starts with YAML frontmatter:

```yaml
---
type: person | organization | tool | project | epic | task | meeting | daily | system | moc | reference
status:           # only for task/project/epic: backlog | in-progress | blocked | done
tags: []          # lowercase-kebab; must be registered in [[taxonomy]]
created: {{CREATED}}   # ISO date first made; never changes
updated: {{CREATED}}   # ISO date last meaningfully edited; bump on real edits
summary:          # one sentence — a cheap-to-scan preview so the kernel can skim without reading the body
provenance: extracted   # extracted (from a source) | inferred (kernel synthesis) | to-confirm (unverified)
---
```

- `type` is required. `status` only where it makes sense (tasks, projects, epics).
- `created` never changes; `updated` bumps on meaningful edits (not on trivial re-links).
- `summary` keeps the graph queryable cheaply — the kernel reads summaries before opening bodies.
- `provenance` defaults to `extracted`. Use `inferred` for the kernel's own synthesis and
  `to-confirm` for anything unverified (also drop a `> ⚠️ **to confirm**` callout in the body).
- Absorbed/relocated source docs (verbatim transcripts, pasted records) may keep their original
  content without frontmatter — they're raw records. New notes always get it.

## Note types

| type | what it is | lives in |
|---|---|---|
| `moc` | a map-of-content / index hub (e.g. [[Home]]) | anywhere |
| `person` | a human | `People/` |
| `organization` | a company / client | `Organizations/` |
| `tool` | a platform in the stack | `Tools/` |
| `epic` | a large project with sub-tasks | `Projects/<Epic>/` (folder + MOC note) |
| `task` | a discrete unit of work | under a project, or `Projects/` |
| `meeting` | a call / 1:1 / transcript | `Meetings/` |
| `daily` | a daily log note | `Daily/` |
| `reference` | a durable external pointer (repo, dashboard, link) | anywhere |
| `system` | meta-notes about the OS | `System/` |

## Linking (the important part)

- Use `[[wikilinks]]` for every internal reference — never bare text for an entity that has a note.
- Stub when needed. If you reference something that deserves a note but doesn't have one, create a stub
  (frontmatter + one line) so the link resolves and the graph connects.
- Link up and across. Each note links up to its parent MOC and across to related people/tools/orgs.
- Unique titles. Obsidian resolves `[[Name]]` vault-wide, so note titles must be unique. Disambiguate
  with parentheses where needed (e.g. `[[Project (codename)]]`).

## Tags & taxonomy

- Tags are lowercase-kebab and must be registered in [[taxonomy]] (`_meta/taxonomy.md`).
- Before inventing a tag, check the taxonomy for an existing one. If a genuinely new tag is needed,
  add it to the taxonomy with a one-line definition in the same edit.
- The `/dream` skill flags off-taxonomy tags and proposes merges for near-duplicates.

## Naming & dates

- File/note titles in Title Case. Folders too.
- Dates are ISO (`YYYY-MM-DD`). Convert relative dates ("today", "this week") to absolute against
  {{OWNER_SHORT}}'s working window — see [[{{OWNER}}]].
- Meeting notes: `Meetings/YYYY-MM-DD — <Who> <What>.md`.

## Lifecycle (inbox → wiki → schema)

- Inbox (raw): unprocessed captures land in `Inbox/`. Digest them into clean, wikilinked notes in their
  proper home, then clear the item. Never silently rewrite source meaning.
- Wiki (the vault): the durable, linked knowledge graph. Merge-first — update an existing note rather
  than creating a near-duplicate.
- Schema (`System/` + `_meta/`): the rules and taxonomy that keep the wiki coherent. When the shape of
  the knowledge changes, the schema changes first, then notes follow.

## Housekeeping

- After any structural change, update the relevant MOC and append a line to [[Changelog]].
- Keep `Inbox/` empty over time — process captures into their real home.
- Flag unconfirmed facts with a `> ⚠️ **to confirm**` callout rather than asserting them.
- Run `/dream` periodically for the deep clean (re-link, dedup, prune-to-`_dump/`, rebuild indexes).
- `_dump/` is local-only scratch (raw drops + prune quarantine): gitignored, never committed or pushed.
  Before any commit, verify its contents are already ingested into the vault; flag anything that isn't
  rather than committing or deleting it.
