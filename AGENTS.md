---
type: system
title: AGENTS.md — AI OS Playbook
description: How to change this playbook - evolve here first, keep it public-safe, then propagate to live vaults.
tags: [system, conventions]
generated:
  by: claude-code/kernel
  at: 2026-09-04T00:00:00Z
created: 2026-09-04
provenance: extracted
---

# AGENTS.md — AI OS Playbook

This repository is the canonical structure for an AI Operating System: the vault scaffold, the bootstrap
procedure, and the conformance tooling. It is not itself a vault of anyone's knowledge — it is the
template every vault is stamped from.

> `CLAUDE.md` beside this file holds one line, `@AGENTS.md`, so Claude Code reads these same rules.
> `AGENTS.md` is canonical. Never fork the rules into a second file.

## This repository is public

Treat every change as published, because it is. Nothing here may name a private vault, a client, an
employer, a person, a machine path, a hostname, or a credential — not in the documents, not in a commit
message, not in a pull request description. Contexts are described through placeholders
(`{{CLIENT_NAME}}`, `{{OWNER}}`, `{{OS_DIR}}`) and examples are invented (`Acme Corp`, `Jane Doe`). If a
change cannot be written without naming something real, it belongs in that vault, not here.

## Evolve here first, then propagate

Structure changes here, then flows outward. When a convention should change:

1. Edit `templates/` in this repository.
2. Add an entry to `CHANGELOG.md` explaining what changed and why.
3. Run the checks below.
4. Apply the change to the live vaults. Each vault is self-contained, so the change has to be made in
   each one; a dream pass carries most of it.

Live vaults are instances of this template — don't let them drift independently. A vault may keep small
local conventions, documented in its own `system/conventions.md`.

## The vaults this produces are self-contained

A vault must never point back at this repository, at the machine it was created on, or at whoever hosts
it. Everything needed to operate a vault — the contract, the conventions, the taxonomy, the dream pass —
ships inside the vault. When you add something to the scaffold, ask whether a vault could still be
operated after this repository disappeared. If not, the rule belongs inside the vault.

## Checks before committing

```bash
python3 scripts/okf_check.py templates/ai-os-scaffold --allow-placeholders
python3 scripts/okf_check.py . --exclude templates --exclude skills
```

Both must report no failures. `--allow-placeholders` exists because the scaffold ships `{{TOKENS}}` where
a real datetime or actor will go. `templates/` is checked on its own because it is a bundle in its own
right, and `skills/` is excluded because a Claude Code `SKILL.md` carries that tool's frontmatter rather
than OKF's. Add `--strict` to also run the PyYAML parse check when it is installed.

## Conventions

- Conventional Commits (`feat(scaffold):`, `docs:`, `fix(scripts):`), with a body explaining the why.
- The scripts are stdlib-only. A vault owner should be able to check conformance with nothing installed.
- Markdown diagrams use mermaid code blocks, not ASCII art.
- This repository is itself an OKF v0.2 bundle: its documents carry frontmatter, `index.md` and `log.md`
  are reserved, and the root `index.md` declares the version.
