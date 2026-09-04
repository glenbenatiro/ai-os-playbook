---
type: documentation
title: BOOTSTRAP - set up the AI OS on a fresh machine
description: The procedure an agent follows to stand up the knowledge layer from scratch on a new machine.
tags: [documentation, bootstrap]
generated:
  by: claude-code/kernel
  at: 2026-09-04T00:00:00Z
created: 2026-06-11
provenance: extracted
---

# BOOTSTRAP — set up the AI OS on a fresh machine

This is the procedure an agent (e.g. Claude Code) follows to stand up your knowledge layer from scratch
on a new machine or VPS. A human runs steps 0–1; the agent does the rest when told "set up my AI OS from
the playbook."

> 🔒 If you version your vaults, keep them private. Each vault holds private operating context (people,
> decisions, working detail). Create remotes with `gh repo create … --private`. This playbook is
> shareable; the vaults it produces usually are not.

> 📦 Each vault is an [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
> v0.2 knowledge bundle — plain markdown + YAML frontmatter, `snake_case` slug filenames in lowercase
> folders, bundle-relative markdown links, and `index.md`/`log.md` reserved files. See
> `references/okf_mapping.md`.

> 🧩 Each vault is self-contained. Once scaffolded it depends on nothing in this repository, so it can be
> handed to another person or machine whole.

---

## 0. Prerequisites (human)

1. Install your agent CLI (e.g. Claude Code).
2. Create `~/Projects/personal/` and clone this playbook into it. The playbook and the personal OS
   both live under `personal/`, alongside one folder per client context:
   ```bash
   mkdir -p ~/Projects/personal && cd ~/Projects/personal
   git clone <ai-os-playbook remote> ai-os-playbook
   ```
3. From `~/Projects/`, start the agent and say: "Set up my AI OS from the playbook."

---

## 1. Pick the machine profile (the agent asks, human answers)

| Profile | When | Folder shape |
|---|---|---|
| Multi-context personal | one machine serving several contexts/clients | `~/Projects/<context>/` per context, each with its own `<context>-os/` + folder `CLAUDE.md`; plus `personal-os/` |
| Dedicated single-context box | a machine provisioned for one context | project repos sit directly under `~/Projects/`; one context-level AI OS `~/Projects/<context>-os/` + `personal-os/` |

Ask the human: which profile, which context(s) live here, and each context's working window + one-line
description. Capture answers — they fill the placeholders below.

---

## 2. Scaffold procedure (the agent)

For each AI OS to create (the personal OS, and one per context on this machine):

1. Copy the scaffold:
   ```bash
   cp -r ~/Projects/personal/ai-os-playbook/templates/ai-os-scaffold "<target>/<name>-os"
   ```
   (Client contexts live at `~/Projects/<context>/<context>-os`; the personal OS at
   `~/Projects/personal/<name>-os`.)
2. Rename the owner seed note: `people/{{OWNER_SLUG}}.md` → `people/<owner_slug>.md` (snake_case, e.g.
   `people/jane_doe.md`).
3. Fill placeholders in every file (see the table in §4 — the fill sweeps all `*.md`, including
   `AGENTS.md`). Replace `{{...}}` tokens; delete placeholder lines that don't apply (e.g. the privacy
   rule for a single-party context). The scaffold ships `AGENTS.md` as the canonical kernel contract and
   a `CLAUDE.md` holding the single line `@AGENTS.md`, so Claude Code imports the same rules.
4. Write the folder rules (context folders only) from `templates/client-AGENTS.md` to
   `~/Projects/<context>/AGENTS.md`, and put a one-line `CLAUDE.md` (`@AGENTS.md`) beside it.
5. Seed real content: create `organizations/<org_slug>.md`, fill the owner note, and stub the known
   project subfolders under `projects/`. Update `home.md` and the relevant `index.md` files so nothing is
   orphaned.
6. Initialize git (private remote, if versioning):
   ```bash
   cd "<target>/<name>-os" && git init && git add -A   # commit only when you approve
   # always --private for vaults:
   gh repo create <org-or-username>/<name>-os --private --source=. --remote=origin --push
   ```

Then, once:

7. Write the user config `~/.claude/CLAUDE.md` from `templates/user-CLAUDE.md` (fill the engagements
   table for the contexts on this machine; keep the generic routing rule verbatim).
8. Install the Dream launcher so `/dream` works everywhere. It is a launcher only — the procedure itself
   ships inside each vault at `system/dream.md`:
   ```bash
   mkdir -p ~/.claude/skills/dream
   cp ~/Projects/personal/ai-os-playbook/skills/dream/SKILL.md ~/.claude/skills/dream/SKILL.md
   ```
9. Run a first dream pass per vault to validate links and generate `_insights.md`.

---

## 3. Verify

- Each `<...>-os/` has `AGENTS.md` (plus the one-line `CLAUDE.md` shim), `system/`, `home.md`, the root
  `index.md` (with `okf_version: "0.2"`), `log.md`, `_meta/taxonomy.md`, `.obsidian/`, and opens in
  Obsidian with a connected graph (no orphan `home`).
- `python3 ~/Projects/personal/ai-os-playbook/scripts/okf_check.py <vault>` reports no failures.
- From a context folder, ask the agent a context question — it should consult that context's `-os/`
  vault without being told the path (the generic routing rule in `~/.claude/CLAUDE.md`).
- The dream pass runs, quarantines (never deletes), and writes `_insights.md` + a report.

---

## 4. Placeholder reference

Tokens used across the templates. Fill per AI OS:

| Token | Meaning | Example |
|---|---|---|
| `{{OWNER}}` | Owner full name | `Jane Doe` |
| `{{OWNER_SHORT}}` | First name / short ref | `Jane` |
| `{{OWNER_SLUG}}` | Owner name as a `snake_case` slug (owner note filename) | `jane_doe` |
| `{{OWNER_ROLE}}` | Role | `automation engineer` |
| `{{LOCATION}}` | Base location | `Anytown` |
| `{{EMAIL}}` | Contact email | `you@example.com` |
| `{{OS_NAME}}` | Display name of the OS | `Acme Corp OS` |
| `{{OS_DIR}}` | Vault folder name | `acme-corp-os` |
| `{{SCOPE}}` / `{{SCOPE_SHORT}}` | What this OS covers | `your Acme Corp work` / `Acme Corp` |
| `{{CLIENT_NAME}}` | Context/org name | `Acme Corp` |
| `{{CLIENT_DESCRIPTION}}` | One-liner about the context | _(from intake)_ |
| `{{WORKING_WINDOW}}` | Working hours for this context | `9 AM–12 PM, weekdays` |
| `{{ENGAGEMENT}}` | Engagement type | `Part-time` |
| `{{HISTORY_NOTE}}` | History with the context | _(from intake)_ |
| `{{ORG_EXAMPLES}}` / `{{ORG_LINKS}}` | Org notes for `CLAUDE.md` / `home.md` | `[Acme Corp](/organizations/acme_corp.md)` |
| `{{TOOL_LINKS}}` | Initial tool links for `home.md` | `[Claude](/tools/claude.md) · [n8n](/tools/n8n.md)` |
| `{{CREATED}}` | Today's ISO date | `2026-01-01` |
| `{{CREATED_AT}}` | Today as an ISO 8601 UTC datetime (`date -u +%Y-%m-%dT%H:%M:%SZ`) | `2026-01-01T00:00:00Z` |
| `{{KERNEL_ACTOR}}` | The agent that maintains the vault, as `<tool>/<version>` | `claude-code/kernel` |
| `{{PRIVACY_RULE}}` | Privacy boundary text (CLAUDE.md rule 11) | see §5 |
| `{{PRINCIPLE_PRIVACY}}` | Privacy principle (Manifesto) | see §5 |
| `{{TAXONOMY_PRIVACY}}` | Privacy tags block (taxonomy) | see §5 |
| `{{OWNER_BIO}}`, `{{WORKING_NOTES}}`, `{{HOW_I_WORK}}` | Owner-note body | _(from intake)_ |
| `{{WORK_FROM_HOME_NOTE}}`, `{{ENGAGEMENTS_TABLE}}` | user-CLAUDE.md fields | _(machine-specific)_ |

## 5. Privacy variants

- Multi-party context (a shared brain is possible — e.g. a client reached via an agency, where some
  knowledge could one day feed a shared team brain):
  - `{{PRIVACY_RULE}}` → "Keep shareable context knowledge separable from personal items. Tag sensitive
    notes `personal`; write specs/decisions so they could feed a shared brain without leakage. When in
    doubt, ask before surfacing a personal item into a shareable context."
  - `{{PRINCIPLE_PRIVACY}}` → "Private by default; designed to share a layer. Keep shareable knowledge
    separable from personal items (see the privacy rule in [Conventions](/system/conventions.md))."
  - `{{TAXONOMY_PRIVACY}}` → `- shareable — could be exported to a shared brain.` /
    `- personal — owner-specific; never feeds a shared brain.`
- Single-party context / personal OS (no shared brain): set `{{PRIVACY_RULE}}` → "This vault is private
  to you; no shared-brain boundary applies." Drop the principle and taxonomy privacy block (or leave a
  one-line "n/a — single-party").

---

## 6. Schedule the Dream skill (optional, when ready)

Wire a recurring deep-clean with the `/schedule` skill (cloud routine) or a local cron, e.g. a weekly
unattended pass per vault:

> `/schedule` → new routine → weekly → command: `/dream ~/Projects/<context>/<context>-os --mode unattended`

Start with one vault, review the first real run's report, then expand. Unattended runs only quarantine
to `.trash/` — they never delete — so they're safe to leave running.
