# Airtable-Databricks Development Sync

## Inspected implementation and documentation boundary

This repository contains two distinct notebook implementations, not a fully isolated replica of production. These notes describe the local source inspected at `a9e61158c26f5e1251d16bdee77c17ec4ff41681`; they do not certify current deployed job settings or runtime outcomes.

| Component | Local source configuration / behavior |
|---|---|
| `sync_notebook_dev.py` | Primary Airtable target `tblFp0tXA3YOJGjMo` (Demotions_DatabricksSync_Dev), base `app1jXoB1g13R9iOl`; primary DBX target `jupiter_dev.brianm.demotion_context_dev`; production demotion source |
| `sync_triage_full.py` | Same dev Airtable table; target `jupiter_dev.brianm.demotion_triage_full`; curated mapping and default 100-record pull followed by MERGE |
| Shared references / other paths | The same base contains shared Halt Codes; the main dev notebook includes reference-creation paths and production `jupiter_prod.jfa_metrics.route_around_context` write paths |

**The old claim that this notebook can be run or modified freely without affecting production is withdrawn.** Separate primary tables are not full isolation. This documents available code paths, not proof that any particular production write occurred. Do not execute/import either notebook as a documentation check; operational execution and any destructive dev/test action require separately scoped approval.

## Source of truth

- [Captured A-1 through A-40 specification](../as-is/automations.md): native Airtable settings and immediate dependencies. It documents the accepted snapshot, not live publication or runtime equivalence.
- [Column mapping reference](COLUMN_MAPPING.md): distinguishes the main sync and mirror representations and names the actual conversion functions.
- [Mirror implementation notes](DEMOTION_TRIAGE_FULL_ARCHITECTURE.md): separates the full-mirror goal from the inspected limited implementation.

`sync_notebook_dev.py` stores its conversions in `cast_airtable_format_to_databricks` and `upload_to_temp_table`; it does not have the COLUMN_MAPPING section referenced by the historical deletion instructions. `sync_triage_full.py` has a separate `AIRTABLE_TO_SPARK_MAPPING`.

## Documentation-only verification

Read the relevant mapping/payload functions and reconcile the canonical documentation. Running a sync, deleting a field, creating a secret scope, or changing production configuration is not necessary to establish the captured rule settings. No column deletion, gate, A-39 retirement, or production rollout is authorized here.

<details>
<summary>Historical setup and dev-testing notes — not proof of isolation or current execution approval</summary>

The earlier README is retained below, including its superseded isolation and mapping instructions. Its run-all/delete-column steps are historical operational guidance, not approved actions in the documentation audit. Use the qualified source facts above.


**Bidirectional** development sync job for testing Airtable schema changes before applying to production.

## Purpose

This is a **separate, owned** sync job that mirrors the production mesa-autonomy-triage sync but:
- Points to `Demotions_DatabricksSync_Dev` Airtable table
- Syncs to `jupiter_dev.brianm.demotion_context_dev` Databricks table
- Can be modified freely without affecting production
- Supports full bidirectional sync (push new demotions, pull triage results)

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BIDIRECTIONAL SYNC                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  demotions_stops_hours ──► Demotions_DatabricksSync_Dev ──► demotion_context│
│       (prod, read)              (dev Airtable)                (dev DBX)     │
│                                      │                            │         │
│   [New demotions pushed]             │     [Triage results pulled]│         │
│                                      ▼                            ▼         │
│                               Triage in UI                   Analytics      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Sync Flow

1. **DBX → Airtable (Push)**: New demotions from `demotions_stops_hours` pushed to dev Airtable
2. **Airtable → DBX (Pull)**: Triage results pulled back to dev Databricks table

## Usage

### 1. Set up Airtable token

Create a Databricks secret scope with your Airtable Personal Access Token:
```bash
databricks secrets create-scope brian.moffatt@bluerivertech.com
databricks secrets put-secret brian.moffatt@bluerivertech.com AIRTABLE_TOKEN
```

Token scopes needed: `data.records:read`, `data.records:write`, `schema.bases:read`

### 2. Run the sync notebook in Databricks

Open `/Repos/brian.moffatt@bluerivertech.com/airtable-databricks-sync-dev/sync_notebook_dev` and run all cells.

### 3. Test column deletions

1. Delete a column from `Demotions_DatabricksSync_Dev` in Airtable UI
2. Comment out the column in `COLUMN_MAPPING` in `sync_notebook_dev.py`
3. Commit, push, and update the Databricks repo
4. Run the sync to verify it still works
5. If successful, coordinate with Jackson team to apply to production

## Configuration

| Setting | Value |
|---------|-------|
| Airtable Base ID | `app1jXoB1g13R9iOl` |
| Airtable Dev Table ID | `tblFp0tXA3YOJGjMo` |
| Databricks Schema | `jupiter_dev.brianm` |
| Databricks Table | `demotion_context_dev` |

## Column Mapping

See `COLUMN_MAPPING.md` for the full list of synced columns.

## Owner

Brian Moffatt

</details>
