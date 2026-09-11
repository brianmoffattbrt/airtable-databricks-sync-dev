# TP-7 Source: Objects Outside of Field

**Historical source, curated for Git.** Example record/media links are redacted; source SQL/comments and decision guidance are retained as reference, not certified deployed queries. The source's Obvious/Potential casing and Impassable spelling differ from the captured A-X choices. Use the exact output mapping in the [draft app contract](../../target/platform-app-contract.md). This is not a second target specification.

**Purpose:** Protocol for determine if the classified object from a “Confirmed” Halt Code 12.27 (Vehicle), 12.24 (Human), or 12.29 (Large Object Non-Navigable) was inside or outside of the field at the time of detection.

## Filters for Analyzed Demotions

- **Confirmed Halt Code** = 12.24, 12,27, 12.29
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
    t1.main_demotion_code IN ('12.24', '12.27', '12.29') -- Filter for specific confirmed demotion codes
    AND t2.system = 'bedrock' -- Filter for system type
    AND t2.machine_type IN ('customer', 'demo', 'engineering') -- Filter for machine group
```

## Required Inputs

Airtable columns required to perform this operation

- **MAIN\_SparkURL\_Manual (Required)**
    - This is manually pulled from TP-2 Find Spark Engagement
    - That process manually pulls the “MAIN\_SparkURL\_Manual” from “SparkAI Query URL” = jupiter\_prod.jfa\_metrics.demotion\_context.SparkAI\_query\_URL 
- **Autonomy state transition history ***(Required only if Spark Engagement not Obvious)*
    - Field Visualization Map or “Viz Map”
    - Satelite map, used to visualization the position of the tractor 
- **Headlands Assessment ***(Required only if Spark Engagement not Obvious)*
    - Result of the Headlands Assessment.
    - Helps determine if tractor is near the edge of the field (Headlands Pass, Headlands Turn/Transition) or Interior of Field (Interior Pass)

## Required Outputs

- **Vehicle/Object Outside Field**
    - Options 

## Protocol

1. **Open Spark Engagement by clicking the “MAIN\_SparkURL\_Manual”**
    1. Example =[live engagement example omitted; the app receives its reference at runtime] 
2. **Open up the “Viz Map” by clicking the “Autonomy state transition history”**
    1. Example = [live vehicle/map example omitted; use the runtime visualization reference]
3. **Determine if the Vehicle, Human or Object is Inside or Outside of the Field**
    1. Enter result into “Vehicle/Object Outside Field”
    2. Use the a combination of the Spark Options are
        1. Inside Field (Obvious)
        2. Outside Field (Obvious)
        3. Outside Field (Potential)
        4. Interior Impassable
        5. N/A - Spark Error (*if no spark engagement available*)
    3. To make final assessment use the following Decision Matrix and Visual Examples below

### Decision Matrix

| **Datapoint** | **Inside Field (Obvious)** | **Outside Field (Obvious)** | **Outside Field (Potential)** | **Interior Impassable** |
| --- | --- | --- | --- | --- |
| Spark Engagement | - No distinguishable field boundary/edge of field between tractor and object. | - Edge of field obvious and object is outside of it.  - Fence or tree line clearly outside of the field. | - Possible edge of field detected, but unclear. - Edge of field is clear, but comparative object location not | - Object appears to be outside of the field, or an object in the middle of the field. |
| Headlands/Pass | - Usually interior pass - Can be headlands pass/turn, need to confirm viz map and spark image though. | - Almost always on a Headlands Pass, Headlands Turn, or Headlands Transition - Can technically be on an interior pass, but will still be near edge of field, confirm with viz map in this case. | - Headlands pass but object alignment uncertain | - Usually Interior Pass, can be any though. |
| Map/Satellite | - If in middle of field, clearly Inside Field - If near edge, try and orient camera direction with vehicle heading to determine location of object. | - Tractor is confirmed to be near edge of field | - Tractor is confirmed to be near edge of field | - Should show red interior boundary around interior obstacle. -  Or at least evidence of path planning going around an object. |

### **Visual Examples**

- **Inside Field (Obvious): **Spark Engagement
    - Clearly close to the tractor with no clear edge of field in sight.
    - Edge of field visible, and object clearly inside.

**Inside Field (Obvious): **Viz Map

- Machine in middle of field helps support this but is NOT required
- If machine near edge of field, try and orient tractor direction from heading arrow and spark image, and confirm if camera pointed towards interior of field.
- If near edge of field, and not clear from viz map/spark engagement, may need to adjust to outside field (potential)

**Outside Field (Obvious): **Spark Engagement

- Edge of field obvious and object is outside of it. 
- Fence or tree line clearly outside of the field.  

**Outside Field (Obvious): **Viz Map

- Confirms vehicle is near the edge of the field 

**Outside Field (Potential): **Spark Engagement

- If edge of field is visible, but it’s difficult to tell if the object is inside or outside that edge. 
- From viz map, you can tell that tractor is near edge of field, but visually in spark engagement edge of field may not be super well defined.
- Object/person may be basically right on the perceived edge of the field.

**Outside Field (Potential): **Viz Map

- Viz map confirms tractor is near edge of field, but again from spark engagement, it’s difficult to tell if the object is truly outside of the field. 

**Interior Impassable: **Spark Engagement

- Can be obviously a structure that is inside of the field
- Most times it looks the same as tress that are outside of the field, only after reviewing viz map is it clear that it’s an interior obstacle (red outlined area on interior of field)

**Interior Impassable: **Viz Map

- See red outlined area as an interior obstacle. Although sometimes can be slightly offset as seen. 
- Some maps will not generate perfectly, second viz map is clearly routing around an interio obstacle, but no red outline is shown.

**N/A - Spark Error:**

- No Spark Image available, so no determination can be made
