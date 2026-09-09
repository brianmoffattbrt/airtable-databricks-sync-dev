# Databricks notebook source
# MAGIC %md
# MAGIC # Airtable → Databricks Sync (DEV)
# MAGIC 
# MAGIC Development sync job for testing schema changes.
# MAGIC 
# MAGIC **Source:** Airtable `Demotions_DatabricksSync_Dev` (tblFp0tXA3YOJGjMo)
# MAGIC **Target:** Databricks `jupiter_dev.brianm.demotion_context_dev`

# COMMAND ----------

# MAGIC %pip install tenacity
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import requests
from datetime import datetime
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, ArrayType
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import urllib.parse

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# Airtable Configuration - DEV TABLE
AIRTABLE_BASE_ID = "app1jXoB1g13R9iOl"  # Triage Tool Prototype
AIRTABLE_DEV_TABLE_ID = "tblFp0tXA3YOJGjMo"  # Demotions_DatabricksSync_Dev

# Try multiple secret scopes (in order of preference)
def get_airtable_token():
    scopes_to_try = [
        "brian.moffatt@bluerivertech.com",
        "andras.nagy@bluerivertech.com", 
        "airtable-sync",
        "jfa-triage"
    ]
    for scope in scopes_to_try:
        try:
            return dbutils.secrets.get(scope=scope, key="AIRTABLE_TOKEN")
        except Exception as e:
            print(f"Could not access scope {scope}: {e}")
            continue
    raise Exception("No accessible secrets scope found with AIRTABLE_TOKEN")

AIRTABLE_TOKEN = get_airtable_token()

# Reference table IDs
HALT_CODES_TABLE_ID = 'tblN8uu4Gl1eDZMLs'
DEMOTION_REASONS_TABLE_ID = 'tblINqDuMCUehLzgj'
JIRA_JRM_SCRUM_BOARD_SYNC_TABLE_ID = 'tbllaxeplHp2Jmrw6'
TEAM_MEMBERS_TABLE_ID = 'tblHQdtGEVbhNRWMR'

# Databricks Configuration - DEV TABLE
DEV_TABLE = "jupiter_dev.brianm.demotion_context_dev"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Helper Functions

# COMMAND ----------

def get_airtable_url(table_id: str) -> str:
    return f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_id}'

@retry(stop=stop_after_attempt(3), wait=wait_fixed(30), retry=retry_if_exception_type(Exception))
def get_airtable_data(table_id: str, limit: int = 10000, formula: str = None) -> list:
    """Fetch records from Airtable with pagination."""
    url = get_airtable_url(table_id)
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    all_records = []
    offset = None
    
    while len(all_records) < limit:
        params = {"maxRecords": min(100, limit - len(all_records))}
        if offset:
            params["offset"] = offset
        if formula:
            params["filterByFormula"] = formula
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Airtable API error: {response.status_code} - {response.text}")
        
        data = response.json()
        all_records.extend(data.get("records", []))
        
        offset = data.get("offset")
        if not offset:
            break
    
    return all_records

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reference Data Mappings

# COMMAND ----------

def build_halt_code_mapping() -> dict:
    """Build mapping of halt code record ID -> halt code value."""
    records = get_airtable_data(HALT_CODES_TABLE_ID)
    return {r["id"]: r["fields"].get("Halt Code") for r in records}

def build_demotion_reason_mapping() -> dict:
    """Build mapping of demotion reason record ID -> reason name."""
    records = get_airtable_data(DEMOTION_REASONS_TABLE_ID)
    return {r["id"]: r["fields"].get("Airtable_Demotion_Reason") for r in records}

def build_jira_mapping() -> dict:
    """Build mapping of Jira record ID -> Issue Key."""
    records = get_airtable_data(JIRA_JRM_SCRUM_BOARD_SYNC_TABLE_ID, limit=2000)
    return {r["id"]: r["fields"].get("Issue Key") for r in records}

def build_reviewer_mapping() -> dict:
    """Build mapping of team member record ID -> name."""
    records = get_airtable_data(TEAM_MEMBERS_TABLE_ID)
    return {r["id"]: r["fields"].get("Name") for r in records}

print("Building reference mappings...")
halt_code_mapping = build_halt_code_mapping()
demotion_reason_mapping = build_demotion_reason_mapping()
jira_mapping = build_jira_mapping()
reviewer_mapping = build_reviewer_mapping()
print(f"Loaded: {len(halt_code_mapping)} halt codes, {len(demotion_reason_mapping)} demotion reasons, {len(jira_mapping)} jira issues, {len(reviewer_mapping)} reviewers")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Column Mapping Definition
# MAGIC 
# MAGIC This is the core mapping that defines which Airtable columns sync to Databricks.
# MAGIC **To test removing a column: Comment it out or delete it from this list.**

# COMMAND ----------

# COLUMN MAPPING: Airtable Field Name -> Databricks Column Name
# Comment out or delete rows to test column removal
COLUMN_MAPPING = {
    # === CRITICAL IDENTIFIERS (DO NOT REMOVE) ===
    "A_UID": "a_uid",
    "Timestamp UTC": "timestamp_utc",
    "VIN": "vin",
    "Bundle": "bundle",
    
    # === TRIAGE RESULTS (Airtable → DBX) ===
    "Demotion Reason": "demotion_reason",  # Linked field - needs lookup
    "Triage Status": "triage_status",
    "Triage Review Complete": "triage_review_complete",
    "Triage Activities Complete": "triage_activities_complete",
    "Investigation Complete": "investigation_complete",
    "Triage Comments - If questions/unusual observations during Triage": "triage_comments",
    "Reviewer": "triage_reviewer",  # Linked field - needs lookup
    "In Scope": "in_scope",
    
    # === HALT CODE DATA ===
    "Halt Code - Import": "halt_code_import",
    "MAIN Demotion Code": "main_demotion_code",  # Linked field - needs lookup
    "MAIN Demotion Reason": "main_demotion_reason",  # Linked field - needs lookup
    "Halt Code Investigation Guide": "halt_code_investigation_guide",  # Lookup field
    "Halt Description": "halt_description",  # Lookup field
    
    # === SECONDARY DEMOTION ===
    "Secondary Demotion Manual": "secondary_demotion",  # Linked field - needs lookup
    "Secondary Demotion Auto": "secondary_demotion_auto",  # Array
    "Secondary Demotion Reason": "secondary_demotion_reason",  # Linked field - needs lookup
    "Manual Demotion Masking": "manual_demotion_masking",
    
    # === PRECEDING STOP ===
    "Preceding Stop Code": "preceding_stop_code",  # Linked field - needs lookup
    "Preceding Stop Datetime (UTC)": "preceding_stop_datetime_utc",
    "Preceding Stop Code Reason": "preceding_stop_code_reason",  # Linked field - needs lookup
    "Preceding Stop Code Error": "preceding_stop_code_error",
    
    # === HEADLANDS DATA ===
    "Headlands vs Interior": "headlands_vs_interior",
    "Headlands Turn": "headlands_turn",
    "Implement Path Position Type Text": "implement_path_position_type_text",
    "Computed Implement Path Position Type Text": "computed_implement_path_position_type_text",
    "Implement Path Position Type": "implement_path_position_type",
    "Implement Path Position Heading": "implement_path_position_heading",
    "Implement Path Position Direction": "implement_path_position_direction",
    
    # === PERCEPTION/SPARK DATA ===
    "Spark Program Name": "spark_program_name",
    "Spark Response": "spark_response",
    "Spark Original Annotation 0 Label": "spark_original_annotation_0_label",
    "Spark Annotation 0 Label": "spark_annotation_0_label",
    "Spark Camera Name": "spark_camera_name",
    "No of Spark Engagements": "no_of_spark_engagements",
    "SparkAI Query URL": "sparkai_query_url",
    "Other SparkAI URL": "other_sparkai_url",  # Array
    
    # === TRIAGE CLASSIFICATIONS ===
    "Operator Error or Misuse": "operator_error_or_misuse",
    "Bug or Intended Behavior": "bug_or_intended_behavior",
    "Vehicle/Object Outside Field": "vehicle_or_object_outside_field",
    "Vehicle Parked/Driving": "vehicle_parked_or_driving",
    "Vehicle On/Off Road": "vehicle_on_or_off_road",
    "Human Detection Details": "human_detection_details",
    "Confirmed Demotion Type": "confirmed_demotion_type",  # Array
    "Manned Type": "manned_type",
    "MTBI Bucket": "mtbi_bucket",  # Array
    
    # === JIRA INTEGRATION ===
    "Confirmed JRM Link": "confirmed_jrm_link",  # Linked field - needs lookup
    "Confirmed Jira URL": "confirmed_jira_url",
    
    # === URLS ===
    "Map pre-signed URL": "map_presigned_url",
    "Foxglove URL": "foxglove_url",
    "Spark URL": "spark_url",
    
    # === MACHINE DATA ===
    "genos_version": "genos_version",
    "Seconds in Autonomy Time Before Demotion": "seconds_in_autonomy_time_before_demotion",
    "Seconds In State 5 And 6": "seconds_in_state_5_and_6",
    "camera_name": "camera_name",
    
    # === DEPRECATED (Remove after testing) ===
    "From State": "from_state",
    "To State": "to_state",
    "Demotion Occurrence": "demotion_occurrence",
    "InOrbit URL": "inorbit_url",
    "Demotions": "demotions",
    "(Archived) Demotion Machine Behavior": "demotion_machine_behavior",
}

print(f"Column mapping defined: {len(COLUMN_MAPPING)} columns")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transform Airtable Records

# COMMAND ----------

def resolve_linked_field(record_fields: dict, field_name: str, mapping: dict) -> str:
    """Resolve a linked record field to its actual value using a mapping."""
    linked_ids = record_fields.get(field_name)
    if not linked_ids:
        return None
    if isinstance(linked_ids, list) and len(linked_ids) > 0:
        return mapping.get(linked_ids[0])
    return mapping.get(linked_ids)

def resolve_linked_field_array(record_fields: dict, field_name: str, mapping: dict) -> list:
    """Resolve a linked record field to array of values."""
    linked_ids = record_fields.get(field_name)
    if not linked_ids:
        return None
    if isinstance(linked_ids, list):
        return [mapping.get(lid) for lid in linked_ids if mapping.get(lid)]
    return [mapping.get(linked_ids)] if mapping.get(linked_ids) else None

def transform_record(record: dict) -> dict:
    """Transform an Airtable record to Databricks row format."""
    fields = record.get("fields", {})
    airtable_id = record.get("id")
    
    row = {"airtable_id": airtable_id}
    
    for at_field, dbx_col in COLUMN_MAPPING.items():
        value = fields.get(at_field)
        
        # Handle linked record fields that need lookup
        if at_field == "Demotion Reason":
            value = resolve_linked_field(fields, at_field, demotion_reason_mapping)
        elif at_field == "MAIN Demotion Reason":
            value = resolve_linked_field(fields, at_field, demotion_reason_mapping)
        elif at_field == "Secondary Demotion Reason":
            value = resolve_linked_field(fields, at_field, demotion_reason_mapping)
        elif at_field == "Preceding Stop Code Reason":
            value = resolve_linked_field(fields, at_field, demotion_reason_mapping)
        elif at_field == "MAIN Demotion Code":
            value = resolve_linked_field(fields, at_field, halt_code_mapping)
        elif at_field == "Secondary Demotion Manual":
            value = resolve_linked_field(fields, at_field, halt_code_mapping)
        elif at_field == "Preceding Stop Code":
            value = resolve_linked_field(fields, at_field, halt_code_mapping)
        elif at_field == "Confirmed JRM Link":
            value = resolve_linked_field(fields, at_field, jira_mapping)
        elif at_field == "Reviewer":
            value = resolve_linked_field(fields, at_field, reviewer_mapping)
        elif at_field == "Halt Code Investigation Guide":
            # Lookup field - take first value if array
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
        elif at_field == "Halt Description":
            # Lookup field - take first value if array
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
        elif at_field in ["Secondary Demotion Auto", "Other SparkAI URL", "Confirmed Demotion Type", "MTBI Bucket"]:
            # Keep as array
            pass
        
        row[dbx_col] = value
    
    return row

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Dev Table

# COMMAND ----------

def create_dev_table():
    """Create the dev table if it doesn't exist."""
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {DEV_TABLE} (
            airtable_id STRING,
            a_uid STRING,
            timestamp_utc STRING,
            vin STRING,
            bundle STRING,
            demotion_reason STRING,
            triage_status STRING,
            triage_review_complete STRING,
            triage_activities_complete STRING,
            investigation_complete STRING,
            triage_comments STRING,
            triage_reviewer STRING,
            in_scope STRING,
            halt_code_import STRING,
            main_demotion_code STRING,
            main_demotion_reason STRING,
            halt_code_investigation_guide STRING,
            halt_description STRING,
            secondary_demotion STRING,
            secondary_demotion_auto ARRAY<STRING>,
            secondary_demotion_reason STRING,
            manual_demotion_masking STRING,
            preceding_stop_code STRING,
            preceding_stop_datetime_utc STRING,
            preceding_stop_code_reason STRING,
            preceding_stop_code_error STRING,
            headlands_vs_interior STRING,
            headlands_turn STRING,
            implement_path_position_type_text STRING,
            computed_implement_path_position_type_text STRING,
            implement_path_position_type STRING,
            implement_path_position_heading STRING,
            implement_path_position_direction STRING,
            spark_program_name STRING,
            spark_response STRING,
            spark_original_annotation_0_label STRING,
            spark_annotation_0_label STRING,
            spark_camera_name STRING,
            no_of_spark_engagements INT,
            sparkai_query_url STRING,
            other_sparkai_url ARRAY<STRING>,
            operator_error_or_misuse STRING,
            bug_or_intended_behavior STRING,
            vehicle_or_object_outside_field STRING,
            vehicle_parked_or_driving STRING,
            vehicle_on_or_off_road STRING,
            human_detection_details STRING,
            confirmed_demotion_type ARRAY<STRING>,
            manned_type STRING,
            mtbi_bucket ARRAY<STRING>,
            confirmed_jrm_link STRING,
            confirmed_jira_url STRING,
            map_presigned_url STRING,
            foxglove_url STRING,
            spark_url STRING,
            genos_version STRING,
            seconds_in_autonomy_time_before_demotion BIGINT,
            seconds_in_state_5_and_6 INT,
            camera_name STRING,
            from_state STRING,
            to_state STRING,
            demotion_occurrence STRING,
            inorbit_url STRING,
            demotions STRING,
            demotion_machine_behavior STRING,
            synced_at TIMESTAMP
        )
        USING DELTA
        COMMENT 'Dev table for testing Airtable sync changes'
    """)
    print(f"Created/verified table: {DEV_TABLE}")

create_dev_table()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run Sync

# COMMAND ----------

def run_sync(limit: int = 100):
    """Fetch records from Airtable dev table and sync to Databricks."""
    print(f"Fetching records from Airtable dev table (limit: {limit})...")
    
    # Filter to recent records (last 7 days)
    formula = "DATETIME_DIFF(NOW(),{Timestamp UTC}, 'days') < 7"
    records = get_airtable_data(AIRTABLE_DEV_TABLE_ID, limit=limit, formula=formula)
    print(f"Fetched {len(records)} records from Airtable")
    
    if not records:
        print("No records to sync")
        return
    
    # Transform records
    rows = [transform_record(r) for r in records]
    print(f"Transformed {len(rows)} records")
    
    # Add sync timestamp
    from datetime import datetime
    sync_time = datetime.utcnow()
    for row in rows:
        row["synced_at"] = sync_time
    
    # Create DataFrame and write
    df = spark.createDataFrame(rows)
    
    # Merge into table (upsert by airtable_id)
    df.createOrReplaceTempView("new_records")
    
    spark.sql(f"""
        MERGE INTO {DEV_TABLE} AS target
        USING new_records AS source
        ON target.airtable_id = source.airtable_id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
    
    print(f"Synced {len(rows)} records to {DEV_TABLE}")
    
    # Show sample
    display(spark.sql(f"SELECT * FROM {DEV_TABLE} ORDER BY synced_at DESC LIMIT 5"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execute Sync
# MAGIC 
# MAGIC Run the cell below to sync data from Airtable to Databricks.

# COMMAND ----------

# Run the sync (adjust limit as needed)
run_sync(limit=500)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Results

# COMMAND ----------

# Check record count
display(spark.sql(f"SELECT COUNT(*) as total_records FROM {DEV_TABLE}"))

# Check latest synced records
display(spark.sql(f"""
    SELECT airtable_id, a_uid, timestamp_utc, vin, triage_status, synced_at 
    FROM {DEV_TABLE} 
    ORDER BY synced_at DESC 
    LIMIT 10
"""))
