---
name: dream
description: Run an AI OS vault's consolidation pass — re-link, repair frontmatter, migrate to OKF v0.2, merge duplicates, refactor, safely quarantine stale notes, rebuild indexes, validate conformance, and regenerate _insights.md. Use when a vault feels messy, after a big import, when migrating a vault to OKF, or on a schedule.
disable-model-invocation: true
argument-hint: "[vault-path] [--mode interactive|unattended]"
---

# /dream — run a vault's consolidation pass

Every AI OS vault carries its own consolidation procedure at `system/dream.md`. This skill is the
launcher: it finds the vault and follows that procedure. The vault owns the rules, so a vault can
evolve its own pass without this skill changing.

## 1. Resolve the vault

The vault root is the path in `$ARGUMENTS`, else the `*-os/` vault in or under the current directory,
else ask. Confirm you have a vault root: it contains `AGENTS.md`, a `system/` directory, and `home.md`.

## 2. Read the procedure

Read `<vault>/system/dream.md` and follow it step by step, in the mode requested (`interactive` by
default, `unattended` for a scheduled run). Read `<vault>/AGENTS.md`, `<vault>/system/conventions.md`
and `<vault>/_meta/taxonomy.md` as it instructs — those rules override anything assumed here.

If `<vault>/system/dream.md` does not exist, stop and say so. Do not improvise a consolidation pass:
an older vault predates the convention and should have the procedure added to it first, so the rules
live with the vault rather than with whichever tool happened to run.

## 3. Guardrails that hold regardless of mode

- Information is never lost. Pruning means quarantining to `.trash/`, never `rm`.
- `.trash/` is local-only. Never stage or push it; surface its contents in the run report instead.
- End with the run report and the "needs your decision" list the procedure asks for.
