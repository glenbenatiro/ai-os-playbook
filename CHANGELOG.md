# Changelog — AI OS Playbook

Changes to the playbook itself (the canonical structure + bootstrap). Conventional-commit style.

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
