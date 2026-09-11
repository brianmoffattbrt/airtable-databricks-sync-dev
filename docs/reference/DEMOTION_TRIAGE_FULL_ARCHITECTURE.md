# Demotion Triage Mirror — Inspected Implementation and Design History

## Implementation facts, not a completeness certificate

The name `demotion_triage_full` describes a design goal. The inspected [sync_triage_full.py](../../sync_triage_full.py), at source revision `a9e61158c26f5e1251d16bdee77c17ec4ff41681`, is a limited dev implementation:

1. Source is the same-base dev Airtable table `tblFp0tXA3YOJGjMo` in `app1jXoB1g13R9iOl`, not the captured production A-X table `tblSJItXuuUd0lyHP`.
2. Destination is `jupiter_dev.brianm.demotion_triage_full`.
3. `get_all_airtable_records(limit=100)` defaults to 100 records. `sync_airtable_to_triage_full()` calls it without overriding that limit. This does not establish a complete production-record mirror.
4. `AIRTABLE_TO_SPARK_MAPPING` is a curated dictionary. `records_to_spark_rows` iterates that dictionary, not every field returned by Airtable; a schema change is not automatically documented or mapped.
5. `transform_field_value` joins linked/lookup list elements into strings, keeps multiple-select lists as arrays, and reduces attachments to joined URLs. It does not preserve every original field representation or attachment attribute.
6. A temporary table is overwritten, then the target is MERGEd by `airtable_record_id` with UPDATE SET * / INSERT *. The implementation is not the direct target-overwrite sketch retained below.
7. `sync_timestamp` is a batch sync time, not the Airtable revision history. This is not a demonstrated complete per-field event-history/audit trail. It does not prove which automation wrote a value.
8. An omitted mapped field becomes None; UPDATE SET * can affect existing mirrored values. This is not evidence a missing/deleted source field has zero impact.

These are local source facts. Current deployed execution, complete populations, and historical correctness are not certified, and no notebook was executed for this documentation update.

## Relationship to A-X documentation

The [canonical captured automation specification](../as-is/automations.md) governs native rule settings and immediate dependencies. Every A-X output is automatic, even where inputs are supplied by a person. The mirror is a separate consumer, not proof of runtime equivalence or a substitute for the captured trigger/action graph.

The inspected main sync already reads `Investigation Complete` and `Reviewer` into context fields. The old motivation claiming those process fields were not tracked in Databricks is not accurate for that inspected implementation. The mirror adds other mapped process fields, but broader field/row completeness must not be inferred from its name.

See [COLUMN_MAPPING.md](COLUMN_MAPPING.md) for first-element name/code resolution in the main sync versus joined IDs in this mirror. These representations and destinations are different contracts.

## Design and operational limits

- A future full-fidelity production mirror, event history, direct-write triage replacement, or table redesign requires a separate specification and approval.
- The historical schema, completion checkmarks, deletion history, and cleanup backlog below are retained observations/proposals with their original limitations, not current integrity verification or deletion approval.
- Separate dev primary tables do not isolate every path in the companion notebook; see the [legacy sync reference](legacy-dev-sync.md).
- Do not run sync, delete a column, create a table, or replay records simply to validate the captured A-X documentation.

<details>
<summary>Historical architecture proposal, SQL/schema sketch, and dev-testing notes — not a verified production implementation</summary>

Everything below is preserved design/history. Claims such as complete mirror, ALL columns, Complete Audit Trail, ready, verified, or safe to remove are not newly established facts. The qualified implementation description above supersedes contradictory wording; original SQL/Python examples and comments are retained unchanged and are not execution instructions.


## Overview

This document describes the new `demotion_triage_full` table architecture that provides a **complete mirror** of the Airtable triage table in Databricks.

## Motivation

**Current State:**
- `demotion_context` only captures ~40 triage OUTPUT fields
- Process fields (Investigation Complete, Reviewer, etc.) are NOT tracked in Databricks
- No historical record of triage process in a queryable format

**New Architecture:**
- `demotion_triage_full` captures ALL 120+ Airtable columns
- Enables analysis of triage PROCESS (not just outcomes)
- Foundation for eventual Airtable replacement

## Data Flow

```
demotions_stops_hours ──► Airtable ──► demotion_triage_full ──► demotion_context
                         (120 cols)    (FULL MIRROR)           (enriched output)
```

## Tables

### `jupiter_dev.brianm.demotion_triage_full`

Full mirror of Airtable with ALL columns.

| Category | Example Fields |
|----------|----------------|
| **Identifiers** | a_uid, vin, airtable_record_id |
| **Timestamps** | timestamp_utc, sync_timestamp |
| **Triage Process** | investigation_complete, triage_activities_complete, reviewer, headlands_reviewer |
| **Triage Output** | confirmed_demotion_type, demotion_reason, in_scope |
| **Headlands** | headlands_assessment, headlands_vs_interior, headlands_turn |
| **Spark Data** | spark_url, spark_response, spark_camera_name |
| **URLs** | foxglove_url, sparkai_query_url, autonomy_state_transition_history |

### Schema (120 columns + 2 metadata)

```sql
CREATE TABLE IF NOT EXISTS jupiter_dev.brianm.demotion_triage_full (
    -- Metadata
    airtable_record_id STRING COMMENT 'Airtable record ID',
    sync_timestamp TIMESTAMP COMMENT 'Last sync time',

    -- Airtable fields (all 120)
    a_uid STRING,
    timestamp_utc STRING,
    vin STRING,
    pilot_vins_linked STRING,
    vin_machine_type STRING,
    map_pre_signed_url STRING,
    sparkai_query_url STRING,
    main_sparkurl_manual STRING,
    duplicate_issue_5_23 STRING,
    triage_activities_complete STRING,
    triage_review_complete STRING,
    from_state STRING,
    main_demotion_status STRING,
    preceding_stop_code STRING,
    secondary_demotion_manual STRING,
    secondary_demotion_auto STRING,
    secondary_demotion_issue STRING,
    manual_demotion_masking STRING,
    confirmed_demotion_type ARRAY<STRING>,
    operator_error_or_misuse STRING,
    investigation_complete STRING,
    demotion_reason STRING,
    main_demotion_reason STRING,
    demotion_occurrence STRING,
    halt_description STRING,
    archived_odd_assessment STRING,
    misuse_check_required STRING,
    triage_comments_if_questions_unusual_observations_during_triage STRING,
    triage_status STRING,
    to_state STRING,
    inorbit_url STRING,
    spark_url STRING,
    spark_misuse_check_results STRING,
    reviewer STRING,
    state_screenshot STRING,
    halt_code_linked STRING,
    jira_link STRING,
    archived_demotion_machine_behavior STRING,
    archived_jira_workflow STRING,
    demotions STRING,
    link_to_webpage STRING,
    occluded_by_lo STRING,
    bug_or_intended_behavior STRING,
    confirmed_jrm_link STRING,
    human_detection_details STRING,
    vehicle_object_outside_field STRING,
    vehicle_type STRING,
    jrm_status STRING,
    timestamp_cst STRING,
    mtbi_bucket ARRAY<STRING>,
    operator_notes_engineering_machines STRING,
    vehicle_parked_driving STRING,
    vehicle_on_off_road STRING,
    misuse_check_reason STRING,
    field_visualization_test STRING,
    spark_program_name STRING,
    spark_response STRING,
    spark_original_annotation_0_label STRING,
    spark_annotation_0_label STRING,
    spark_camera_name STRING,
    original_annotation_0_label STRING,
    annotation_0_label STRING,
    halt_code_investigation_guide STRING,
    confirmed_jira_url STRING,
    headlands_reviewer STRING,
    headlands_assessment_comments_optional STRING,
    in_scope STRING,
    secondary_demotion_reason STRING,
    preceding_stop_datetime_utc TIMESTAMP,
    headlands_protocol STRING,
    autonomy_state_transition_history STRING,
    bundle_group STRING,
    manned_type STRING,
    other_sparkai_url ARRAY<STRING>,
    no_of_spark_engagements BIGINT,
    bundle STRING,
    headlands_data_issue ARRAY<STRING>,
    triage_process STRING,
    manual_masking_notes STRING,
    manual_demotion_on_false_positive STRING,
    vis_map_error_reason_for_failure STRING,
    vis_map_error_reason_category STRING,
    vis_map_error_demotion_failure_log_time TIMESTAMP,
    jrm_611_spark_engagement STRING,
    seconds_in_autonomy_time_before_demotion BIGINT,
    preceding_stop_code_reason STRING,
    preceding_stop_code_error STRING,
    implement_path_position_heading STRING,
    implement_path_position_direction BIGINT,
    headlands_assessment STRING,
    headlands_vs_interior STRING,
    headlands_turn STRING,
    implement_path_position_type BIGINT,
    implement_path_position_type_text STRING,
    spark_utc_time STRING,
    halt_code_import STRING,
    main_demotion_code STRING,
    foxglove_url STRING,
    headlands_assessment_complete STRING,
    human_change_to_vehicle STRING,
    computed_implement_path_position_type_text STRING,
    genos_version STRING,
    seconds_in_state_5_and_6 BIGINT,
    camera_name STRING,
    recent_human_detection STRING,
    secondary_demotion_manual_updated STRING,
    preceding_stop_code_copy STRING,
    jrm_link_append_helper STRING,
    triage_protocol_tag ARRAY<STRING>,
    vin_match STRING,
    perception_stops_in_last_10_minutes DOUBLE,
    test_field STRING,
    route_around STRING,
    confirmed_headlands STRING,
    temp_spark_request_time TIMESTAMP,
    temp_central_time STRING,
    temp_brian_review STRING,
    clear_text_vin STRING,
    airtable_id STRING,
    nonnavigable_object_misuse_details STRING
)
COMMENT 'Full mirror of Airtable triage table - contains ALL columns'
```

## Field Mapping

| Airtable Field | Spark Column | Type |
|----------------|--------------|------|
| A_UID | a_uid | STRING |
| Timestamp UTC | timestamp_utc | STRING |
| VIN | vin | STRING |
| Triage Activities Complete | triage_activities_complete | STRING |
| Investigation Complete | investigation_complete | STRING |
| Reviewer | reviewer | STRING |
| Confirmed Demotion Type | confirmed_demotion_type | ARRAY<STRING> |
| Headlands Assessment | headlands_assessment | STRING |
| Headlands vs Interior | headlands_vs_interior | STRING |
| ... | ... | ... |

See `AIRTABLE_TO_SPARK_MAPPING` in the sync notebook for the complete mapping.

## Sync Logic

### Phase 1: Push (DBX → Airtable)
No change - still pushes new demotions from `demotions_stops_hours` to Airtable.

### Phase 2: Pull (Airtable → DBX)
**NEW:** Pull ALL fields, write to `demotion_triage_full`, then update `demotion_context`.

```python
# 1. Pull ALL records from Airtable (no field filter)
records = get_airtable_data(limit=20000)

# 2. Transform and write to demotion_triage_full
df = transform_airtable_to_spark(records)
df.write.mode("overwrite").saveAsTable("demotion_triage_full")

# 3. Update demotion_context (existing logic, or join from demotion_triage_full)
```

## Benefits

1. **Complete Audit Trail**: Every Airtable field is now queryable in SQL
2. **Process Analytics**: Can now analyze triage time, reviewer workload, etc.
3. **Airtable Migration Path**: Table schema is ready for direct writes when we remove Airtable
4. **Debugging**: Full visibility into Airtable state for troubleshooting

## Next Steps

1. ✅ Create `demotion_triage_full` table in dev
2. ✅ Update sync to pull ALL fields and populate table
3. ✅ Verify data integrity
4. ⏳ Update dashboards to use new table for process metrics
5. ⏳ Plan production rollout

## Column Cleanup Backlog

Columns that need sync code changes before deletion:

| Column | Reason | Data Usage | Action Needed |
|--------|--------|------------|---------------|
| `Secondary Demotion Auto` | Barely used (0.08% of records) | 285 of 375,492 records | Remove from sync code, then delete |

## Columns Successfully Deleted (Dev Testing)

| Column | Date Deleted | Sync Status |
|--------|--------------|-------------|
| Halt Code Investigation Guide | 2026-09-09 | ✅ Sync works |
| InOrbit URL | 2026-09-09 | ✅ Sync works |
| Other SparkAI URL | 2026-09-09 | ✅ Sync works |
| Spark URL | 2026-09-09 | ✅ Sync works |
| Autonomy state transition history | 2026-09-09 | ✅ Sync works |

</details>
