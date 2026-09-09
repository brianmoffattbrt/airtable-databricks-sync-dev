# Databricks notebook source
# MAGIC %md
# MAGIC # Airtable <-> Databricks Sync (DEV)
# MAGIC 
# MAGIC **BIDIRECTIONAL** development sync job for testing schema changes.
# MAGIC 
# MAGIC - **Source Airtable:** `Demotions_DatabricksSync_Dev` (tblFp0tXA3YOJGjMo)
# MAGIC - **Target Databricks:** `jupiter_dev.brianm.demotion_context_dev`
# MAGIC - **Source Data:** `jupiter_prod.jfa_metrics.demotions_stops_hours` (read-only)
# MAGIC 
# MAGIC ## Sync Flow
# MAGIC 1. DBX -> Airtable: Push new demotions to dev Airtable table
# MAGIC 2. Airtable -> DBX: Pull triage results back to dev Databricks table

# COMMAND ----------

# MAGIC %pip install tenacity
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import requests
from datetime import datetime, timedelta
from pyspark.sql.functions import col, trim, unix_timestamp, current_timestamp
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, ArrayType, DoubleType, LongType, BooleanType, FloatType, DayTimeIntervalType
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import urllib.parse

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

# Airtable Configuration - DEV TABLE
AIRTABLE_BASE_ID = "app1jXoB1g13R9iOl"  # Triage Tool Prototype
AIRTABLE_DEV_TABLE_ID = "tblFp0tXA3YOJGjMo"  # Demotions_DatabricksSync_Dev

# Reference table IDs (same as prod - read-only)
HALT_CODES_TABLE_ID = 'tblN8uu4Gl1eDZMLs'
DEMOTION_REASONS_TABLE_ID = 'tblINqDuMCUehLzgj'
JIRA_JRM_SCRUM_BOARD_SYNC_TABLE_ID = 'tbllaxeplHp2Jmrw6'
TEAM_MEMBERS_TABLE_ID = 'tblHQdtGEVbhNRWMR'
ERC_TABLE_ID = 'tblgvlFdCWixrylVF'
MACHINE_INFORMATION_TABLE_ID = 'tblW8Zbo7GVQMkVdC'

# Databricks Configuration - DEV TABLE
DEV_TABLE = "jupiter_dev.brianm.demotion_context_dev"
SOURCE_TABLE = "jupiter_prod.jfa_metrics.demotions_stops_hours"  # Read-only source

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
            token = dbutils.secrets.get(scope=scope, key="AIRTABLE_TOKEN")
            print(f"Using AIRTABLE_TOKEN from scope: {scope}")
            return token
        except Exception as e:
            print(f"Could not access scope {scope}: {e}")
            continue
    raise Exception("No accessible secrets scope found with AIRTABLE_TOKEN")

AIRTABLE_TOKEN = get_airtable_token()

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

def safe_timestamp_format(timestamp, format="%Y-%m-%dT%H:%M:%S.%f") -> str:
    """Convert timestamp to Airtable-compatible format."""
    if timestamp is None:
        return None
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return timestamp.strftime(format)[:-3] + "Z"

def convert_to_string_or_none(value):
    if value is None or value == "None":
        return None
    return f"{value}"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reference Data Mappings

# COMMAND ----------

print("Building reference mappings...")

def build_halt_code_mapping() -> dict:
    """Build mapping of halt code value -> record ID."""
    records = get_airtable_data(HALT_CODES_TABLE_ID)
    return {r["fields"].get("Halt Code"): r["id"] for r in records if r["fields"].get("Halt Code")}

def build_halt_code_name_mapping() -> dict:
    """Build mapping of halt code record ID -> code name."""
    records = get_airtable_data(HALT_CODES_TABLE_ID)
    return {r["id"]: r["fields"].get("Code Name") for r in records}

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

def build_erc_mapping() -> dict:
    """Build mapping of ERC value -> record ID."""
    records = get_airtable_data(ERC_TABLE_ID)
    return {r["fields"].get("ERC"): r["id"] for r in records if r["fields"].get("ERC")}

def build_vin_mapping() -> dict:
    """Build mapping of VIN -> record ID from machine_information."""
    records = get_airtable_data(MACHINE_INFORMATION_TABLE_ID, limit=5000)
    return {r["fields"].get("VIN"): r["id"] for r in records if r["fields"].get("VIN")}

# Build all mappings
halt_code_mapping = build_halt_code_mapping()  # halt_code -> record_id
halt_code_name_mapping = build_halt_code_name_mapping()  # record_id -> code_name
swapped_halt_code_mapping = {v: k for k, v in halt_code_mapping.items()}  # record_id -> halt_code
demotion_reason_mapping = build_demotion_reason_mapping()  # record_id -> reason_name
swapped_demotion_reason_mapping = {v: k for k, v in demotion_reason_mapping.items()}  # reason_name -> record_id
jira_mapping = build_jira_mapping()
reviewer_mapping = build_reviewer_mapping()
erc_mapping = build_erc_mapping()
vin_mapping = build_vin_mapping()

print(f"Loaded: {len(halt_code_mapping)} halt codes, {len(demotion_reason_mapping)} demotion reasons, {len(jira_mapping)} jira issues, {len(reviewer_mapping)} reviewers, {len(vin_mapping)} VINs")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Column Mapping Definition
# MAGIC 
# MAGIC This is the core mapping that defines which columns sync between Airtable and Databricks.
# MAGIC **To test removing a column: Comment it out or delete it from this list.**

# COMMAND ----------

# COLUMN MAPPING: Airtable Field Name -> Databricks Column Name
# Comment out or delete rows to test column removal
# Direction: "both" = synced in both directions, "at_to_dbx" = Airtable to DBX only, "dbx_to_at" = DBX to Airtable only

COLUMN_MAPPING = {
    # === CRITICAL IDENTIFIERS (DO NOT REMOVE) ===
    "A_UID": {"dbx_col": "a_uid", "direction": "both"},
    "Timestamp UTC": {"dbx_col": "timestamp_utc", "direction": "both"},
    "VIN": {"dbx_col": "vin", "direction": "both"},
    "Bundle": {"dbx_col": "bundle", "direction": "both"},
    
    # === TRIAGE RESULTS (Airtable → DBX) ===
    "Demotion Reason": {"dbx_col": "demotion_reason", "direction": "at_to_dbx", "linked": "demotion_reason"},
    "Triage Status": {"dbx_col": "triage_status", "direction": "at_to_dbx"},
    "Triage Review Complete": {"dbx_col": "triage_review_complete", "direction": "at_to_dbx"},
    "Triage Activities Complete": {"dbx_col": "triage_activities_complete", "direction": "at_to_dbx"},
    "Investigation Complete": {"dbx_col": "investigation_complete", "direction": "at_to_dbx"},
    "Triage Comments - If questions/unusual observations during Triage": {"dbx_col": "triage_comments", "direction": "at_to_dbx"},
    "Reviewer": {"dbx_col": "triage_reviewer", "direction": "at_to_dbx", "linked": "reviewer"},
    "In Scope": {"dbx_col": "in_scope", "direction": "at_to_dbx"},
    
    # === HALT CODE DATA ===
    "Halt Code - Import": {"dbx_col": "halt_code", "direction": "dbx_to_at"},
    "Halt Code - Linked": {"dbx_col": "halt_code_linked", "direction": "dbx_to_at", "linked": "halt_code"},
    "MAIN Demotion Code": {"dbx_col": "main_demotion_code", "direction": "at_to_dbx", "linked": "halt_code"},
    "MAIN Demotion Reason": {"dbx_col": "main_demotion_reason", "direction": "at_to_dbx", "linked": "demotion_reason"},
    "Halt Code Investigation Guide": {"dbx_col": "halt_code_investigation_guide", "direction": "at_to_dbx", "lookup": True},
    "Halt Description": {"dbx_col": "halt_description", "direction": "at_to_dbx", "lookup": True},
    
    # === SECONDARY DEMOTION ===
    "Secondary Demotion Manual": {"dbx_col": "secondary_demotion", "direction": "at_to_dbx", "linked": "halt_code"},
    "Secondary Demotion Auto": {"dbx_col": "secondary_demotion_auto", "direction": "both", "array": True},
    "Secondary Demotion Reason": {"dbx_col": "secondary_demotion_reason", "direction": "at_to_dbx", "linked": "demotion_reason"},
    "Manual Demotion Masking": {"dbx_col": "manual_demotion_masking", "direction": "at_to_dbx"},
    
    # === PRECEDING STOP ===
    "Preceding Stop Code": {"dbx_col": "preceding_stop_code", "direction": "both", "linked": "halt_code"},
    "Preceding Stop Datetime (UTC)": {"dbx_col": "preceding_stop_datetime_utc", "direction": "dbx_to_at"},
    "Preceding Stop Code Reason": {"dbx_col": "preceding_stop_code_reason", "direction": "at_to_dbx", "linked": "demotion_reason"},
    "Preceding Stop Code Error": {"dbx_col": "preceding_stop_code_error", "direction": "dbx_to_at"},
    
    # === HEADLANDS DATA ===
    "Headlands vs Interior": {"dbx_col": "headlands_vs_interior", "direction": "at_to_dbx"},
    "Headlands Turn": {"dbx_col": "headlands_turn", "direction": "at_to_dbx"},
    "Implement Path Position Type Text": {"dbx_col": "implement_path_position_type_text", "direction": "both"},
    "Computed Implement Path Position Type Text": {"dbx_col": "computed_implement_path_position_type_text", "direction": "both"},
    "Implement Path Position Type": {"dbx_col": "implement_path_position_type", "direction": "dbx_to_at"},
    "Implement Path Position Heading": {"dbx_col": "implement_path_position_heading", "direction": "dbx_to_at"},
    "Implement Path Position Direction": {"dbx_col": "implement_path_position_direction", "direction": "dbx_to_at"},
    
    # === PERCEPTION/SPARK DATA ===
    "Spark Program Name": {"dbx_col": "spark_program_name", "direction": "dbx_to_at"},
    "Spark Response": {"dbx_col": "spark_response", "direction": "dbx_to_at"},
    "Spark Original Annotation 0 Label": {"dbx_col": "spark_original_annotation_0_label", "direction": "dbx_to_at"},
    "Spark Annotation 0 Label": {"dbx_col": "spark_annotation_0_label", "direction": "dbx_to_at"},
    "Spark Camera Name": {"dbx_col": "spark_camera_name", "direction": "dbx_to_at"},
    "No of Spark Engagements": {"dbx_col": "no_of_spark_engagements", "direction": "dbx_to_at"},
    "SparkAI Query URL": {"dbx_col": "sparkai_query_url", "direction": "dbx_to_at"},
    "Other SparkAI URL": {"dbx_col": "other_sparkai_url", "direction": "dbx_to_at", "array": True},
    "Spark URL": {"dbx_col": "spark_url", "direction": "dbx_to_at"},
    
    # === TRIAGE CLASSIFICATIONS ===
    "Operator Error or Misuse": {"dbx_col": "operator_error_or_misuse", "direction": "at_to_dbx"},
    "Bug or Intended Behavior": {"dbx_col": "bug_or_intended_behavior", "direction": "at_to_dbx"},
    "Vehicle/Object Outside Field": {"dbx_col": "vehicle_or_object_outside_field", "direction": "at_to_dbx"},
    "Vehicle Parked/Driving": {"dbx_col": "vehicle_parked_or_driving", "direction": "at_to_dbx"},
    "Vehicle On/Off Road": {"dbx_col": "vehicle_on_or_off_road", "direction": "at_to_dbx"},
    "Human Detection Details": {"dbx_col": "human_detection_details", "direction": "at_to_dbx"},
    "Confirmed Demotion Type": {"dbx_col": "confirmed_demotion_type", "direction": "at_to_dbx", "array": True},
    "Manned Type": {"dbx_col": "manned_type", "direction": "at_to_dbx"},
    "MTBI Bucket": {"dbx_col": "mtbi_bucket", "direction": "dbx_to_at", "array": True},
    
    # === JIRA INTEGRATION ===
    "Confirmed JRM Link": {"dbx_col": "confirmed_jrm_link", "direction": "at_to_dbx", "linked": "jira"},
    "Confirmed Jira URL": {"dbx_col": "confirmed_jira_url", "direction": "at_to_dbx"},
    
    # === URLS ===
    "Map pre-signed URL": {"dbx_col": "map_presigned_url", "direction": "dbx_to_at"},
    "Foxglove URL": {"dbx_col": "foxglove_url", "direction": "dbx_to_at"},
    
    # === MACHINE DATA ===
    "genos_version": {"dbx_col": "genos_version", "direction": "dbx_to_at"},
    "Seconds in Autonomy Time Before Demotion": {"dbx_col": "seconds_in_autonomy_time_before_demotion", "direction": "dbx_to_at"},
    "Seconds In State 5 And 6": {"dbx_col": "seconds_in_state_5_and_6", "direction": "dbx_to_at"},
    "camera_name": {"dbx_col": "camera_name", "direction": "dbx_to_at"},
    
    # === DEPRECATED (Remove after testing) ===
    "From State": {"dbx_col": "from_state", "direction": "dbx_to_at"},
    "To State": {"dbx_col": "to_state", "direction": "dbx_to_at"},
    "Demotion Occurrence": {"dbx_col": "demotion_occurrence", "direction": "dbx_to_at"},
    "InOrbit URL": {"dbx_col": "inorbit_url", "direction": "dbx_to_at"},
    "Demotions": {"dbx_col": "demotions", "direction": "dbx_to_at"},
    "(Archived) Demotion Machine Behavior": {"dbx_col": "demotion_machine_behavior", "direction": "at_to_dbx"},
}

print(f"Column mapping defined: {len(COLUMN_MAPPING)} columns")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: DBX → Airtable (Push New Demotions)

# COMMAND ----------

def get_new_demotions(limit: int = 100):
    """Get new demotions from demotions_stops_hours that aren't in our dev table yet."""
    # For dev, we'll get recent demotions from the last 7 days
    query = f"""
        SELECT dsh.*
        FROM {SOURCE_TABLE} AS dsh
        LEFT JOIN {DEV_TABLE} dc 
            ON dsh.vin = dc.vin 
            AND dsh.timestamp_utc = dc.timestamp_utc 
            AND dsh.demotions = 1
        WHERE dsh.timestamp_utc >= date_sub(current_date(), 7)
        AND dsh.demotions = 1 
        AND dsh.halt_code != '0.0'
        AND dc.vin IS NULL
        LIMIT {limit}
    """
    return spark.sql(query)

def create_halt_code_if_needed(halt_code: str, halt_name: str = None, halt_description: str = None) -> str:
    """Create a halt code record if it doesn't exist, return record ID."""
    if halt_code in halt_code_mapping:
        return halt_code_mapping[halt_code]
    
    # Parse ERC and supplement code
    parts = str(halt_code).split(".")
    if len(parts) != 2:
        print(f"Invalid halt code format: {halt_code}")
        return None
    
    erc_value = int(parts[0])
    supplement_code = int(parts[1])
    
    erc_id = erc_mapping.get(erc_value)
    if not erc_id:
        print(f"ERC {erc_value} not found in mapping")
        return None
    
    payload = {
        "records": [{
            "fields": {
                "ERC": [erc_id],
                "Supplement Code": supplement_code,
                "Demotion Reason_Old": ["recBuyNxcnrReNpJ0"],  # DR-10 Unassigned
            }
        }],
        "typecast": True,
    }
    
    if halt_name:
        payload["records"][0]["fields"]["Code Name"] = halt_name
    if halt_description:
        payload["records"][0]["fields"]["Description"] = halt_description
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(
        f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{HALT_CODES_TABLE_ID}",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        record_id = response.json()["records"][0]["id"]
        halt_code_mapping[halt_code] = record_id
        print(f"Created halt code {halt_code} -> {record_id}")
        return record_id
    else:
        print(f"Failed to create halt code {halt_code}: {response.text}")
        return None

def push_to_airtable(demotions_df, batch_size: int = 10):
    """Push new demotions to Airtable dev table."""
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }
    
    records = demotions_df.collect()
    print(f"Pushing {len(records)} records to Airtable...")
    
    success_count = 0
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        payload = {
            "records": [],
            "typecast": True,
            "performUpsert": {
                "fieldsToMergeOn": ["A_UID"]
            },
        }
        
        for row in batch:
            row_dict = row.asDict()
            
            # Build A_UID
            a_uid = f"{row_dict.get('vin')} | {row_dict.get('timestamp_utc')}"
            
            # Get halt code record ID
            halt_code = str(row_dict.get('halt_code', ''))
            halt_code_id = halt_code_mapping.get(halt_code)
            if not halt_code_id and halt_code:
                halt_code_id = create_halt_code_if_needed(
                    halt_code, 
                    row_dict.get('halt_name'),
                    row_dict.get('halt_description')
                )
            
            # Get VIN link
            vin = row_dict.get('vin')
            vin_link = [vin_mapping[vin]] if vin and vin in vin_mapping else []
            
            # Build fields dict, only including non-None values
            fields = {
                "A_UID": a_uid,
                "VIN": vin,
            }
            
            # Add optional fields only if they have values
            if row_dict.get('bundle'):
                fields["Bundle"] = row_dict.get('bundle')
            if halt_code:
                fields["Halt Code - Import"] = halt_code
            if halt_code_id:
                fields["Halt Code - Linked"] = [halt_code_id]
            if row_dict.get('from_state') is not None:
                fields["From State"] = str(row_dict.get('from_state'))
            if row_dict.get('to_state') is not None:
                fields["To State"] = str(row_dict.get('to_state'))
            if row_dict.get('sparkai_url'):
                fields["Spark URL"] = row_dict.get('sparkai_url')
            if row_dict.get('foxglove_url'):
                fields["Foxglove URL"] = row_dict.get('foxglove_url')
            if row_dict.get('timestamp_utc'):
                fields["Timestamp UTC"] = safe_timestamp_format(row_dict.get('timestamp_utc'))
            if row_dict.get('map_presigned_url'):
                fields["Map pre-signed URL"] = row_dict.get('map_presigned_url')
            if vin_link:  # Only add if non-empty
                fields["Pilot VINs Linked"] = vin_link
            if row_dict.get('demotion_occurrence'):
                fields["Demotion Occurrence"] = row_dict.get('demotion_occurrence')
            if row_dict.get('latitude'):
                fields["latitude"] = float(row_dict.get('latitude'))
            if row_dict.get('longitude'):
                fields["longitude"] = float(row_dict.get('longitude'))
            if row_dict.get('genos_version'):
                fields["genos_version"] = row_dict.get('genos_version')
            
            record = {"fields": fields}
            
            payload["records"].append(record)
        
        # Send batch
        response = requests.post(
            f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_DEV_TABLE_ID}",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            success_count += len(batch)
            print(f"Pushed batch {i//batch_size + 1}: {len(batch)} records")
        else:
            print(f"Failed batch {i//batch_size + 1}: {response.text}")
    
    print(f"Successfully pushed {success_count}/{len(records)} records to Airtable")
    return success_count

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Airtable → DBX (Pull Triage Results)

# COMMAND ----------

def resolve_linked_field(record_fields: dict, field_name: str, mapping: dict) -> str:
    """Resolve a linked record field to its actual value using a mapping."""
    linked_ids = record_fields.get(field_name)
    if not linked_ids:
        return None
    if isinstance(linked_ids, list) and len(linked_ids) > 0:
        return mapping.get(linked_ids[0])
    return mapping.get(linked_ids)

def transform_airtable_record(record: dict) -> dict:
    """Transform an Airtable record to Databricks row format."""
    fields = record.get("fields", {})
    airtable_id = record.get("id")
    
    row = {"airtable_id": airtable_id}
    
    for at_field, config in COLUMN_MAPPING.items():
        dbx_col = config["dbx_col"]
        direction = config.get("direction", "both")
        
        # Skip fields that only go DBX -> Airtable
        if direction == "dbx_to_at":
            continue
        
        value = fields.get(at_field)
        
        # Handle linked record fields
        if config.get("linked") == "demotion_reason":
            value = resolve_linked_field(fields, at_field, demotion_reason_mapping)
        elif config.get("linked") == "halt_code":
            value = resolve_linked_field(fields, at_field, swapped_halt_code_mapping)
        elif config.get("linked") == "jira":
            value = resolve_linked_field(fields, at_field, jira_mapping)
        elif config.get("linked") == "reviewer":
            value = resolve_linked_field(fields, at_field, reviewer_mapping)
        elif config.get("lookup"):
            # Lookup fields return arrays
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
        
        row[dbx_col] = value
    
    return row

def pull_from_airtable(limit: int = 500):
    """Pull triage results from Airtable dev table."""
    print(f"Fetching records from Airtable dev table (limit: {limit})...")
    
    # Don't filter - just get all records (dev table should be small)
    # The DATETIME_DIFF formula was causing issues with the date format
    records = get_airtable_data(AIRTABLE_DEV_TABLE_ID, limit=limit, formula=None)
    print(f"Fetched {len(records)} records from Airtable")
    
    if not records:
        print("No records to sync")
        return None
    
    # Transform records
    rows = [transform_airtable_record(r) for r in records]
    print(f"Transformed {len(rows)} records")
    
    # Add sync timestamp
    sync_time = datetime.utcnow()
    for row in rows:
        row["synced_at"] = sync_time
    
    return rows

def merge_to_dev_table(rows: list):
    """Merge Airtable records into dev Databricks table."""
    if not rows:
        return
    
    df = spark.createDataFrame(rows)
    df.createOrReplaceTempView("airtable_records")
    
    # Upsert by airtable_id
    spark.sql(f"""
        MERGE INTO {DEV_TABLE} AS target
        USING airtable_records AS source
        ON target.airtable_id = source.airtable_id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
    
    print(f"Merged {len(rows)} records to {DEV_TABLE}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Dev Table (if needed)

# COMMAND ----------

def create_dev_table():
    """Create the dev table if it doesn't exist."""
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {DEV_TABLE} (
            airtable_id STRING,
            a_uid STRING,
            timestamp_utc TIMESTAMP,
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
            halt_code STRING,
            halt_code_linked STRING,
            main_demotion_code STRING,
            main_demotion_reason STRING,
            halt_code_investigation_guide STRING,
            halt_description STRING,
            secondary_demotion STRING,
            secondary_demotion_auto ARRAY<STRING>,
            secondary_demotion_reason STRING,
            manual_demotion_masking STRING,
            preceding_stop_code STRING,
            preceding_stop_datetime_utc TIMESTAMP,
            preceding_stop_code_reason STRING,
            preceding_stop_code_error STRING,
            headlands_vs_interior STRING,
            headlands_turn STRING,
            implement_path_position_type_text STRING,
            computed_implement_path_position_type_text STRING,
            implement_path_position_type STRING,
            implement_path_position_heading FLOAT,
            implement_path_position_direction STRING,
            spark_program_name STRING,
            spark_response STRING,
            spark_original_annotation_0_label STRING,
            spark_annotation_0_label STRING,
            spark_camera_name STRING,
            no_of_spark_engagements INT,
            sparkai_query_url STRING,
            other_sparkai_url ARRAY<STRING>,
            spark_url STRING,
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
        COMMENT 'Dev table for testing Airtable sync changes - mirrors demotion_context'
    """)
    print(f"Created/verified table: {DEV_TABLE}")

create_dev_table()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run Full Sync

# COMMAND ----------

def run_full_sync(push_limit: int = 50, pull_limit: int = 500):
    """Run bidirectional sync: push new demotions, pull triage results."""
    print("=" * 60)
    print("STARTING BIDIRECTIONAL SYNC")
    print("=" * 60)
    
    # Part 1: Push new demotions to Airtable
    print("\n--- Part 1: DBX -> Airtable (Push New Demotions) ---")
    new_demotions = get_new_demotions(limit=push_limit)
    if new_demotions.count() > 0:
        push_to_airtable(new_demotions)
    else:
        print("No new demotions to push")
    
    # Part 2: Pull triage results from Airtable
    print("\n--- Part 2: Airtable -> DBX (Pull Triage Results) ---")
    rows = pull_from_airtable(limit=pull_limit)
    if rows:
        merge_to_dev_table(rows)
    
    print("\n" + "=" * 60)
    print("SYNC COMPLETE")
    print("=" * 60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execute Sync
# MAGIC 
# MAGIC Run the cell below to perform bidirectional sync.
# MAGIC - `push_limit`: Max new demotions to push to Airtable
# MAGIC - `pull_limit`: Max records to pull from Airtable

# COMMAND ----------

# Run the full bidirectional sync
run_full_sync(push_limit=50, pull_limit=500)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Results

# COMMAND ----------

# Check record count
display(spark.sql(f"SELECT COUNT(*) as total_records FROM {DEV_TABLE}"))

# Check latest synced records
display(spark.sql(f"""
    SELECT airtable_id, a_uid, vin, triage_status, investigation_complete, synced_at 
    FROM {DEV_TABLE} 
    ORDER BY synced_at DESC 
    LIMIT 10
"""))
