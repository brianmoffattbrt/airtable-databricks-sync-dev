# Triage Workflows

A single project for replacing Airtable-dependent demotion triage with Databricks workflows and a platform-owned manual-review app.

This project evolves the existing dev-sync repository and preserves its history. The selected company destination is `BlueRiverTechnology/triage-workflows`, private initially. Remote ownership/visibility changes require explicit confirmation; a local directory or this README does not establish that the transfer has occurred.

## Start here

| Document | What it establishes |
|---|---|
| [Captured automations](docs/as-is/automations.md) | A-1 through A-40 settings and immediate dependencies; not live-publication/runtime certification |
| [Manual-process catalog](docs/as-is/manual-processes.md) | Known manual candidates, sources, aliases, outputs, and real gaps |
| [Platform app contract](docs/target/platform-app-contract.md) | Proposed read view, input fields, write table, and outputs; TP-7 worked example |
| [Automation migration map](docs/target/automation-migration.md) | Traceability to A-numbers and explicit target design decisions; no replacement jobs implemented yet |
| [Decisions](docs/decisions.md) | Approved repository choices versus proposed business/contract changes |
| [Sources and curation](docs/reference/source-inventory.md) | What was imported, retained, redacted, and excluded |

**As-is is not target.** The accepted Airtable configuration is a captured snapshot. Proposed fixes or new app schemas belong in target documents until approved/applied. Git history preserves earlier versions; do not maintain competing current copies of the same rule.

## Ownership and boundaries

- This repository owns triage/backend specifications, app data contracts, offline utilities, and future DBX jobs/tests.
- The platform team owns the app code and resolves Spark engagement references into media. Do not build or import a second UI here merely to fill out the tree.
- A-X actions are automatic. A person can supply a TP input or separately override a value, but that is not a human output step inside an A-X execution.
- The three additional OFF automations are inventory-only. Manual contracts do not inherit the completed A-X documentation sign-off.
- Legacy Mesa production integration remains external until a separately approved cutover.

## Legacy code: preserve, do not run as setup

`sync_notebook_dev.py` and `sync_triage_full.py` intentionally remain at their existing root paths, unchanged, for compatibility. They are Airtable-dependent development notebooks, not the new production engine. They include real write/cleanup paths and shared/production dependencies. **Do not import or execute them as repository verification.**

See [legacy context](docs/reference/legacy-context.md), [dev sync notes](docs/reference/legacy-dev-sync.md), [mapping distinctions](docs/reference/COLUMN_MAPPING.md), and [mirror limitations](docs/reference/DEMOTION_TRIAGE_FULL_ARCHITECTURE.md).

The observed Databricks Git folder is `/Repos/brian.moffatt@bluerivertech.com/airtable-databricks-sync-dev`, on main at `a323693ecffc5964aaaedf6133579c081b3cbe96`. Setup preserves that checkout, not refreshes it. No direct matching job was found among 62 visible jobs; that does not prove no indirect/manual use. A future pull after private transfer may require organization-authorized Git access. Git folders/local checkouts are copies of one GitHub repository, not separate hosted projects.

## Offline utility verification

The four files under `tools/legacy_audits` are reviewed offline analysis utilities and tests, not an approved implementation of all forty rules. Their models retain explicit unknowns/calibration limits. No new dependencies are required for the existing tests.

From the repository root:

```bash
python3 -B -m unittest discover -s tools/legacy_audits -p 'test_*.py' -v
python3 -B tools/legacy_audits/analyze_a39_redundancy.py --help
python3 -B tools/legacy_audits/audit_halt_code_incident.py --help
```

The tests use synthetic inputs and temporary local files. Do not run the audit CLIs against production exports just to validate this repository. Generated reports and raw exports stay out of Git. The sanitizer in a legacy utility is not a complete publication/privacy review.

## Working with changes

1. Start a small branch for a coherent change; do not discard uncommitted work.
2. For a source correction or an actually applied Airtable change, update the as-is specification and record the evidence/date/scope. A proposal is not an applied change.
3. For desired DBX/app behavior, update the target contract and relevant decision. Identify affected A-numbers/TPs, differences, and compatibility impact.
4. When implementation is added, keep coupled code, contracts, documentation, and tests together. Coordinate breaking app fields/enums/keys with the platform team.
5. Review diffs and privacy before committing/pushing; respect company review/security controls. No public publication, collaborator invitation, or policy bypass is implied by this README.

The annotated starting tag is `baseline-captured-triage`, created during baseline setup. It records captured A-X documentation plus explicitly draft manual/target contracts, not a production deployment.

For inspection after that tag exists:

```bash
git show baseline-captured-triage:docs/as-is/automations.md
git log --oneline --decorate
```

Prefer normal revert commits for shared changes, or a clean recovery branch from a known tag. Never reset/force-push over uncommitted work. Restoring Git files does **not** undo live Airtable settings, DBX rows, manual submissions, or deployed jobs; those require separate rollback procedures and approval.

## Growth path

1. Version the reviewed baseline and explicit manual gaps.
2. Agree on the platform app contract and finish only the missing TP details.
3. Build DBX-native event identity, facts/reference tables, and manual-result ingestion.
4. Implement/test rules with A-number traceability and approved differences; one A-number does not require one separately scheduled job.
5. Integrate the platform app and validate shadow/parallel behavior.
6. Approve productionization, data migration, rollback, and retirement of legacy writers before removing Airtable.

Future implementation belongs in `src/triage_workflows/`, `sql/`, `resources/`, and `tests/`. These are reserved layout directions, not empty scaffolding or an already selected deployment framework. Do not import the Mesa Terraform/workflows or assume the dev mirror is an Airtable-independent input source.

## Content policy

Curated additions preserve rule settings, reference identities, and useful provenance while redacting unnecessary live customer/record/media examples. Raw exports, credentials, caches, environments, and active user configuration are excluded. Existing public Git history is preserved, not retroactively sanitized or unpublished. The original local evidence remains owner-held; references in this repo disclose what is and is not independently reproducible.
