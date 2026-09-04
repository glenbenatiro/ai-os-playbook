---
type: changelog
title: Changelog - AI OS Playbook
description: Changes to the playbook itself - the canonical structure and the bootstrap procedure.
tags: [changelog]
generated:
  by: claude-code/kernel
  at: 2026-09-04T00:00:00Z
created: 2026-06-11
provenance: extracted
---

# Changelog — AI OS Playbook

Changes to the playbook itself (the canonical structure + bootstrap). Conventional-commit style.

## 2026-09-04 — OKF v0.2, AGENTS.md canonical, self-contained vaults

Four changes, all of which propagate to every live vault.

- **OKF v0.2.** Vaults declared conformance to v0.1 against a spec URL that has since moved; the standard
  now lives at [GoogleCloudPlatform/open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
  and is at v0.2. Frontmatter `timestamp` becomes `generated: {by, at}` (an actor plus an ISO 8601
  datetime with a UTC offset). The vault's lifecycle vocabulary moves out of `status` — which OKF
  reserves for `draft`/`stable`/`deprecated` — into a new `stage` field, with `status: deprecated` set
  on retired notes. `# Citations` is retired in favour of the `sources` frontmatter list. Reserved files
  lose their frontmatter, and the root `index.md` declares `okf_version: "0.2"` and nothing else.
- **`AGENTS.md` is the canonical kernel contract**, with `CLAUDE.md` reduced to the single line
  `@AGENTS.md`. `AGENTS.md` is the cross-tool standard, so the vendor-neutral file no longer depends on
  the vendor-specific one. `templates/client-CLAUDE.md` becomes `templates/client-AGENTS.md` for the same
  reason.
- **Vaults are self-contained.** The scaffold no longer refers to this repository or to any machine path,
  and the contract states the rule outright: everything needed to operate a vault lives inside it. The
  consolidation pass moves from `skills/dream/SKILL.md` into the vault at `system/dream.md`, tool-agnostic
  and readable by any agent; the Claude skill becomes a launcher that reads the vault's own copy.
- **Conformance is testable.** New `scripts/okf_check.py` (stdlib only) verifies a bundle, and
  `scripts/okf_migrate_0_1_to_0_2.py` performs the migration idempotently. This repository is now an OKF
  bundle itself, with its own `AGENTS.md`, `index.md` and document frontmatter.

Also adds a capture-back rule to the contract: an agent working in a project repo that a vault covers has
to surface a durable learning and offer to record it, rather than leaving it in the conversation. Fixes
two pieces of drift: the root `index.md` never listed `sources/`, and several documents pointed at
`CLAUDE.md` for rules that now live in `AGENTS.md`.

## 2026-06-22 — Raw-context routing + `sources/` folder

Generalized raw-context handling beyond meetings. Standalone raw context (a chat/DM, email, pasted note,
brain-dump) that's reusable but not tied to a meeting now has a home; project-specific raw routes to the
build repo. Changes to the canonical scaffold:

- **`templates/ai-os-scaffold/CLAUDE.md`** — new "Raw context — routing" section: a 3-way rule (meeting →
  `meetings/<slug>/raw/`; project working material → the project repo `docs/sources/`; standalone reusable
  → `sources/`), with the OS bar ("useful beyond this one task/project") as the tiebreak. Added a
  `sources/` bullet to "Where things go".
- **`templates/ai-os-scaffold/system/conventions.md`** — added `source` to the `type` enum + note-types
  table (lives in `sources/`); added `sources/` to the lowercase-folders list; extended "Raw records
  exempt" to cover `sources/`; added a Lifecycle routing pointer.
- **`templates/ai-os-scaffold/sources/index.md`** — new folder MOC; **`home.md`** lists `sources/`.

## 2026-06-21 — Foldered raw-source + paired-summary meeting convention

Codified how meeting transcripts/sources are stored, so every vault inherits it (previously only ad-hoc).
Changes to the canonical scaffold:

- **`templates/ai-os-scaffold/CLAUDE.md`** — new "Meetings — raw sources + paired summary" section: each
  meeting is a folder `meetings/<slug>/` with a slug-named summary (the folder note) + a `raw/` subfolder
  holding verbatim transcripts/sources, one file per source. The raw↔summary pairing is **mandatory**
  (write the summary in the same turn); no `index.md` inside a meeting folder; `_dump/` transcripts get
  their content captured into the folder. Rule 6 cross-links the section.
- **`templates/ai-os-scaffold/system/conventions.md`** — added `meeting-transcript` / `meeting-source`
  to the `type` enum + note-types table (living in `meetings/<slug>/raw/`); a "Raw records exempt"
  frontmatter bullet; rewrote the meeting-naming rule to the foldered shape; added a lifecycle pairing
  reminder.

## 2026-06-16 — Full OKF v0.1 conformance

Migrated the playbook to conform to Google's [OKF (Open Knowledge Format) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf).
Each vault is now an OKF knowledge bundle. Changes to the canonical scaffold + conventions:

- **Frontmatter** renamed to OKF fields: `summary`→`description`, `updated`→`timestamp`; added a
  required `title` (the human name, since filenames are now slugs); kept `created`/`provenance`/`status`
  and added `resource` as OKF extension fields. `type` remains required and non-empty (OKF conformance).
- **Filenames** are now `snake_case` slugs and **folders are lowercase** (`people/`, `tools/`, `system/`,
  …) — matching OKF's own example bundles.
- **Links** are OKF bundle-relative markdown links `[Text](/folder/slug.md)` instead of `[[wikilinks]]`
  (verified to resolve in Obsidian's graph, with ghost nodes intact).
- **Reserved files:** per-folder `index.md` (root one declares `okf_version: "0.1"`) for
  progressive disclosure; `System/Changelog.md` → root `log.md` (OKF date-grouped history).
- **`/dream`** rewritten as the OKF maintenance + migration engine (re-link, repair, rebuild `index.md`,
  validate conformance, and migrate pre-OKF vaults).
- New `references/okf_mapping.md` documents the OKF↔AI-OS mapping; `README.md`, `BOOTSTRAP.md`,
  `templates/user-CLAUDE.md`, and `templates/client-CLAUDE.md` updated to the new conventions.

## 2026-06-11 — Initial release

- Canonical `templates/ai-os-scaffold/`: the vault skeleton — kernel `CLAUDE.md`, `System/` (OS Manifesto,
  Conventions, Changelog), `Home.md` (MOC), `People/ Organizations/ Tools/ Projects/ Meetings/ Daily/`,
  `Inbox/`, `_meta/taxonomy.md`, `_insights.md`, `_dump/`, `.obsidian/`, and a README.
- Kernel contract: 11 rules — proactive linking + stub-on-mention, valid frontmatter, link up/across,
  update-the-index, log structural changes, faithful edits, digest the Inbox, never-silently-delete
  (quarantine to `_dump/`), ISO dates, flag-uncertainty/provenance, and a privacy boundary.
- Frontmatter standard: `type, status, tags, created, updated, summary, provenance`
  (`provenance` ∈ `extracted | inferred | to-confirm`).
- Controlled-vocabulary tags (`_meta/taxonomy.md`), graph analytics (`_insights.md`), and an
  `Inbox → wiki → schema` lifecycle.
- `templates/user-CLAUDE.md` (generic AI OS routing rule) and `templates/client-CLAUDE.md` (folder-level
  routing section).
- LLM-agnostic entrypoint: `AGENTS.md` alongside `CLAUDE.md`, so any agent (Codex, Cursor, Gemini CLI,
  Windsurf, …) boots into kernel mode without forking the rules.
- `skills/dream/`: the `/dream` consolidation skill — re-link, repair, merge, refactor, safe-quarantine
  to `_dump/`, rebuild MOCs + `_insights.md`; interactive and unattended modes.
- `README.md` (layered model, evolve-here-first rule) and `BOOTSTRAP.md` (machine profiles, placeholder
  reference, privacy variants, `/schedule` wiring).
