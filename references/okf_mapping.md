---
type: reference
title: OKF v0.2 ↔ AI OS mapping
description: How the AI OS vault standard maps onto Open Knowledge Format v0.2 - fields, structure, and the v0.1 migration.
tags: [reference, okf]
generated:
  by: claude-code/kernel
  at: 2026-09-04T00:00:00Z
created: 2026-06-16
provenance: extracted
---

# OKF v0.2 ↔ AI OS mapping

The canonical reference for how the AI OS vault standard maps onto **OKF (Open Knowledge Format) v0.2**,
Google Cloud's open, vendor-neutral standard for representing knowledge as plain markdown + YAML
frontmatter. Every AI OS vault is an OKF v0.2 knowledge bundle.

- Spec: <https://github.com/GoogleCloudPlatform/open-knowledge-format> (read `SPEC.md`).
- OKF is intentionally minimal: a directory of markdown files, a non-empty `type` per note, and two
  reserved filenames. Everything else is guidance, and consumers must tolerate what they don't recognise.

## Conformance bar (OKF §11) — the whole thing

A bundle is conformant if:

1. every non-reserved `.md` has a parseable YAML frontmatter block;
2. every frontmatter has a **non-empty `type`**;
3. the reserved files `index.md` / `log.md` follow their structure (§8 / §9).

Everything else — links, filenames, other fields — is soft guidance. Consumers must tolerate missing
fields, unknown `type` values, extra keys, broken links, and a missing `index.md`.

Run `scripts/okf_check.py <vault>` to verify a bundle, and `scripts/okf_migrate_0_1_to_0_2.py <vault>`
to carry a v0.1 bundle across.

## Frontmatter mapping

| AI OS field | OKF v0.2 field | Notes |
|---|---|---|
| `type` | `type` (**required**) | The one hard conformance rule. Our values: person, organization, tool, project, epic, task, meeting, meeting-transcript, meeting-source, source, daily, system, moc, reference. |
| `title` | `title` (recommended) | Human display name. **Required in our use**, because filenames are slugs. |
| `description` | `description` (recommended) | One-sentence preview. |
| `generated` | `generated` (**replaces v0.1 `timestamp`**) | `by` is an actor, `at` an ISO 8601 datetime with an explicit UTC offset. Set both on a meaningful edit. |
| `tags` | `tags` (recommended) | Lowercase `snake_case`; registered in `_meta/taxonomy.md`. |
| `status` | `status` | OKF lifecycle **only**: `draft` / `stable` / `deprecated`; absent means stable. |
| `stage` | extension | This vault's own lifecycle vocabulary (`backlog`, `in-progress`, `blocked`, `done`, `retired`), moved out of `status` in the v0.2 migration so the OKF field keeps its OKF meaning. A `retired` note also carries `status: deprecated`. |
| `verified` | `verified` | Optional confirmation events, each `{ by, at }`. Drives OKF's trust tiers. |
| `stale_after` | `stale_after` | Optional ISO 8601 datetime after which content should be re-checked. |
| `sources` | `sources` (**replaces the v0.1 `# Citations` body list**) | Each entry needs a `resource`; `id` lets a claim cite it with a `[^id]` footnote. |
| `resource` | `resource` (recommended) | Canonical URI, where the note maps to one. |
| `created` | extension | Immutable date first created. OKF preserves unknown keys. |
| `provenance` | extension | `extracted` / `inferred` / `to-confirm`. |

**Actors** (`generated.by`, `verified[].by`) follow OKF §7: `<producer>/<version>` for an agent or tool,
`human:<id>` for a person, `process:<id>` for an automated job. The `human:` prefix is how a consumer
tells human-reviewed content apart from machine-produced content, so never use it for the latter.

**Timestamps** are ISO 8601 datetimes with an explicit offset (`2026-06-30T14:00:00Z`). A bare date is a
v0.1 leftover.

## Structure mapping

| AI OS | OKF | Notes |
|---|---|---|
| Filenames = `snake_case` slugs | (free) | Avoids spaces in link paths. |
| Folders = lowercase | (free) | Matches OKF's example bundles. |
| Links = `[Text](/folder/slug.md)` | bundle-relative links (§6) | Leading-slash, absolute from bundle root. Verified to resolve in Obsidian's graph, edges and ghost nodes intact. |
| per-folder `index.md` | `index.md` (§8) | Progressive-disclosure listing, **no frontmatter** — except the **root** `index.md`, whose frontmatter is `okf_version: "0.2"` and nothing else. |
| root `log.md` | `log.md` (§9) | Date-grouped change history, newest first; `**Update**` / `**Creation**` / `**Deprecation**` prefixes. No frontmatter. |
| `# Overview` / `# Schema` / `# Examples` | conventional headings (§4) | Used where they apply. `# Citations` is retired in favour of the `sources` field. |
| `AGENTS.md` | concept document | The kernel operating contract. Carries frontmatter like any note. |
| `CLAUDE.md` | excluded | Bundle tooling: a one-line `@AGENTS.md` import shim, so it cannot carry frontmatter and is not checked. |
| `system/dream.md` | concept document | The vault's own consolidation procedure. |
| `.obsidian/`, `.trash/` | excluded | Display config and local-only prune quarantine. |

## Why we keep Obsidian + the graph

We adopt OKF's recommended leading-slash bundle-relative links (`[Text](/folder/slug.md)`). An A/B test
confirmed Obsidian resolves these into graph edges and still renders ghost nodes for not-yet-created
targets — so full OKF conformance and a rich Obsidian graph coexist with no trade-off.

## Migrating a vault

**Pre-OKF → OKF.** The [dream pass](../templates/ai-os-scaffold/system/dream.md) carries the mechanical,
information-preserving migration: rename files to slugs + lowercase folders, add `title`, rewrite
`[[wikilinks]]` into bundle-relative markdown links, add `index.md`/`log.md`, and validate conformance.

**v0.1 → v0.2.** Four mechanical changes, all handled by `scripts/okf_migrate_0_1_to_0_2.py`:

1. `timestamp: <date>` becomes `generated: { by: <actor>, at: <datetime> }`.
2. A lifecycle value in `status` moves to `stage`; `retired` also gets `status: deprecated`.
3. A `# Citations` body list becomes `sources:` frontmatter.
4. The root `index.md` declares `okf_version: "0.2"`, and frontmatter comes off the other reserved files.

Run `scripts/okf_check.py <vault>` afterwards; the migration is idempotent, so a second run is a no-op.
