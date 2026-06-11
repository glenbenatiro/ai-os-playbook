# Changelog — AI OS Playbook

Changes to the playbook itself (the canonical structure + bootstrap). Conventional-commit style.

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
