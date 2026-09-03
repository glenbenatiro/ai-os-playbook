---
name: dream
description: Deep-clean and OKF-maintain an AI OS vault — re-link, repair frontmatter, migrate legacy notes to OKF v0.1 (snake_case slugs, lowercase folders, title field, bundle-relative links, index.md/log.md), merge duplicates, refactor, safely quarantine stale notes, rebuild indexes, validate conformance, and regenerate _insights.md. Use when a vault feels messy, after a big import, when migrating a vault to OKF, or on a schedule.
disable-model-invocation: true
argument-hint: "[vault-path] [--mode interactive|unattended]"
---

# /dream — AI OS vault consolidation & OKF maintenance

You are running a **consolidation pass** ("dreaming") over an AI OS vault — an
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundle and
Karpathy-style LLM-OS (see the vault's own `CLAUDE.md` + `system/conventions.md`). Day-to-day editing
leaves gaps: unlinked mentions, drifted frontmatter, near-duplicate notes, stale entries, stale `index.md`.
Your job is to comb the whole vault and groom it back to the conventions — and, when a vault predates OKF,
**migrate it** — **without ever destroying information**.

## 0. Resolve target & mode

- **Vault:** the path in `$ARGUMENTS`, else the `*-os/` vault in or under the current directory, else ask.
  Confirm you found a vault root (it has a `CLAUDE.md`, a `system/` or `System/`, and a `home.md`/`Home.md`).
  If not, stop.
- **Read the vault's own contract first:** `<vault>/CLAUDE.md`, `system/conventions.md`, `_meta/taxonomy.md`.
  Those rules **override** anything here on conflict — every vault is allowed local conventions.
- **Mode:**
  - `interactive` (default): apply safe changes directly; **propose** anything destructive or ambiguous
    (merges, moves, prunes, a first-time OKF migration) and ask before doing them.
  - `unattended` (for cron / `/schedule`): apply safe changes; for anything destructive or ambiguous,
    **quarantine to `.trash/` and report** — never delete, never guess on a risky merge.

## 1. Inventory (read before you write)

Build a picture of the vault: every note's path, `type`, `title`, `tags`, `created`/`timestamp`,
`description`, outbound links, and inbound backlinks. Note the folder each `type` is supposed to live in.

## 2. OKF migration (run only if the vault predates OKF — skip whatever is already done)

Detect legacy markers: Title-Case filenames, `[[wikilinks]]`, `summary`/`updated` frontmatter fields,
Title-Case folders, a `System/Changelog.md`. Where present, migrate — a mechanical,
information-preserving transform (in `interactive` mode, confirm before the first run; do it folder by
folder):

a. **Index** every note: current path, basename, `title` (H1 or filename), and any aliases.
b. **Compute targets:** `snake_case(basename)` filename in a lowercased folder; record an old→new path
   map. Resolve slug collisions by appending a short disambiguator.
c. **Rewrite links** across all notes using the map: `[[Name]]` → `[Name](/folder/slug.md)`;
   `[[Name|Alias]]` → `[Alias](/folder/slug.md)`; `[[Name#Heading]]` → `[Name](/folder/slug.md#heading)`.
   Stubs (targets with no file) link to the intended slug path — OKF tolerates them.
d. **Rename** files (`git mv` so renames show as renames) to the new paths; lowercase the folders. Keep
   these names **verbatim**: `CLAUDE.md`, `AGENTS.md`, `README.md`, `index.md`, `log.md`, `_meta/`,
   `.obsidian/`.
e. **Frontmatter:** add `title` (the old human name); rename `summary`→`description`, `updated`→`timestamp`;
   ensure a non-empty `type`; keep `created`/`provenance`/`status`/`resource`. Add frontmatter
   (`type: system`) to `CLAUDE.md`/`AGENTS.md`/`README.md` if missing.
f. **Reserved files:** create the root `index.md` (`okf_version: "0.1"` + a grouped listing) and a
   per-folder `index.md`; convert `System/Changelog.md` → root `log.md` (date-grouped, newest first).
g. **Verify** (step 8) that no `[[wikilinks]]` remain and every md-link path resolves or is an
   intentional stub.

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
- Normalize **frontmatter** to the OKF schema: `type` (required, non-empty), `title`, `description`,
  `tags`, `timestamp`; `created`/`provenance` always, `status` where the type warrants it. Add a missing
  `description` by reading the note. Bump `timestamp` only where you made a real content change. Never
  alter `created`.
- **Tags:** flag any tag not registered in `_meta/taxonomy.md`. Map obvious synonyms to the canonical
  tag; for genuinely new-but-useful tags, add them to the taxonomy with a one-line definition.

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

- Refresh `home.md`, section MOCs, and **every folder's `index.md`** (and the root `index.md` with
  `okf_version: "0.1"`) so nothing is orphaned and new notes are reachable. Index entries are
  `- [Title](slug.md) — description`.
- **Regenerate `_insights.md`** (overwrite it): hubs (most-linked), orphans (no links in or out),
  broken/unresolved links remaining, suggested links you did *not* auto-apply, prune candidates now in
  `.trash/`, off-taxonomy tags, and an **OKF-conformance** section (notes missing a non-empty `type`,
  unparseable frontmatter, malformed `index.md`/`log.md`, any remaining `[[wikilinks]]`). Set its
  `timestamp` and the "Last run" line to today's date.

## 9. Report + log

- Append a dated entry to `log.md` (OKF format: `## YYYY-MM-DD`, newest first; `**Update**` /
  `**Creation**` / `**Deprecation**` prefixes) summarizing the structural changes.
- End your turn with a **run report**: what you changed (counts: links added, stubs created, notes
  merged/moved/dumped, frontmatter fixed, notes migrated to OKF), and a clear **"needs your decision"**
  list (everything in `.trash/`, risky merges you held back, new tags you added). In `interactive` mode,
  this is where you ask about the proposals you surfaced.

## Guardrails

- **Information is never lost** — prune = quarantine to `.trash/`, never `rm`.
- **`.trash/` is local-only — never commit it.** It is gitignored quarantine for prune
  candidates. If a run commits (e.g. unattended/cron), never stage or push `.trash/`; surface its
  contents in the report instead, so nothing is lost silently.
- The vault's own `CLAUDE.md`/`conventions.md` win on any conflict with this skill.
- **OKF migration is mechanical and reviewable** — prefer `git mv` so renames show as renames; never lose
  a fact or a `created` date or a `provenance` value in the rewrite. Work folder-by-folder on large
  vaults (`people/` → `organizations/` → `tools/` → `projects/` → `meetings/` → `daily/`) so a long run
  stays resumable and reviewable.
- Prefer many small, reviewable edits over sweeping rewrites.
