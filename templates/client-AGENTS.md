# AGENTS.md — {{CLIENT_NAME}} (folder context)

This folder holds {{OWNER}}'s work for {{CLIENT_NAME}}. Each project subfolder has its own `AGENTS.md`
for technical conventions. This file holds the shared context common to all {{CLIENT_NAME}} work, and
points every agent at the AI operating system where that context lives.

> Keep a `CLAUDE.md` beside this file containing exactly one line — `@AGENTS.md` — so Claude Code imports
> these rules instead of a second copy of them. `AGENTS.md` is the cross-tool standard; never fork the
> rules into both files.

## What {{CLIENT_NAME}} is

- {{CLIENT_DESCRIPTION}}
- The canonical, always-current description lives in the OS (`{{OS_DIR}}/organizations/<client_slug>.md`).

## How {{OWNER}} works for them

- {{OWNER}} — {{OWNER_ROLE}}. {{WORK_FROM_HOME_NOTE}}
- {{ENGAGEMENT}}: {{WORKING_WINDOW}}. When {{OWNER_SHORT}} says "today" / "tomorrow" in this context,
  interpret it against that window.
- {{HISTORY_NOTE}}

## ⭐ The AI Operating System (read this)

There is an AI operating system for {{CLIENT_NAME}} in this folder:

> `{{OS_DIR}}/`

It is a Karpathy-style LLM-OS and an
[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format) v0.2
knowledge bundle: an Obsidian-readable markdown vault (notes + bundle-relative links, viewed as a graph)
that an LLM maintains as its kernel. It is the durable context store for everything about {{CLIENT_NAME}}
— the org, people, tools, projects, meetings, decisions.

Rules for any LLM/agent working anywhere in this folder:

1. Consult it first. Before asking {{OWNER_SHORT}} for context that might already be known (who someone
   is, what a project does, how something works), check the OS — start at `{{OS_DIR}}/home.md`.
2. Feed it back. When you learn something durable while working in this folder — a person, a process, a
   tool, a decision, a fact about the org — **say so and offer to record it in the OS**, rather than
   leaving it in the conversation. Describe the new information in natural language and let the OS kernel
   file and link it, or follow the OS's own `AGENTS.md` operating contract. {{OWNER_SHORT}} does not
   hand-edit the OS; it's LLM-maintained.
3. Keep code out of it. The OS holds context, not code. Technical/implementation details stay in the
   relevant project repo. The OS only holds reusable context and pointers to the code.
4. One-off, project-only details (a specific bug, a local config) stay in the project — don't clutter
   the OS with them. The bar for the OS is "useful beyond this one task/project."

The OS has its own operating contract at `{{OS_DIR}}/AGENTS.md` and rules in its `system/conventions.md`
— follow those when writing into the vault. Run its dream pass (`{{OS_DIR}}/system/dream.md`) periodically
to keep the graph tidy.
