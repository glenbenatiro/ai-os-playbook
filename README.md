# AI OS Playbook

A portable, repeatable structure for an AI Operating System (AI OS) — a knowledge layer that an LLM
maintains for you — plus the procedure to bootstrap it on any machine. It's the single source of truth
for the structure: define it once, apply it to every context, carry it to any new machine.

Built and battle-tested with Claude Code; LLM-agnostic by design. Shared as a set of best practices for
anyone who wants a durable, self-maintaining context store for their AI agents.

## What an AI OS is

A Karpathy-style LLM-OS: a plain-markdown, Obsidian-readable vault (wikilinked notes + a graph view)
that an LLM maintains as its kernel. You speak in natural language; the agent does the reading, writing,
linking, and housekeeping. The vault is durable memory (the "disk"); the context window is RAM; Obsidian
is the display. It's the durable context store so you never have to repeat yourself to an LLM twice.

This is the same lineage as Karpathy's "LLM OS" framing and the public "LLM Wiki" pattern — see each
vault's `System/OS Manifesto.md`.

> Not to be confused with the academic *agiresearch/AI OS* (an agent-runtime OS). Same name, different thing.

### LLM-agnostic by design

The vaults aren't tied to any one model or tool. The knowledge is plain markdown + `[[wikilinks]]` +
YAML — any agent (Claude Code, Codex, Cursor, Gemini CLI, Windsurf, a local model) or even `grep` can
read and write it. The operating contract ships as two entrypoints describing the same rules: `CLAUDE.md`
(Claude Code, canonical) and `AGENTS.md` (the cross-tool standard the others read). Point any tool's own
rules file (`.cursor/rules`, `GEMINI.md`, …) at `CLAUDE.md` and keep it as the single source — never
fork the rules. The `/dream` maintenance routine is a Claude skill, but its spec (`skills/dream/SKILL.md`)
is plain markdown any agent can follow step-by-step.

## The layered model

A clean separation between global facts, a personal layer, and one AI OS per context (client, project,
or area):

| Layer | Location | Owner | Purpose |
|---|---|---|---|
| 0 — User config | `~/.claude/CLAUDE.md` | hybrid | Who you are + global conventions + a generic AI OS routing rule + pointer here |
| 1 — Personal OS | `~/Projects/personal-os/` | agent (kernel) | Cross-context AI OS: you, your stack, working patterns |
| 2 — Context CLAUDE.md | `~/Projects/<context>/CLAUDE.md` | hybrid | People + working-arrangement context for that area |
| 3 — Context AI OS | `~/Projects/<context>/<context>-os/` | agent (kernel) | The knowledge graph for that context |
| 4 — Project/code | `~/Projects/<context>/<project>/CLAUDE.md` | hybrid | Per-repo technical conventions |

## What's in this repo

```
ai-os-playbook/
  README.md                  # this file
  BOOTSTRAP.md               # how an agent scaffolds the AI OS on a fresh machine
  CHANGELOG.md               # changes to the playbook itself
  LICENSE                    # MIT
  skills/
    dream/SKILL.md           # the /dream vault-consolidation skill (install to ~/.claude/skills/)
  templates/
    user-CLAUDE.md           # -> ~/.claude/CLAUDE.md
    client-CLAUDE.md         # -> ~/Projects/<context>/CLAUDE.md
    ai-os-scaffold/           # the canonical vault skeleton (copied per context)
```

## Keep AI OS repos private

Vaults hold private operating context (people, decisions, working detail). If you version them, create
the remotes private (`gh repo create … --private`). This playbook itself is fine to share; the vaults it
produces generally are not.

## The canonical conventions (what every vault inherits)

- Kernel contract (`<vault>/CLAUDE.md`): proactive linking, stub-on-mention, update-the-index,
  log-structural-changes, faithful edits, never-silently-delete, ISO dates, flag-uncertainty, privacy.
- Frontmatter: `type, status, tags, created, updated, summary, provenance`
  (`provenance` ∈ `extracted | inferred | to-confirm`).
- Structure: `Home.md` (MOC) · `System/` (Manifesto, Conventions, Changelog) · `People/`
  `Organizations/` `Tools/` `Projects/` `Meetings/` `Daily/` · `Inbox/` (raw capture) ·
  `_meta/taxonomy.md` (controlled tag vocabulary) · `_insights.md` (graph analytics) · `_dump/`
  (prune quarantine) · `.obsidian/` (graph-view config).
- Linking: `[[wikilinks]]` for every entity; stubs so links always resolve; link up + across.
- Lifecycle: `Inbox → wiki → schema`. Periodic `/dream` deep-clean.

## How to evolve the structure (the rule that keeps it scalable)

Structure changes here first, then propagates. When a convention should change, edit the `templates/`
in this repo, bump `CHANGELOG.md`, then apply the change to the live vaults (a `/dream` run can carry
most of it). Live vaults are instances of this template — don't let them drift independently. Each vault
may keep small local conventions, documented in its own `System/`.

## Quick start

- New machine: read `BOOTSTRAP.md`.
- New context on an existing machine: copy `templates/ai-os-scaffold/` → `<context>/<context>-os/`, fill
  placeholders, `git init`, write `<context>/CLAUDE.md` from `templates/client-CLAUDE.md`.
- Tidy a vault: run `/dream` on it.

## Credits

Inspired by Andrej Karpathy's "LLM OS" framing and the open-source "LLM Wiki" pattern for
agent-maintained Obsidian knowledge bases.

## License

[MIT](LICENSE) — use it, adapt it, share it.
