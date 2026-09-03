# OKF v0.1 ↔ AI OS mapping

This is the canonical reference for how the AI OS standard maps onto **OKF (Open Knowledge Format)
v0.1** — Google Cloud's open, vendor-neutral standard for representing knowledge as plain markdown +
YAML frontmatter. Every AI OS vault is an OKF v0.1 knowledge bundle.

- Spec: <https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf> (read `SPEC.md`).
- OKF is intentionally minimal: a directory of markdown files, a non-empty `type` per note, and two
  optional reserved files. It explicitly names Obsidian as a compatible tool (SPEC §10).

## Conformance bar (OKF §9) — the whole thing

A bundle is conformant if:
1. every non-reserved `.md` has a parseable YAML frontmatter block;
2. every frontmatter has a **non-empty `type`**;
3. the reserved files `index.md` / `log.md` follow their structure (§6 / §7) when present.

Everything else — links, filenames, other fields — is soft guidance. Consumers must tolerate missing
fields, unknown `type` values, extra keys, broken links, and missing `index.md`.

## Frontmatter mapping

| AI OS field | OKF field | Notes |
|---|---|---|
| `type` | `type` (**required**) | The one hard conformance rule. Our values: person, organization, tool, project, epic, task, meeting, daily, system, moc, reference. |
| `title` | `title` (recommended) | Human display name. **Required in our use** because filenames are slugs, so the readable name lives here. |
| `summary` → `description` | `description` (recommended) | One-sentence preview. Renamed from the old `summary`. |
| `updated` → `timestamp` | `timestamp` (recommended) | Last meaningful change, ISO-8601 (`YYYY-MM-DD` is valid). Renamed from the old `updated`. |
| `tags` | `tags` (recommended) | Lowercase `snake_case`; registered in `_meta/taxonomy.md`. |
| `created` | extension | Immutable date first created. OKF preserves unknown keys (§4.1). |
| `provenance` | extension | `extracted` / `inferred` / `to-confirm`. |
| `status` | extension | tasks/projects/epics only. |
| `resource` | `resource` (recommended) | Canonical URI, where the note maps to one. |

## Structure mapping

| AI OS | OKF | Notes |
|---|---|---|
| Filenames = `snake_case` slugs | (free) | OKF's own bundles use snake_case slug filenames; avoids spaces in link paths. |
| Folders = lowercase | (free) | Matches OKF's example bundles (`tables/`, `references/`). |
| Links = `[Text](/folder/slug.md)` | bundle-relative links (§5.1) | Leading-slash, absolute from bundle root. **Verified to resolve in Obsidian's graph (edges + ghost nodes).** |
| per-folder `index.md` | `index.md` (§6) | Progressive-disclosure listing, no frontmatter — except the **root** `index.md`, which declares `okf_version: "0.1"`. |
| root `log.md` (was `System/Changelog.md`) | `log.md` (§7) | Date-grouped change history, newest first; `**Update**`/`**Creation**`/`**Deprecation**` prefixes. |
| `# Overview` / `# Schema` / `# Examples` / `# Citations` | conventional headings (§4.2) | Used where they apply. |
| Exceptions kept verbatim | — | `CLAUDE.md`, `AGENTS.md`, `README.md`, `index.md`, `log.md`, `_meta/`, `.obsidian/`. |

## Why we keep Obsidian + the graph

We adopt OKF's *recommended* leading-slash bundle-relative links (`[Text](/folder/slug.md)`). An A/B test
confirmed Obsidian resolves these into graph edges and still renders ghost nodes for not-yet-created
targets — so full OKF conformance and a rich Obsidian graph coexist with no trade-off.

## Migrating a pre-OKF vault

The `/dream` skill carries the mechanical, information-preserving migration: rename files to slugs +
lowercase folders, add `title`, rename `summary`/`updated`, rewrite `[[wikilinks]]` → bundle-relative md
links, add `index.md`/`log.md`, and validate conformance. See `skills/dream/SKILL.md` §2.
