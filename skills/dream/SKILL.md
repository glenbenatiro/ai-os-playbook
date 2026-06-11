---
name: dream
description: Deep-clean an AI OS vault — re-link, repair frontmatter, merge duplicates, refactor, safely quarantine stale notes, rebuild MOCs, and regenerate _insights.md. The "memory consolidation" pass that catches what day-to-day editing misses. Use when an AI OS vault feels messy, after a big import, or on a schedule.
disable-model-invocation: true
argument-hint: "[vault-path] [--mode interactive|unattended]"
---

# /dream — AI OS vault consolidation

You are running a **consolidation pass** ("dreaming") over an AI OS vault — a Karpathy-style LLM-OS
markdown vault (see the vault's own `CLAUDE.md` + `System/Conventions.md`). Day-to-day editing leaves
gaps: unlinked mentions, drifted frontmatter, near-duplicate notes, stale entries, orphaned indexes.
Your job is to comb the whole vault and groom it back to the conventions — **without ever destroying
information**.

## 0. Resolve target & mode

- **Vault:** the path in `$ARGUMENTS`, else the `*-os/` vault in or under the current directory, else
  ask. Confirm you found a vault root (it has a `CLAUDE.md`, `System/`, and `Home.md`). If not, stop.
- **Read the vault's own contract first:** `<vault>/CLAUDE.md`, `System/Conventions.md`, `_meta/taxonomy.md`.
  Those rules **override** anything here on conflict — every vault is allowed local conventions.
- **Mode:**
  - `interactive` (default): apply safe changes directly; **propose** anything destructive or ambiguous
    (merges, moves, prunes) and ask before doing them.
  - `unattended` (for cron / `/schedule`): apply safe changes; for anything destructive or ambiguous,
    **quarantine to `_dump/` and report** — never delete, never guess on a risky merge.

## 1. Inventory (read before you write)

Build a picture of the vault: every note's path, `type`, `tags`, `created/updated`, `summary`,
outbound `[[links]]`, and inbound backlinks. Note the folder each `type` is supposed to live in.

## 2. Re-link (the most important pass)

- Scan note bodies for **unlinked mentions** of entities that already have notes → wrap them in
  `[[links]]`. Respect "link on meaningful mention," not every incidental word.
- For link-worthy entities that are mentioned but have **no note**, create a **stub** (frontmatter +
  one-line `summary` + a sentence) so the link resolves and the graph connects.
- Ensure every note links **up** to its parent MOC and **across** to related entities; ensure hub/MOC
  notes link back **down** to their children.

## 3. Repair

- Fix **broken/unresolved links** (rename target, fix typo, or stub it).
- Normalize **frontmatter**: ensure required fields exist (`type`, `created`, `updated`, `summary`,
  `provenance`; `status` where the type warrants it). Add missing `summary` by reading the note. Bump
  `updated` only where you made a real content change. Never alter `created`.
- **Tags:** flag any tag not registered in `_meta/taxonomy.md`. Map obvious synonyms to the canonical
  tag; for genuinely new-but-useful tags, add them to the taxonomy with a one-line definition.

## 4. Merge-first dedup

- Detect duplicate / near-duplicate notes (same entity, split notes). **Merge** into the best-named
  canonical note: combine substance, preserve every fact and its `provenance`, repoint inbound links,
  leave a `> note: merged from [[Old Title]] on <date>` line. In `unattended` mode, only auto-merge
  unambiguous exact-subject dupes; send judgment calls to the report.

## 5. Refactor

- Split oversized grab-bag notes into atomic notes + a MOC; promote a concept that recurs across many
  notes into its own note; move misfiled notes to the folder their `type` dictates (update links).
- Keep edits **faithful** — relocate and restructure, don't rewrite meaning.

## 6. Prune — safely

- Identify **stale / empty / superseded / orphaned** notes. Do **not** delete them. **Move** each to
  `_dump/` with a one-line reason appended to the note (`> dumped <date>: <why>`), and list them in the
  report for the owner's decision. Honour the vault's "never silently delete" rule even unattended.

## 7. Rebuild indexes & insights

- Refresh `Home.md` and section MOCs so nothing is orphaned and new notes are reachable.
- **Regenerate `_insights.md`** (overwrite it): hubs (most-linked), orphans (no links in or out),
  broken/unresolved links remaining, suggested links you did *not* auto-apply, prune candidates now in
  `_dump/`, and off-taxonomy tags. Set its `updated` and the "Last run" line to today's date.

## 8. Report + log

- Append one dated line to `System/Changelog.md` summarizing the structural changes.
- End your turn with a **run report**: what you changed (counts: links added, stubs created, notes
  merged/moved/dumped, frontmatter fixed), and a clear **"needs your decision"** list (everything in
  `_dump/`, risky merges you held back, new tags you added). In `interactive` mode, this is where you
  ask about the proposals you surfaced.

## Guardrails

- **Information is never lost** — prune = quarantine to `_dump/`, never `rm`.
- **`_dump/` is local-only — never commit it.** It is gitignored scratch (raw drops + prune quarantine).
  If a run commits (e.g. unattended/cron), never stage or push `_dump/`; surface its contents in the
  report instead. Before any commit, confirm `_dump/` items are already reflected in the vault.
- The vault's own `CLAUDE.md`/`Conventions.md` win on any conflict with this skill.
- Prefer many small, reviewable edits over sweeping rewrites. Preserve `created` dates and `provenance`.
- If the vault is large, work folder-by-folder (`People/` → `Organizations/` → `Tools/` → `Projects/`
  → `Meetings/` → `Daily/`) so a long run stays resumable and reviewable.
