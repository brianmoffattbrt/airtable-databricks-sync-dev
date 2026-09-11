# Column Mapping Reference — Main Sync versus Dev Mirror

## Authority and scope

Use the [canonical A-X specification](../as-is/automations.md) for native automation settings and the [immediate dependency catalog](../as-is/automations.md#immediate-dependency-catalog) for original/MAIN/secondary reference lineage. The table below records inspected local implementation facts, not live deployment or complete migration equivalence.

**Two different mappings must not be conflated:**
- [sync_notebook_dev.py](../../sync_notebook_dev.py): inspect `cast_airtable_format_to_databricks`, `upload_to_temp_table`, `send_data_to_airtable`, and `update_airtable_demotions`. There is no COLUMN_MAPPING constant/section in this notebook.
- [sync_triage_full.py](../../sync_triage_full.py): inspect `AIRTABLE_TO_SPARK_MAPPING`, `transform_field_value`, `records_to_spark_rows`, and `sync_airtable_to_triage_full`.

Source revision inspected: `a9e61158c26f5e1251d16bdee77c17ec4ff41681`. Code type hints in the mirror mapping drive conversion; they are not independently authoritative Airtable schema types. For example, MAIN_SparkURL_Manual is a stored URL in the accepted schema while the mirror mapping uses a singleLineText conversion hint.

## Immediate field representation differences

| Airtable value | Main sync implementation | Dev mirror implementation |
|---|---|---|
| Record ID | `Airtable_ID` | `airtable_record_id` |
| A_UID | Constructed as `VIN \| timestamp` for ingestion/upsert; do not infer a context `a_uid` column from the old table | Mapped to `a_uid` as stored text |
| MAIN Demotion Code | First linked record resolved through `swapped_halt_code_records_mapping` into `main_demotion_code` | Linked IDs joined into string `main_demotion_code` |
| Secondary Demotion Manual | First linked record resolved to `secondary_demotion` | Joined IDs in `secondary_demotion_manual` |
| Preceding Stop Code | First link resolved in the context conversion, including `Preceding_Stop_Code` | Joined IDs in `preceding_stop_code` |
| Reason lookup fields | First result resolved through reason mapping | Lookup list elements converted to a joined string, not the same resolved-name contract |
| Confirmed JRM Link | First link resolved through `jira_issue_mapping` | Joined IDs in `confirmed_jrm_link` |
| Reviewer | First link resolved to `triage_reviewer` | Joined IDs in `reviewer`; distinct from `headlands_reviewer` |
| Confirmed Demotion Type | Multiple-select list read from Airtable | Multiple-select list retained, not joined as a linked field |
| Investigation / activities / scope / operator / bug | Named field values read by the main conversion | Corresponding choice values mapped to strings |
| Vehicle/Object Outside Field | `vehicle_or_object_outside_field` | `vehicle_object_outside_field` |
| MAIN_SparkURL_Manual | Not a mapped input in the inspected main conversion; A-29 is a reader, not its producer | `main_sparkurl_manual` |
| Misuse Check Required | Not a direct mapping in the inspected main notebook | `misuse_check_required`; lookup values are joined |

These are immediate interfaces, not a complete source-to-reporting transformation audit. The mirror defaults to 100 records and uses a curated mapping; calling it full does not certify complete field/record/history coverage.

## Removal and schema-change boundary

**The former heading “NOT in Sync (Safe to Delete)” is withdrawn.** Absence from one mapping does not establish absence from another notebook, native automation, formula, interface, or manual workflow. `records_to_spark_rows` uses `fields.get`; omitted fields become None, and the mirror target MERGE uses UPDATE SET *. Missing-field tolerance is therefore not proof of no effect on previously stored values.

Existing candidate lists, code/type labels, and version dates below are historical. They are not current deletion findings, nor authorization to delete fields even in dev/test. No live sync, schema mutation, new record census, or destructive test is needed for the bounded A-X documentation sign-off.

<details>
<summary>Historical mapping worksheet and removal instructions — superseded/unvalidated</summary>

The following old tables mix purposes and representations and are retained only as historical context. Where they disagree, the named implementation and qualified mapping above govern the local-code facts; the canonical specification governs captured Airtable settings. Original operational instructions are not authorized by this documentation update.


This document tracks which Airtable columns are synced in the **bidirectional** dev sync job.

## Sync Architecture

```
demotions_stops_hours (prod)     Demotions_DatabricksSync_Dev (AT)     demotion_context_dev (DBX)
         |                                    |                                   |
         +---------> DBX_TO_AT push --------->+                                   |
                                              +<-------- AT_TO_DBX pull ----------+
                                              |                                   |
                                              +---------> merge ----------------->+
```

## How to Test Column Removal

1. **Delete column from Airtable Dev table** (Demotions_DatabricksSync_Dev)
2. **Comment out the column** in `sync_notebook_dev.py` under `COLUMN_MAPPING`
3. **Run the sync** and verify it completes without errors
4. **Check the data** in `jupiter_dev.brianm.demotion_context_dev`
5. **If successful**, coordinate with Jackson team to apply same change to prod

---

## Current Column Mapping

### Critical Identifiers (DO NOT REMOVE)
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| A_UID | a_uid | STRING |
| Timestamp UTC | timestamp_utc | STRING |
| VIN | vin | STRING |
| Bundle | bundle | STRING |

### Triage Results (Airtable → DBX)
| Airtable Field | DBX Column | Type | Notes |
|----------------|------------|------|-------|
| Demotion Reason | demotion_reason | STRING | Linked → lookup |
| Triage Status | triage_status | STRING | DEPRECATED |
| Triage Review Complete | triage_review_complete | STRING | |
| Triage Activities Complete | triage_activities_complete | STRING | |
| Investigation Complete | investigation_complete | STRING | |
| Triage Comments | triage_comments | STRING | |
| Reviewer | triage_reviewer | STRING | Linked → lookup |
| In Scope | in_scope | STRING | |

### Halt Code Data
| Airtable Field | DBX Column | Type | Notes |
|----------------|------------|------|-------|
| Halt Code - Import | halt_code_import | STRING | |
| MAIN Demotion Code | main_demotion_code | STRING | Linked → lookup |
| MAIN Demotion Reason | main_demotion_reason | STRING | Linked → lookup |
| Halt Code Investigation Guide | halt_code_investigation_guide | STRING | Lookup field |
| Halt Description | halt_description | STRING | Lookup field |

### Secondary Demotion
| Airtable Field | DBX Column | Type | Notes |
|----------------|------------|------|-------|
| Secondary Demotion Manual | secondary_demotion | STRING | Linked → lookup |
| Secondary Demotion Auto | secondary_demotion_auto | ARRAY | |
| Secondary Demotion Reason | secondary_demotion_reason | STRING | Linked → lookup |
| Manual Demotion Masking | manual_demotion_masking | STRING | |

### Preceding Stop
| Airtable Field | DBX Column | Type | Notes |
|----------------|------------|------|-------|
| Preceding Stop Code | preceding_stop_code | STRING | Linked → lookup |
| Preceding Stop Datetime (UTC) | preceding_stop_datetime_utc | STRING | |
| Preceding Stop Code Reason | preceding_stop_code_reason | STRING | Linked → lookup |
| Preceding Stop Code Error | preceding_stop_code_error | STRING | |

### Headlands Data
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| Headlands vs Interior | headlands_vs_interior | STRING |
| Headlands Turn | headlands_turn | STRING |
| Implement Path Position Type Text | implement_path_position_type_text | STRING |
| Computed Implement Path Position Type Text | computed_implement_path_position_type_text | STRING |
| Implement Path Position Type | implement_path_position_type | STRING |
| Implement Path Position Heading | implement_path_position_heading | STRING |
| Implement Path Position Direction | implement_path_position_direction | STRING |

### Perception/Spark Data
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| Spark Program Name | spark_program_name | STRING |
| Spark Response | spark_response | STRING |
| Spark Original Annotation 0 Label | spark_original_annotation_0_label | STRING |
| Spark Annotation 0 Label | spark_annotation_0_label | STRING |
| Spark Camera Name | spark_camera_name | STRING |
| No of Spark Engagements | no_of_spark_engagements | INT |
| SparkAI Query URL | sparkai_query_url | STRING |
| Other SparkAI URL | other_sparkai_url | ARRAY |

### Triage Classifications
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| Operator Error or Misuse | operator_error_or_misuse | STRING |
| Bug or Intended Behavior | bug_or_intended_behavior | STRING |
| Vehicle/Object Outside Field | vehicle_or_object_outside_field | STRING |
| Vehicle Parked/Driving | vehicle_parked_or_driving | STRING |
| Vehicle On/Off Road | vehicle_on_or_off_road | STRING |
| Human Detection Details | human_detection_details | STRING |
| Confirmed Demotion Type | confirmed_demotion_type | ARRAY |
| Manned Type | manned_type | STRING |
| MTBI Bucket | mtbi_bucket | ARRAY |

### Jira Integration
| Airtable Field | DBX Column | Type | Notes |
|----------------|------------|------|-------|
| Confirmed JRM Link | confirmed_jrm_link | STRING | Linked → lookup |
| Confirmed Jira URL | confirmed_jira_url | STRING | |

### URLs
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| Map pre-signed URL | map_presigned_url | STRING |
| Foxglove URL | foxglove_url | STRING |
| Spark URL | spark_url | STRING |

### Machine Data
| Airtable Field | DBX Column | Type |
|----------------|------------|------|
| genos_version | genos_version | STRING |
| Seconds in Autonomy Time Before Demotion | seconds_in_autonomy_time_before_demotion | BIGINT |
| Seconds In State 5 And 6 | seconds_in_state_5_and_6 | INT |
| camera_name | camera_name | STRING |

### DEPRECATED (Remove After Testing)
| Airtable Field | DBX Column | Type | Status |
|----------------|------------|------|--------|
| From State | from_state | STRING | DEPRECATED |
| To State | to_state | STRING | DEPRECATED |
| Demotion Occurrence | demotion_occurrence | STRING | DEPRECATED |
| InOrbit URL | inorbit_url | STRING | DEPRECATED |
| Demotions | demotions | STRING | DEPRECATED |
| (Archived) Demotion Machine Behavior | demotion_machine_behavior | STRING | DEPRECATED |

---

## Columns NOT in Sync (Safe to Delete)

These columns exist in Airtable but are NOT synced to Databricks:

| Airtable Field | Reason |
|----------------|--------|
| (Archived) Jira Workflow | Archived |
| (Archived) ODD Assessment | Archived |
| Duplicate Issue 5_23 | Cleanup artifact |
| Test Field | Dev only |
| Temp_Brian_Review | Temp |
| Temp_Spark_Request_time | Temp |
| Temp - Central Time | Temp formula |
| Vin Match | Unused formula |
| JRM Link Append Helper | Helper formula |
| Secondary Demotion Manual_updated | Temp copy |
| Preceding Stop Code copy | Duplicate |
| Timestamp CST | Redundant |

---

## Version History

| Date | Change | By |
|------|--------|-----|
| 2025-01-13 | Initial sync setup | Brian |

</details>
