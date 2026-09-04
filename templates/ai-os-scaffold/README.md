---
type: system
title: README — {{OS_NAME}}
description: Public-facing intro to this AI Operating System vault.
tags: [system]
generated:
  by: {{KERNEL_ACTOR}}
  at: {{CREATED_AT}}
created: {{CREATED}}
provenance: extracted
---

# {{OS_NAME}}

This is [{{OWNER}}](/people/{{OWNER_SLUG}}.md)'s AI Operating System for {{SCOPE}} — a Karpathy-style
LLM-OS: an Obsidian-readable markdown vault that an LLM maintains as its kernel, and the durable context
store for the org, people, tools, projects, and meetings.

**This vault follows the [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
v0.2.** It is an OKF knowledge bundle: every note is plain markdown with YAML frontmatter carrying a
non-empty `type`; `index.md` and `log.md` are OKF's reserved files; the root [index](/index.md) declares
`okf_version: "0.2"`; and notes link to each other with bundle-relative markdown links. Any OKF-aware
tool, any agent, or plain `grep` can read it.

- Start at [home](/home.md). The kernel's operating contract is [AGENTS.md](/AGENTS.md); the rules are in
  [Conventions](/system/conventions.md); the philosophy is in [OS Manifesto](/system/os_manifesto.md).
- {{OWNER_SHORT}} does not hand-edit this vault — the agent does the reading, writing, and linking.
- This vault is self-contained: everything needed to operate it lives inside it.
- Run the [dream pass](/system/dream.md) to deep-clean.
