---
type: system
title: OS Manifesto
description: What this AI Operating System is and the Karpathy LLM-OS framing it follows.
tags: [system, philosophy]
generated:
  by: {{KERNEL_ACTOR}}
  at: {{CREATED_AT}}
created: {{CREATED}}
provenance: extracted
---

# OS Manifesto

## Why this exists

This vault is a personal AI Operating System for [{{OWNER}}](/people/{{OWNER_SLUG}}.md)'s {{SCOPE}}. It is
one place where context lives — people, clients, tools, projects, meetings, and the running state of the
work — and where an LLM ([Claude](/tools/claude.md), via Claude Code) does the upkeep so the knowledge
stays current and connected without anyone hand-maintaining it.

## The LLM-OS framing

Andrej Karpathy described large language models not as chatbots but as the kernel process of a new
operating system: the LLM orchestrates tools, memory, and I/O the way a kernel orchestrates a computer.
This vault takes that literally.

| Classic OS | This OS |
|---|---|
| CPU / kernel | Claude Code — the process that reads, writes, links, and reasons over the vault |
| RAM | the model's context window (what's loaded for the current task) |
| Disk / filesystem | this markdown vault — durable memory |
| Files & folders | notes & sections, addressed by bundle-relative markdown links `[Text](/folder/slug.md)` |
| System calls | skills / tools — Bash, web search, MCP, and the [dream pass](/system/dream.md) |
| Processes / apps | long-running agents & routines |
| GUI / display | [Obsidian](/tools/obsidian.md) — the human window onto the vault, especially the graph view |
| Boot config | [AGENTS.md](/AGENTS.md) at the vault root — the kernel's operating contract |

## A specified, portable format

This vault is an **[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
v0.2 knowledge bundle**. OKF is an open, vendor-neutral standard for representing knowledge as plain
markdown + YAML frontmatter: a non-empty `type` on every note, `index.md`/`log.md` reserved files, and
bundle-relative markdown links. "Plain markdown, no lock-in" is no longer just a principle — it's a named
standard the vault conforms to, readable by humans, by Obsidian, and by any OKF-aware agent. v0.2 also
makes provenance first-class: `generated` records who wrote a note and when, `verified` records who
confirmed it, and `sources` records what it was drawn from.

## Principles

1. The kernel is proactive. The LLM doesn't just transcribe what's said — it links, files, and tidies as
   it goes. A new mention of a person or tool becomes a link (and a stub note if needed).
2. Everything is connected. Links are the point. A note with no links is a bug. The graph view is the
   dashboard; a healthy graph means a healthy OS.
3. Plain markdown, OKF-conformant, no lock-in. Just files — readable without Obsidian, diffable in git,
   portable, and conformant to an open standard (OKF v0.2). The vault is self-contained: everything
   needed to operate it lives inside it.
4. Source of truth for context, not code. Operating context lives here; code lives in the project repos.
   Where they overlap, this holds the planning/spec notes and pointers to the code.
5. It improves by use. Every interaction should leave the OS a little better organized than before. The
   [dream pass](/system/dream.md) is the periodic deep-clean that catches what day-to-day editing misses.
6. Provenance is tracked. Notes mark whether a claim was `extracted` from a source, `inferred` by the
   kernel, or is still `to-confirm`. The OS never launders a guess into a fact.
7. {{PRINCIPLE_PRIVACY}}

See [Conventions](/system/conventions.md) for the concrete rules and [AGENTS.md](/AGENTS.md) for the
kernel's operating contract.
