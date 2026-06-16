# CLAUDE.md — About {{OWNER}} (user-level)

Basic facts about {{OWNER_SHORT}}, loaded into every Claude Code session. Context-specific detail lives
in each project folder's own `CLAUDE.md` — this file stays general.

## Who I am

- {{OWNER}} — {{OWNER_ROLE}}, based in {{LOCATION}}.
- {{WORK_FROM_HOME_NOTE}}
- Email: {{EMAIL}}.

## My engagements

{{ENGAGEMENTS_TABLE}}

- When I say "today" / "tomorrow," interpret it against whichever context's working block applies.

## Git commits

- Before committing, review the diff against the latest commit (`git diff HEAD`, and skim `git log -1`)
  so the message accurately and specifically describes what changed.
- Use Conventional Commits format: `type(optional-scope): summary` — e.g. `feat(auth): add OAuth login`,
  `fix: handle empty inbox`, `docs(os): expand conventions`. Common types: `feat`, `fix`, `docs`,
  `refactor`, `chore`, `test`, `style`, `perf`, `build`, `ci`.
- Keep the summary line imperative and under ~72 chars; add a body explaining the *why* when the change
  isn't self-evident.

## How this is organized — the AI OS knowledge layer

My knowledge layer is a set of AI Operating Systems (AI OS) — Karpathy-style LLM-OS vaults and
[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundles:
Obsidian-readable markdown + YAML frontmatter + bundle-relative links, graph-viewable, and maintained by
the agent, not hand-edited. The canonical structure and the machine-bootstrap procedure live in
`~/Projects/ai-os-playbook/`.

The layers:
- User level (this file) — who I am, global conventions.
- Personal OS — `~/Projects/personal-os/` — my cross-context AI OS (me, my stack, working patterns). The
  top of the knowledge graph.
- Per context — each `~/Projects/<context>/` folder has its own `CLAUDE.md` (folder context) and its own
  AI OS vault at `~/Projects/<context>/<context>-os/`.

AI OS routing rule (generic — works for any context, no per-context edits):
> When working under `~/Projects/<context>/`, look for a `<context>-os/` vault. If one exists, that is
> that context's AI OS: read it for context before asking me something it might already know (start at
> its `home.md`), and keep it updated per its own `CLAUDE.md` and `system/conventions.md`. The personal
> layer is `~/Projects/personal-os/`. The OS holds context, not code — code stays in the project repos;
> the OS holds reusable context and pointers to it.

To set up the AI OS on a new machine, read `~/Projects/ai-os-playbook/BOOTSTRAP.md`. To deep-clean a
vault, run the `/dream` skill on it.
