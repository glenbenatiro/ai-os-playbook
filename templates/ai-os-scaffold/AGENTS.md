---
type: system
title: AGENTS.md — Kernel of the {{OS_NAME}}
description: The kernel operating contract — the rules any agent follows on every change to this OKF vault.
tags: [system, conventions]
generated:
  by: {{KERNEL_ACTOR}}
  at: {{CREATED_AT}}
created: {{CREATED}}
provenance: extracted
---

# AGENTS.md — Kernel of the {{OS_NAME}}

This vault is {{OWNER}}'s AI Operating System for {{SCOPE}}, structured as an
[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2
knowledge bundle. You are its kernel: {{OWNER_SHORT}} speaks in natural language, and you do the
reading, writing, linking, and housekeeping of the markdown "filesystem." {{OWNER_SHORT}} views the
result in Obsidian (the display), mainly through the graph view. See
[OS Manifesto](/system/os_manifesto.md) for the full framing.

> This file is the operating contract. Read it before any edit. Follow [Conventions](/system/conventions.md) exactly.
> {{OWNER_SHORT}} does not hand-edit this vault — every create/read/update/delete goes through you.

## Entrypoints

This file is the canonical contract, because `AGENTS.md` is the cross-tool standard that every agent
reads. `CLAUDE.md` sits beside it holding exactly one line — `@AGENTS.md` — so Claude Code imports
these same rules rather than a second copy of them. If you maintain another tool's rules file
(`.cursor/rules`, `GEMINI.md`, …), point it here as well. Never fork the rules into a second file.

## This vault is self-contained

Everything needed to operate this vault lives inside it: this contract, [Conventions](/system/conventions.md),
the [taxonomy](/_meta/taxonomy.md), and the [dream pass](/system/dream.md). It depends on no external
template, repository, or machine path, so it can be handed to another person or another machine whole.
If you find a rule here that points outside the vault, that is a bug — bring the rule inside.

## What you are here to do

When {{OWNER_SHORT}} asks you to add / edit / delete / link / find information about {{SCOPE_SHORT}}, you
are the one who makes the change in the vault. Be proactive, not literal — do the obvious adjacent work
that keeps the OS coherent, then tell {{OWNER_SHORT}} what you did.

## The operating contract (do this on every change)

1. Keep frontmatter valid & OKF-conformant. Every concept note carries the YAML frontmatter defined in
   [Conventions](/system/conventions.md) — `type` (required, non-empty), `title`, `description`, `tags`,
   `generated`, plus extensions `created` / `provenance` / `stage` / `resource`. New notes get the full
   set. When you make a meaningful edit, set `generated.by` to yourself and `generated.at` to the
   current UTC time (`date -u +%Y-%m-%dT%H:%M:%SZ`); never alter `created`.
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
   meaning. Meetings specifically follow the foldered raw-source + paired-summary rule — see
   [Meetings — raw sources + paired summary](#meetings--raw-sources--paired-summary).
7. Digest the `inbox/`, don't rewrite sources. `inbox/` is the raw, unprocessed capture zone. Turn raw
   input into clean, linked notes in their proper home, then clear the inbox item — but never silently
   alter the meaning of source material.
8. Never silently delete. Before removing or overwriting content, surface what's there and confirm. If
   something contradicts how it was described, say so rather than proceeding. Prune candidates go to
   `.trash/` (quarantine), never straight to deletion.
9. Convert relative dates to absolute. Use ISO dates (`YYYY-MM-DD`) in prose and ISO 8601 UTC datetimes
   in frontmatter. {{OWNER_SHORT}}'s working window for this context is {{WORKING_WINDOW}} — read
   "today"/"tomorrow" against that window (see [{{OWNER}}](/people/{{OWNER_SLUG}}.md)).
10. Flag uncertainty, don't invent. If a fact is unconfirmed, write it with a `> ⚠️ **to confirm**`
    callout rather than stating it as settled. Mark synthesized claims `provenance: inferred`.
11. Respect the privacy boundary. {{PRIVACY_RULE}}
12. Capture back from the work. Inside this vault, capturing is your default — new signal gets filed
    without being asked. When you are working in any other repo or project that this vault covers and
    you learn something durable (a person, a decision, a process, a tool, a fact about the context),
    proactively tell {{OWNER_SHORT}} and offer to write it in here. Never let a durable fact die in a
    project thread. The bar is "useful beyond this one task" — one-off, project-local detail stays in
    the project.

## Meetings — raw sources + paired summary

Each meeting is a **folder**: `meetings/<slug>/` (snake_case, e.g. `meetings/2026_05_18_jane_kickoff/`).

- **Summary (the folder note):** `meetings/<slug>/<slug>.md`, `type: meeting` — the canonical, scannable
  record. Capture who/context, decisions, action items (each linked to its project/person), and a link to
  every raw source. This is the note the rest of the vault links to.
- **Raw sources:** every transcript / pasted chat / notes goes **verbatim** under `meetings/<slug>/raw/`,
  one file per source — `type: meeting-transcript` for speech-to-text, `type: meeting-source` for pasted
  text. Raw files are ground-truth and exempt from full frontmatter (a minimal `type` + `source:` line is
  enough; see [Conventions](/system/conventions.md)).
- **The pairing is mandatory.** A raw source must never be committed without its paired summary — write
  the summary in the **same turn**. A raw transcript with no summary is a capture bug: nobody re-reads
  60KB of speech-to-text to find a decision.
- **No `index.md` inside a meeting folder** — the slug-named summary is the entry point (a folder note).
  The parent [meetings/index.md](/meetings/index.md) lists each meeting, linking to its summary.

## Raw context — routing

Any raw artifact (transcript, chat/DM, email, pasted note, brain-dump) routes by three questions, in order:

1. **Tied to a meeting/event?** → `meetings/<slug>/raw/` with a paired summary (see Meetings above).
2. **Project-specific working material** (build inputs, specs, data)? → the **project repo** (e.g.
   `docs/sources/`), kept verbatim next to the docs it feeds; the OS keeps only a digested note + a
   pointer to the repo.
3. **Standalone but reusable context** (a decision email, a chat that sets direction, a brain-dump about a
   person/org)? → `sources/`, verbatim (`type: source`, with `kind` / `from` / `date`) + a short digest
   linking to the note(s) it feeds.

The test between 2 and 3 is the OS bar — *"useful beyond this one task/project"* → `sources/`; otherwise
the repo. Always keep the raw **and** a digest, and link them.

## Filenames & links (OKF)

- Filenames are `snake_case` slugs inside lowercase folders; the human name lives in the `title` field
  (e.g. `people/jane_doe.md` with `title: Jane Doe`).
- Links are **bundle-relative markdown links** `[Text](/folder/slug.md)` — absolute from the vault root,
  starting with `/`. Never use `[[wikilinks]]`.
- Reserved files: per-folder `index.md` (a listing) and root `log.md` (the change history). OKF reserves
  both, so **they carry no frontmatter** — except the **root** `index.md`, whose frontmatter is the single
  line `okf_version: "0.2"` and nothing else.
- `CLAUDE.md` is bundle tooling, not a concept: it holds the one-line `@AGENTS.md` import and is excluded
  from conformance. See [Conventions](/system/conventions.md).

## Where things go (see [home](/home.md) for the live map)

- `people/` — humans in this context ([{{OWNER}}](/people/{{OWNER_SLUG}}.md), colleagues, contacts).
- `organizations/` — orgs ({{ORG_EXAMPLES}}).
- `tools/` — the working stack for this context (added as it's discovered).
- `projects/` — epics/projects. Each gets its own note (an epic gets a folder + MOC note).
- `meetings/` — one folder per meeting (`meetings/<slug>/`): a slug-named summary note + a `raw/`
  subfolder holding verbatim transcripts/sources. Lift action items into the relevant project notes.
- `sources/` — standalone verbatim raw captures (chat/email/note) that are reusable context but **not**
  tied to a meeting; each `type: source` + a short digest. (Project-specific raw goes in the project repo.)
- `daily/` — daily notes / log.
- `inbox/` — capture zone for raw, unsorted input. Process it into the right home, then clear it.
- `system/` — how the OS works ([OS Manifesto](/system/os_manifesto.md), [Conventions](/system/conventions.md),
  [the dream pass](/system/dream.md)).
- `_meta/` — machine-facing meta: [taxonomy](/_meta/taxonomy.md) (the controlled tag vocabulary).
- `index.md` / `log.md` — OKF reserved files: per-folder listings, and the vault-root change history.
- `_insights.md` — analytics (hubs, orphans, broken links, suggested links) — regenerated by the dream pass.

## Maintenance — the dream pass

Periodically (or on a schedule), run the consolidation pass specified in [dream](/system/dream.md): a deep
comb over the vault that re-links, repairs frontmatter, merges duplicates, refactors, safely quarantines
stale notes to `.trash/`, rebuilds the `index.md` files + MOCs, regenerates `_insights.md`, and validates
OKF conformance. The procedure is plain markdown, so any agent can follow it; in Claude Code the `/dream`
skill runs it. Do it after big imports or when the graph feels messy. It never hard-deletes; it reports
what needs {{OWNER_SHORT}}'s decision.

## Style

- Filenames are `snake_case` slugs; the `title` field holds the human name. Links are bundle-relative
  markdown links `[Text](/folder/slug.md)`.
- This vault is the source of truth for {{OWNER_SHORT}}'s operating context — not for code (code lives in
  the project repos).
- Be honest in status notes: if something is blocked, untested, or unconfirmed, say so.
