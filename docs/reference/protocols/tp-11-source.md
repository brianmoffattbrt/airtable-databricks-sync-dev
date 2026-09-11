# TP-11 Source: Human Changed to Vehicle

**Incomplete historical source, curated for Git.** The purpose concerns human-to-vehicle corrections, but the procedure copies vehicle/road/motion steps. It does not establish no-match/completion semantics or an accepted correction-detection procedure. Live links are redacted; original SQL/comments remain reference only. See the [manual catalog](../../as-is/manual-processes.md).

**Purpose:** Protocol for 12.27, confirmed vehicle detection, to determine if any of the related spark engagements were first for a detected human, but spark corrected them to a vehicle detection.

## Filters for Analyzed Demotions

- **Confirmed Halt Code** = 12.27
- **Machine Group = **customer, demo, or engineering
- Example query:

```
SELECT
    t1.unique_id
FROM
    jupiter_prod.jfa_metrics.demotion_context AS t1  -- The table with the demotion codes
INNER JOIN
    jupiter_prod.jfa_metrics.machine_information AS t2 -- The table with the VIN group info
    ON t1.vin = t2.vin 
WHERE
    t1.main_demotion_code IN ('12.27') -- Filter for specific confirmed demotion codes for vehicles
    AND t2.system = 'bedrock' -- Filter for system type
    AND t2.machine_type IN ('customer', 'demo', 'engineering') -- Filter for machine group
```

## Required Inputs

Airtable columns required to perform this operation

- **SparkAI Query URL**

## Required Outputs

- **Human Change to Vehicle**

## Protocol

1. **Open Spark Engagement by clicking the “MAIN\_SparkURL\_Manual”**
    1. Example = [live engagement example omitted; the app receives its reference at runtime] 
2. **Open up the “Viz Map” by clicking the “Autonomy state transition history”**
    1. Example = [live vehicle/map example omitted; use the runtime visualization reference]
3. **Determine the “Vehicle Type”**

| **Option** | **Example** |
| --- | --- |
|  | - Truck or car that you would see normally driving down a road - Passenger trucks do drive into the fields as seen in the second image |
|  | - Golf cart like vehicle, green/black in color - Usually driving in interior of field |
|  | - Farming or Industrial vehicle, not something typically seen on the road  - **IMPORTANT:** Identify another tractor as in image one, especially if driving on interior of field. |
|  | - Vehicle does not fit any of the above categories |

1. **Determine the “Vehicle On/Off Road”**

| **Option** | **Example** |
| --- | --- |
|  | - Cars all on clearly defined road - If Unclear, use viz map to help confirm tractor is near road  - Headlands Assessment can also be used to confirm, more likely for Headlands Pass, Headlands Turn/Transition |
|  | - Cars clearly OFF road - If unclear, viz map can help confirm tractor is not near road  -  - Car can still be NEAR road, but not on it. Below example is still considered OFF ROAD |

1. **Determine the “Vehicle Driving/Parked”**

| **Option** | **Example** |
| --- | --- |
|  | Indicators can be: - Vehicle on Road - Dust trailing behind vehicle, indicating movement - Vehicle behind implement while implement is moving, must be driving to be in that position Spark Images can be “Played” to see multiple frames to help determine |
|  | Indicators can be: - People near vehicle or leaning up against it - Logical place to park - Vehicle on dirt, NO DUST behind the vehicle that would indicate movement. “Playing” the spark image can help confirm vehicle is not moving/parked |
