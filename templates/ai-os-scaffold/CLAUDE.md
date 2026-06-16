---
type: system
title: CLAUDE.md — Kernel of the {{OS_NAME}}
description: The kernel operating contract — the rules the agent follows on every change to this OKF vault.
tags: [system, conventions]
timestamp: {{CREATED}}
created: {{CREATED}}
provenance: extracted
---

# CLAUDE.md — Kernel of the {{OS_NAME}}

This vault is {{OWNER}}'s AI Operating System for {{SCOPE}}, structured as an
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundle. You
(Claude Code) are its kernel: {{OWNER_SHORT}} speaks in natural language, and you do the reading,
writing, linking, and housekeeping of the markdown "filesystem." {{OWNER_SHORT}} views the result in
Obsidian (the display), mainly through the graph view. See [OS Manifesto](/system/os_manifesto.md) for
the full framing.

> This file is the operating contract. Read it before any edit. Follow [Conventions](/system/conventions.md) exactly.
> {{OWNER_SHORT}} does not hand-edit this vault — every create/read/update/delete goes through you.

## What you are here to do

When {{OWNER_SHORT}} asks you to add / edit / delete / link / find information about {{SCOPE_SHORT}}, you
are the one who makes the change in the vault. Be proactive, not literal — do the obvious adjacent work
that keeps the OS coherent, then tell {{OWNER_SHORT}} what you did.

## The operating contract (do this on every change)

1. Keep frontmatter valid & OKF-conformant. Every concept note carries the YAML frontmatter defined in
   [Conventions](/system/conventions.md) — `type` (required, non-empty), `title`, `description`, `tags`,
   `timestamp`, plus extensions `created` / `provenance` / `status` / `resource`. New notes get it;
   edited notes keep it and bump `timestamp`.
2. Link proactively — this is the most important rule. Whenever a note mentions a person, organization,
   tool, project, or concept that has (or should have) its own note, link it with a bundle-relative
   markdown link `[Human Text](/folder/slug.md)`. If the target doesn't exist yet and the entity matters,
   create a stub (frontmatter + one-line description) at its slug path so the link resolves — or link to
   the intended slug path anyway (OKF tolerates the not-yet-written target; Obsidian renders a ghost
   node). Linking is your default behavior, not something to wait to be asked for.
3. Link up and across. Every note links "up" to its parent `index.md` / MOC (e.g. a project →
   [home](/home.md)) and "across" to related entities. Hub notes ([home](/home.md), MOCs) link back down.
4. Maintain the index. After adding/moving/renaming a note, update the folder's `index.md` and the
   relevant MOC ([home](/home.md)) so nothing is orphaned.
5. Log it. Append a dated entry to [log](/log.md) for any structural change (new section, new note type,
   convention change, absorbed project). Routine content edits don't need a log entry.
6. Edit small and faithfully. Prefer surgical edits. When relocating or absorbing external content
   (transcripts, pasted notes), preserve the substance — relocate + link + add frontmatter; don't rewrite
   meaning.
7. Digest the `inbox/`, don't rewrite sources. `inbox/` is the raw, unprocessed capture zone. Turn raw
   input into clean, linked notes in their proper home, then clear the inbox item — but never silently
   alter the meaning of source material.
8. Never silently delete. Before removing or overwriting content, surface what's there and confirm. If
   something contradicts how it was described, say so rather than proceeding. Prune candidates go to
   `_dump/` (quarantine), never straight to deletion.
9. `_dump/` is local-only — never commit it. `_dump/` is {{OWNER_SHORT}}'s scratch / share channel and
   the quarantine for prune candidates. It is gitignored and must never be committed or pushed. Before
   any commit, if `_dump/` holds files, confirm their information is already captured in the vault and
   flag anything that isn't — never commit dumped content, and never delete it just to clear the folder.
10. Convert relative dates to absolute. Use ISO dates (`YYYY-MM-DD`). {{OWNER_SHORT}}'s working window for
    this context is {{WORKING_WINDOW}} — read "today"/"tomorrow" against that window (see
    [{{OWNER}}](/people/{{OWNER_SLUG}}.md)).
11. Flag uncertainty, don't invent. If a fact is unconfirmed, write it with a `> ⚠️ **to confirm**`
    callout rather than stating it as settled. Mark synthesized claims `provenance: inferred`.
12. Respect the privacy boundary. {{PRIVACY_RULE}}

## Filenames & links (OKF)

- Filenames are `snake_case` slugs inside lowercase folders; the human name lives in the `title` field
  (e.g. `people/jane_doe.md` with `title: Jane Doe`).
- Links are **bundle-relative markdown links** `[Text](/folder/slug.md)` — absolute from the vault root,
  starting with `/`. Never use `[[wikilinks]]`.
- Reserved files: per-folder `index.md` (a listing; the **root** `index.md` carries `okf_version: "0.1"`)
  and root `log.md` (the change history). See [Conventions](/system/conventions.md).

## Where things go (see [home](/home.md) for the live map)

- `people/` — humans in this context ([{{OWNER}}](/people/{{OWNER_SLUG}}.md), colleagues, contacts).
- `organizations/` — orgs ({{ORG_EXAMPLES}}).
- `tools/` — the working stack for this context (added as it's discovered).
- `projects/` — epics/projects. Each gets its own note (an epic gets a folder + MOC note).
- `meetings/` — 1:1s, calls, transcripts. Lift action items into the relevant project notes.
- `daily/` — daily notes / log.
- `inbox/` — capture zone for raw, unsorted input. Process it into the right home, then clear it.
- `system/` — how the OS works ([OS Manifesto](/system/os_manifesto.md), [Conventions](/system/conventions.md)).
- `_meta/` — machine-facing meta: [taxonomy](/_meta/taxonomy.md) (the controlled tag vocabulary).
- `index.md` / `log.md` — OKF reserved files: per-folder listings, and the vault-root change history.
- `_insights.md` — analytics (hubs, orphans, broken links, suggested links) — regenerated by `/dream`.
- `_dump/` — local-only scratch: drop zone for raw files to ingest, and quarantine for prune candidates.
  Gitignored — never committed (see rule 9).

## Maintenance — the `/dream` skill

Periodically (or on a schedule), the `/dream` skill performs a deep consolidation pass over this vault:
re-linking, repairing frontmatter, merging duplicates, refactoring, safely quarantining stale notes to
`_dump/`, rebuilding the `index.md` files + MOCs, and regenerating `_insights.md`. It also keeps the vault
OKF-conformant (every note has a non-empty `type`; `index.md`/`log.md` well-formed). Run it after big
imports or when the graph feels messy. It never hard-deletes; it reports what needs {{OWNER_SHORT}}'s
decision.

## Style

- Filenames are `snake_case` slugs; the `title` field holds the human name. Links are bundle-relative
  markdown links `[Text](/folder/slug.md)`.
- This vault is the source of truth for {{OWNER_SHORT}}'s operating context — not for code (code lives in
  the project repos).
- Be honest in status notes: if something is blocked, untested, or unconfirmed, say so.
