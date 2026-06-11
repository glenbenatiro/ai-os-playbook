---
type: system
tags: [system, philosophy]
created: {{CREATED}}
updated: {{CREATED}}
summary: What this AI Operating System is and the Karpathy LLM-OS framing it follows.
provenance: extracted
---

# OS Manifesto

## Why this exists

This vault is a personal AI Operating System for [[{{OWNER}}]]'s {{SCOPE}}. It is one place where
context lives — people, clients, tools, projects, meetings, and the running state of the work — and
where an LLM ([[Claude]], via Claude Code) does the upkeep so the knowledge stays current and connected
without anyone hand-maintaining it.

## The LLM-OS framing

Andrej Karpathy described large language models not as chatbots but as the kernel process of a new
operating system: the LLM orchestrates tools, memory, and I/O the way a kernel orchestrates a computer.
This vault takes that literally.

| Classic OS | This OS |
|---|---|
| CPU / kernel | Claude Code — the process that reads, writes, links, and reasons over the vault |
| RAM | the model's context window (what's loaded for the current task) |
| Disk / filesystem | this markdown vault — durable memory |
| Files & folders | notes & sections, addressed by `[[wikilink]]` |
| System calls | skills / tools — Bash, web search, MCP, and the `/dream` maintenance skill |
| Processes / apps | long-running agents & routines |
| GUI / display | [[Obsidian]] — the human window onto the vault, especially the graph view |
| Boot config | `CLAUDE.md` at the vault root — the kernel's operating contract |

## Principles

1. The kernel is proactive. The LLM doesn't just transcribe what's said — it links, files, and tidies as
   it goes. A new mention of a person or tool becomes a link (and a stub note if needed).
2. Everything is connected. Wikilinks are the point. A note with no links is a bug. The graph view is
   the dashboard; a healthy graph means a healthy OS.
3. Plain markdown, no lock-in. Just files. Readable without Obsidian, diffable in git, portable.
4. Source of truth for context, not code. Operating context lives here; code lives in the project repos.
   Where they overlap, this holds the planning/spec notes and pointers to the code.
5. It improves by use. Every interaction should leave the OS a little better organized than before. The
   `/dream` skill is the periodic deep-clean that catches what day-to-day editing misses.
6. Provenance is tracked. Notes mark whether a claim was `extracted` from a source, `inferred` by the
   kernel, or is still `to-confirm`. The OS never launders a guess into a fact.
7. {{PRINCIPLE_PRIVACY}}

See [[Conventions]] for the concrete rules and `CLAUDE.md` for the kernel's operating contract.
