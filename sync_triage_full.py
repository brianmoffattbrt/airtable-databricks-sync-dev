# Databricks notebook source
# MAGIC %md
# MAGIC # Sync Airtable to demotion_triage_full (FULL MIRROR)
# MAGIC 
# MAGIC This notebook pulls ALL fields from Airtable and writes them to `demotion_triage_full`.
# MAGIC 
# MAGIC **Purpose:** Create a complete mirror of Airtable triage data in Databricks for:
# MAGIC - Full audit trail of all triage process data
# MAGIC - Analytics on triage workflow (not just outcomes)
# MAGIC - Foundation for eventual Airtable replacement

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, LongType, DoubleType, TimestampType
from pyspark.sql.functions import current_timestamp, lit
from datetime import datetime
import requests
import urllib.parse

# Get spark session
spark = SparkSession.builder.getOrCreate()

# DEV CONFIG
AIRTABLE_BASE_ID = "app1jXoB1g13R9iOl"  # Triage Tool Prototype base
AIRTABLE_TABLE_ID = "tblFp0tXA3YOJGjMo"  # DEV TABLE: Demotions_DatabricksSync_Dev
AIRTABLE_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}'
AIRTABLE_TOKEN = dbutils.secrets.get(scope="brian.moffatt@bluerivertech.com", key="AIRTABLE_TOKEN")
DEMOTION_TRIAGE_FULL_TABLE = "jupiter_dev.brianm.demotion_triage_full"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Field Mapping
# MAGIC 
# MAGIC Maps all 120 Airtable fields to Spark column names.

# COMMAND ----------

# Complete mapping of Airtable field names to Spark column names
# Format: 'Airtable Field Name': ('spark_column_name', 'airtable_type')
AIRTABLE_TO_SPARK_MAPPING = {
    'A_UID': ('a_uid', 'multilineText'),
    'Timestamp UTC': ('timestamp_utc', 'singleLineText'),
    'VIN': ('vin', 'singleSelect'),
    'Pilot VINs Linked': ('pilot_vins_linked', 'multipleRecordLinks'),
    'VIN_machine_type': ('vin_machine_type', 'multipleLookupValues'),
    'Map pre-signed URL': ('map_pre_signed_url', 'singleLineText'),
    'SparkAI Query URL': ('sparkai_query_url', 'singleLineText'),
    'MAIN_SparkURL_Manual': ('main_sparkurl_manual', 'singleLineText'),
    'Duplicate Issue 5_23': ('duplicate_issue_5_23', 'singleSelect'),
    'Triage Activities Complete': ('triage_activities_complete', 'singleSelect'),
    'Triage Review Complete': ('triage_review_complete', 'singleSelect'),
    'From State': ('from_state', 'singleSelect'),
    'Main Demotion Status': ('main_demotion_status', 'singleSelect'),
    'Preceding Stop Code': ('preceding_stop_code', 'multipleRecordLinks'),
    'Secondary Demotion Manual': ('secondary_demotion_manual', 'multipleRecordLinks'),
    'Secondary Demotion Auto': ('secondary_demotion_auto', 'multipleRecordLinks'),
    'Secondary Demotion Issue': ('secondary_demotion_issue', 'singleSelect'),
    'Manual Demotion Masking': ('manual_demotion_masking', 'singleSelect'),
    'Confirmed Demotion Type': ('confirmed_demotion_type', 'multipleSelects'),
    'Operator Error or Misuse': ('operator_error_or_misuse', 'singleSelect'),
    'Investigation Complete': ('investigation_complete', 'singleSelect'),
    'Demotion Reason': ('demotion_reason', 'multipleLookupValues'),
    'MAIN Demotion Reason': ('main_demotion_reason', 'multipleLookupValues'),
    'Demotion Occurrence': ('demotion_occurrence', 'singleSelect'),
    'Halt Description': ('halt_description', 'multipleLookupValues'),
    '(Archived) ODD Assessment': ('archived_odd_assessment', 'singleSelect'),
    'Misuse Check Required': ('misuse_check_required', 'multipleLookupValues'),
    'Triage Comments - If questions/unusual observations during Triage': ('triage_comments_if_questions_unusual_observations_during_triage', 'richText'),
    'Triage Status': ('triage_status', 'singleSelect'),
    'To State': ('to_state', 'singleSelect'),
    'InOrbit URL': ('inorbit_url', 'singleLineText'),
    'Spark URL': ('spark_url', 'singleLineText'),
    'Spark Misuse Check Results': ('spark_misuse_check_results', 'singleSelect'),
    'Reviewer': ('reviewer', 'multipleRecordLinks'),
    'State screenshot': ('state_screenshot', 'multipleAttachments'),
    'Halt Code - Linked': ('halt_code_linked', 'multipleRecordLinks'),
    'Jira Link': ('jira_link', 'multipleLookupValues'),
    '(Archived) Demotion Machine Behavior': ('archived_demotion_machine_behavior', 'multipleLookupValues'),
    '(Archived) Jira Workflow': ('archived_jira_workflow', 'singleSelect'),
    'Demotions': ('demotions', 'singleSelect'),
    'Link to Webpage': ('link_to_webpage', 'multilineText'),
    'Occluded by LO?': ('occluded_by_lo', 'singleSelect'),
    'Bug or Intended Behavior': ('bug_or_intended_behavior', 'singleSelect'),
    'Confirmed JRM Link': ('confirmed_jrm_link', 'multipleRecordLinks'),
    'Human Detection Details': ('human_detection_details', 'singleSelect'),
    'Vehicle/Object Outside Field': ('vehicle_object_outside_field', 'singleSelect'),
    'Vehicle Type': ('vehicle_type', 'singleSelect'),
    'JRM Status': ('jrm_status', 'multipleLookupValues'),
    'Timestamp CST': ('timestamp_cst', 'formula'),
    'MTBI Bucket': ('mtbi_bucket', 'multipleSelects'),
    'Operator Notes (Engineering Machines)': ('operator_notes_engineering_machines', 'multilineText'),
    'Vehicle Parked/Driving': ('vehicle_parked_driving', 'singleSelect'),
    'Vehicle On/Off Road': ('vehicle_on_off_road', 'singleSelect'),
    'Misuse Check Reason': ('misuse_check_reason', 'singleSelect'),
    'Field Visualization (Test)': ('field_visualization_test', 'singleLineText'),
    'Spark Program Name': ('spark_program_name', 'singleLineText'),
    'Spark Response': ('spark_response', 'singleLineText'),
    'Spark Original Annotation 0 Label': ('spark_original_annotation_0_label', 'singleLineText'),
    'Spark Annotation 0 Label': ('spark_annotation_0_label', 'singleLineText'),
    'Spark Camera Name': ('spark_camera_name', 'singleLineText'),
    'Original Annotation 0 Label': ('original_annotation_0_label', 'singleSelect'),
    'Annotation 0 Label': ('annotation_0_label', 'singleSelect'),
    'Halt Code Investigation Guide': ('halt_code_investigation_guide', 'multipleLookupValues'),
    'Confirmed Jira URL': ('confirmed_jira_url', 'singleLineText'),
    'Headlands Reviewer': ('headlands_reviewer', 'multipleRecordLinks'),
    'Headlands Assessment Comments (Optional)': ('headlands_assessment_comments_optional', 'multilineText'),
    'In Scope': ('in_scope', 'singleSelect'),
    'Secondary Demotion Reason': ('secondary_demotion_reason', 'multipleLookupValues'),
    'Preceding Stop Datetime (UTC)': ('preceding_stop_datetime_utc', 'dateTime'),
    'Headlands Protocol': ('headlands_protocol', 'singleLineText'),
    'Autonomy state transition history': ('autonomy_state_transition_history', 'formula'),
    'Bundle Group': ('bundle_group', 'singleSelect'),
    'Manned Type': ('manned_type', 'singleSelect'),
    'Other SparkAI URL': ('other_sparkai_url', 'multipleSelects'),
    'No of Spark Engagements': ('no_of_spark_engagements', 'number'),
    'Bundle': ('bundle', 'singleSelect'),
    'Headlands Data Issue': ('headlands_data_issue', 'multipleSelects'),
    'Triage Process': ('triage_process', 'multipleLookupValues'),
    'Manual Masking Notes': ('manual_masking_notes', 'singleLineText'),
    'Manual Demotion on False Positive': ('manual_demotion_on_false_positive', 'singleSelect'),
    'Vis Map Error - Reason for Failure': ('vis_map_error_reason_for_failure', 'singleSelect'),
    'Vis Map Error - Reason Category': ('vis_map_error_reason_category', 'singleSelect'),
    'Vis Map Error - Demotion Failure Log Time': ('vis_map_error_demotion_failure_log_time', 'dateTime'),
    'JRM-611 - Spark Engagement': ('jrm_611_spark_engagement', 'singleSelect'),
    'Seconds in Autonomy Time Before Demotion': ('seconds_in_autonomy_time_before_demotion', 'number'),
    'Preceding Stop Code Reason': ('preceding_stop_code_reason', 'multipleLookupValues'),
    'Preceding Stop Code Error': ('preceding_stop_code_error', 'singleSelect'),
    'Implement Path Position Heading': ('implement_path_position_heading', 'singleLineText'),
    'Implement Path Position Direction': ('implement_path_position_direction', 'number'),
    'Headlands Assessment': ('headlands_assessment', 'singleSelect'),
    'Headlands vs Interior': ('headlands_vs_interior', 'singleSelect'),
    'Headlands Turn': ('headlands_turn', 'singleSelect'),
    'Implement Path Position Type': ('implement_path_position_type', 'number'),
    'Implement Path Position Type Text': ('implement_path_position_type_text', 'singleSelect'),
    'Spark UTC Time': ('spark_utc_time', 'formula'),
    'Halt Code - Import': ('halt_code_import', 'singleSelect'),
    'MAIN Demotion Code': ('main_demotion_code', 'multipleRecordLinks'),
    'Foxglove URL': ('foxglove_url', 'singleLineText'),
    'Headlands Assessment Complete': ('headlands_assessment_complete', 'singleSelect'),
    'Human Change to Vehicle': ('human_change_to_vehicle', 'singleLineText'),
    'Computed Implement Path Position Type Text': ('computed_implement_path_position_type_text', 'singleSelect'),
    'genos_version': ('genos_version', 'singleLineText'),
    'Seconds In State 5 And 6': ('seconds_in_state_5_and_6', 'number'),
    'camera_name': ('camera_name', 'singleSelect'),
    'Recent Human Detection?': ('recent_human_detection', 'singleLineText'),
    'Secondary Demotion Manual_updated': ('secondary_demotion_manual_updated', 'multipleRecordLinks'),
    'Preceding Stop Code copy': ('preceding_stop_code_copy', 'multipleRecordLinks'),
    'JRM Link Append Helper': ('jrm_link_append_helper', 'formula'),
    'Triage Protocol Tag': ('triage_protocol_tag', 'multipleSelects'),
    'Vin Match': ('vin_match', 'formula'),
    '# Perception Stops in last 10 minutes': ('perception_stops_in_last_10_minutes', 'number'),
    'Test Field': ('test_field', 'singleSelect'),
    'route_around': ('route_around', 'multipleRecordLinks'),
    'Confirmed Headlands': ('confirmed_headlands', 'singleSelect'),
    'Temp_Spark_Request_time': ('temp_spark_request_time', 'dateTime'),
    'Temp - Central Time': ('temp_central_time', 'formula'),
    'Temp_Brian_Review': ('temp_brian_review', 'singleSelect'),
    'clear_text_vin': ('clear_text_vin', 'multipleLookupValues'),
    'airtable_id': ('airtable_id', 'formula'),
    'NonNavigable Object Misuse Details': ('nonnavigable_object_misuse_details', 'singleSelect'),
}

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Table

# COMMAND ----------

def create_demotion_triage_full_table():
    """Create the demotion_triage_full table if it doesn't exist."""
    spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {DEMOTION_TRIAGE_FULL_TABLE} (
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
    """)
    print(f"Table {DEMOTION_TRIAGE_FULL_TABLE} created/verified")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pull ALL Airtable Data

# COMMAND ----------

def get_all_airtable_records(limit=20000):
    """
    Pull ALL records from Airtable with ALL fields.
    Uses pagination to handle large datasets.
    """
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    complete_response = []
    offset = None
    
    # Filter to last 6 months (same as main sync)
    formula = "DATETIME_DIFF(NOW(),{Timestamp UTC}, 'months') < 6"
    formula_encoded = urllib.parse.quote(formula)
    
    while True:
        url = f"{AIRTABLE_URL}?maxRecords=100&filterByFormula={formula_encoded}"
        if offset:
            url += f"&offset={offset}"
        
        print(f"Fetching records... (current count: {len(complete_response)})")
        resp = requests.get(url, headers=headers)
        data = resp.json()
        
        if 'error' in data:
            print(f"Error: {data['error']}")
            break
            
        records = data.get('records', [])
        complete_response.extend(records)
        
        if len(complete_response) >= limit:
            print(f"Reached limit of {limit} records")
            break
            
        offset = data.get('offset')
        if not offset:
            break
    
    print(f"Total records fetched: {len(complete_response)}")
    return complete_response

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transform Airtable Records to Spark DataFrame

# COMMAND ----------

def transform_field_value(value, airtable_type):
    """
    Transform an Airtable field value to a format suitable for Spark.
    """
    if value is None:
        return None
    
    # Handle arrays - convert to first element or string representation
    if airtable_type in ['multipleRecordLinks', 'multipleLookupValues']:
        if isinstance(value, list):
            # For linked records, just store the IDs as comma-separated
            return ','.join(str(v) for v in value) if value else None
        return str(value) if value else None
    
    # Handle multiple selects - keep as array
    if airtable_type == 'multipleSelects':
        return value if isinstance(value, list) else [value] if value else None
    
    # Handle attachments - store as JSON-like string
    if airtable_type == 'multipleAttachments':
        if isinstance(value, list) and value:
            # Just store URLs
            urls = [att.get('url', '') for att in value if isinstance(att, dict)]
            return ','.join(urls) if urls else None
        return None
    
    # Handle numbers
    if airtable_type == 'number':
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None
    
    # Handle dates
    if airtable_type == 'dateTime':
        # Keep as string, will be parsed by Spark
        return str(value) if value else None
    
    # Default: convert to string
    return str(value) if value is not None else None


def records_to_spark_rows(records):
    """
    Convert Airtable records to a list of dictionaries for Spark.
    """
    rows = []
    sync_time = datetime.utcnow()
    
    for record in records:
        row = {
            'airtable_record_id': record.get('id'),
            'sync_timestamp': sync_time,
        }
        
        fields = record.get('fields', {})
        
        # Map each Airtable field to its Spark column
        for airtable_name, (spark_name, airtable_type) in AIRTABLE_TO_SPARK_MAPPING.items():
            value = fields.get(airtable_name)
            row[spark_name] = transform_field_value(value, airtable_type)
        
        rows.append(row)
    
    return rows

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sync Function

# COMMAND ----------

def sync_airtable_to_triage_full():
    """
    Main sync function:
    1. Create table if not exists
    2. Pull ALL records from Airtable
    3. Transform to Spark format
    4. MERGE into demotion_triage_full (upsert)
    """
    print("=" * 60)
    print("Starting Airtable -> demotion_triage_full sync")
    print("=" * 60)
    
    # Step 1: Ensure table exists
    create_demotion_triage_full_table()
    
    # Step 2: Pull all records
    records = get_all_airtable_records()
    if not records:
        print("No records to sync")
        return
    
    # Step 3: Transform to Spark rows
    print("Transforming records...")
    rows = records_to_spark_rows(records)
    
    # Step 4: Create DataFrame
    print(f"Creating DataFrame with {len(rows)} rows...")
    df = spark.createDataFrame(rows)
    
    # Step 5: Write to table (use MERGE to upsert by airtable_record_id)
    # First, write to a temp table
    temp_table = f"{DEMOTION_TRIAGE_FULL_TABLE}_temp"
    df.write.mode("overwrite").saveAsTable(temp_table)
    
    # Then MERGE
    print("Merging to target table...")
    spark.sql(f"""
        MERGE INTO {DEMOTION_TRIAGE_FULL_TABLE} AS target
        USING {temp_table} AS source
        ON target.airtable_record_id = source.airtable_record_id
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
    
    # Cleanup temp table
    spark.sql(f"DROP TABLE IF EXISTS {temp_table}")
    
    print("=" * 60)
    print(f"Sync complete! {len(rows)} records synced to {DEMOTION_TRIAGE_FULL_TABLE}")
    print("=" * 60)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Execution

# COMMAND ----------

# Run the sync
sync_airtable_to_triage_full()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Results

# COMMAND ----------

# Show record count and sample
count = spark.sql(f"SELECT COUNT(*) as cnt FROM {DEMOTION_TRIAGE_FULL_TABLE}").collect()[0]['cnt']
print(f"Total records in {DEMOTION_TRIAGE_FULL_TABLE}: {count}")

# Show sample of key process fields that weren't tracked before
display(spark.sql(f"""
    SELECT 
        a_uid,
        vin,
        triage_activities_complete,
        investigation_complete,
        headlands_assessment_complete,
        reviewer,
        headlands_reviewer,
        headlands_assessment,
        headlands_vs_interior,
        sync_timestamp
    FROM {DEMOTION_TRIAGE_FULL_TABLE}
    LIMIT 10
"""))
