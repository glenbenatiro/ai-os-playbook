---
type: system
title: The dream pass — vault consolidation & OKF maintenance
description: The periodic deep-clean any agent runs over this vault — re-link, repair, merge, refactor, safely prune, rebuild indexes, validate OKF conformance.
tags: [system, conventions]
generated:
  by: {{KERNEL_ACTOR}}
  at: {{CREATED_AT}}
created: {{CREATED}}
provenance: extracted
---

# The dream pass

A **consolidation pass** ("dreaming") over this vault. Day-to-day editing leaves gaps: unlinked
mentions, drifted frontmatter, near-duplicate notes, stale entries, stale `index.md`. This procedure
combs the whole vault and grooms it back to the conventions — **without ever destroying information**.

It is plain markdown on purpose: any agent can follow it step by step. In Claude Code, the `/dream`
skill runs it. Do a pass after a big import, when the graph feels messy, or on a schedule.

## 0. Resolve target & mode

- **Read the vault's contract first:** [AGENTS.md](/AGENTS.md), [Conventions](/system/conventions.md),
  [taxonomy](/_meta/taxonomy.md). Those rules **override** anything here on conflict.
- **Mode:**
  - `interactive` (default): apply safe changes directly; **propose** anything destructive or ambiguous
    (merges, moves, prunes, a first-time OKF migration) and ask before doing them.
  - `unattended` (for a cron or scheduled run): apply safe changes; for anything destructive or
    ambiguous, **quarantine to `.trash/` and report** — never delete, never guess on a risky merge.

## 1. Inventory (read before you write)

Build a picture of the vault: every note's path, `type`, `title`, `tags`, `created`/`generated`,
`description`, outbound links, and inbound backlinks. Note the folder each `type` is supposed to live in.

## 2. OKF migration (skip whatever is already done)

Detect legacy markers and migrate — a mechanical, information-preserving transform. In `interactive`
mode, confirm before the first run; work folder by folder.

**Pre-OKF markers:** Title-Case filenames, `[[wikilinks]]`, `summary`/`updated` frontmatter fields,
Title-Case folders, a `System/Changelog.md`.

a. **Index** every note: current path, basename, `title` (H1 or filename), and any aliases.
b. **Compute targets:** `snake_case(basename)` in a lowercased folder; record an old→new path map.
   Resolve slug collisions with a short disambiguator.
c. **Rewrite links** using the map: `[[Name]]` → `[Name](/folder/slug.md)`; `[[Name|Alias]]` →
   `[Alias](/folder/slug.md)`; `[[Name#Heading]]` → `[Name](/folder/slug.md#heading)`. Stubs (targets
   with no file) link to the intended slug path — OKF tolerates them.
d. **Rename** files (`git mv`, so renames show as renames) and lowercase the folders. Keep these names
   **verbatim**: `AGENTS.md`, `CLAUDE.md`, `README.md`, `index.md`, `log.md`, `_meta/`, `.obsidian/`.
e. **Frontmatter:** add `title`; rename `summary`→`description`; ensure a non-empty `type`; keep
   `created`/`provenance`/`stage`/`resource`.
f. **Reserved files:** create the root `index.md` (`okf_version: "0.2"` and nothing else in its
   frontmatter) and a per-folder `index.md`; convert any `System/Changelog.md` into the root `log.md`.

**v0.1 → v0.2 leftovers**, wherever they remain:

- `timestamp: <date>` → `generated:` with `by:` (the actor that wrote it — `<tool>/<version>`,
  `human:<id>` or `process:<id>`) and `at:` (an ISO 8601 datetime with an explicit UTC offset).
- A lifecycle value in `status:` → move it to `stage:`. OKF reserves `status` for
  `draft` / `stable` / `deprecated`; a note whose `stage` is `retired` also gets `status: deprecated`.
- A `# Citations` body list → `sources:` frontmatter entries (`id`, `resource`, `title`), with
  per-claim attribution as `[^id]` markdown footnotes.
- Frontmatter on a reserved `index.md` or `log.md` → remove it; the root `index.md` keeps only
  `okf_version`.

## 3. Re-link (the most important pass)

- Scan note bodies for **unlinked mentions** of entities that already have notes → wrap them in
  bundle-relative markdown links `[Text](/folder/slug.md)`. Respect "link on meaningful mention," not
  every incidental word.
- For link-worthy entities mentioned but with **no note**, create a **stub** (frontmatter + one-line
  `description` + a sentence) at the slug path so the link resolves and the graph connects.
- Ensure every note links **up** to its parent `index.md`/MOC and **across** to related entities; ensure
  hub/MOC notes link back **down** to their children.

## 4. Repair

- Fix **broken/unresolved links** (rename target, fix typo, or stub it).
- Normalize **frontmatter** to the v0.2 schema in [Conventions](/system/conventions.md): `type`
  (required, non-empty), `title`, `description`, `tags`, `generated`; `created`/`provenance` always,
  `stage` where the type warrants it. Add a missing `description` by reading the note. Update
  `generated` only where you made a real content change. Never alter `created`.
- **Tags:** flag any tag not registered in [taxonomy](/_meta/taxonomy.md). Map obvious synonyms to the
  canonical tag; for genuinely new-but-useful tags, add them to the taxonomy with a one-line definition.

## 5. Merge-first dedup

- Detect duplicate / near-duplicate notes (same entity, split notes). **Merge** into the best-named
  canonical note: combine substance, preserve every fact and its `provenance`, repoint inbound links,
  leave a `> note: merged from [Old Title](/folder/old_slug.md) on <date>` line. In `unattended` mode,
  only auto-merge unambiguous exact-subject dupes; send judgment calls to the report.

## 6. Refactor

- Split oversized grab-bag notes into atomic notes + a MOC; promote a concept that recurs across many
  notes into its own note; move misfiled notes to the folder their `type` dictates (update links).
- Keep edits **faithful** — relocate and restructure, don't rewrite meaning.

## 7. Prune — safely

- Identify **stale / empty / superseded / orphaned** notes. Do **not** delete them. **Move** each to
  `.trash/` with a one-line reason appended to the note (`> dumped <date>: <why>`), and list them in the
  report for the owner's decision. Honour the vault's "never silently delete" rule even unattended.

## 8. Rebuild indexes, insights & conformance

- Refresh [home](/home.md), section MOCs, and **every folder's `index.md`** so nothing is orphaned and
  new notes are reachable. Index entries are `- [Title](slug.md) — description`.
- **Regenerate `_insights.md`** (overwrite it): hubs (most-linked), orphans (no links in or out),
  broken/unresolved links remaining, suggested links you did *not* auto-apply, prune candidates now in
  `.trash/`, off-taxonomy tags, and an **OKF conformance** section.
- Conformance is exactly four things: every non-reserved note has parseable frontmatter with a
  non-empty `type`; `generated` carries a `by` and an ISO 8601 `at`; `status`, where present, is one of
  `draft`/`stable`/`deprecated`; and the reserved files are clean — no frontmatter on any `index.md` or
  `log.md` except the root `index.md`, which declares `okf_version: "0.2"` and nothing else. `CLAUDE.md`
  is tooling (the `@AGENTS.md` import shim) and is excluded.

## 9. Report + log

- Append a dated entry to [log](/log.md) (`## YYYY-MM-DD`, newest first; `**Update**` / `**Creation**` /
  `**Deprecation**` prefixes) summarizing the structural changes.
- End with a **run report**: what changed (counts: links added, stubs created, notes merged/moved/dumped,
  frontmatter fixed) and a clear **"needs your decision"** list (everything in `.trash/`, risky merges
  held back, new tags added). In `interactive` mode, this is where you ask about the proposals you
  surfaced.

## Guardrails

- **Information is never lost** — prune = quarantine to `.trash/`, never `rm`.
- **`.trash/` is local-only — never commit it.** If a run commits (unattended or scheduled), never stage
  or push `.trash/`; surface its contents in the report instead, so nothing is lost silently.
- The vault's [AGENTS.md](/AGENTS.md) and [Conventions](/system/conventions.md) win on any conflict with
  this procedure.
- **Migration is mechanical and reviewable** — prefer `git mv` so renames show as renames; never lose a
  fact, a `created` date, or a `provenance` value in a rewrite.
- Prefer many small, reviewable edits over sweeping rewrites. On a large vault work folder by folder
  (`people/` → `organizations/` → `tools/` → `projects/` → `meetings/` → `daily/`) so a long run stays
  resumable and reviewable.
