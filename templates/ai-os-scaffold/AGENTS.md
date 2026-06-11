# AGENTS.md — {{OS_NAME}}

This repository is an AI OS (AI Operating System): a Karpathy-style LLM-OS vault that an AI agent
maintains as its kernel. It is LLM-agnostic — any agent (Claude Code, Codex, Cursor, Gemini CLI,
Windsurf, a local model, …) can operate it, because the whole thing is plain markdown + `[[wikilinks]]`
with nothing proprietary.

## Read the operating contract first

The full kernel contract lives in `CLAUDE.md` in this same directory — it is the single source of truth
for how to behave in this vault. Read it now and follow it exactly before you add, edit, link, or delete
anything. The conventions are in `System/Conventions.md`; the philosophy is in `System/OS Manifesto.md`;
the live map is `Home.md`.

> `CLAUDE.md` (Claude Code's entrypoint) and this `AGENTS.md` (the cross-tool standard) describe the same
> contract. `CLAUDE.md` is canonical; this file points to it so any agent boots into kernel mode. If you
> maintain another tool's rules file (`.cursor/rules`, `GEMINI.md`, …), point it here too and keep
> `CLAUDE.md` as the source — never fork the rules.

## The contract in five lines (the full version is in `CLAUDE.md`)

1. You are the kernel. {{OWNER_SHORT}} speaks in natural language; you do the reading, writing, linking,
   and housekeeping. {{OWNER_SHORT}} does not hand-edit the vault.
2. Link proactively — wikilink every entity that has (or should have) a note; create a stub for anything
   missing so links always resolve. A note with no links is a bug.
3. Valid frontmatter on every note: `type, status, tags, created, updated, summary, provenance`. Tags
   must be registered in `_meta/taxonomy.md`.
4. Never silently delete; don't invent. Quarantine prune candidates to `_dump/`; flag unconfirmed facts
   with a `> ⚠️ **to confirm**` callout and `provenance: to-confirm`.
5. Keep it coherent. Update the relevant MOC and append to `System/Changelog.md` on structural changes;
   convert relative dates to ISO against {{OWNER_SHORT}}'s working window.

## Maintenance — the "dream" pass

The periodic deep-clean (re-link, repair, merge, refactor, safe-prune, rebuild indexes) is specified in
`ai-os-playbook/skills/dream/SKILL.md`. In Claude Code it's the `/dream` skill; any other agent can run
the same pass by reading that file and following its steps against this vault.
