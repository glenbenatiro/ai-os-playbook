---
type: documentation
title: AI OS Playbook
description: A portable, LLM-agnostic structure for building AI Operating Systems - markdown vaults an LLM maintains as its kernel.
tags: [documentation, ai_os]
generated:
  by: claude-code/kernel
  at: 2026-09-04T00:00:00Z
created: 2026-06-11
provenance: extracted
---

# AI OS Playbook

A portable, repeatable structure for an AI Operating System (AI OS) — a knowledge layer that an LLM
maintains for you — plus the procedure to bootstrap it on any machine. It's the single source of truth
for the structure: define it once, apply it to every context, carry it to any new machine.

Built and battle-tested with Claude Code; LLM-agnostic by design. Shared as a set of best practices for
anyone who wants a durable, self-maintaining context store for their AI agents.

## What an AI OS is

A Karpathy-style LLM-OS: a plain-markdown, Obsidian-readable vault — an
[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2
knowledge bundle (markdown + YAML frontmatter + bundle-relative links, viewed as a graph) — that an LLM
maintains as its kernel. You speak in natural language; the agent does the reading, writing, linking, and housekeeping. The
vault is durable memory (the "disk"); the context window is RAM; Obsidian is the display. It's the durable
context store so you never have to repeat yourself to an LLM twice.

This is the same lineage as Karpathy's "LLM OS" framing and the public "LLM Wiki" pattern — see each
vault's `system/os_manifesto.md`.

> Not to be confused with the academic *agiresearch/AI OS* (an agent-runtime OS). Same name, different thing.

### LLM-agnostic by design

The vaults aren't tied to any one model or tool. The knowledge is plain markdown + YAML frontmatter +
bundle-relative links, conformant to
[OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format) — any agent (Claude Code, Codex,
Cursor, Gemini CLI, Windsurf, a local model), any OKF-aware tool, or even `grep` can read and write it.

The operating contract lives in **`AGENTS.md`**, the cross-tool standard every agent reads. `CLAUDE.md`
sits beside it holding one line — `@AGENTS.md` — which Claude Code resolves as an import, so there is one
copy of the rules and no vendor-specific fork. Point any other tool's rules file (`.cursor/rules`,
`GEMINI.md`, …) at `AGENTS.md` too.

Each vault is **self-contained**: the contract, the conventions, the taxonomy and the maintenance
procedure all ship inside it, so a vault can be handed to another person or machine whole and depends on
nothing here.

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
  AGENTS.md                  # how to change this playbook (CLAUDE.md is a one-line shim)
  CHANGELOG.md               # changes to the playbook itself
  index.md                   # OKF root reserved file
  LICENSE                    # MIT
  references/
    okf_mapping.md           # OKF v0.2 <-> AI OS field/structure mapping (the standard this conforms to)
  scripts/
    okf_check.py             # conformance checker (stdlib only)
    okf_migrate_0_1_to_0_2.py # carries a v0.1 bundle to v0.2
  skills/
    dream/SKILL.md           # /dream launcher for Claude Code (install to ~/.claude/skills/)
  templates/
    user-CLAUDE.md           # -> ~/.claude/CLAUDE.md
    client-AGENTS.md         # -> ~/Projects/<context>/AGENTS.md (+ a one-line CLAUDE.md shim)
    ai-os-scaffold/          # the canonical vault skeleton (OKF v0.2 bundle; copied per context)
```

## Keep AI OS repos private

Vaults hold private operating context (people, decisions, working detail). If you version them, create
the remotes private (`gh repo create … --private`). This playbook itself is fine to share; the vaults it
produces generally are not.

## The canonical conventions (what every vault inherits)

- OKF v0.2 conformance: every vault is an OKF knowledge bundle (a non-empty `type` on every note;
  `index.md`/`log.md` reserved and frontmatter-free; the root `index.md` declaring `okf_version`).
  See `references/okf_mapping.md`, and run `scripts/okf_check.py <vault>` to verify it.
- Kernel contract (`<vault>/AGENTS.md`): proactive linking, stub-on-mention, maintain-the-index,
  log-structural-changes, faithful edits, never-silently-delete, ISO dates, flag-uncertainty, privacy,
  and capture-back — when an agent working in a project repo learns something durable, it says so and
  offers to record it in the vault.
- Frontmatter: `type, title, description, tags, generated {by, at}` + extensions
  `created, provenance, stage, resource` (`provenance` ∈ `extracted | inferred | to-confirm`). OKF's
  `status` is reserved for `draft | stable | deprecated`; the vault's own lifecycle lives in `stage`.
- Filenames are `snake_case` slugs in lowercase folders; the human name lives in `title`.
- Structure: `home.md` (MOC) · root `index.md` (declares `okf_version`) · `log.md` (change history) ·
  `system/` (manifesto, conventions, the dream pass) · `people/ organizations/ tools/ projects/ meetings/
  daily/ sources/` · `inbox/` (raw capture) · `_meta/taxonomy.md` · `_insights.md` (graph analytics) ·
  `.obsidian/` (graph-view config).
- Linking: bundle-relative markdown links `[Text](/folder/slug.md)` for every entity; stubs so links
  always resolve; link up + across.
- Lifecycle: `inbox → wiki → schema`. Periodic deep-clean via the vault's own `system/dream.md` (also
  performs the OKF migration); in Claude Code the `/dream` skill runs it.

## How to evolve the structure (the rule that keeps it scalable)

Structure changes here first, then propagates. When a convention should change, edit the `templates/`
in this repo, bump `CHANGELOG.md`, run `scripts/okf_check.py`, then apply the change to the live vaults
(a dream pass can carry most of it). Live vaults are instances of this template — don't let them drift
independently. Each vault may keep small local conventions, documented in its own `system/`.

Because vaults are self-contained, the change has to land in each one; nothing is inherited at runtime.
See `AGENTS.md` for the full working rules for this repository.

## Quick start

- New machine: read `BOOTSTRAP.md`.
- New context on an existing machine: copy `templates/ai-os-scaffold/` → `<context>/<context>-os/`, fill
  placeholders, `git init`, write `<context>/AGENTS.md` from `templates/client-AGENTS.md` (plus a
  one-line `CLAUDE.md` shim).
- Check a vault: `python3 scripts/okf_check.py <vault>`.
- Tidy a vault: run its dream pass (`/dream` in Claude Code).

## Credits

Inspired by Andrej Karpathy's "LLM OS" framing and the open-source "LLM Wiki" pattern for
agent-maintained Obsidian knowledge bases.

## License

[MIT](LICENSE) — use it, adapt it, share it.
