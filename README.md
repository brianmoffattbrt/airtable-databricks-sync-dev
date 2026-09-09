# Airtable-Databricks Sync (Dev)

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
