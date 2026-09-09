# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks <-> Airtable Sync (DEV CLONE)
# MAGIC 
# MAGIC **This is an EXACT CLONE of the production mesa sync notebook, pointing to DEV tables.**
# MAGIC 
# MAGIC Use this to test schema changes before applying to production.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC This notebooks is intended to provide all the neccessary functionality to perform Databricks <-> Airtable sync flow. It includes uploading latest updates from "demotions_stops_hours" to the Airtable table "DemotionContext", pulling the data and merging it back to "demotion_context" Databricks table, as well as cleaning up processed Airtable instances. 
# MAGIC
# MAGIC **DEV CHANGES:**
# MAGIC - Airtable table: `Demotions_DatabricksSync_Dev` (tblFp0tXA3YOJGjMo)
# MAGIC - Databricks table: `jupiter_dev.brianm.demotion_context_dev`
# MAGIC - Uses brian.moffatt secrets scope
# MAGIC
# MAGIC [Documentation describing the flow](https://bluerivertechnology.atlassian.net/wiki/spaces/MESA/pages/3852271663/Implementation+Iterations)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prerequisites

# COMMAND ----------

# MAGIC %md
# MAGIC First of all we need to import required Python modules and setup secrets, that we'll use further in the script.

# COMMAND ----------

# MAGIC %pip install /Workspace/Shared/Libraries/keyforge-1.44.1-py3-none-any.whl tenacity
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from pyspark.shell import spark
import requests
from datetime import datetime, timedelta
from pyspark.sql.functions import trim, unix_timestamp, current_timestamp
from pyspark.sql import Row
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType, \
    LongType, DayTimeIntervalType, ArrayType, FloatType, BooleanType
from pprint import pprint
from requests import request
import keyforge
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, wait_fixed
import time
import urllib.parse
import re

# COMMAND ----------

# ============================================================================
# DEV CONFIG: Hardcoded dev table IDs instead of secrets
# These are the ONLY lines that differ from production
# ============================================================================
TEMP_TABLES_PATH = "jupiter_dev.brianm."  # Dev temp tables go in brianm schema
AIRTABLE_TABLE_NAME = "Demotions_DatabricksSync_Dev"  # Dev Airtable table name
AIRTABLE_BASE_ID = "app1jXoB1g13R9iOl"  # Same base (Triage Tool Prototype)
AIRTABLE_TABLE_ID = "tblFp0tXA3YOJGjMo"  # DEV TABLE: Demotions_DatabricksSync_Dev
DEMOTION_CONTEXT_TABLE = "jupiter_dev.brianm.demotion_context_dev"  # DEV Databricks table
ROUTE_AROUND_CONTEXT_TABLE = dbutils.secrets.get(scope="andras.nagy@bluerivertech.com", key="ROUTE_AROUND_CONTEXT_TABLE")  # Keep prod (not testing this)
ROUTE_AROUND_TABLE_ID = dbutils.secrets.get(scope="andras.nagy@bluerivertech.com", key="ROUTE_AROUND_TABLE_ID")  # Keep prod (not testing this)
DEMOTIONS_STOP_HOURS_TABLE = "jupiter_prod.jfa_metrics.demotions_stops_hours"  # Read from prod source
AIRTABLE_TOKEN = dbutils.secrets.get(scope="brian.moffatt@bluerivertech.com", key="AIRTABLE_TOKEN")  # Use Brian's token
# ============================================================================
AIRTABLE_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}'
AIRTABLE_URL_GET = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}'
KEYFORGE_TOKEN = keyforge.get_token(cache_token_allowed=False).access_token
HALT_CODES_TABLE_ID = 'tblN8uu4Gl1eDZMLs'
DEMOTION_REASONS_TABLE_ID = 'tblINqDuMCUehLzgj'
JIRA_JRM_SCRUM_BOARD_SYNC_TABLE_ID = 'tbllaxeplHp2Jmrw6'
TEAM_MEMBERS_TABLE_ID = 'tblHQdtGEVbhNRWMR'
ERC_TABLE_ID = 'tblgvlFdCWixrylVF'
MACHINE_INFORMATION_TABLE_ID = 'tblW8Zbo7GVQMkVdC'
start_time = time.time()

# COMMAND ----------

def get_AIRTABLE_URL_for_table(table_id: str):
    return f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_id}'

# COMMAND ----------

def is_valid_vin(vin: str) -> bool:
    return bool(vin and re.match(r"^[A-HJ-NPR-Z0-9]{17}$", vin))


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(30),
    retry=retry_if_exception_type(Exception),
)
def hash_vin(value, *args):
    """
    Hashes the given string or list of strings with a centrally managed salt.

    Args:
        value (str): The string to hash.
        args (list): The list of strings to hash. User can provide either a single string or a list of strings.
    Returns:
        str|list[str]: The hash of the string or list of hashed strings.
    """
    if not is_valid_vin(value):
        return value
    params = {"data": value if len(args) == 0 else [value, *args]}
    headers = {"Content-Type": "application/json", **{"Authorization": f"Bearer {KEYFORGE_TOKEN}"}}
    r = request("POST", "https://api.tartarus.prod.mesa.brtws.com/de-identification/hash_with_salt", json=params, headers=headers)
    if (
        r.status_code == 200 and
        r.headers["content-type"].strip().startswith("application/json")
    ):
        return r.json().get("de-identified")
    else:
        raise ValueError(f"Failed to hash {value} with status code {r.status_code}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tables creation / deletion

# COMMAND ----------

def get_all_airtable_tables() -> list[dict]:
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        url=f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables",
        headers=headers
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Request failed with status code {}".format(response.status_code))
    
    data = response.json()
    return data['tables']

def get_current_data_schema(table_id: str = AIRTABLE_TABLE_ID):
    tables = get_all_airtable_tables()
    for table in tables:
        if table['id'].strip() == table_id:
            return table

current_data_schema = get_current_data_schema()

# Preprocess the table schema
fields_to_create = []

# Remove ids
for field in current_data_schema['fields']:
    # if field['name'] == 'Halt Code - Linked':
    #     continue
    field_to_create = {**field}
    field_to_create.pop("id")
    if 'options' in field_to_create:
        if 'choices' in field_to_create['options']:
            for choice in field_to_create['options']['choices']:
                # choice.pop('id')
                ...
    fields_to_create.append(field_to_create)

# for field in fields_to_create:
#     if 'options' in field:
#         field.pop('options')
#     field['type'] = 'multilineText'
for field in fields_to_create:
    if 'options' in field:
        if 'choices' in field['options']:
            for choice in field['options']['choices']:
                del choice['id']
        
    match field['type']:
        case "multipleLookupValues" | "formula" | "multipleRecordLinks" | "button" | "multipleAttachments":
            field['type'] = 'multilineText'
            if 'options' in field:
                field.pop('options')
    
    match field['name']:
        case 'Bundle' | 'Halt Code - Import' | "VIN":
            field['type'] = 'singleLineText'
            if 'options' in field:
                field.pop('options')
        case 'To State':
            field['options']['choices'] = [{'color': 'orangeDark1', 'name': '0'},
                          {'color': 'redBright', 'name': '1'},
                          {'color': 'orangeLight1', 'name': '2'}]
        case 'Demotions': 
            field['options']['choices'] = [{'color': 'blueLight2', 'name': '1'}]
    
pprint(fields_to_create)


# COMMAND ----------

def create_new_airtable_table(fields):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "description": "Table for Databricks <-> Airtable automatic sync.",
        "fields": fields,
        "name": AIRTABLE_TABLE_NAME,
        }

    response = requests.post(
        url=f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables", 
        headers=headers,
        json=data,
    )
    if response.status_code != 200:
        print(response.json())
        raise Exception("Request failed with status code {}".format(response.status_code))



# COMMAND ----------

# MAGIC %md
# MAGIC Databricks table (for `demotion_context` and temp tables).

# COMMAND ----------

def create_demotion_context_table(table_name: str = None):
    if table_name is not None:
        table_name = f'{TEMP_TABLES_PATH}{table_name}' 
    else:
        table_name = DEMOTION_CONTEXT_TABLE
    print(f'Created {table_name} in Databricks')
    spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        System STRING, 
        VIN STRING, 
        MachinePIN_masked STRING,
        Vehicle STRING, 
        Bundle STRING, 
        Demotions INTEGER, 
        Stops int, 
        halt_code STRING, 
        halt_name STRING, 
        halt_description STRING, 
        demotion_occurrence STRING, 
        ec_tags STRING, 
        ec_ticket_url STRING, 
        formant_url STRING, 
        prior_timestamp TIMESTAMP, 
        last_activation_time TIMESTAMP, 
        from_state STRING, 
        to_state STRING,
        InOrbit_URL STRING, 
        SparkAI_URL STRING, 
        Foxglove_URL STRING, 
        timestamp_diff_from_last_activation INTERVAL DAY TO SECOND, 
        minutes_from_activation DOUBLE, 
        seconds_from_activation BIGINT, 
        hours_from_activation DOUBLE, 
        ID BIGINT, 
        Airtable_ID STRING,
        Timestamp TIMESTAMP, 
        Timestamp_utc TIMESTAMP, 
        county STRING, 
        state STRING, 
        country STRING, 
        operation_time STRING, 
        demotion_reason STRING, 
        triage_status STRING, 
        demotion_machine_behavior STRING, 
        odd_assessment STRING,
        map_presigned_url STRING,
        airtable_deleted BOOLEAN,
        triage_review_complete STRING,
        latitude DOUBLE,
        longitude DOUBLE,
        spark_program_name STRING, 
        spark_response STRING,
        spark_original_annotation_0_label STRING,
        spark_annotation_0_label STRING,
        spark_camera_name STRING,
        halt_code_investigation_guide STRING,
        operator_error_or_misuse STRING,
        headlands_vs_interior STRING,
        headlands_turn STRING,
        vehicle_or_object_outside_field STRING,
        vehicle_parked_or_driving STRING,
        vehicle_on_or_off_road STRING,
        bug_or_intended_behavior STRING, 
        confirmed_jrm_link STRING,
        triage_activities_complete STRING,
        confirmed_jira_url STRING,
        triage_reviewer STRING,
        triage_comments STRING,
        in_scope STRING,
        manual_demotion_masking STRING,
        secondary_demotion STRING,
        secondary_demotion_reason STRING,
        MTBI_bucket ARRAY<STRING>,
        confirmed_demotion_type ARRAY<STRING>,
        manned_type STRING,
        SparkAI_query_URL STRING,
        other_sparkai_url ARRAY<STRING>,
        secondary_demotion_auto ARRAY<STRING>,
        no_of_spark_engagements INTEGER,
        prev_stop_halt_code STRING,
        prev_stop_timestamp TIMESTAMP,
        seconds_in_autonomy_time_before_demotion BIGINT,
        Preceding_Stop_Code STRING,
        Preceding_Stop_Code_Error STRING,
        Preceding_Stop_Datetime_UTC TIMESTAMP,
        Preceding_Stop_Code_Reason STRING,
        implement_path_position_type BIGINT,
        implement_path_position_type_text STRING,
        implement_path_position_heading FLOAT,
        implement_path_position_direction BIGINT,
        human_detection_details STRING,
        spark_multiurl_pkey_uid STRING, 
        aletheia_image STRING,
        secondary_demotion_array ARRAY<STRING>,
        stop_interrupted_by_manual_demotion BOOLEAN,
        other_spark_reasons ARRAY<STRING>,
        spark_window_search_time TIMESTAMP,
        camera_angle_y_pos FLOAT,
        camera_angle_x_pos FLOAT,
        spark_uuid STRING,
        spark_timestamp TIMESTAMP,
        spark_machine_id STRING,
        spark_token STRING,
        spark_date_closed TIMESTAMP,
        spark_date_created TIMESTAMP,
        spark_state STRING,
        billable_org_name STRING,
        client_name STRING,
        field_name STRING,
        farm_name STRING,
        org_id BIGINT,
        field_operation_guid STRING,
        crop_id STRING,
        client_guid STRING,
        sparkai_program STRING,
        machine_name STRING,
        field_guid STRING,
        farm_guid STRING,
        is_system_triggered_demotion INTEGER,
        is_human_triggered_demotion INTEGER,
        is_unintended_perception_demotion INTEGER,
        is_intended_perception_demotion INTEGER,
        is_non_perception_demotion INTEGER,
        is_intended_manual_demotion INTEGER,
        is_product_demotion INTEGER,
        is_customer_demotion INTEGER,
        is_triaged_demotion INTEGER,
        is_verified_with_demotion_context INTEGER,
        is_rtf_demotion INTEGER,
        is_verified_demotion INTEGER,
        triaged_halt_code_name STRING,
        triaged_halt_code_description STRING,
        enable_point_cloud_processor BOOLEAN,
        genos_version STRING,
        computed_implement_path_position_type_text STRING,
        seconds_in_state_5_and_6 INTEGER,
        main_demotion_code STRING,
        main_demotion_reason STRING,
        investigation_complete STRING
    )""")


# COMMAND ----------

DAYS_TO_EXPIRE = 14

def delete_expired_temp_tables():
    deleted_tables = []
    temp_tables_path_formatted = TEMP_TABLES_PATH[:-1]  # TEMP_TABLES_PATH ENV ends with dot
    output_table_data = spark.sql(f'SHOW TABLES IN {temp_tables_path_formatted}')
    for table_name in output_table_data.collect():
        demotion_datetime = datetime.strptime(table_name['tableName'][-19:], "%Y_%m_%d_%H_%M_%S")
        formatted_datetime = demotion_datetime.strftime("%Y-%m-%d %H:%M:%S")
        parsed_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
        current_datetime = datetime.now()
        time_difference = current_datetime - parsed_datetime
        if time_difference.days > DAYS_TO_EXPIRE:
            spark.sql(f'DROP TABLE IF EXISTS {TEMP_TABLES_PATH}{table_name["tableName"]}')
            print(f'{table_name["tableName"]} was deleted')
            deleted_tables.append(table_name["tableName"])
    return deleted_tables


# COMMAND ----------

# MAGIC %md
# MAGIC Function to retrieve airtable data. See [documentation](https://airtable.com/app1jXoB1g13R9iOl/api/docs#curl/table:demotioncontext:list) for further details.

# COMMAND ----------

def get_airtable_data(
        url: str = None,
        limit=1000,
        formula: str | None = None,
        params: dict | None = None,
):
    url = url or AIRTABLE_URL
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    initial_url = url
    complete_response = []
    offset = 0
    offset_value = 0
    while offset_value < limit:
        url = initial_url + f'?offset={offset}&maxRecords=20000'
        if formula:
            url += f'&filterByFormula={formula}'
        print(url)
        resp = requests.get(url, headers=headers, params=params)
        resp = resp.json()
        if 'error' in resp:
            print(f'Error occurred: {resp["error"]}')
            break
        data = resp['records']
        offset_value += 100
        complete_response += data
        if 'offset' in resp:
            offset = resp['offset']
        else:
            break
    return complete_response

# COMMAND ----------

# MAGIC %md
# MAGIC Demotion Reason and Halt Code mapping

# COMMAND ----------

def get_halt_code_records_mapping():
    mapping = {}
    halt_codes_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(HALT_CODES_TABLE_ID),
        limit=1000
    )
    for halt_code_record in halt_codes_data:
        mapping[halt_code_record['fields']['Halt Code']] = halt_code_record['id']
    return mapping

halt_code_records_mapping = get_halt_code_records_mapping()

def swap_key_value(dictionary):
    return {value: key for key, value in dictionary.items()}

swapped_halt_code_records_mapping = swap_key_value(halt_code_records_mapping)

# COMMAND ----------

def get_demotion_reason_mapping():
    mapping = {}
    demotion_reason_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(DEMOTION_REASONS_TABLE_ID), limit=1000
    )
    for demotion_reason_record in demotion_reason_data:
        mapping[demotion_reason_record["id"]] = demotion_reason_record["fields"][
            "Airtable_Demotion_Reason"
        ]
    return mapping


demotion_reason_mapping = get_demotion_reason_mapping()
swapped_demotion_reason_mapping = swap_key_value(demotion_reason_mapping)


# COMMAND ----------

def get_jira_issue_key_mapping():
    mapping = {}
    jira_issue_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(JIRA_JRM_SCRUM_BOARD_SYNC_TABLE_ID), limit=2000
    )
    for jira_issue_record in jira_issue_data:
        mapping[jira_issue_record["id"]] = jira_issue_record["fields"][
            "Issue Key"
        ]
    return mapping


jira_issue_mapping = get_jira_issue_key_mapping()


# COMMAND ----------

def get_reviewer_name_mapping():
    mapping = {}
    reviewer_name_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(TEAM_MEMBERS_TABLE_ID), limit=1000
    )
    for reviewer_name_record in reviewer_name_data:
        mapping[reviewer_name_record["id"]] = reviewer_name_record["fields"][
            "Name"
        ]
    return mapping


reviewer_name_mapping = get_reviewer_name_mapping()

# COMMAND ----------

formula = "DATETIME_DIFF(NOW(),{Timestamp UTC}, 'months') < 6"
formula_encoded = urllib.parse.quote(formula)


def get_demotions_a_uid_mapping():
    mapping = {}
    params = {
        "fields[]": ["A_UID"],
    }
    demotions_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(AIRTABLE_TABLE_ID),
        formula=formula_encoded,
        params=params,
        limit=20000
    )
    for demotion in demotions_data:
        mapping[demotion["id"]] = demotion["fields"]["A_UID"]
    return mapping


demotions_a_uid_mapping = get_demotions_a_uid_mapping()
swapped_demotions_a_uid_mapping = swap_key_value(demotions_a_uid_mapping)


# COMMAND ----------

# MAGIC
# MAGIC %md
# MAGIC ## Utils

# COMMAND ----------

# MAGIC %md
# MAGIC Generate name for temprary table in Databricks for Airtable changes.

# COMMAND ----------

def get_temp_table_name() -> str:
    current_time = datetime.now()
    temp_table_name = "demotion_context_" + current_time.strftime("%Y_%m_%d_%H_%M_%S")
    create_demotion_context_table(temp_table_name)

    return temp_table_name


# COMMAND ----------

# MAGIC %md
# MAGIC Converters

# COMMAND ----------

def parse_datetime(date_str):
    if isinstance(date_str, str):
        if date_str[-1] != "Z":
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
        else:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_str


def parse_float(value: float | None):
    if value is not None:
        return float(value)
    

def parse_int(value: int | None):
    if value is not None:
        return int(value)


def safe_airtable_timestamp_format(timestamp, format = "%Y-%m-%dT%H:%M:%S.%f") -> str:
    if isinstance(timestamp, str):
        timestamp_dt = datetime.fromisoformat(timestamp)
    else:
        timestamp_dt = timestamp
    timestamp_str = timestamp_dt.strftime(format)[:-3] + "Z"

    return timestamp_str

# COMMAND ----------

# MAGIC %md
# MAGIC ## Databricks communication

# COMMAND ----------

# MAGIC %md
# MAGIC Get updates from `demotions_stop_hours` table

# COMMAND ----------

def get_demotions_stops_hours_updates(limit: int = 10):
    data = spark.sql(f"""
        SELECT dsh.*
        FROM jupiter_prod.jfa_metrics.demotions_stops_hours AS dsh
        ANTI JOIN {DEMOTION_CONTEXT_TABLE} dc 
            ON dsh.`vin` = dc.`VIN` 
            AND dsh.`timestamp_utc` = dc.`Timestamp_utc` 
            AND dsh.demotions = dc.demotions
        WHERE dsh.`timestamp_utc` >= '2024-10-01'
        AND dsh.id is not null
        AND dsh.demotions = 1 
        AND dsh.halt_code != "0.0"
        AND dsh.demotion_context__airtable_deleted IS NOT TRUE
        limit {limit}
    """)
    return data

# COMMAND ----------

# MAGIC %md
# MAGIC Functionality to merge data into Databricks `demotion_context` table.

# COMMAND ----------

# Schema for demotion context table
schema = StructType([
    StructField("System", StringType(), True),
    StructField("VIN", StringType(), True),
    StructField("MachinePIN_masked", StringType(), True),
    StructField("Vehicle", StringType(), True),
    StructField("Bundle", StringType(), True),
    StructField("Demotions", IntegerType(), True),
    StructField("Stops", IntegerType(), True),
    StructField("halt_code", StringType(), True),
    StructField("halt_name", StringType(), True),
    StructField("halt_description", StringType(), True),
    StructField("demotion_occurrence", StringType(), True),
    StructField("ec_tags", StringType(), True),
    StructField("ec_ticket_url", StringType(), True),
    StructField("formant_url", StringType(), True),
    StructField("prior_timestamp", TimestampType(), True),
    StructField("last_activation_time", TimestampType(), True),
    StructField("from_state", StringType(), True),
    StructField("to_state", StringType(), True),
    StructField("SparkAI_URL", StringType(), True),
    StructField("Foxglove_URL", StringType(), True),
    StructField("timestamp_diff_from_last_activation", DayTimeIntervalType(), True),
    StructField("minutes_from_activation", DoubleType(), True),
    StructField("seconds_from_activation", LongType(), True),
    StructField("ID", LongType(), True),
    StructField("Airtable_ID", StringType(), True),
    StructField("hours_from_activation", DoubleType(), True),
    StructField("Timestamp_utc", TimestampType(), True),
    StructField("Timestamp", TimestampType(), True),
    StructField("county", StringType(), True),
    StructField("state", StringType(), True),
    StructField("country", StringType(), True),
    StructField("operation_time", StringType(), True),  
    StructField("demotion_reason", StringType(), True),
    StructField("triage_status", StringType(), True),
    StructField("demotion_machine_behavior", StringType(), True),
    StructField("triage_review_complete", StringType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("spark_program_name", StringType(), True),
    StructField("spark_response", StringType(), True),
    StructField("spark_original_annotation_0_label", StringType(), True),
    StructField("spark_annotation_0_label", StringType(), True),
    StructField("spark_camera_name", StringType(), True),
    StructField("map_presigned_url", StringType(), True),
    StructField("halt_code_investigation_guide", StringType(), True),
    StructField("operator_error_or_misuse", StringType(), True),
    StructField("headlands_vs_interior", StringType(), True),
    StructField("headlands_turn", StringType(), True),
    StructField("vehicle_or_object_outside_field", StringType(), True),
    StructField("vehicle_parked_or_driving", StringType(), True),
    StructField("vehicle_on_or_off_road", StringType(), True),
    StructField("bug_or_intended_behavior", StringType(), True),
    StructField("confirmed_jrm_link", StringType(), True),
    StructField("triage_activities_complete", StringType(), True),
    StructField("confirmed_jira_url", StringType(), True),
    StructField("triage_reviewer", StringType(), True),
    StructField("triage_comments", StringType(), True),
    StructField("in_scope", StringType(), True),
    StructField("manual_demotion_masking", StringType(), True),
    StructField("secondary_demotion", StringType(), True),
    StructField("secondary_demotion_reason", StringType(), True),
    StructField("confirmed_demotion_type", ArrayType(StringType()), True),
    StructField("manned_type", StringType(), True),
    StructField("SparkAI_query_URL", StringType(), True),
    StructField("other_sparkai_url", ArrayType(StringType()), True),
    StructField("secondary_demotion_auto", ArrayType(StringType()), True),
    StructField("no_of_spark_engagements", IntegerType(), True),
    StructField("prev_stop_halt_code", StringType(), True),
    StructField("main_demotion_code", StringType(), True),
    StructField("main_demotion_reason", StringType(), True),
    StructField("investigation_complete", StringType(), True),
    StructField("Preceding_Stop_Code", StringType(), True),
    StructField("Preceding_Stop_Code_Reason", StringType(), True),
    StructField("implement_path_position_type_text", StringType(), True),
    StructField("human_detection_details", StringType(), True),
    StructField("spark_multiurl_pkey_uid", StringType(), True),
    StructField("aletheia_image", StringType(), True),
    StructField("secondary_demotion_array", ArrayType(StringType(), True), True),
    StructField("stop_interrupted_by_manual_demotion", BooleanType(), True),
    StructField("other_spark_reasons", ArrayType(StringType(), True), True),
    StructField("spark_window_search_time", TimestampType(), True),
    StructField("camera_angle_y_pos", FloatType(), True),
    StructField("camera_angle_x_pos", FloatType(), True),
    StructField("spark_uuid", StringType(), True),
    StructField("spark_timestamp", TimestampType(), True),
    StructField("spark_machine_id", StringType(), True),
    StructField("spark_token", StringType(), True),
    StructField("spark_date_closed", TimestampType(), True),
    StructField("spark_date_created", TimestampType(), True),
    StructField("spark_state", StringType(), True),
    StructField("billable_org_name", StringType(), True),
    StructField("client_name", StringType(), True),
    StructField("field_name", StringType(), True),
    StructField("farm_name", StringType(), True),
    StructField("org_id", LongType(), True),
    StructField("field_operation_guid", StringType(), True),
    StructField("crop_id", StringType(), True),
    StructField("client_guid", StringType(), True),
    StructField("sparkai_program", StringType(), True),
    StructField("machine_name", StringType(), True),
    StructField("field_guid", StringType(), True),
    StructField("farm_guid", StringType(), True),
    StructField("is_system_triggered_demotion", IntegerType(), True),
    StructField("is_human_triggered_demotion", IntegerType(), True),
    StructField("is_unintended_perception_demotion", IntegerType(), True),
    StructField("is_intended_perception_demotion", IntegerType(), True),
    StructField("is_non_perception_demotion", IntegerType(), True),
    StructField("is_intended_manual_demotion", IntegerType(), True),
    StructField("is_product_demotion", IntegerType(), True),
    StructField("is_customer_demotion", IntegerType(), True),
    StructField("is_triaged_demotion", IntegerType(), True),
    StructField("is_verified_with_demotion_context", IntegerType(), True),
    StructField("is_rtf_demotion", IntegerType(), True),
    StructField("is_verified_demotion", IntegerType(), True),
    StructField("triaged_halt_code_name", StringType(), True),
    StructField("triaged_halt_code_description", StringType(), True),
    StructField("enable_point_cloud_processor", BooleanType(), True),
    StructField("genos_version", StringType(), True),
    StructField("computed_implement_path_position_type_text", StringType(), True),
])

# COMMAND ----------

def cast_airtable_format_to_databricks(records):
    def convert_to_int_or_none(value):
        if value is not None:
            return int(value)
        return None

    list_of_rows = []
    for record in records:
        row_data = Row(
            System=record.get('fields').get('system') if "System" not in record.get('fields') else record.get(
                'fields').get("System"),
            VIN=record.get('fields').get('vin') if "VIN" not in record.get('fields') else record.get('fields').get(
                "VIN"),
            MachinePIN_masked=hash_vin(record.get('fields').get('vin')) if "VIN" not in record.get('fields') else hash_vin(
                record.get('fields').get("VIN")),
            Vehicle=record.get('fields').get('vehicle') if "Vehicle" not in record.get('fields') else record.get(
                'fields').get("Vehicle"),
            Bundle=record.get('fields').get('bundle') if "Bundle" not in record.get('fields') else record.get(
                'fields').get("Bundle"),
            Demotions=convert_to_int_or_none(record.get('fields').get('demotions')),
            Stops=convert_to_int_or_none(record.get('fields').get('stops')),
            halt_code=record.get('fields').get('halt_code'),
            halt_name=record.get('fields').get('halt_name'),
            halt_description=record.get('fields').get('halt_description'),
            demotion_occurrence=record.get('fields').get('demotion_occurrence'),
            ec_tags=record.get('fields').get('ec_tags'),
            ec_ticket_url=record.get('fields').get('ec_ticket_url'),
            formant_url=record.get('fields').get('formant_url'),
            prior_timestamp=parse_datetime(record.get('fields').get('prior_timestamp')),
            last_activation_time=parse_datetime(record.get('fields').get('last_activation_time')),
            from_state=record.get('fields').get('from_state'),
            to_state=record.get('fields').get('to_state'),
            SparkAI_URL=record.get('fields').get('sparkai_url'),
            Foxglove_URL=record.get('fields').get('foxglove_url'),
            timestamp_diff_from_last_activation=record.get('fields').get('timestamp_diff_from_last_activation'),
            minutes_from_activation=parse_float(record.get('fields').get('minutes_from_activation')),
            seconds_from_activation=parse_int(record.get('fields').get('seconds_from_activation')),
            ID=record.get('fields').get('id'),
            Airtable_ID=record.get('id'),
            hours_from_activation=parse_float(record.get('fields').get('hours_from_activation')),
            Timestamp_utc=parse_datetime(
                record.get('fields').get('timestamp_utc')) if "Timestamp UTC" not in record.get(
                'fields') else parse_datetime(record.get('fields').get('Timestamp UTC')),
            Timestamp=parse_datetime(record.get('fields').get('timestamp')),
            county=record.get('fields').get('county'),
            state=record.get('fields').get('state'),
            country=record.get('fields').get('country'),
            operation_time=record.get('fields').get('operation_time'),
            demotion_reason=demotion_reason_mapping.get(record.get('fields').get('Demotion Reason')[0]) if record.get('fields').get('Demotion Reason') else None,
            triage_status=record.get('fields').get('Triage Status'),
            demotion_machine_behavior=record.get('fields').get('(Archived) Demotion Machine Behavior')[0] if record.get('fields').get('(Archived) Demotion Machine Behavior') else None,
            triage_review_complete=record.get('fields').get('triage_review_complete'),
            longitude=record.get('fields').get('longitude'),
            latitude=record.get('fields').get('latitude'),
            spark_program_name=record.get('fields').get('spark_program_name'),
            spark_response=record.get('fields').get('spark_response'),
            spark_original_annotation_0_label=record.get('fields').get('spark_original_annotation_0_label'),
            spark_annotation_0_label=record.get('fields').get('spark_annotation_0_label'),
            spark_camera_name=record.get('fields').get('spark_camera_name'),
            map_presigned_url=record.get('fields').get('map_presigned_url'),
            halt_code_investigation_guide=record.get('fields').get('Halt Code Investigation Guide')[0] if record.get('fields').get('Halt Code Investigation Guide') else None,
            operator_error_or_misuse=record.get('fields').get('Operator Error or Misuse'),
            headlands_vs_interior=record.get('fields').get('Headlands vs Interior'),
            headlands_turn=record.get('fields').get('Headlands Turn'),
            vehicle_or_object_outside_field=record.get('fields').get('Vehicle/Object Outside Field'),
            vehicle_parked_or_driving=record.get('fields').get('Vehicle Parked/Driving'),
            vehicle_on_or_off_road=record.get('fields').get('Vehicle On/Off Road'),
            bug_or_intended_behavior=record.get('fields').get('Bug or Intended Behavior'),
            confirmed_jrm_link=jira_issue_mapping[record.get('fields').get('Confirmed JRM Link')[0]] if record.get('fields').get('Confirmed JRM Link') else None,
            triage_activities_complete=record.get('fields').get('Triage Activities Complete'),
            confirmed_jira_url=record.get('fields').get('Confirmed Jira URL'),
            triage_reviewer=reviewer_name_mapping[record.get('fields').get('Reviewer')[0]] if record.get('fields').get('Reviewer') else None,
            triage_comments=record.get('fields').get('Triage Comments - If questions/unusual observations during Triage'),
            in_scope=record.get('fields').get('In Scope'),
            manual_demotion_masking=record.get('fields').get('Manual Demotion Masking'),
            secondary_demotion=swapped_halt_code_records_mapping.get(record.get('fields').get('Secondary Demotion Manual')[0]) if record.get('fields').get('Secondary Demotion Manual') else None,
            secondary_demotion_reason=demotion_reason_mapping.get(record.get('fields').get('Secondary Demotion Reason')[0]) if record.get('fields').get('Secondary Demotion Reason') else None,
            confirmed_demotion_type=record.get('fields').get('Confirmed Demotion Type'),
            manned_type=record.get('fields').get('Manned Type'),
            SparkAI_query_URL=record.get('fields').get('SparkAI Query URL'),
            other_sparkai_url=record.get('fields').get('Other SparkAI URL'),
            secondary_demotion_auto=record.get('fields').get('Secondary Demotion Auto'),
            no_of_spark_engagements=record.get('fields').get('No of Spark Engagements'),
            prev_stop_halt_code=swapped_halt_code_records_mapping.get(record.get('fields').get('Preceding Stop Code')[0]) if record.get('fields').get('Preceding Stop Code') else None,
            main_demotion_code=swapped_halt_code_records_mapping.get(record.get('fields').get('MAIN Demotion Code')[0]) if record.get('fields').get('MAIN Demotion Code') else None,
            main_demotion_reason=demotion_reason_mapping.get(record.get('fields').get('MAIN Demotion Reason')[0]) if record.get('fields').get('MAIN Demotion Reason') else None,
            investigation_complete=record.get('fields').get('Investigation Complete'),
            Preceding_Stop_Code=swapped_halt_code_records_mapping.get(record.get('fields').get('Preceding Stop Code')[0]) if record.get('fields').get('Preceding Stop Code') else None,
            Preceding_Stop_Code_Reason=demotion_reason_mapping.get(record.get('fields').get('Preceding Stop Code Reason')[0]) if record.get('fields').get('Preceding Stop Code Reason') else None,
            implement_path_position_type_text=record.get('fields').get('Implement Path Position Type Text'),
            human_detection_details=record.get('fields').get('Human Detection Details'),
            spark_multiurl_pkey_uid=record.get('fields').get('spark_multiurl_pkey_uid'),
            aletheia_image=record.get('fields').get('aletheia_image'),
            secondary_demotion_array=record.get('fields').get('secondary_demotion_array'),
            stop_interrupted_by_manual_demotion=record.get('fields').get('stop_interrupted_by_manual_demotion'),
            other_spark_reasons=record.get('fields').get('other_spark_reasons'),
            spark_window_search_time=record.get('fields').get('spark_window_search_time'),
            camera_angle_y_pos=record.get('fields').get('camera_angle_y_pos'),
            camera_angle_x_pos=record.get('fields').get('camera_angle_x_pos'),
            spark_uuid=record.get('fields').get('spark_uuid'),
            spark_timestamp=record.get('fields').get('spark_timestamp'),
            spark_machine_id=record.get('fields').get('spark_machine_id'),
            spark_token=record.get('fields').get('spark_token'),
            spark_date_closed=record.get('fields').get('spark_date_closed'),
            spark_date_created=record.get('fields').get('spark_date_created'),
            spark_state=record.get('fields').get('spark_state'),
            billable_org_name=record.get('fields').get('billable_org_name'),
            client_name=record.get('fields').get('client_name'),
            field_name=record.get('fields').get('field_name'),
            farm_name=record.get('fields').get('farm_name'),
            org_id=record.get('fields').get('org_id'),
            field_operation_guid=record.get('fields').get('field_operation_guid'),
            crop_id=record.get('fields').get('crop_id'),
            client_guid=record.get('fields').get('client_guid'),
            sparkai_program=record.get('fields').get('sparkai_program'),
            machine_name=record.get('fields').get('machine_name'),
            field_guid=record.get('fields').get('field_guid'),
            farm_guid=record.get('fields').get('farm_guid'),
            is_system_triggered_demotion=record.get('fields').get('is_system_triggered_demotion'),
            is_human_triggered_demotion=record.get('fields').get('is_human_triggered_demotion'),
            is_unintended_perception_demotion=record.get('fields').get('is_unintended_perception_demotion'),
            is_intended_perception_demotion=record.get('fields').get('is_intended_perception_demotion'),
            is_non_perception_demotion=record.get('fields').get('is_non_perception_demotion'),
            is_intended_manual_demotion=record.get('fields').get('is_intended_manual_demotion'),
            is_product_demotion=record.get('fields').get('is_product_demotion'),
            is_customer_demotion=record.get('fields').get('is_customer_demotion'),
            is_triaged_demotion=record.get('fields').get('is_triaged_demotion'),
            is_verified_with_demotion_context=record.get('fields').get('is_verified_with_demotion_context'),
            is_rtf_demotion=record.get('fields').get('is_rtf_demotion'),
            is_verified_demotion=record.get('fields').get('is_verified_demotion'),
            triaged_halt_code_name=record.get('fields').get('triaged_halt_code_name'),
            triaged_halt_code_description=record.get('fields').get('triaged_halt_code_description'),
            enable_point_cloud_processor=record.get('fields').get('enable_point_cloud_processor'),
            genos_version=record.get('fields').get('genos_version'),
            computed_implement_path_position_type_text=record.get('fields').get('Computed Implement Path Position Type Text'),
        )
        list_of_rows.append(row_data)
                
    return spark.createDataFrame(list_of_rows, schema=schema)

# COMMAND ----------


def save_to_demotion_context(airtable_rows, new_demotion_updates):
    # Convert airtable rows to Row class
    airtable_df = cast_airtable_format_to_databricks(airtable_rows.get("records"))

    demotion_records = [{"fields": row.asDict()} for row in new_demotion_updates.collect()]
    new_demotion_records = cast_airtable_format_to_databricks(demotion_records)

    # Join full_df with airtable_df and select from airtable neccessary columns value
    result_df = (
        new_demotion_records.alias("new_demotion_records")
        .drop("Airtable_ID", "demotion_reason", "triage_status", "demotion_machine_behavior")
        .join(
            airtable_df.alias("airtable_df"),
            (
                    (trim(col("new_demotion_records.vin")) == trim(col("airtable_df.VIN"))) &
                    (
                            unix_timestamp(col("new_demotion_records.timestamp_utc"))
                            == unix_timestamp(col("airtable_df.Timestamp_utc"))
                    ) &
                    (col("new_demotion_records.demotions") == 1) &
                    (col("new_demotion_records.halt_code") != "0.0")
            ),
            "left")
        .select(
            "new_demotion_records.*",
            "airtable_df.Airtable_ID",
            "airtable_df.demotion_reason",
            "airtable_df.triage_status",
            "airtable_df.demotion_machine_behavior",
        )
    )

    result_df = result_df.withColumn("created_at", current_timestamp()).withColumn("updated_at", current_timestamp())
    result_df.write.format("delta").mode("append").saveAsTable(DEMOTION_CONTEXT_TABLE)


# COMMAND ----------

def merge_to_demotion_context(temp_table_name):
    spark.sql(f"""
    MERGE INTO {DEMOTION_CONTEXT_TABLE} AS target
        USING {TEMP_TABLES_PATH}{temp_table_name} AS source
        ON target.Airtable_ID = source.Airtable_ID
        WHEN MATCHED AND (
            target.System IS DISTINCT FROM source.System OR
            target.VIN IS DISTINCT FROM source.VIN OR
            target.MachinePIN_masked IS DISTINCT FROM source.MachinePIN_masked OR
            target.Vehicle IS DISTINCT FROM source.Vehicle OR
            target.Bundle IS DISTINCT FROM source.Bundle OR
            target.Demotions IS DISTINCT FROM source.Demotions OR
            target.Stops IS DISTINCT FROM source.Stops OR
            target.halt_code IS DISTINCT FROM source.halt_code OR
            target.halt_name IS DISTINCT FROM source.halt_name OR
            target.halt_description IS DISTINCT FROM source.halt_description OR
            target.demotion_occurrence IS DISTINCT FROM source.demotion_occurrence OR
            target.ec_tags IS DISTINCT FROM source.ec_tags OR
            target.ec_ticket_url IS DISTINCT FROM source.ec_ticket_url OR
            target.formant_url IS DISTINCT FROM source.formant_url OR
            target.prior_timestamp IS DISTINCT FROM source.prior_timestamp OR
            target.last_activation_time IS DISTINCT FROM source.last_activation_time OR
            target.from_state IS DISTINCT FROM source.from_state OR
            target.to_state IS DISTINCT FROM source.to_state OR
            target.InOrbit_URL IS DISTINCT FROM source.InOrbit_URL OR
            target.SparkAI_URL IS DISTINCT FROM source.SparkAI_URL OR
            target.Foxglove_URL IS DISTINCT FROM source.Foxglove_URL OR
            target.timestamp_diff_from_last_activation IS DISTINCT FROM source.timestamp_diff_from_last_activation OR
            target.minutes_from_activation IS DISTINCT FROM source.minutes_from_activation OR
            target.seconds_from_activation IS DISTINCT FROM source.seconds_from_activation OR
            target.ID IS DISTINCT FROM source.ID OR
            target.Airtable_ID IS DISTINCT FROM source.Airtable_ID OR
            target.hours_from_activation IS DISTINCT FROM source.hours_from_activation OR
            target.Timestamp IS DISTINCT FROM source.Timestamp OR
            target.county IS DISTINCT FROM source.county OR
            target.state IS DISTINCT FROM source.state OR
            target.country IS DISTINCT FROM source.country OR
            target.operation_time IS DISTINCT FROM source.operation_time OR
            target.demotion_reason IS DISTINCT FROM source.demotion_reason OR
            target.triage_status IS DISTINCT FROM source.triage_status OR
            target.demotion_machine_behavior IS DISTINCT FROM source.demotion_machine_behavior OR
            target.odd_assessment IS DISTINCT FROM source.odd_assessment OR
            target.triage_review_complete IS DISTINCT FROM source.triage_review_complete OR
            target.longitude IS DISTINCT FROM source.longitude OR
            target.latitude IS DISTINCT FROM source.latitude OR
            target.spark_program_name IS DISTINCT FROM source.spark_program_name OR
            target.spark_response IS DISTINCT FROM source.spark_response OR
            target.spark_original_annotation_0_label IS DISTINCT FROM source.spark_original_annotation_0_label OR
            target.spark_annotation_0_label IS DISTINCT FROM source.spark_annotation_0_label OR
            target.spark_camera_name IS DISTINCT FROM source.spark_camera_name OR
            target.map_presigned_url IS DISTINCT FROM source.map_presigned_url OR
            target.halt_code_investigation_guide IS DISTINCT FROM source.halt_code_investigation_guide OR
            target.operator_error_or_misuse IS DISTINCT FROM source.operator_error_or_misuse OR
            target.headlands_vs_interior IS DISTINCT FROM source.headlands_vs_interior OR
            target.headlands_turn IS DISTINCT FROM source.headlands_turn OR
            target.vehicle_or_object_outside_field IS DISTINCT FROM source.vehicle_or_object_outside_field OR
            target.vehicle_parked_or_driving IS DISTINCT FROM source.vehicle_parked_or_driving OR
            target.vehicle_on_or_off_road IS DISTINCT FROM source.vehicle_on_or_off_road OR
            target.bug_or_intended_behavior IS DISTINCT FROM source.bug_or_intended_behavior OR
            target.confirmed_jrm_link IS DISTINCT FROM source.confirmed_jrm_link OR
            target.triage_activities_complete IS DISTINCT FROM source.triage_activities_complete OR
            target.confirmed_jira_url IS DISTINCT FROM source.confirmed_jira_url OR
            target.triage_reviewer IS DISTINCT FROM source.triage_reviewer OR
            target.triage_comments IS DISTINCT FROM source.triage_comments OR
            target.in_scope IS DISTINCT FROM source.in_scope OR
            target.manual_demotion_masking IS DISTINCT FROM source.manual_demotion_masking OR
            target.secondary_demotion IS DISTINCT FROM source.secondary_demotion OR
            target.secondary_demotion_reason IS DISTINCT FROM source.secondary_demotion_reason OR
            target.MTBI_bucket IS DISTINCT FROM source.MTBI_bucket OR
            target.confirmed_demotion_type IS DISTINCT FROM source.confirmed_demotion_type OR
            target.manned_type IS DISTINCT FROM source.manned_type OR
            target.SparkAI_query_URL IS DISTINCT FROM source.SparkAI_query_URL OR
            target.other_sparkai_url IS DISTINCT FROM source.other_sparkai_url OR
            target.secondary_demotion_auto IS DISTINCT FROM source.secondary_demotion_auto OR
            target.no_of_spark_engagements IS DISTINCT FROM source.no_of_spark_engagements OR
            target.prev_stop_halt_code IS DISTINCT FROM source.prev_stop_halt_code OR
            target.prev_stop_timestamp IS DISTINCT FROM source.prev_stop_timestamp OR
            target.main_demotion_code IS DISTINCT FROM source.main_demotion_code OR
            target.main_demotion_reason IS DISTINCT FROM source.main_demotion_reason OR
            target.investigation_complete IS DISTINCT FROM source.investigation_complete OR
            target.seconds_in_autonomy_time_before_demotion IS DISTINCT FROM source.seconds_in_autonomy_time_before_demotion OR
            target.Preceding_Stop_Code IS DISTINCT FROM source.Preceding_Stop_Code OR
            target.Preceding_Stop_Code_Error IS DISTINCT FROM source.Preceding_Stop_Code_Error OR
            target.Preceding_Stop_Datetime_UTC IS DISTINCT FROM source.Preceding_Stop_Datetime_UTC OR
            target.Preceding_Stop_Code_Reason IS DISTINCT FROM source.Preceding_Stop_Code_Reason OR
            target.implement_path_position_heading IS DISTINCT FROM source.implement_path_position_heading OR
            target.implement_path_position_direction IS DISTINCT FROM source.implement_path_position_direction OR
            target.implement_path_position_type IS DISTINCT FROM source.implement_path_position_type OR
            target.implement_path_position_type_text IS DISTINCT FROM source.implement_path_position_type_text OR
            target.computed_implement_path_position_type_text IS DISTINCT FROM source.computed_implement_path_position_type_text OR
            target.genos_version IS DISTINCT FROM source.genos_version OR
            target.seconds_in_state_5_and_6 IS DISTINCT FROM source.seconds_in_state_5_and_6
    ) THEN
        UPDATE SET
            target.System = CASE WHEN source.System IS NOT NULL THEN source.System ELSE target.System END,
            target.VIN = CASE WHEN source.VIN IS NOT NULL THEN source.VIN ELSE target.VIN END,
            target.MachinePIN_masked = CASE WHEN source.MachinePIN_masked IS NOT NULL THEN source.MachinePIN_masked ELSE target.MachinePIN_masked END,
            target.Vehicle = CASE WHEN source.Vehicle IS NOT NULL THEN source.Vehicle ELSE target.Vehicle END,
            target.Bundle = CASE WHEN source.Bundle IS NOT NULL THEN source.Bundle ELSE target.Bundle END,
            target.Demotions = CASE WHEN source.Demotions IS NOT NULL THEN source.Demotions ELSE target.Demotions END,
            target.Stops = CASE WHEN source.Stops IS NOT NULL THEN source.Stops ELSE target.Stops END,
            target.halt_code = CASE WHEN source.halt_code IS NOT NULL THEN source.halt_code ELSE target.halt_code END,
            target.halt_name = CASE WHEN source.halt_name IS NOT NULL THEN source.halt_name ELSE target.halt_name END,
            target.halt_description = CASE WHEN source.halt_description IS NOT NULL THEN source.halt_description ELSE target.halt_description END,
            target.demotion_occurrence = CASE WHEN source.demotion_occurrence IS NOT NULL THEN source.demotion_occurrence ELSE target.demotion_occurrence END,
            target.ec_tags = CASE WHEN source.ec_tags IS NOT NULL THEN source.ec_tags ELSE target.ec_tags END,
            target.ec_ticket_url = CASE WHEN source.ec_ticket_url IS NOT NULL THEN source.ec_ticket_url ELSE target.ec_ticket_url END,
            target.formant_url = CASE WHEN source.formant_url IS NOT NULL THEN source.formant_url ELSE target.formant_url END,
            target.prior_timestamp = CASE WHEN source.prior_timestamp IS NOT NULL THEN source.prior_timestamp ELSE target.prior_timestamp END,
            target.last_activation_time = CASE WHEN source.last_activation_time IS NOT NULL THEN source.last_activation_time ELSE target.last_activation_time END,
            target.from_state = CASE WHEN source.from_state IS NOT NULL THEN source.from_state ELSE target.from_state END,
            target.to_state = CASE WHEN source.to_state IS NOT NULL THEN source.to_state ELSE target.to_state END,
            target.InOrbit_URL = CASE WHEN source.InOrbit_URL IS NOT NULL THEN source.InOrbit_URL ELSE target.InOrbit_URL END,
            target.SparkAI_URL = CASE WHEN source.SparkAI_URL IS NOT NULL THEN source.SparkAI_URL ELSE target.SparkAI_URL END,
            target.Foxglove_URL = CASE WHEN source.Foxglove_URL IS NOT NULL THEN source.Foxglove_URL ELSE target.Foxglove_URL END,
            target.timestamp_diff_from_last_activation = CASE WHEN source.timestamp_diff_from_last_activation IS NOT NULL THEN source.timestamp_diff_from_last_activation ELSE target.timestamp_diff_from_last_activation END,
            target.minutes_from_activation = CASE WHEN source.minutes_from_activation IS NOT NULL THEN source.minutes_from_activation ELSE target.minutes_from_activation END,
            target.seconds_from_activation = CASE WHEN source.seconds_from_activation IS NOT NULL THEN source.seconds_from_activation ELSE target.seconds_from_activation END,
            target.ID = CASE WHEN source.ID IS NOT NULL THEN source.ID ELSE target.ID END,
            target.Airtable_ID = CASE WHEN source.Airtable_ID IS NOT NULL THEN source.Airtable_ID ELSE target.Airtable_ID END,
            target.hours_from_activation = CASE WHEN source.hours_from_activation IS NOT NULL THEN source.hours_from_activation ELSE target.hours_from_activation END,
            target.Timestamp = CASE WHEN source.Timestamp IS NOT NULL THEN source.Timestamp ELSE target.Timestamp END,
            target.county = CASE WHEN source.county IS NOT NULL THEN source.county ELSE target.county END,
            target.state = CASE WHEN source.state IS NOT NULL THEN source.state ELSE target.state END,
            target.country = CASE WHEN source.country IS NOT NULL THEN source.country ELSE target.country END,
            target.operation_time = CASE WHEN source.operation_time IS NOT NULL THEN source.operation_time ELSE target.operation_time END,
            target.demotion_reason = CASE WHEN source.demotion_reason IS NOT NULL THEN source.demotion_reason ELSE target.demotion_reason END,
            target.triage_status = CASE WHEN source.triage_status IS NOT NULL THEN source.triage_status ELSE target.triage_status END,
            target.demotion_machine_behavior = CASE WHEN source.demotion_machine_behavior IS NOT NULL THEN source.demotion_machine_behavior ELSE target.demotion_machine_behavior END,
            target.odd_assessment = CASE WHEN source.odd_assessment IS NOT NULL THEN source.odd_assessment ELSE target.odd_assessment END,
            target.triage_review_complete = CASE WHEN source.triage_review_complete IS NOT NULL THEN source.triage_review_complete ELSE target.triage_review_complete END,
            target.longitude = CASE WHEN source.longitude IS NOT NULL THEN source.longitude ELSE target.longitude END,
            target.latitude = CASE WHEN source.latitude IS NOT NULL THEN source.latitude ELSE target.latitude END,
            target.spark_program_name = CASE WHEN source.spark_program_name IS NOT NULL THEN source.spark_program_name ELSE target.spark_program_name END,
            target.spark_response = CASE WHEN source.spark_response IS NOT NULL THEN source.spark_response ELSE target.spark_response END,
            target.spark_original_annotation_0_label = CASE WHEN source.spark_original_annotation_0_label IS NOT NULL THEN source.spark_original_annotation_0_label ELSE target.spark_original_annotation_0_label END,
            target.spark_annotation_0_label = CASE WHEN source.spark_annotation_0_label IS NOT NULL THEN source.spark_annotation_0_label ELSE target.spark_annotation_0_label END,
            target.spark_camera_name = CASE WHEN source.spark_camera_name IS NOT NULL THEN source.spark_camera_name ELSE target.spark_camera_name END,
            target.map_presigned_url = CASE WHEN source.map_presigned_url IS NOT NULL THEN source.map_presigned_url ELSE target.map_presigned_url END,
            target.halt_code_investigation_guide = CASE WHEN source.halt_code_investigation_guide IS NOT NULL THEN source.halt_code_investigation_guide ELSE target.halt_code_investigation_guide END,
            target.operator_error_or_misuse = CASE WHEN source.operator_error_or_misuse IS NOT NULL THEN source.operator_error_or_misuse ELSE target.operator_error_or_misuse END,
            target.headlands_vs_interior = CASE WHEN source.headlands_vs_interior IS NOT NULL THEN source.headlands_vs_interior ELSE target.headlands_vs_interior END,
            target.headlands_turn = CASE WHEN source.headlands_turn IS NOT NULL THEN source.headlands_turn ELSE target.headlands_turn END,
            target.vehicle_or_object_outside_field = CASE WHEN source.vehicle_or_object_outside_field IS NOT NULL THEN source.vehicle_or_object_outside_field ELSE target.vehicle_or_object_outside_field END,
            target.vehicle_parked_or_driving = CASE WHEN source.vehicle_parked_or_driving IS NOT NULL THEN source.vehicle_parked_or_driving ELSE target.vehicle_parked_or_driving END,
            target.vehicle_on_or_off_road = CASE WHEN source.vehicle_on_or_off_road IS NOT NULL THEN source.vehicle_on_or_off_road ELSE target.vehicle_on_or_off_road END,
            target.bug_or_intended_behavior = CASE WHEN source.bug_or_intended_behavior IS NOT NULL THEN source.bug_or_intended_behavior ELSE target.bug_or_intended_behavior END,
            target.confirmed_jrm_link = CASE WHEN source.confirmed_jrm_link IS NOT NULL THEN source.confirmed_jrm_link ELSE target.confirmed_jrm_link END,
            target.triage_activities_complete = CASE WHEN source.triage_activities_complete IS NOT NULL THEN source.triage_activities_complete ELSE target.triage_activities_complete END,
            target.confirmed_jira_url = CASE WHEN source.confirmed_jira_url IS NOT NULL THEN source.confirmed_jira_url ELSE target.confirmed_jira_url END,
            target.triage_reviewer = CASE WHEN source.triage_reviewer IS NOT NULL THEN source.triage_reviewer ELSE target.triage_reviewer END,
            target.triage_comments = CASE WHEN source.triage_comments IS NOT NULL THEN source.triage_comments ELSE target.triage_comments END,
            target.in_scope = CASE WHEN source.in_scope IS NOT NULL THEN source.in_scope ELSE target.in_scope END,
            target.manual_demotion_masking = CASE WHEN source.manual_demotion_masking IS NOT NULL THEN source.manual_demotion_masking ELSE target.manual_demotion_masking END,
            target.secondary_demotion = CASE WHEN source.secondary_demotion IS NOT NULL THEN source.secondary_demotion ELSE target.secondary_demotion END,
            target.secondary_demotion_reason = CASE WHEN source.secondary_demotion_reason IS NOT NULL THEN source.secondary_demotion_reason ELSE target.secondary_demotion_reason END,
            target.MTBI_bucket = CASE WHEN source.MTBI_bucket IS NOT NULL THEN source.MTBI_bucket ELSE target.MTBI_bucket END,
            target.confirmed_demotion_type = CASE WHEN source.confirmed_demotion_type IS NOT NULL THEN source.confirmed_demotion_type ELSE target.confirmed_demotion_type END,
            target.manned_type = CASE WHEN source.manned_type IS NOT NULL THEN source.manned_type ELSE target.manned_type END,
            target.SparkAI_query_URL = CASE WHEN source.SparkAI_query_URL IS NOT NULL THEN source.SparkAI_query_URL ELSE target.SparkAI_query_URL END,
            target.other_sparkai_url = CASE WHEN source.other_sparkai_url IS NOT NULL THEN source.other_sparkai_url ELSE target.other_sparkai_url END,
            target.secondary_demotion_auto = CASE WHEN source.secondary_demotion_auto IS NOT NULL THEN source.secondary_demotion_auto ELSE target.secondary_demotion_auto END,
            target.no_of_spark_engagements = CASE WHEN source.no_of_spark_engagements IS NOT NULL THEN source.no_of_spark_engagements ELSE target.no_of_spark_engagements END,
            target.prev_stop_halt_code = CASE WHEN source.prev_stop_halt_code IS NOT NULL THEN source.prev_stop_halt_code ELSE target.prev_stop_halt_code END,
            target.prev_stop_timestamp = CASE WHEN source.prev_stop_timestamp IS NOT NULL THEN source.prev_stop_timestamp ELSE target.prev_stop_timestamp END,
            target.main_demotion_code = CASE WHEN source.main_demotion_code IS NOT NULL THEN source.main_demotion_code ELSE target.main_demotion_code END,
            target.main_demotion_reason = CASE WHEN source.main_demotion_reason IS NOT NULL THEN source.main_demotion_reason ELSE target.main_demotion_reason END,
            target.investigation_complete = CASE WHEN source.investigation_complete IS NOT NULL THEN source.investigation_complete ELSE target.investigation_complete END,
            target.seconds_in_autonomy_time_before_demotion = CASE WHEN source.seconds_in_autonomy_time_before_demotion IS NOT NULL THEN source.seconds_in_autonomy_time_before_demotion ELSE target.seconds_in_autonomy_time_before_demotion END,
            target.Preceding_Stop_Code = CASE WHEN source.Preceding_Stop_Code IS NOT NULL THEN source.Preceding_Stop_Code ELSE target.Preceding_Stop_Code END,
            target.Preceding_Stop_Code_Error = CASE WHEN source.Preceding_Stop_Code_Error IS NOT NULL THEN source.Preceding_Stop_Code_Error ELSE target.Preceding_Stop_Code_Error END,
            target.Preceding_Stop_Datetime_UTC = CASE WHEN source.Preceding_Stop_Datetime_UTC IS NOT NULL THEN source.Preceding_Stop_Datetime_UTC ELSE target.Preceding_Stop_Datetime_UTC END,
            target.Preceding_Stop_Code_Reason = CASE WHEN source.Preceding_Stop_Code_Reason IS NOT NULL THEN source.Preceding_Stop_Code_Reason ELSE target.Preceding_Stop_Code_Reason END,
            target.implement_path_position_type = CASE WHEN source.implement_path_position_type IS NOT NULL THEN source.implement_path_position_type ELSE target.implement_path_position_type END,
            target.implement_path_position_type_text = CASE WHEN source.implement_path_position_type_text IS NOT NULL THEN source.implement_path_position_type_text ELSE target.implement_path_position_type_text END,
            target.implement_path_position_heading = CASE WHEN source.implement_path_position_heading IS NOT NULL THEN source.implement_path_position_heading ELSE target.implement_path_position_heading END,
            target.implement_path_position_direction = CASE WHEN source.implement_path_position_direction IS NOT NULL THEN source.implement_path_position_direction ELSE target.implement_path_position_direction END,
            target.computed_implement_path_position_type_text = CASE WHEN source.computed_implement_path_position_type_text IS NOT NULL THEN source.computed_implement_path_position_type_text ELSE target.computed_implement_path_position_type_text END,
            target.genos_version = CASE WHEN source.genos_version IS NOT NULL THEN source.genos_version ELSE target.genos_version END,
            target.seconds_in_state_5_and_6 = CASE WHEN source.seconds_in_state_5_and_6 IS NOT NULL THEN source.seconds_in_state_5_and_6 ELSE target.seconds_in_state_5_and_6 END,
            target.updated_at = current_timestamp()
    """)

# COMMAND ----------

# MAGIC %md
# MAGIC Get record by VIN and timestamp (except seonds)

# COMMAND ----------

def get_demotion_context_record_fuzzy(vin, timestamp):
    # Truncate seconds and microseconds from the input timestamp
    print(repr(timestamp))
    truncated_timestamp = timestamp.replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%S.%f')
    print(f'Trying to get demotion context for VIN {vin} - {truncated_timestamp}.')
    
    return spark.sql(f"""
        SELECT *
        FROM {DEMOTION_CONTEXT_TABLE}
        WHERE VIN = '{vin}'
        AND date_trunc('second', Timestamp_utc) = '{truncated_timestamp}'
    """)

# COMMAND ----------

# MAGIC %md
# MAGIC Function to upload data to temp table.

# COMMAND ----------

def upload_to_temp_table(data, temp_table_name: str):
    def parse_datetime(date_str):
        if date_str is None:
            return None
        if isinstance(date_str, str):
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_str
    records_from_airtable = data
    rows = []

    def half_name_parse(value):
        halt_code_linked = value.get('fields').get('Halt Code - Linked')
        
        if halt_code_linked is not None:
            result = code_name_records_mapping.get(halt_code_linked[0])
            return result
            
        else:
            return None
    num = 0
    print("Length of the records_from_airtable : ", len(records_from_airtable))
    for record in records_from_airtable:
        num+=1
        print(f'record nr {num}')
        row_data = Row(
            System=record.get('fields').get('System'),
            VIN=record.get('fields').get('VIN'),
            MachinePIN_masked=hash_vin(record.get('fields').get('VIN')),
            Vehicle=record.get('fields').get('Vehicle'),
            Bundle=record.get('fields').get('Bundle'),
            Demotions=record.get('fields').get('demotions'),
            Stops=record.get('fields').get('Stops'),
            halt_code=record.get('fields').get('Halt Code - Import'),
            halt_name=half_name_parse(record),
            halt_description=record.get('fields').get('Halt Description')[0] if record.get('fields').get('Halt Description') else None,
            demotion_occurrence=record.get('fields').get('Demotion Occurrence'),
            ec_tags=record.get('fields').get('ec_tags'),
            ec_ticket_url=record.get('fields').get('ec_ticket_url'),
            formant_url=record.get('fields').get('ec_ticket_url'),
            prior_timestamp=parse_datetime(record.get('fields').get('Timestamp_utc')),
            last_activation_time=parse_datetime(record.get('fields').get('Timestamp_utc')),
            from_state=record.get('fields').get('From State'),
            to_state=record.get('fields').get('To State'),
            SparkAI_URL=record.get('fields').get('Spark URL'),
            Foxglove_URL=record.get('fields').get('Foxglove URL'),
            timestamp_diff_from_last_activation=record.get('fields').get('timestamp_diff_from_last_activation'),
            minutes_from_activation=record.get('fields').get('minutes_from_activation'),
            seconds_from_activation=record.get('fields').get('seconds_from_activation'),
            ID=record.get('fields').get('ID'),
            Airtable_ID=record.get('id'),
            hours_from_activation=record.get('fields').get('hours_from_activation'),
            Timestamp_utc=parse_datetime(record.get('fields').get('Timestamp UTC')),
            Timestamp=parse_datetime(record.get('fields').get('Timestamp')),
            county=record.get('fields').get('county'), 
            state=record.get('fields').get('state'), 
            country=record.get('fields').get('country'), 
            operation_time=record.get('fields').get('operation_time'), 
            demotion_reason=demotion_reason_mapping[record.get('fields').get('Demotion Reason')[0]] if record.get('fields').get('Demotion Reason') else None,
            triage_status=record.get('fields').get('Triage Status'),  
            demotion_machine_behavior=record.get('fields').get('(Archived) Demotion Machine Behavior')[0] if record.get('fields').get('(Archived) Demotion Machine Behavior') else [],
            triage_review_complete=record.get('fields').get('Triage Review Complete'),
            longitude=record.get('fields').get('longitude'),
            latitude=record.get('fields').get('latitude'),
            spark_program_name=record.get('fields').get('spark_program_name'),
            spark_response=record.get('fields').get('spark_response'),
            spark_original_annotation_0_label=record.get('fields').get('spark_original_annotation_0_label'),
            spark_annotation_0_label=record.get('fields').get('spark_annotation_0_label'),
            spark_camera_name=record.get('fields').get('spark_camera_name'),
            map_presigned_url=record.get('fields').get('Map pre-signed URL'),
            halt_code_investigation_guide=record.get('fields').get('Halt Code Investigation Guide')[0] if record.get('fields').get('Halt Code Investigation Guide') else None,
            operator_error_or_misuse=record.get('fields').get('Operator Error or Misuse'),
            headlands_vs_interior=record.get('fields').get('Headlands vs Interior'),
            headlands_turn=record.get('fields').get('Headlands Turn'),
            vehicle_or_object_outside_field=record.get('fields').get('Vehicle/Object Outside Field'),
            vehicle_parked_or_driving=record.get('fields').get('Vehicle Parked/Driving'),
            vehicle_on_or_off_road=record.get('fields').get('Vehicle On/Off Road'),
            bug_or_intended_behavior=record.get('fields').get('Bug or Intended Behavior'),
            confirmed_jrm_link=jira_issue_mapping[record.get('fields').get('Confirmed JRM Link')[0]] if record.get('fields').get('Confirmed JRM Link') else None,
            triage_activities_complete=record.get('fields').get('Triage Activities Complete'),
            confirmed_jira_url=record.get('fields').get('Confirmed Jira URL'),
            triage_reviewer=reviewer_name_mapping[record.get('fields').get('Reviewer')[0]] if record.get('fields').get('Reviewer') else None,
            triage_comments=record.get('fields').get('Triage Comments - If questions/unusual observations during Triage'),
            in_scope=record.get('fields').get('In Scope'),
            manual_demotion_masking=record.get('fields').get('Manual Demotion Masking'),
            secondary_demotion=swapped_halt_code_records_mapping.get(record.get('fields').get('Secondary Demotion Manual')[0]) if record.get('fields').get('Secondary Demotion Manual') else None,
            secondary_demotion_reason=demotion_reason_mapping.get(record.get('fields').get('Secondary Demotion Reason')[0]) if record.get('fields').get('Secondary Demotion Reason') else None,
            confirmed_demotion_type=record.get('fields').get('Confirmed Demotion Type'),
            manned_type=record.get('fields').get('Manned Type'),
            SparkAI_query_URL=record.get('fields').get('SparkAI Query URL'),
            other_sparkai_url=record.get('fields').get('Other SparkAI URL'),
            secondary_demotion_auto=next((key for key, value in halt_code_records_mapping.items() if value == record.get('fields').get('Secondary Demotion Auto')), None),
            no_of_spark_engagements=record.get('fields').get('No of Spark Engagements'),
            prev_stop_halt_code=swapped_halt_code_records_mapping.get(record.get('fields').get('Preceding Stop Code')[0]) if record.get('fields').get('Preceding Stop Code') else None,
            main_demotion_code=swapped_halt_code_records_mapping.get(record.get('fields').get('MAIN Demotion Code')[0]) if record.get('fields').get('MAIN Demotion Code') else None ,
            main_demotion_reason=demotion_reason_mapping.get(record.get('fields').get('MAIN Demotion Reason')[0]) if record.get('fields').get('MAIN Demotion Reason') else None,
            investigation_complete=record.get('fields').get('Investigation Complete'),
            Preceding_Stop_Code=swapped_halt_code_records_mapping.get(record.get('fields').get('Preceding Stop Code')[0]) if record.get('fields').get('Preceding Stop Code') else None,
            Preceding_Stop_Code_Reason=demotion_reason_mapping.get(record.get('fields').get('Preceding Stop Code Reason')[0]) if record.get('fields').get('Preceding Stop Code Reason') else None,
            implement_path_position_type_text=record.get('fields').get('Implement Path Position Type Text'),
            human_detection_details=record.get('fields').get('Human Detection Details'),
            spark_multiurl_pkey_uid=record.get('fields').get('spark_multiurl_pkey_uid'),
            aletheia_image=record.get('fields').get('aletheia_image'),
            secondary_demotion_array=record.get('fields').get('secondary_demotion_array'),
            stop_interrupted_by_manual_demotion=record.get('fields').get('stop_interrupted_by_manual_demotion'),
            other_spark_reasons=record.get('fields').get('other_spark_reasons'),
            spark_window_search_time=record.get('fields').get('spark_window_search_time'),
            camera_angle_y_pos=record.get('fields').get('camera_angle_y_pos'),
            camera_angle_x_pos=record.get('fields').get('camera_angle_x_pos'),
            spark_uuid=record.get('fields').get('spark_uuid'),
            spark_timestamp=record.get('fields').get('spark_timestamp'),
            spark_machine_id=record.get('fields').get('spark_machine_id'),
            spark_token=record.get('fields').get('spark_token'),
            spark_date_closed=record.get('fields').get('spark_date_closed'),
            spark_date_created=record.get('fields').get('spark_date_created'),
            spark_state=record.get('fields').get('spark_state'),
            billable_org_name=record.get('fields').get('billable_org_name'),
            client_name=record.get('fields').get('client_name'),
            field_name=record.get('fields').get('field_name'),
            farm_name=record.get('fields').get('farm_name'),
            org_id=record.get('fields').get('org_id'),
            field_operation_guid=record.get('fields').get('field_operation_guid'),
            crop_id=record.get('fields').get('crop_id'),
            client_guid=record.get('fields').get('client_guid'),
            sparkai_program=record.get('fields').get('sparkai_program'),
            machine_name=record.get('fields').get('machine_name'),
            field_guid=record.get('fields').get('field_guid'),
            farm_guid=record.get('fields').get('farm_guid'),
            is_system_triggered_demotion=record.get('fields').get('is_system_triggered_demotion'),
            is_human_triggered_demotion=record.get('fields').get('is_human_triggered_demotion'),
            is_unintended_perception_demotion=record.get('fields').get('is_unintended_perception_demotion'),
            is_intended_perception_demotion=record.get('fields').get('is_intended_perception_demotion'),
            is_non_perception_demotion=record.get('fields').get('is_non_perception_demotion'),
            is_intended_manual_demotion=record.get('fields').get('is_intended_manual_demotion'),
            is_product_demotion=record.get('fields').get('is_product_demotion'),
            is_customer_demotion=record.get('fields').get('is_customer_demotion'),
            is_triaged_demotion=record.get('fields').get('is_triaged_demotion'),
            is_verified_with_demotion_context=record.get('fields').get('is_verified_with_demotion_context'),
            is_rtf_demotion=record.get('fields').get('is_rtf_demotion'),
            is_verified_demotion=record.get('fields').get('is_verified_demotion'),
            triaged_halt_code_name=record.get('fields').get('triaged_halt_code_name'),
            triaged_halt_code_description=record.get('fields').get('triaged_halt_code_description'),
            enable_point_cloud_processor=record.get('fields').get('enable_point_cloud_processor'),
            genos_version=record.get('fields').get('genos_version'),
            computed_implement_path_position_type_text=record.get('fields').get(
                'Computed Implement Path Position Type Text'),
        )
        rows.append(row_data)

    # Convert Row to DataFrame
    df = spark.createDataFrame(rows, schema=schema)

    df.write.format("delta").mode("append").saveAsTable(f'{TEMP_TABLES_PATH}{temp_table_name}')

    print(f'Uploaded {len(records_from_airtable)} to {temp_table_name}.')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Airtable communication

# COMMAND ----------

# MAGIC %md
# MAGIC Mapping for get the ERC value and ID from the table. ERC value - the first part of halt code.

# COMMAND ----------

def get_halt_code_erc_mapping():
    mapping = {}

    erc_records_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(ERC_TABLE_ID),
        limit=1000
    )

    for erc_record in erc_records_data:
        mapping[erc_record['fields']['ERC']] = erc_record['id']
    return mapping

part_halt_code_erc_mapping = get_halt_code_erc_mapping()

# COMMAND ----------

# MAGIC %md
# MAGIC Function to send data to the Airtable. See [documentation](https://airtable.com/app1jXoB1g13R9iOl/api/docs#curl/table:demotioncontext:create) for further details.

# COMMAND ----------

def send_data_to_airtable(demotions_data):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }

    print(f"Found {demotions_data.count()} rows to upload in Airtable")

    records = [{"fields": row.asDict()} for row in demotions_data.collect()]
    data = {"records": records}
    timestamp_format_airtable = "%Y-%m-%dT%H:%M:%S.%f"

    def create_draft_halt_code(halt_code, extra): # value, field_name):
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json",
        }
        halt_code = str(halt_code)
        halt_code_list = halt_code.split(".")

        payload = [
            {
                "fields": {
                    "ERC": [part_halt_code_erc_mapping[int(halt_code_list[0])]],
                    "Supplement Code": int(halt_code_list[1]),
                    "Demotion Reason_Old": ["recBuyNxcnrReNpJ0"]  # DR-10 Unassigned
                }
            }
        ]

        if extra:
            payload[0]['fields'].update(extra)

        payload = {
            "records": payload,
            "typecast": True,
        }  # Allow creation of new records for single / multiple option fields

        HALT_CODE_TABLE_URL = (
            f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{HALT_CODES_TABLE_ID}"
        )

        response = requests.post(HALT_CODE_TABLE_URL, headers=headers, json=payload)
        print(f"Created new halt code record: {response.json()}")
        halt_code_id = response.json().get("records")[0].get("id")
        halt_code_records_mapping[halt_code] = halt_code_id

        return halt_code_id

    def convert_to_string_or_none(value):
        if value is None or value == "None":
            return None
        return f"{value}"

    def convert_jira(value):
        if value is None or value == "None":
            return "No Jira Ticket Create"
        return f"{value}"

    def convert_pilot_vins(value):
        if value in get_vin_id_mapping:
            return [get_vin_id_mapping[value]]
        else:
            return []

    result_data = {
        "records": [],
    }
    for i in range(0, len(data["records"]), 10):
        payload = {
            "records": [],
            "typecast": True,
            "performUpsert": {
                "fieldsToMergeOn": ["A_UID"]
            },
        }
        for field in data["records"][
            i : i + 10 if i + 10 < len(data["records"]) else len(data["records"])
        ]:
            halt_code_ids = {}
            for halt_code_field in [
                "halt_code",
                "prev_stop_halt_code",
                "secondary_demotion_auto"
            ]:
                halt_code_field_value = field.get("fields").get(halt_code_field)
                if halt_code_field_value:
                    if not isinstance(halt_code_field_value, list):
                        halt_code_field_value = [halt_code_field_value]
                        
                    for halt_code in halt_code_field_value:
                        halt_code_id = halt_code_records_mapping.get(str(halt_code))
                        if halt_code_id is None:
                            extra = {}
                            if halt_code_field == "halt_code":
                                extra = {
                                    "Code Name": field.get('fields').get("halt_name"),
                                    "Description": field.get('fields').get("halt_description")
                                }
                            halt_code_id = create_draft_halt_code(halt_code, extra)
                        
                        if halt_code_field not in halt_code_ids:
                            halt_code_ids[halt_code_field] = []
                        halt_code_ids[halt_code_field].append(halt_code_id)
            
            print("Existing halt codes mapping:")
            print(halt_code_ids)

            record = {
                "fields": {
                    "A_UID": f"{field.get('fields').get('vin')} | {field.get('fields').get('timestamp_utc')}",
                    "Bundle": field.get("fields").get("bundle"),
                    "Demotion Occurrence": field.get("fields").get(
                        "demotion_occurrence"
                    ),
                    "From State": convert_to_string_or_none(
                        field.get("fields").get("from_state")
                    ),
                    "To State": convert_to_string_or_none(
                        field.get("fields").get("to_state")
                    ),
                    "Spark URL": f"{field.get('fields').get('sparkai_URL')}",
                    "Foxglove URL": field.get("fields").get("foxglove_URL"),
                    "Triage Status": field.get("fields").get("triage_status"),
                    "VIN": field.get("fields").get("vin"),
                    "Halt Code - Linked": halt_code_ids.get('halt_code'),
                    "Timestamp UTC": safe_airtable_timestamp_format(field.get("fields").get("timestamp_utc")),
                    "Halt Code - Import": field.get("fields").get("halt_code"),
                    "Pilot VINs Linked": convert_pilot_vins(
                        field.get("fields").get("vin")
                    ),
                    "Link to Webpage": field.get("fields").get("sparkai_url"),
                    "Spark Program Name": field.get("fields").get("spark_program_name"),
                    "Spark Original Annotation 0 Label": field.get("fields").get(
                        "spark_original_annotation_0_label"
                    ),
                    "Spark Annotation 0 Label": field.get("fields").get(
                        "spark_annotation_0_label"
                    ),
                    "Spark Camera Name": field.get("fields").get("spark_camera_name"),
                    "Spark Response": field.get("fields").get("spark_response"),
                    "Map pre-signed URL": field.get("fields").get("map_presigned_url"),
                    "Manned Type": field.get("fields").get("manned_type"),
                    "SparkAI Query URL": field.get("fields").get("sparkai_query_url"),
                    "Other SparkAI URL": field.get("fields").get("other_sparkai_url"),
                    "Secondary Demotion Auto": halt_code_ids.get('secondary_demotion_auto'),
                    "No of Spark Engagements": field.get("fields").get("no_of_spark_engagements"),
                    "Preceding Stop Code": convert_none(field.get("fields").get("preceding_stop_code")),
                    "Implement Path Position Type Text": field.get("fields").get("implement_path_position_type_text"),
                    "Computed Implement Path Position Type Text": field.get("fields").get(
                        "computed_implement_path_position_type_text"),
                    "genos_version": field.get("fields").get("genos_version"),
                }
            }
            payload["records"].append(record)

        response = requests.patch(AIRTABLE_URL, headers=headers, json=payload)

        if response.status_code != 200:
            print(payload)
            print(response.json())
            raise Exception(
                "Request failed with status code {}. {}".format(
                    response.status_code, response.text
                )
            )

        result_data["records"].extend(response.json()["records"])

    return result_data

# COMMAND ----------

def patch_data_to_airtable(id_, data: dict):
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}",
               "Content-Type": "application/json"}
    response = requests.patch(AIRTABLE_URL, headers=headers, json={
        'records': [{
            'id': id_,
            'fields': data,
        }]
    })
    if response.status_code != 200:
        raise Exception("Request failed with status code {}. {}".format(response.status_code, response.text))


# COMMAND ----------

def clear_empty_demotions(data: dict) -> list: 
    resp_dfn = []
    for record in data:
        if record['fields'].get('A_UID') is None:
            print(f'INFO: Field A_UID is empty, skipping record: {record["id"]}')
            continue
        resp_dfn += [record]
    return resp_dfn


# COMMAND ----------

# MAGIC %md
# MAGIC Deletion of items

# COMMAND ----------

def format_timestamp_utc(value):
    if value:
          # Assuming the timestamp string is in a recognizable format, e.g., ISO 8601
          # Adjust the format string as per your actual timestamp format
          timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"  # Example format, adjust as needed
          datetime_obj = datetime.strptime(value, timestamp_format)
          print(datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f"))
          return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")  # Adjust the format as needed
    return None

spark.conf.set("spark.sql.ansi.enabled", "false")
def get_airtable_ids_to_delete() -> list[int]:
    data = spark.sql(f"""
        SELECT *
        FROM {DEMOTION_CONTEXT_TABLE}
        WHERE triage_activities_complete = 'Complete'
        AND airtable_deleted IS NOT True
        AND timestamp_utc < date_sub(current_date(), 180)
    """).collect()

    ids_to_delete = [d['Airtable_ID'] for d in data]
    VIN_list = [d['VIN'] for d in data]
    timestamp_list = [d['Timestamp_utc'].strftime("%Y-%m-%dT%H:%M:%S.%f") for d in data]
  
    return ids_to_delete, VIN_list, timestamp_list


# COMMAND ----------

def delete_airtable_items(
    ids_to_delete: list[int], VIN_list, timestamp_list, url: str | None = None
):
    initial_url = url or AIRTABLE_URL
    headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}"}
    for id_, vin, timestamp in zip(ids_to_delete, VIN_list, timestamp_list):
        url = initial_url + f"/{id_}"
        print(f"Removing {id_}...")
        response = requests.delete(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to delete {id_}: {response.text}")
        spark.sql(
            f"UPDATE {DEMOTION_CONTEXT_TABLE} SET airtable_deleted=True WHERE Airtable_ID = '{id_}'"
        )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Field mappers

# COMMAND ----------

# MAGIC %md
# MAGIC Analyze fields relations to other tables

# COMMAND ----------

def get_code_name_records_mapping():
    mapping = {}
    halt_codes_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(HALT_CODES_TABLE_ID),
        limit=1000
    )
    for halt_code_record in halt_codes_data:
        if 'Code Name' in halt_code_record.get('fields', {}):
            a = halt_code_record['fields']['Code Name']
            mapping[halt_code_record['id']] = a
    return mapping  

code_name_records_mapping = get_code_name_records_mapping()


# COMMAND ----------

def get_vin_id_mapping():
    mapping = {}
    vin_id_data = get_airtable_data(
        url=get_AIRTABLE_URL_for_table(MACHINE_INFORMATION_TABLE_ID),
        limit=1000
    )
    for vin_id_record in vin_id_data:
       mapping[vin_id_record['fields']['vin']] = vin_id_record['id']
    return mapping  

get_vin_id_mapping = get_vin_id_mapping()

def convert_pilot_vins(value):
      if value in get_vin_id_mapping:
        return get_vin_id_mapping[value]
      else:
        return None
    

# COMMAND ----------

# MAGIC %md
# MAGIC **Update Pilot VIN's Linked field**

# COMMAND ----------

def fix_records_with_empty_pilot_vin():
    formula = "AND({Pilot VINs Linked} = '')"
    records = get_airtable_data(
        formula=formula, limit=1000
    )

    for record in records:
        vin = record["fields"].get("VIN")
        if vin in get_vin_id_mapping.keys():
            record_id = record["id"]
            vin_id = get_vin_id_mapping[vin]
            patch_data_to_airtable(id_=record_id, data={"Pilot VINs Linked": [vin_id]})
            print(f"Updated record: {record_id} with pilot_vin_linked: {vin_id}")
    

# COMMAND ----------

# MAGIC %md
# MAGIC `Update pre-signed url`

# COMMAND ----------

def get_unique_map_presigned_urls():
    presigned_url_data = spark.sql(f"""
        SELECT VIN, Timestamp_utc, map_presigned_url, Airtable_ID, ReasonForFailure, ReasonCategory, DemotionFailureLogTime_ts
        FROM (
            SELECT ps.VIN, ps.Timestamp_utc, ps.map_presigned_url, dc.Airtable_ID, ps.ReasonForFailure, ps.ReasonCategory, ps.DemotionFailureLogTime_ts,
                ROW_NUMBER() OVER (PARTITION BY ps.VIN, ps.Timestamp_utc ORDER BY ps.Timestamp_utc) AS row_num
            FROM jupiter_dev.demotion_work_field_image_dev.vw_vin_timestamputc_presignedurl ps
            LEFT JOIN {DEMOTION_CONTEXT_TABLE} dc ON 
            dc.VIN = ps.VIN AND 
            dc.Timestamp_utc = ps.Timestamp_utc AND 
            dc.Demotions = 1 AND
            dc.Airtable_ID IS NOT NULL AND
            dc.map_presigned_url is null and
            ps.map_presigned_url is not null and
            dc.airtable_deleted IS NOT TRUE
            WHERE dc.Airtable_ID IS NOT NULL
        ) subquery
        WHERE row_num = 1;
    """)
    return presigned_url_data

def patch_pre_signed_to_airtable():
    joined_data = get_unique_map_presigned_urls()
    records = []
    for row in joined_data.collect():
        fields = {
            "Map pre-signed URL": row["map_presigned_url"] if "map_presigned_url" in row else None,
            "Vis Map Error - Reason for Failure": row["ReasonForFailure"] if "ReasonForFailure" in row and row[
                "ReasonForFailure"] is not None else "",
            "Vis Map Error - Reason Category": row["ReasonCategory"] if "ReasonCategory" in row and row[
                "ReasonCategory"] is not None else "",
            "Vis Map Error - Demotion Failure Log Time": safe_airtable_timestamp_format(
                row["DemotionFailureLogTime_ts"]
            ) if "DemotionFailureLogTime_ts" in row and row["DemotionFailureLogTime_ts"] is not None else None
        }
        record = {
            'id': row["Airtable_ID"],
            'fields': fields
        }
        records.append(record)

    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }

    for i in range(0, len(records), 10):
        data = {
            'records': records[i:i+10]
        }
        print("Updating map_presigned_url's...")
        response = requests.patch(AIRTABLE_URL, headers=headers, json=data)
        print('Response status code:', response.status_code)
        if response.status_code == 422 and response.json()['error']['type'] == 'ROW_DOES_NOT_EXIST':
            record_id = response.json()['error']['message'].split(' ')[2]
            spark.sql(f"""
                      UPDATE {DEMOTION_CONTEXT_TABLE} 
                      SET airtable_deleted = TRUE, updated_at = current_timestamp()
                      WHERE Airtable_ID = '{record_id}'
                      """)
        elif response.status_code != 200:
            error_message = "Request failed with status code {}".format(response.status_code)
            print(response.json())
            raise Exception(error_message)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Demotion Stops Hours Updates Sync To Demotion Context

# COMMAND ----------

DEMOTIONS_STOPS_HOURS_UPDATES_QUERY = f"""
    WITH deduplicated_source AS (
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY VIN, Timestamp_utc, Demotions ORDER BY Id) AS row_num
        FROM jupiter_prod.jfa_metrics.demotions_stops_hours
    )
    SELECT
    source.*,
    target.Airtable_ID
    FROM {DEMOTION_CONTEXT_TABLE} AS target
    JOIN (SELECT * FROM deduplicated_source WHERE row_num = 1) AS source
    ON target.VIN = source.VIN
    AND target.Timestamp_utc = source.Timestamp_utc
    AND target.demotions = source.demotions
    WHERE (
    target.Airtable_ID is not null AND
    target.airtable_deleted is not TRUE AND (
        target.System IS DISTINCT FROM source.System OR
        target.VIN IS DISTINCT FROM source.VIN OR
        target.Bundle IS DISTINCT FROM source.Bundle OR
        target.Stops IS DISTINCT FROM source.Stops OR
        target.halt_code IS DISTINCT FROM source.halt_code OR
        target.halt_name IS DISTINCT FROM source.halt_name OR
        target.demotion_occurrence IS DISTINCT FROM source.demotion_occurrence OR
        target.prior_timestamp IS DISTINCT FROM source.prior_timestamp OR
        target.last_activation_time IS DISTINCT FROM source.last_activation_time OR
        target.from_state IS DISTINCT FROM source.from_state OR
        target.to_state IS DISTINCT FROM source.to_state OR
        target.timestamp_diff_from_last_activation IS DISTINCT FROM source.timestamp_diff_from_last_activation OR
        target.minutes_from_activation IS DISTINCT FROM source.minutes_from_activation OR
        target.seconds_from_activation IS DISTINCT FROM source.seconds_from_activation OR
        target.hours_from_activation IS DISTINCT FROM source.hours_from_activation OR
        target.county IS DISTINCT FROM source.county OR
        target.state IS DISTINCT FROM source.state OR
        target.country IS DISTINCT FROM source.country OR
        target.operation_time IS DISTINCT FROM source.operation_time OR
        target.spark_program_name IS DISTINCT FROM source.spark_program_name OR
        target.spark_response IS DISTINCT FROM source.spark_response OR
        target.spark_original_annotation_0_label IS DISTINCT FROM source.spark_original_annotation_0_label OR
        target.spark_annotation_0_label IS DISTINCT FROM source.spark_annotation_0_label OR
        target.spark_camera_name IS DISTINCT FROM source.spark_camera_name OR
        target.manned_type IS DISTINCT FROM source.manned_type OR
        target.SparkAI_query_URL IS DISTINCT FROM source.SparkAI_query_URL OR
        target.other_sparkai_url IS DISTINCT FROM source.other_sparkai_url OR
        target.secondary_demotion_auto IS DISTINCT FROM CAST(source.secondary_demotion_auto AS ARRAY<STRING>) OR
        target.no_of_spark_engagements IS DISTINCT FROM source.no_of_spark_engagements OR
        target.seconds_in_autonomy_time_before_demotion IS DISTINCT FROM source.seconds_in_autonomy_time_before_demotion OR
        target.Preceding_Stop_Code IS DISTINCT FROM source.Preceding_Stop_Code OR
        target.Preceding_Stop_Code_Error IS DISTINCT FROM source.Preceding_Stop_Code_Error OR
        target.implement_path_position_heading IS DISTINCT FROM source.implement_path_position_heading OR
        target.implement_path_position_direction IS DISTINCT FROM source.implement_path_position_direction OR
        target.implement_path_position_type IS DISTINCT FROM source.implement_path_position_type OR
        target.implement_path_position_type_text IS DISTINCT FROM source.implement_path_position_type_text OR
        target.computed_implement_path_position_type_text IS DISTINCT FROM source.computed_implement_path_position_type_text OR
        target.genos_version IS DISTINCT FROM source.genos_version OR
        target.seconds_in_state_5_and_6 IS DISTINCT FROM source.seconds_in_state_5_and_6
        )
    )
"""

UPDATE_DEMOTION_CONTEXT_RECORDS_QUERY = f"""
    WITH deduplicated_source AS (
        SELECT *,
        ROW_NUMBER() OVER (PARTITION BY VIN, Timestamp_utc, Demotions ORDER BY Id) AS row_num
        FROM jupiter_prod.jfa_metrics.demotions_stops_hours
    )
    MERGE INTO {DEMOTION_CONTEXT_TABLE} AS target
    USING (SELECT * FROM deduplicated_source WHERE row_num = 1) AS source
    ON target.VIN = source.VIN
    AND target.Timestamp_utc = source.Timestamp_utc
    AND target.Demotions = source.Demotions
    AND target.Airtable_ID is not null
    AND target.airtable_deleted is not true
    WHEN MATCHED AND (
        target.System IS DISTINCT FROM source.System OR
        target.VIN IS DISTINCT FROM source.VIN OR
        target.Bundle IS DISTINCT FROM source.Bundle OR
        target.Stops IS DISTINCT FROM source.Stops OR
        target.halt_code IS DISTINCT FROM source.halt_code OR
        target.halt_name IS DISTINCT FROM source.halt_name OR
        target.demotion_occurrence IS DISTINCT FROM source.demotion_occurrence OR
        target.prior_timestamp IS DISTINCT FROM source.prior_timestamp OR
        target.last_activation_time IS DISTINCT FROM source.last_activation_time OR
        target.from_state IS DISTINCT FROM source.from_state OR
        target.to_state IS DISTINCT FROM source.to_state OR
        target.timestamp_diff_from_last_activation IS DISTINCT FROM source.timestamp_diff_from_last_activation OR
        target.minutes_from_activation IS DISTINCT FROM source.minutes_from_activation OR
        target.seconds_from_activation IS DISTINCT FROM source.seconds_from_activation OR
        target.hours_from_activation IS DISTINCT FROM source.hours_from_activation OR
        target.county IS DISTINCT FROM source.county OR
        target.state IS DISTINCT FROM source.state OR
        target.country IS DISTINCT FROM source.country OR
        target.operation_time IS DISTINCT FROM source.operation_time OR
        target.spark_program_name IS DISTINCT FROM source.spark_program_name OR
        target.spark_response IS DISTINCT FROM source.spark_response OR
        target.spark_original_annotation_0_label IS DISTINCT FROM source.spark_original_annotation_0_label OR
        target.spark_annotation_0_label IS DISTINCT FROM source.spark_annotation_0_label OR
        target.spark_camera_name IS DISTINCT FROM source.spark_camera_name OR
        target.manned_type IS DISTINCT FROM source.manned_type OR
        target.SparkAI_query_URL IS DISTINCT FROM source.SparkAI_query_URL OR
        target.other_sparkai_url IS DISTINCT FROM source.other_sparkai_url OR
        target.secondary_demotion_auto IS DISTINCT FROM CAST(source.secondary_demotion_auto AS ARRAY<STRING>) OR
        target.no_of_spark_engagements IS DISTINCT FROM source.no_of_spark_engagements OR
        target.seconds_in_autonomy_time_before_demotion IS DISTINCT FROM source.seconds_in_autonomy_time_before_demotion OR
        target.Preceding_Stop_Code IS DISTINCT FROM source.Preceding_Stop_Code OR
        target.Preceding_Stop_Code_Error IS DISTINCT FROM source.Preceding_Stop_Code_Error OR
        target.implement_path_position_heading IS DISTINCT FROM source.implement_path_position_heading OR
        target.implement_path_position_direction IS DISTINCT FROM source.implement_path_position_direction OR
        target.implement_path_position_type IS DISTINCT FROM source.implement_path_position_type OR
        target.implement_path_position_type_text IS DISTINCT FROM source.implement_path_position_type_text OR
        target.computed_implement_path_position_type_text IS DISTINCT FROM source.computed_implement_path_position_type_text OR
        target.genos_version IS DISTINCT FROM source.genos_version OR
        target.seconds_in_state_5_and_6 IS DISTINCT FROM source.seconds_in_state_5_and_6
    ) THEN
    UPDATE SET 
        target.System = source.System,
        target.VIN = source.VIN,
        target.Bundle = source.Bundle,
        target.Stops = source.Stops,
        target.halt_code = source.halt_code,
        target.halt_name = source.halt_name,
        target.demotion_occurrence = source.demotion_occurrence,
        target.prior_timestamp = source.prior_timestamp,
        target.last_activation_time = source.last_activation_time,
        target.from_state = source.from_state,
        target.to_state = source.to_state,
        target.timestamp_diff_from_last_activation = source.timestamp_diff_from_last_activation,
        target.minutes_from_activation = source.minutes_from_activation,
        target.seconds_from_activation = source.seconds_from_activation,
        target.hours_from_activation = source.hours_from_activation,
        target.county = source.county,
        target.state = source.state,
        target.country = source.country,
        target.operation_time = source.operation_time,
        target.spark_program_name = source.spark_program_name,
        target.spark_response = source.spark_response,
        target.spark_original_annotation_0_label = source.spark_original_annotation_0_label,
        target.spark_annotation_0_label = source.spark_annotation_0_label,
        target.spark_camera_name = source.spark_camera_name,
        target.manned_type = source.manned_type,
        target.SparkAI_query_URL = source.SparkAI_query_URL,
        target.other_sparkai_url = source.other_sparkai_url,
        target.secondary_demotion_auto = CAST(source.secondary_demotion_auto AS ARRAY<STRING>),
        target.no_of_spark_engagements = source.no_of_spark_engagements,
        target.seconds_in_autonomy_time_before_demotion = source.seconds_in_autonomy_time_before_demotion,
        target.Preceding_Stop_Code = source.Preceding_Stop_Code,
        target.Preceding_Stop_Code_Error = source.Preceding_Stop_Code_Error,
        target.implement_path_position_heading = source.implement_path_position_heading,
        target.implement_path_position_direction = source.implement_path_position_direction,
        target.implement_path_position_type = source.implement_path_position_type,
        target.implement_path_position_type_text = source.implement_path_position_type_text,
        target.computed_implement_path_position_type_text = source.computed_implement_path_position_type_text,
        target.genos_version = source.genos_version,
        target.seconds_in_state_5_and_6 = source.seconds_in_state_5_and_6
"""

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json",
}


def convert_to_string_or_none(value):
    if value is None or value == "None":
        return None
    return f"{value}"


def convert_none(value):
    if value == "None":
        return None
    return value


def convert_jira(value):
    if value is None or value == "None":
        return "No Jira Ticket Create"
    return f"{value}"


def convert_pilot_vins(value):
    if value in get_vin_id_mapping:
        return [get_vin_id_mapping[value]]
    else:
        return []


def create_draft_halt_code(halt_code, extra):
    halt_code = str(halt_code)
    halt_code_list = halt_code.split(".")

    payload = [
        {
            "fields": {
                "ERC": [part_halt_code_erc_mapping[int(halt_code_list[0])]],
                "Supplement Code": int(halt_code_list[1]),
                "Demotion Reason_Old": ["recBuyNxcnrReNpJ0"]  # DR-10 Unassigned
            }
        }
    ]

    if extra:
        payload[0]['fields'].update(extra)

    payload = {
        "records": payload,
        "typecast": True,
    }  # Allow creation of new records for single / multiple option fields

    HALT_CODE_TABLE_URL = (
        f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{HALT_CODES_TABLE_ID}"
    )

    response = requests.post(HALT_CODE_TABLE_URL, headers=HEADERS, json=payload)
    print(f"Created new halt code record: {response.json()}")
    halt_code_id = response.json().get("records")[0].get("id")
    halt_code_records_mapping[halt_code] = halt_code_id

    return halt_code_id


def update_airtable_demotions():
    updated_records = spark.sql(DEMOTIONS_STOPS_HOURS_UPDATES_QUERY)
    print(f"{updated_records.count()} records to be updated")
    records = [{"fields": row.asDict()} for row in updated_records.collect()]
    data = {"records": records}
    for i in range(0, len(data["records"]), 10):
        payload = {
            "records": [],
            "typecast": True,
        }
        airtable_ids = []
        for field in data["records"][i: min(i + 10, len(data["records"]))]:
            airtable_id = field["fields"]["Airtable_ID"]
            if not airtable_id or airtable_id in airtable_ids:
                continue
            airtable_ids.append(airtable_id)

            halt_code_ids = {}
            for halt_code_field in [
                "halt_code",
                "prev_stop_halt_code",
                "secondary_demotion_auto"
            ]:
                halt_code_field_value = field.get("fields").get(halt_code_field)
                if halt_code_field_value:
                    if not isinstance(halt_code_field_value, list):
                        halt_code_field_value = [halt_code_field_value]

                    for halt_code in halt_code_field_value:
                        halt_code_id = halt_code_records_mapping.get(str(halt_code))
                        if halt_code_id is None:
                            extra = {}
                            if halt_code_field == "halt_code":
                                extra = {
                                    "Code Name": field.get('fields').get("halt_name"),
                                    "Description": field.get('fields').get("halt_description")
                                }
                            halt_code_id = create_draft_halt_code(halt_code, extra)

                        if halt_code_field not in halt_code_ids:
                            halt_code_ids[halt_code_field] = []
                        halt_code_ids[halt_code_field].append(halt_code_id)

            record = {
                "id": airtable_id,
                "fields": {
                    "A_UID": f"{field.get('fields').get('vin')} | {field.get('fields').get('timestamp_utc')}",
                    "Bundle": field.get("fields").get("bundle"),
                    "Demotion Occurrence": field.get("fields").get("demotion_occurrence"),
                    "From State": convert_to_string_or_none(field.get("fields").get("from_state")),
                    "To State": convert_to_string_or_none(field.get("fields").get("to_state")),
                    "Spark URL": f"{field.get('fields').get('sparkai_url')}",
                    "Foxglove URL": field.get("fields").get("foxglove_url"),
                    "Triage Status": field.get("fields").get("triage_status"),
                    "VIN": field.get("fields").get("vin"),
                    "Halt Code - Linked": halt_code_ids.get('halt_code'),
                    "Timestamp UTC": safe_airtable_timestamp_format(field.get("fields").get("timestamp_utc")),
                    "Halt Code - Import": field.get("fields").get("halt_code"),
                    "Pilot VINs Linked": convert_pilot_vins(field.get("fields").get("vin")),
                    "Link to Webpage": field.get("fields").get("sparkai_url", ""),
                    "Spark Program Name": field.get("fields").get("spark_program_name", ""),
                    "Spark Original Annotation 0 Label": field.get("fields").get("spark_original_annotation_0_label",
                                                                                 ""),
                    "Spark Annotation 0 Label": field.get("fields").get("spark_annotation_0_label", ""),
                    "Spark Camera Name": field.get("fields").get("spark_camera_name", ""),
                    "Spark Response": field.get("fields").get("spark_response", ""),
                    "Manned Type": field.get("fields").get("manned_type", ""),
                    "SparkAI Query URL": field.get("fields").get("sparkai_query_url"),
                    "Other SparkAI URL": field.get("fields").get("other_sparkai_url", ""),
                    "Secondary Demotion Auto": halt_code_ids.get('secondary_demotion_auto', []),
                    "No of Spark Engagements": field.get("fields").get("no_of_spark_engagements"),
                    "Preceding Stop Code": convert_none(field.get("fields").get("preceding_stop_code")),
                    "Implement Path Position Type Text": field.get("fields").get("implement_path_position_type_text"),
                    "genos_version": field.get('fields').get('genos_version'),
                    "Computed Implement Path Position Type Text": field.get('fields').get(
                        'computed_implement_path_position_type_text'),
                }
            }
            payload["records"].append(record)
        response = requests.patch(
            url=AIRTABLE_URL,
            headers=HEADERS,
            json=payload,
        )
        if response.status_code == 422 and response.json()['error']['type'] == 'ROW_DOES_NOT_EXIST':
            record_id = response.json()['error']['message'].split(' ')[2]
            print(f"Updating record {record_id}")
            spark.sql(f"UPDATE {DEMOTION_CONTEXT_TABLE} SET airtable_deleted=TRUE WHERE Airtable_ID = '{record_id}'")
            continue
        elif response.status_code != 200:
            print(payload)
            print(response.json())
            error_message = "Request failed with status code {}".format(response.status_code)
            raise Exception(error_message)
    print("Updated demotions records in AIRTABLE")


def update_demotion_context_records():
    spark.sql(UPDATE_DEMOTION_CONTEXT_RECORDS_QUERY)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Flows definition

# COMMAND ----------

# MAGIC %md
# MAGIC Here we define functions that encapsulate the flows for the sync process.

# COMMAND ----------

formula = "DATETIME_DIFF(NOW(),{Timestamp UTC}, 'months') < 6"
formula_encoded = urllib.parse.quote(formula)


def process_demotions_updates():
    update_airtable_demotions()
    update_demotion_context_records()


def process_databricks_changes():
    current_count = 0
    while True:
        print(f"Current count: {current_count}")
        new_demotion_updates = get_demotions_stops_hours_updates(1000)

        if new_demotion_updates.count() == 0:
            break
        resp = send_data_to_airtable(new_demotion_updates)
        save_to_demotion_context(resp, new_demotion_updates)
        current_count += 10


def process_airtable_updates():
    data = get_airtable_data(
        limit=20000,
        formula=formula_encoded,
    )
    valid_data = clear_empty_demotions(data)
    print(f"Received {len(valid_data)} items from Airtable.")
    temp_table_name = get_temp_table_name()
    upload_to_temp_table(valid_data, temp_table_name)
    merge_to_demotion_context(temp_table_name)


def cleanup_airtable():
    ids_to_delete, vin_list, timestamp_list = get_airtable_ids_to_delete()
    print(ids_to_delete)
    delete_airtable_items(ids_to_delete, vin_list, timestamp_list)
    print(f"Deleted {len(ids_to_delete)} records from Airtable")
    deleted_tables = delete_expired_temp_tables()
    print(f"Deleted {len(deleted_tables)} expired temp tables.")
    fix_records_with_empty_pilot_vin()


def assert_no_detached_records():
    data = get_airtable_data(
        limit=20000,
        formula=formula_encoded,
    )
    ids_to_check = set()
    for item in data:
        if "A_UID" in item["fields"]:
            ids_to_check.add(item["id"])
    print(f"Found {len(ids_to_check)} records in Airtable.")
    airtable_ids_str = ",".join(f"'{id}'" for id in ids_to_check)
    ids_exist = spark.sql(
        f"""
        SELECT Airtable_ID
        FROM {DEMOTION_CONTEXT_TABLE}
        WHERE Airtable_ID IN ({airtable_ids_str})
    """
    ).collect()
    ids_exist = set(d.Airtable_ID for d in ids_exist)
    print(f"Found {len(ids_exist)} records in Databricks.")
    if ids_to_check != ids_exist:
        raise RuntimeError(
            f"Some records from Airtable were not found in the demotion context table: {ids_to_check - ids_exist}"
        )


def delete_unprocessable_records():
    deleted_records_len = spark.sql(
    f"""
        DELETE FROM {DEMOTION_CONTEXT_TABLE}
        WHERE Demotions = 1 AND halt_code != "0.0" AND Airtable_ID IS NULL
    """
    ).count()
    print("Unprocessable records deleted: ", deleted_records_len)


# COMMAND ----------

# MAGIC %md
# MAGIC # Route Around Table Sync

# COMMAND ----------

# MAGIC %md
# MAGIC ### Route Around Context Table

# COMMAND ----------

def create_route_around_context_table(table_name: str = None) -> None:
    if table_name is not None:
        table_name = f'{TEMP_TABLES_PATH}{table_name}'
    else:
        table_name = ROUTE_AROUND_CONTEXT_TABLE
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        airtable_id STRING,
        a_uid STRING,
        identifier_value STRING,
        content_major_version BIGINT,
        content_minor_version BIGINT,
        event_type BIGINT,
        event_type_guid STRING,
        vin STRING,
        vpu_idx INT,
        label STRING,
        system STRING,
        bundle STRING,
        genos_version STRING,
        request_time TIMESTAMP,
        response_time TIMESTAMP,
        user_response STRING,
        auto_response STRING,
        halt_code STRING COMMENT 'Code representing the specific halt encountered by the vehicle',
        demotion_context__main_demotion_code STRING COMMENT 'Represents the main code associated with the demotion context, useful for categorizing demotion types.',
        demotion_timestamp TIMESTAMP COMMENT 'The exact date and time in Coordinated Universal Time (UTC) when the state is transitioned.',
        demotion_id STRING,
        demotions_stops_hours_uuid STRING,
        time_to_demotion_mins BIGINT,
        original_route_around_result STRING,
        is_route_around BOOLEAN,
        triage_status STRING,
        triage_result STRING,
        triage_description STRING,
        is_auto_triggered_route_around BOOLEAN,
        is_human_triggered_route_around BOOLEAN,
        is_success_route_around BOOLEAN,
        route_around_type STRING,
        period_of_day STRING,
        success_state STRING,
        is_route_around_triaged BOOLEAN,
        updated_at TIMESTAMP,
        created_at TIMESTAMP
    )""")
    print("Route Around Context Created Successfully")


# COMMAND ----------

# MAGIC %md
# MAGIC ### Route Around Schema

# COMMAND ----------

# DBTITLE 1,Route Around Schema
# Schema for route around table
route_around_schema = StructType([
    StructField("airtable_id", StringType(), True),
    StructField("a_uid", StringType(), True),
    StructField("identifier_value", StringType(), True),
    StructField("content_major_version", LongType(), True),
    StructField("content_minor_version", LongType(), True),
    StructField("event_type", LongType(), True),
    StructField("event_type_guid", StringType(), True),
    StructField("vin", StringType(), True),
    StructField("vpu_idx", IntegerType(), True),
    StructField("label", StringType(), True),
    StructField("system", StringType(), True),
    StructField("bundle", StringType(), True),
    StructField("genos_version", StringType(), True),
    StructField("request_time", TimestampType(), True),
    StructField("response_time", TimestampType(), True),
    StructField("user_response", StringType(), True),
    StructField("auto_response", StringType(), True),
    StructField("halt_code", StringType(), True),
    StructField("demotion_context__main_demotion_code", StringType(), True),
    StructField("demotion_timestamp", TimestampType(), True),
    StructField("demotion_id", StringType(), True),
    StructField("demotions_stops_hours_uuid", StringType(), True),
    StructField("time_to_demotion_mins", LongType(), True),
    StructField("original_route_around_result", StringType(), True),
    StructField("is_route_around", BooleanType(), True),
    StructField("triage_status", StringType(), True),
    StructField("triage_result", StringType(), True),
    StructField("triage_description", StringType(), True),
    StructField("is_auto_triggered_route_around", BooleanType(), True),
    StructField("is_human_triggered_route_around", BooleanType(), True),
    StructField("is_success_route_around", BooleanType(), True),
    StructField("route_around_type", StringType(), True),
    StructField("period_of_day", StringType(), True),
    StructField("success_state", StringType(), True),
    StructField("is_route_around_triaged", BooleanType(), True),
])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Utils

# COMMAND ----------

# DBTITLE 1,Cell 69
ROUTE_AROUND_AIRTABLE_URL = get_AIRTABLE_URL_for_table(table_id=ROUTE_AROUND_TABLE_ID)


def get_route_around_temp_table_name() -> str:
    current_time = datetime.now()
    return "route_around_context_" + current_time.strftime("%Y_%m_%d_%H_%M_%S")


def map_airtable_route_around_data_to_dbx(airtable_data: list, df_mode: bool = False):
    rows = []
    for record in airtable_data:
        airtable_record_fields = record["fields"]
        row_data = Row(
            airtable_id=record["id"],
            a_uid=demotions_a_uid_mapping.get(airtable_record_fields["a_uid"][0]) if airtable_record_fields.get(
                "a_uid") else None,
            identifier_value=airtable_record_fields.get("identifier_value"),
            content_major_version=airtable_record_fields.get("content_major_version"),
            content_minor_version=airtable_record_fields.get("content_minor_version"),
            event_type=airtable_record_fields.get("event_type"),
            event_type_guid=airtable_record_fields.get("event_type_guid"),
            vin=airtable_record_fields.get("vin"),
            vpu_idx=airtable_record_fields.get("vpu_idx"),
            label=airtable_record_fields.get("label"),
            system=airtable_record_fields.get("system"),
            bundle=airtable_record_fields.get("bundle"),
            genos_version=airtable_record_fields.get("genos_version"),
            request_time=parse_datetime(airtable_record_fields["request_time"]) if airtable_record_fields.get(
                "request_time") else None,
            response_time=parse_datetime(airtable_record_fields["response_time"]) if airtable_record_fields.get(
                "response_time") else None,
            user_response=airtable_record_fields.get("user_response"),
            auto_response=airtable_record_fields.get("auto_response"),
            halt_code=airtable_record_fields.get("halt_code"),
            demotion_context__main_demotion_code=airtable_record_fields.get("demotion_context__main_demotion_code"),
            demotion_timestamp=parse_datetime(
                airtable_record_fields["demotion_timestamp"]) if airtable_record_fields.get(
                "demotion_timestamp") else None,
            demotion_id=airtable_record_fields.get("demotion_id"),
            demotions_stops_hours_uuid=airtable_record_fields.get("demotions_stops_hours_uuid"),
            time_to_demotion_mins=airtable_record_fields.get("time_to_demotion_mins"),
            original_route_around_result=airtable_record_fields.get("original_route_around_result"),
            is_route_around=airtable_record_fields.get("is_route_around"),
            triage_status=airtable_record_fields.get("triage_status"),
            triage_result=airtable_record_fields.get("triage_result"),
            triage_description=airtable_record_fields.get("triage_description"),
            is_auto_triggered_route_around=airtable_record_fields.get("is_auto_triggered_route_around"),
            is_human_triggered_route_around=airtable_record_fields.get("is_human_triggered_route_around"),
            is_success_route_around=airtable_record_fields.get("is_success_route_around"),
            route_around_type=airtable_record_fields.get("route_around_type"),
            period_of_day=airtable_record_fields.get("period_of_day"),
            success_state=airtable_record_fields.get("success_state"),
            is_route_around_triaged=airtable_record_fields.get("is_route_around_triaged"),
        )
        rows.append(row_data)
    if df_mode:
        return spark.createDataFrame(rows, schema=route_around_schema)
    return rows


def map_dbx_route_around_data_to_context_schema(dbx_data: list, df_mode: bool = True):
    rows = []
    for record in dbx_data:
        record = record.asDict()
        row_data = Row(
            airtable_id=None,
            a_uid=record.get("a_uid"),
            identifier_value=record.get("identifier_value"),
            content_major_version=record.get("content_major_version"),
            content_minor_version=record.get("content_minor_version"),
            event_type=record.get("event_type"),
            event_type_guid=record.get("event_type_guid"),
            vin=record.get("vin"),
            vpu_idx=record.get("vpu_idx"),
            label=record.get("label"),
            system=record.get("system"),
            bundle=record.get("bundle"),
            genos_version=record.get("genos_version"),
            request_time=record.get("request_time"),
            response_time=record.get("response_time"),
            user_response=record.get("user_response"),
            auto_response=record.get("auto_response"),
            halt_code=record.get("halt_code"),
            demotion_context__main_demotion_code=record.get("demotion_context__main_demotion_code"),
            demotion_timestamp=record.get("demotion_timestamp"),
            demotion_id=record.get("demotion_id"),
            demotions_stops_hours_uuid=record.get("demotions_stops_hours_uuid"),
            time_to_demotion_mins=record.get("time_to_demotion_mins"),
            original_route_around_result=record.get("original_route_around_result"),
            is_route_around=record.get("is_route_around"),
            triage_status=record.get("triage_status"),
            triage_result=record.get("triage_result"),
            triage_description=record.get("triage_description"),
            is_auto_triggered_route_around=record.get("is_auto_triggered_route_around"),
            is_human_triggered_route_around=record.get("is_human_triggered_route_around"),
            is_success_route_around=record.get("is_success_route_around"),
            route_around_type=record.get("route_around_type"),
            period_of_day=record.get("period_of_day"),
            success_state=record.get("success_state"),
            is_route_around_triaged=record.get("is_route_around_triaged"),
        )
        rows.append(row_data)
    if df_mode:
        return spark.createDataFrame(rows, schema=route_around_schema)
    return rows


def upload_to_temp_route_around_table(temp_table_name, data):
    df = spark.createDataFrame(data, schema=route_around_schema)
    df.write.format("delta").mode("append").saveAsTable(f'{TEMP_TABLES_PATH}{temp_table_name}')
    print(f'Uploaded {len(data)} to {temp_table_name}.')


def merge_to_route_around_context(temp_table_name):
    spark.sql(f"""
    MERGE INTO {ROUTE_AROUND_CONTEXT_TABLE} AS target
        USING {TEMP_TABLES_PATH}{temp_table_name} AS source
        ON target.airtable_id = source.airtable_id
        AND target.identifier_value = source.identifier_value
        WHEN MATCHED AND (
            target.identifier_value IS DISTINCT FROM source.identifier_value OR
            target.a_uid IS DISTINCT FROM source.a_uid OR
            target.content_major_version IS DISTINCT FROM source.content_major_version OR
            target.content_minor_version IS DISTINCT FROM source.content_minor_version OR
            target.event_type IS DISTINCT FROM source.event_type OR
            target.event_type_guid IS DISTINCT FROM source.event_type_guid OR
            target.vin IS DISTINCT FROM source.vin OR
            target.vpu_idx IS DISTINCT FROM source.vpu_idx OR
            target.label IS DISTINCT FROM source.label OR
            target.system IS DISTINCT FROM source.system OR
            target.bundle IS DISTINCT FROM source.bundle OR
            target.genos_version IS DISTINCT FROM source.genos_version OR
            target.request_time IS DISTINCT FROM source.request_time OR
            target.response_time IS DISTINCT FROM source.response_time OR
            target.user_response IS DISTINCT FROM source.user_response OR
            target.auto_response IS DISTINCT FROM source.auto_response OR
            target.halt_code IS DISTINCT FROM source.halt_code OR
            target.demotion_context__main_demotion_code IS DISTINCT FROM source.demotion_context__main_demotion_code OR
            target.demotion_timestamp IS DISTINCT FROM source.demotion_timestamp OR
            target.demotion_id IS DISTINCT FROM source.demotion_id OR
            target.demotions_stops_hours_uuid IS DISTINCT FROM source.demotions_stops_hours_uuid OR
            target.time_to_demotion_mins IS DISTINCT FROM source.time_to_demotion_mins OR
            target.original_route_around_result IS DISTINCT FROM source.original_route_around_result OR
            target.is_route_around IS DISTINCT FROM source.is_route_around OR
            target.triage_status IS DISTINCT FROM source.triage_status OR
            target.triage_result IS DISTINCT FROM source.triage_result OR
            target.triage_description IS DISTINCT FROM source.triage_description OR
            target.is_auto_triggered_route_around IS DISTINCT FROM source.is_auto_triggered_route_around OR
            target.is_human_triggered_route_around IS DISTINCT FROM source.is_human_triggered_route_around OR
            target.is_success_route_around IS DISTINCT FROM source.is_success_route_around OR
            target.route_around_type IS DISTINCT FROM source.route_around_type OR
            target.period_of_day IS DISTINCT FROM source.period_of_day OR
            target.success_state IS DISTINCT FROM source.success_state OR
            target.is_route_around_triaged IS DISTINCT FROM source.is_route_around_triaged
        ) THEN
            UPDATE SET
                target.identifier_value = CASE WHEN source.identifier_value IS NOT NULL THEN source.identifier_value ELSE target.identifier_value END,
                target.a_uid = CASE WHEN source.a_uid IS NOT NULL THEN source.a_uid ELSE target.a_uid END,
                target.content_major_version = CASE WHEN source.content_major_version IS NOT NULL THEN source.content_major_version ELSE target.content_major_version END,
                target.content_minor_version = CASE WHEN source.content_minor_version IS NOT NULL THEN source.content_minor_version ELSE target.content_minor_version END,
                target.event_type = CASE WHEN source.event_type IS NOT NULL THEN source.event_type ELSE target.event_type END,
                target.event_type_guid = CASE WHEN source.event_type_guid IS NOT NULL THEN source.event_type_guid ELSE target.event_type_guid END,
                target.vin = CASE WHEN source.vin IS NOT NULL THEN source.vin ELSE target.vin END,
                target.vpu_idx = CASE WHEN source.vpu_idx IS NOT NULL THEN source.vpu_idx ELSE target.vpu_idx END,
                target.label = CASE WHEN source.label IS NOT NULL THEN source.label ELSE target.label END,
                target.system = CASE WHEN source.system IS NOT NULL THEN source.system ELSE target.system END,
                target.bundle = CASE WHEN source.bundle IS NOT NULL THEN source.bundle ELSE target.bundle END,
                target.genos_version = CASE WHEN source.genos_version IS NOT NULL THEN source.genos_version ELSE target.genos_version END,
                target.request_time = CASE WHEN source.request_time IS NOT NULL THEN source.request_time ELSE target.request_time END,
                target.response_time = CASE WHEN source.response_time IS NOT NULL THEN source.response_time ELSE target.response_time END,
                target.user_response = CASE WHEN source.user_response IS NOT NULL THEN source.user_response ELSE target.user_response END,
                target.auto_response = CASE WHEN source.auto_response IS NOT NULL THEN source.auto_response ELSE target.auto_response END,
                target.halt_code = CASE WHEN source.halt_code IS NOT NULL THEN source.halt_code ELSE target.halt_code END,
                target.demotion_context__main_demotion_code = CASE WHEN source.demotion_context__main_demotion_code IS NOT NULL THEN source.demotion_context__main_demotion_code ELSE target.demotion_context__main_demotion_code END,
                target.demotion_timestamp = CASE WHEN source.demotion_timestamp IS NOT NULL THEN source.demotion_timestamp ELSE target.demotion_timestamp END,
                target.demotion_id = CASE WHEN source.demotion_id IS NOT NULL THEN source.demotion_id ELSE target.demotion_id END,
                target.demotions_stops_hours_uuid = CASE WHEN source.demotions_stops_hours_uuid IS NOT NULL THEN source.demotions_stops_hours_uuid ELSE target.demotions_stops_hours_uuid END,
                target.time_to_demotion_mins = CASE WHEN source.time_to_demotion_mins IS NOT NULL THEN source.time_to_demotion_mins ELSE target.time_to_demotion_mins END,
                target.original_route_around_result = CASE WHEN source.original_route_around_result IS NOT NULL THEN source.original_route_around_result ELSE target.original_route_around_result END,
                target.is_route_around = CASE WHEN source.is_route_around IS NOT NULL THEN source.is_route_around ELSE target.is_route_around END,
                target.triage_status = CASE WHEN source.triage_status IS NOT NULL THEN source.triage_status ELSE target.triage_status END,
                target.triage_result = CASE WHEN source.triage_result IS NOT NULL THEN source.triage_result ELSE target.triage_result END,
                target.triage_description = CASE WHEN source.triage_description IS NOT NULL THEN source.triage_description ELSE target.triage_description END,
                target.is_auto_triggered_route_around = CASE WHEN source.is_auto_triggered_route_around IS NOT NULL THEN source.is_auto_triggered_route_around ELSE target.is_auto_triggered_route_around END,
                target.is_human_triggered_route_around = CASE WHEN source.is_human_triggered_route_around IS NOT NULL THEN source.is_human_triggered_route_around ELSE target.is_human_triggered_route_around END,
                target.is_success_route_around = CASE WHEN source.is_success_route_around IS NOT NULL THEN source.is_success_route_around ELSE target.is_success_route_around END,
                target.route_around_type = CASE WHEN source.route_around_type IS NOT NULL THEN source.route_around_type ELSE target.route_around_type END,
                target.period_of_day = CASE WHEN source.period_of_day IS NOT NULL THEN source.period_of_day ELSE target.period_of_day END,
                target.success_state = CASE WHEN source.success_state IS NOT NULL THEN source.success_state ELSE target.success_state END,
                target.is_route_around_triaged = CASE WHEN source.is_route_around_triaged IS NOT NULL THEN source.is_route_around_triaged ELSE target.is_route_around_triaged END,
                target.updated_at = current_timestamp()
    """)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Sync Route Around Triage Info To Context Table

# COMMAND ----------

def sync_route_around_triage_info():
    airtable_data = get_airtable_data(url=ROUTE_AROUND_AIRTABLE_URL)
    print(f"Received {len(airtable_data)} items from Route Around Airtable.")

    temp_table_name = get_route_around_temp_table_name()
    create_route_around_context_table(table_name=temp_table_name)

    data = map_airtable_route_around_data_to_dbx(airtable_data=airtable_data)
    upload_to_temp_route_around_table(temp_table_name=temp_table_name, data=data)
    merge_to_route_around_context(temp_table_name)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Get New Route Around Records

# COMMAND ----------

def get_new_route_around_records(limit: int = 1000):
    query = f"""
        SELECT ra.*
        FROM jupiter_prod.jfa_metrics.route_around AS ra
        ANTI JOIN {ROUTE_AROUND_CONTEXT_TABLE} rac 
        ON ra.identifier_value = rac.identifier_value
        limit {limit}    
    """
    records = spark.sql(query)
    return records


# COMMAND ----------

# MAGIC %md
# MAGIC ### Map Route Around DBX Records To Airtable Format

# COMMAND ----------

def map_dbx_route_around_data_to_airtable(route_around_record) -> dict:
    route_around_record_data = route_around_record.asDict()

    return {
        "fields": {
            "identifier_value": route_around_record_data.get("identifier_value"),
            "a_uid": swapped_demotions_a_uid_mapping.get(route_around_record_data.get("a_uid")),
            "content_major_version": route_around_record_data.get("content_major_version"),
            "content_minor_version": route_around_record_data.get("content_minor_version"),
            "event_type": route_around_record_data.get("event_type"),
            "event_type_guid": route_around_record_data.get("event_type_guid"),
            "vin": route_around_record_data.get("vin"),
            "vpu_idx": route_around_record_data.get("vpu_idx"),
            "label": route_around_record_data.get("label"),
            "system": route_around_record_data.get("system"),
            "bundle": route_around_record_data.get("bundle"),
            "genos_version": route_around_record_data.get("genos_version"),
            "request_time": safe_airtable_timestamp_format(
                route_around_record_data["request_time"]) if route_around_record_data.get("request_time") else None,
            "response_time": safe_airtable_timestamp_format(
                route_around_record_data["response_time"]) if route_around_record_data.get("response_time") else None,
            "user_response": route_around_record_data.get("user_response"),
            "auto_response": route_around_record_data.get("auto_response"),
            "halt_code": route_around_record_data.get("halt_code"),
            "demotion_context__main_demotion_code": route_around_record_data.get(
                "demotion_context__main_demotion_code"),
            "demotion_timestamp": safe_airtable_timestamp_format(
                route_around_record_data["demotion_timestamp"]) if route_around_record_data.get(
                "demotion_timestamp") else None,
            "demotion_id": route_around_record_data.get("demotion_id"),
            "demotions_stops_hours_uuid": route_around_record_data.get("demotions_stops_hours_uuid"),
            "time_to_demotion_mins": route_around_record_data.get("time_to_demotion_mins"),
            "original_route_around_result": route_around_record_data.get("original_route_around_result"),
            "is_route_around": route_around_record_data.get("is_route_around"),
            "is_auto_triggered_route_around": route_around_record_data.get("is_auto_triggered_route_around"),
            "is_human_triggered_route_around": route_around_record_data.get("is_human_triggered_route_around"),
            "is_success_route_around": route_around_record_data.get("is_success_route_around"),
            "route_around_type": route_around_record_data.get("route_around_type"),
            "period_of_day": route_around_record_data.get("period_of_day"),
            "success_state": route_around_record_data.get("success_state"),
            "is_route_around_triaged": route_around_record_data.get("is_route_around_triaged"),
        }
    }


# COMMAND ----------

# MAGIC %md
# MAGIC ### Sync New Route Around Records

# COMMAND ----------

from typing import List

AIRTABLE_MAX_BATCH_SIZE = 10


def send_batch_to_airtable(batch: List, url: str, fieldsToMergeOn: List[str] = None):
    payload = {
        "records": batch,
        "typecast": True,
    }
    response = None
    if fieldsToMergeOn:
        payload["performUpsert"] = {
            "fieldsToMergeOn": fieldsToMergeOn
        }
        response = requests.patch(url, headers=HEADERS, json=payload)
    else:
        response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(payload)
        print(response.json())
        raise Exception(
            "Request failed with status code {}. {}".format(
                response.status_code, response.text
            )
        )
    print("Batch has been uploaded successfully to the Airtable")
    return response.json()["records"]


def save_new_route_around_records_to_context_table(airtable_records, new_context_records_batch):
    new_airtable_records_df = map_airtable_route_around_data_to_dbx(airtable_records, df_mode=True)
    new_context_records_df = map_dbx_route_around_data_to_context_schema(new_context_records_batch, df_mode=True)

    result_df = (
        new_context_records_df
        .drop("airtable_id", "triage_status", "triage_result", "triage_description")
        .alias("new_context_records")
        .join(
            new_airtable_records_df
            .alias("airtable_df"),
            (
                (trim(col("new_context_records.identifier_value")) == trim(col("airtable_df.identifier_value")))
            ),
            "left"
        )
        .select(
            "new_context_records.*",
            "airtable_df.airtable_id",
            "airtable_df.triage_status",
            "airtable_df.triage_result",
            "airtable_df.triage_description",
        )
    )

    result_df = result_df.withColumn("created_at", current_timestamp()).withColumn("updated_at", current_timestamp())
    result_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(ROUTE_AROUND_CONTEXT_TABLE)


def sync_new_route_around_records():
    new_records = get_new_route_around_records(limit=1500)
    print(f"{new_records.count()} new records found")
    record_iterator = new_records.toLocalIterator()
    new_context_records_batch = []
    current_batch = []

    for row in record_iterator:
        mapped_record = map_dbx_route_around_data_to_airtable(row)
        current_batch.append(mapped_record)
        new_context_records_batch.append(row)
        if len(current_batch) == AIRTABLE_MAX_BATCH_SIZE:
            airtable_records = send_batch_to_airtable(
                batch=current_batch,
                url=ROUTE_AROUND_AIRTABLE_URL,
                fieldsToMergeOn=["identifier_value"],
            )
            save_new_route_around_records_to_context_table(
                airtable_records=airtable_records,
                new_context_records_batch=new_context_records_batch
            )
            new_context_records_batch = []
            current_batch = []

    if current_batch:
        airtable_records = send_batch_to_airtable(
            batch=current_batch,
            url=ROUTE_AROUND_AIRTABLE_URL,
            fieldsToMergeOn=["identifier_value"],
        )
        save_new_route_around_records_to_context_table(
            airtable_records=airtable_records,
            new_context_records_batch=new_context_records_batch
        )

    print("New Route Records uploaded to the Airtable.")


# COMMAND ----------

# MAGIC %md
# MAGIC ## Update Existing Router Around Records

# COMMAND ----------

ROUTE_AROUND_UPDATES_QUERY = f"""
    SELECT source.*, target.airtable_id
    FROM {ROUTE_AROUND_CONTEXT_TABLE} AS target
    JOIN jupiter_prod.jfa_metrics.route_around AS source
    ON target.identifier_value = source.identifier_value
    WHERE (
        target.a_uid IS DISTINCT FROM source.a_uid OR
        target.time_to_demotion_mins IS DISTINCT FROM source.time_to_demotion_mins OR
        target.demotions_stops_hours_uuid IS DISTINCT FROM source.demotions_stops_hours_uuid OR
        target.demotion_id IS DISTINCT FROM source.demotion_id OR
        target.demotion_timestamp IS DISTINCT FROM source.demotion_timestamp OR
        target.demotion_context__main_demotion_code IS DISTINCT FROM source.demotion_context__main_demotion_code OR
        target.halt_code IS DISTINCT FROM source.halt_code OR

        target.period_of_day IS DISTINCT FROM source.period_of_day OR
        target.route_around_type IS DISTINCT FROM source.route_around_type OR
        target.is_human_triggered_route_around IS DISTINCT FROM source.is_human_triggered_route_around OR
        target.is_auto_triggered_route_around IS DISTINCT FROM source.is_auto_triggered_route_around OR
        target.original_route_around_result IS DISTINCT FROM source.original_route_around_result OR
        target.auto_response IS DISTINCT FROM source.auto_response OR
        target.user_response IS DISTINCT FROM source.user_response OR
        target.request_time IS DISTINCT FROM source.request_time OR
        target.response_time IS DISTINCT FROM source.response_time OR
        target.genos_version IS DISTINCT FROM source.genos_version OR
        target.label IS DISTINCT FROM source.label
    )
"""

UPDATE_ROUTE_AROUND_CONTEXT_RECORDS_QUERY = f"""
    MERGE INTO {ROUTE_AROUND_CONTEXT_TABLE} AS target
    USING jupiter_prod.jfa_metrics.route_around AS source
    ON target.identifier_value = source.identifier_value
    WHEN MATCHED AND (
        target.a_uid IS DISTINCT FROM source.a_uid OR
        target.time_to_demotion_mins IS DISTINCT FROM source.time_to_demotion_mins OR
        target.demotions_stops_hours_uuid IS DISTINCT FROM source.demotions_stops_hours_uuid OR
        target.demotion_id IS DISTINCT FROM source.demotion_id OR
        target.demotion_timestamp IS DISTINCT FROM source.demotion_timestamp OR
        target.demotion_context__main_demotion_code IS DISTINCT FROM source.demotion_context__main_demotion_code OR
        target.halt_code IS DISTINCT FROM source.halt_code OR

        target.period_of_day IS DISTINCT FROM source.period_of_day OR
        target.route_around_type IS DISTINCT FROM source.route_around_type OR
        target.is_human_triggered_route_around IS DISTINCT FROM source.is_human_triggered_route_around OR
        target.is_auto_triggered_route_around IS DISTINCT FROM source.is_auto_triggered_route_around OR
        target.original_route_around_result IS DISTINCT FROM source.original_route_around_result OR
        target.auto_response IS DISTINCT FROM source.auto_response OR
        target.user_response IS DISTINCT FROM source.user_response OR
        target.request_time IS DISTINCT FROM source.request_time OR
        target.response_time IS DISTINCT FROM source.response_time OR
        target.genos_version IS DISTINCT FROM source.genos_version OR
        target.label IS DISTINCT FROM source.label
    ) THEN
    UPDATE SET 
        target.a_uid = source.a_uid,
        target.time_to_demotion_mins = source.time_to_demotion_mins,
        target.demotions_stops_hours_uuid = source.demotions_stops_hours_uuid,
        target.demotion_id = source.demotion_id,
        target.demotion_timestamp = source.demotion_timestamp,
        target.demotion_context__main_demotion_code = source.demotion_context__main_demotion_code,
        target.halt_code = source.halt_code,

        target.period_of_day = source.period_of_day,
        target.route_around_type = source.route_around_type,
        target.is_human_triggered_route_around = source.is_human_triggered_route_around,
        target.is_auto_triggered_route_around = source.is_auto_triggered_route_around,
        target.original_route_around_result = source.original_route_around_result,
        target.auto_response = source.auto_response,
        target.user_response = source.user_response,
        target.request_time = source.request_time,
        target.response_time = source.response_time,
        target.genos_version = source.genos_version,
        target.label = source.label
"""


def update_airtable_route_around():
    updated_records = spark.sql(ROUTE_AROUND_UPDATES_QUERY)
    print(f"{updated_records.count()} records to be updated")
    records = [{"fields": row.asDict()} for row in updated_records.collect()]
    data = {"records": records}
    for i in range(0, len(data["records"]), 10):
        payload = {
            "records": [],
            "typecast": True,
        }
        airtable_ids = []
        for field in data["records"][i: min(i + 10, len(data["records"]))]:
            airtable_id = field["fields"]["airtable_id"]
            if not airtable_id or airtable_id in airtable_ids:
                continue
            airtable_ids.append(airtable_id)

            record = {
                "id": airtable_id,
                "fields": {
                    "a_uid": swapped_demotions_a_uid_mapping.get(field["fields"]["a_uid"]) if field["fields"].get(
                        "a_uid") else None,
                    "time_to_demotion_mins": field["fields"].get("time_to_demotion_mins"),
                    "demotions_stops_hours_uuid": field["fields"].get("demotions_stops_hours_uuid"),
                    "demotion_id": field["fields"].get("demotion_id"),
                    "demotion_timestamp": safe_airtable_timestamp_format(field["fields"].get("demotion_timestamp")) if
                    field["fields"].get("demotion_timestamp") else None,
                    "demotion_context__main_demotion_code": field["fields"].get("demotion_context__main_demotion_code"),
                    "halt_code": field["fields"].get("halt_code"),
                    "period_of_day": field["fields"].get("period_of_day"),
                    "route_around_type": field["fields"].get("route_around_type"),
                    "is_human_triggered_route_around": field["fields"].get("is_human_triggered_route_around"),
                    "is_auto_triggered_route_around": field["fields"].get("is_auto_triggered_route_around"),
                    "original_route_around_result": field["fields"].get("original_route_around_result"),
                    "auto_response": field["fields"].get("auto_response"),
                    "user_response": field["fields"].get("user_response"),
                    "request_time": safe_airtable_timestamp_format(field["fields"]["request_time"]) if field[
                        "fields"].get("request_time") else None,
                    "response_time": safe_airtable_timestamp_format(field["fields"]["response_time"]) if field[
                        "fields"].get("response_time") else None,
                    "genos_version": field["fields"].get("genos_version"),
                    "label": field["fields"].get("label"),
                }
            }
            payload["records"].append(record)
        response = requests.patch(
            url=ROUTE_AROUND_AIRTABLE_URL,
            headers=HEADERS,
            json=payload,
        )
        if response.status_code == 422 and response.json()['error']['type'] == 'ROW_DOES_NOT_EXIST':
            record_id = response.json()['error']['message'].split(' ')[2]
            print(payload)
            raise Exception(f"Route around record {record_id} doesn't exist")
        elif response.status_code != 200:
            print(payload)
            print(response.json())
            error_message = "Request failed with status code {}".format(response.status_code)
            raise Exception(error_message)
    print("Updated route around records in AIRTABLE")


def update_route_around_context_records():
    spark.sql(UPDATE_ROUTE_AROUND_CONTEXT_RECORDS_QUERY)


# COMMAND ----------

def update_existing_route_around_records():
    update_airtable_route_around()
    update_route_around_context_records()


# COMMAND ----------

def sync_route_around_data():
    create_route_around_context_table()
    sync_route_around_triage_info()
    sync_new_route_around_records()
    update_existing_route_around_records()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Execution section

# COMMAND ----------

# MAGIC %md
# MAGIC Section to run the sync flows. Please, comment parts of the flow you'd like to skip.

# COMMAND ----------

process_demotions_updates()
process_airtable_updates()
cleanup_airtable()
process_databricks_changes()
patch_pre_signed_to_airtable()
assert_no_detached_records()
delete_unprocessable_records()
sync_route_around_data()

# COMMAND ----------

dbutils.jobs.taskValues.set("task_status", "success")
dbutils.jobs.taskValues.set("task_duration", time.time() - start_time)