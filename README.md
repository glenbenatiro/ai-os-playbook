# AI OS Playbook

A portable, repeatable structure for an AI Operating System (AI OS) — a knowledge layer that an LLM
maintains for you — plus the procedure to bootstrap it on any machine. It's the single source of truth
for the structure: define it once, apply it to every context, carry it to any new machine.

Built and battle-tested with Claude Code; LLM-agnostic by design. Shared as a set of best practices for
anyone who wants a durable, self-maintaining context store for their AI agents.

## What an AI OS is

A Karpathy-style LLM-OS: a plain-markdown, Obsidian-readable vault — an
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundle
(markdown + YAML frontmatter + bundle-relative links, viewed as a graph) — that an LLM maintains as its
kernel. You speak in natural language; the agent does the reading, writing, linking, and housekeeping. The
vault is durable memory (the "disk"); the context window is RAM; Obsidian is the display. It's the durable
context store so you never have to repeat yourself to an LLM twice.

This is the same lineage as Karpathy's "LLM OS" framing and the public "LLM Wiki" pattern — see each
vault's `system/os_manifesto.md`.

> Not to be confused with the academic *agiresearch/AI OS* (an agent-runtime OS). Same name, different thing.

### LLM-agnostic by design

The vaults aren't tied to any one model or tool. The knowledge is plain markdown + YAML frontmatter +
bundle-relative links, conformant to
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) — any agent (Claude
Code, Codex, Cursor, Gemini CLI, Windsurf, a local model), any OKF-aware tool, or even `grep` can read and
write it. The operating contract ships as two entrypoints describing the same rules: `CLAUDE.md`
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
  references/
    okf_mapping.md           # OKF v0.1 <-> AI OS field/structure mapping (the standard this conforms to)
  skills/
    dream/SKILL.md           # the /dream vault-consolidation + OKF-migration skill (install to ~/.claude/skills/)
  templates/
    user-CLAUDE.md           # -> ~/.claude/CLAUDE.md
    client-CLAUDE.md         # -> ~/Projects/<context>/CLAUDE.md
    ai-os-scaffold/           # the canonical vault skeleton (OKF v0.1 bundle; copied per context)
```

## Keep AI OS repos private

Vaults hold private operating context (people, decisions, working detail). If you version them, create
the remotes private (`gh repo create … --private`). This playbook itself is fine to share; the vaults it
produces generally are not.

## The canonical conventions (what every vault inherits)

- OKF v0.1 conformance: every vault is an OKF knowledge bundle (a non-empty `type` on every note;
  `index.md`/`log.md` reserved files). See `references/okf_mapping.md`.
- Kernel contract (`<vault>/CLAUDE.md`): proactive linking, stub-on-mention, maintain-the-index,
  log-structural-changes, faithful edits, never-silently-delete, ISO dates, flag-uncertainty, privacy.
- Frontmatter: `type, title, description, tags, timestamp` + extensions
  `created, provenance, status, resource` (`provenance` ∈ `extracted | inferred | to-confirm`).
- Filenames are `snake_case` slugs in lowercase folders; the human name lives in `title`.
- Structure: `home.md` (MOC) · root `index.md` (declares `okf_version`) · `log.md` (change history) ·
  `system/` (manifesto, conventions) · `people/ organizations/ tools/ projects/ meetings/ daily/` ·
  `inbox/` (raw capture) · `_meta/taxonomy.md` · `_insights.md` (graph analytics) · `_dump/` (prune
  quarantine) · `.obsidian/` (graph-view config).
- Linking: bundle-relative markdown links `[Text](/folder/slug.md)` for every entity; stubs so links
  always resolve; link up + across.
- Lifecycle: `inbox → wiki → schema`. Periodic `/dream` deep-clean (also performs the OKF migration).

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
