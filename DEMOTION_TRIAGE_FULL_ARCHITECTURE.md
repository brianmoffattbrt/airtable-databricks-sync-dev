# Demotion Triage Full - Architecture Document

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
2. ⏳ Update sync to pull ALL fields and populate table
3. ⏳ Verify data integrity
4. ⏳ Update dashboards to use new table for process metrics
5. ⏳ Plan production rollout
