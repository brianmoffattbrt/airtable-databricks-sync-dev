# Source Inventory and Curation

This inventory distinguishes accepted configuration evidence, local implementation facts, incomplete manual sources, and proposed target design. It is not a fresh live export or certification of every source system.

## Repository history

The foundation is the existing `brianmoffattbrt/airtable-databricks-sync-dev` repository, GitHub ID 1362874924, inspected on main at `a9e61158c26f5e1251d16bdee77c17ec4ff41681` with 17 commits beginning `e0b70ad`. The selected transfer destination is `BlueRiverTechnology/triage-workflows`, preserving identity/history. During preflight the source was public, without workflows, Pages, forks, stars, subscribers, rulesets, or protected main. These are observations, not immutable settings or proof transfer has occurred.

The related code revision identifies tracked source, not the later uncommitted Markdown improvements imported during setup. The original working directories are retained; no source workspace or record has been changed to produce this curated baseline.

## Imported sources

| Source | Repository representation | Evidence limits |
|---|---|---|
| Reviewed AIRTABLE_AUTOMATIONS.md from the triage documentation workspace | [As-is automation specification](../as-is/automations.md), including E01–E40 transcriptions/register | Accepted captured settings and owner confirmations; live publication/runtime equivalence not certified |
| Earlier column/migration, column-usage, comprehensive audit, and project overview documents | [Legacy context](legacy-context.md), manual catalog, selected field facts | Unique useful context retained; stale duplicates and removal claims do not become current definitions |
| Current dev-sync README, COLUMN_MAPPING.md and DEMOTION_TRIAGE_FULL_ARCHITECTURE.md working copies | [Legacy README](legacy-dev-sync.md), [mapping](COLUMN_MAPPING.md), [mirror notes](DEMOTION_TRIAGE_FULL_ARCHITECTURE.md) | Include reviewed uncommitted documentation corrections; not a deployed-job certification |
| Mesa docs/index.md and sync notebook at b277e47f569425e262b53f340f7d7af0a07b46e9 | [Legacy context](legacy-context.md) and its external source reference | External team-owned legacy implementation; not imported Terraform, app code, or deployment |
| Original TP-7 through TP-11 Markdown protocols | [Curated protocol sources](protocols/tp-07-source.md) and adjacent files | Real example links redacted; blank option cells/copied procedures remain explicitly incomplete |
| Earlier airtable_column_audit.csv | [Selected field contracts](field-contracts.md) | Type/example evidence only; not complete enum, current schema, population, or deletion proof |
| Four untracked audit/analysis Python files in the dev workspace | [Offline utilities](../../tools/legacy_audits/analyze_a39_redundancy.py) and sibling module/tests | Imported without logic changes; offline model limits remain; not the production rule engine |

## Reference snapshots

| Source artifact | Included artifact | Provenance / scope |
|---|---|---|
| a39-redundancy/run-20260910-initial/reference_labels.json | [reference-labels.json](reference-labels.json) | Reason/process reference labels from read-only calls; preserve leading/trailing spaces and IDs, not enabled-state evidence |
| a39-redundancy/run-20260910-a28-published/halt_records.json | [halt-code-records.json](halt-code-records.json) | Reference-only code/reason/process/misuse snapshot, 139081 source bytes; source SHA-256 c3f1d7885eca3cc87314c49f0f6104743dd0e3cc1a95183b4e468073bc842d17 |
| a39-redundancy/run-20260910-a28-published/a28_policy.json | [a28-policy.json](a28-policy.json) | Owner-confirmed A28_HEADLANDS_COMPLETE_OTHERWISE_V2, later corroborated by captures; not an immutable Airtable revision ID |
| a39-redundancy/run-20260910-initial/source_schema.json and manifest.jsonl | [Selected metadata facts](field-contracts.md) | Original full schema stays owner-held; irrelevant choice lists can contain customer IDs. This is not a full schema export |
| Initial ui_evidence_a39_a28.json | E39 and historical source notes in the as-is document | Original file remains owner-held. Its A-28 portion is superseded by V2; do not revive it as current policy |

The published-run halt snapshot manifest records save time 2026-09-10T17:23:52.441261+00:00 and capture_time_verified=false. The initial schema manifest likewise does not establish exact capture/publication time. Saved time and filesystem mtime are not publication timestamps. No raw manifest containing personal temporary paths is required to read these specifications.

Reference IDs are retained because they explain captured bindings; future DBX runtime identities are a separate data-model decision. Missing keys and duplicate/reference identities must not be silently coerced, filled, or deduplicated into a different policy. These catalogs are snapshots, not proof of complete future code coverage.

## Curation rules applied to additions

- Raw production_records.json, repeat_ids.json, ready-record exports, analysis outputs, bulk incident data, environments, caches, credentials, active user configuration, and real media are not included.
- The full 14-record A_UID list is omitted. Live incident record IDs are replaced by consistent CASE-* aliases; the original mapping stays owner-held, not published alongside the aliases.
- Actual example engagement/map URLs and their vehicle identifiers are replaced by omission markers in protocol sources.
- Required configured reference IDs, field/base/table identities, exact code/choice labels, and reviewer trailing-space semantics are preserved. Those are not anonymized as if they were demotion/customer record IDs.
- Historical observations remain historical, not a new finding. Preserved SQL/comments are reference material, not runnable migration instructions.
- Personal-home/ephemeral-file dependencies are replaced by portable references or this provenance description. Actual legacy Databricks workspace paths are retained where needed to explain compatibility; they are not local filesystem dependencies.

Existing Git history is preserved as requested. This curation is not a claim that earlier public copies were erased or retroactively sanitized. A discovered historical secret/content problem requires a separate response, not automatic history rewriting or public republication.

## What is not certified

The original screenshots are represented by accepted supplied captures/transcriptions, not fabricated retained-image filenames. Manual protocols with missing values remain draft. No current published-rule fingerprint, exhaustive hidden integration inventory, production census, or native-runtime parity test is supplied by repository setup. Those limits do not invalidate the completed captured A-X documentation scope.
