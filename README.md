# Airtable-Databricks Sync (Dev)

Development sync job for testing Airtable schema changes before applying to production.

## Purpose

This is a **separate, owned** sync job that mirrors the production mesa-autonomy-triage sync but:
- Points to `Demotions_DatabricksSync_Dev` Airtable table
- Syncs to `jupiter_dev.brianm.demotion_context_dev` Databricks table
- Can be modified freely without affecting production

## Architecture

```
Airtable (Dev)                         Databricks (Dev)
┌─────────────────────────┐           ┌─────────────────────────────────┐
│ Demotions_DatabricksSync │  ──────► │ jupiter_dev.brianm              │
│ _Dev                     │  sync    │ .demotion_context_dev           │
│ (tblFp0tXA3YOJGjMo)      │           │                                 │
└─────────────────────────┘           └─────────────────────────────────┘
```

## Usage

### 1. Run the sync notebook in Databricks

Upload `sync_notebook_dev.py` to Databricks and run it.

### 2. Test column deletions

1. Delete a column from `Demotions_DatabricksSync_Dev` in Airtable
2. Remove the column mapping from `sync_notebook_dev.py`
3. Run the sync to verify it still works
4. If successful, coordinate with Jackson team to apply to production

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
