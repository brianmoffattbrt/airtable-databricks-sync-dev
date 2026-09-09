# Column Mapping Reference

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
