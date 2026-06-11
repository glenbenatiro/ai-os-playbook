# CLAUDE.md — {{CLIENT_NAME}} (folder context)

This folder holds {{OWNER}}'s work for {{CLIENT_NAME}}. Each project subfolder has its own `CLAUDE.md` /
`AGENTS.md` for technical conventions. This file holds the shared context common to all {{CLIENT_NAME}}
work, and points every agent at the AI operating system where that context lives.

## What {{CLIENT_NAME}} is

- {{CLIENT_DESCRIPTION}}
- The canonical, always-current description lives in the OS (`{{OS_DIR}}/Organizations/{{CLIENT_NAME}}.md`).

## How {{OWNER}} works for them

- {{OWNER}} — {{OWNER_ROLE}}. {{WORK_FROM_HOME_NOTE}}
- {{ENGAGEMENT}}: {{WORKING_WINDOW}}. When {{OWNER_SHORT}} says "today" / "tomorrow" in this context,
  interpret it against that window.
- {{HISTORY_NOTE}}

## ⭐ The AI Operating System (read this)

There is an AI operating system for {{CLIENT_NAME}} in this folder:

> `{{OS_DIR}}/`

It is a Karpathy-style LLM-OS: an Obsidian-readable markdown vault (wikilinked notes + a graph view)
that an LLM maintains as its kernel. It is the durable context store for everything about
{{CLIENT_NAME}} — the org, people, tools, projects, meetings, decisions.

Rules for any LLM/agent working anywhere in this folder:

1. Consult it first. Before asking {{OWNER_SHORT}} for context that might already be known (who someone
   is, what a project does, how something works), check the OS — start at `{{OS_DIR}}/Home.md`.
2. Feed it. When you learn something broadly useful across projects (a person, a process, a tool, a
   decision, a fact about the org), store it in the OS. Describe the new information in natural language
   and let the OS kernel file and link it — or follow the OS's own `CLAUDE.md` operating contract.
   {{OWNER_SHORT}} does not hand-edit the OS; it's LLM-maintained.
3. Keep code out of it. The OS holds context, not code. Technical/implementation details stay in the
   relevant project repo. The OS only holds reusable context and pointers to the code.
4. One-off, project-only details (a specific bug, a local config) stay in the project — don't clutter
   the OS with them. The bar for the OS is "useful beyond this one task/project."

The OS has its own operating contract at `{{OS_DIR}}/CLAUDE.md` and rules in its `System/Conventions.md`
— follow those when writing into the vault. Run `/dream` on it periodically to keep the graph tidy.
