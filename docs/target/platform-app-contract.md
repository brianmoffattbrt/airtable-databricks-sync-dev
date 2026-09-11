# Platform App Contract

**Status: DRAFT, version `draft-0.1`.** These are proposed interfaces for discussion with the platform team. No objects, grants, app features, ingestion jobs, or enforcement described here have been created or verified by repository setup. Production bindings remain unassigned. The platform team owns the app and resolves Spark engagement IDs/URLs into media.

The [manual baseline](../as-is/manual-processes.md) records source evidence and gaps; [captured A-X rules](../as-is/automations.md) record current selected automation settings. This contract is not a claim that those settings have already been migrated.

## 1. What the app reads

Proposed dev read object **R**: `jupiter_dev.brianm.triage_review_tasks`, a view of prepared review tasks. Catalog/schema and existence/access must be agreed before implementation. The name is a proposal, not a command to query a currently available object.

The view is produced from DBX-owned event facts, reference catalogs, current derived state, and accepted manual inputs. Its grain is an event/process/input-revision task. Ongoing production must not depend on Airtable API lookups, Airtable record IDs, or the old limited dev mirror to supply these values.

| Common read field | Proposed type | Contract |
|---|---|---|
| event_id | STRING | Opaque DBX-native key supplied by backend; app returns it unchanged |
| process_key | STRING | Proposed descriptive key from the per-process matrix; TP labels are display/source aliases |
| input_revision | STRING | Opaque revision of the relevant review inputs, returned unchanged on submission |
| contract_version | STRING | Schema/contract version used to interpret the task |
| event_timestamp_utc | TIMESTAMP | Event context with explicit UTC convention and source precision |
| main_demotion_codes | ARRAY<STRING> | Preserve code strings and multiplicity, not a floating point or first-link-only representation |
| system, machine_type | STRING | Context for approved eligibility/cohort filters, not new predicates inserted into A-X definitions |
| main_spark_engagement_id | STRING, nullable | Stable selected engagement reference where available |
| main_spark_engagement_url | STRING, nullable | Selected engagement URL where available; no embedded credentials |
| spark_selection_status | STRING | Proposed distinction between pending, selected, and explicitly missing evidence; not inferred from blank URL alone |
| viz_map_url | STRING, nullable | Relevant visualization reference, required by applicable TP logic when evidence is ambiguous |
| headlands_assessment | STRING, nullable | Current assessment context; distinguish unknown/unreviewed from explicit choices |

Additional fields are process-specific below. This is not a final DDL. The actual event-key derivation/backfill mapping must be validated against authoritative source keys. Legacy examples of `unique_id` and VIN/timestamp joins do not by themselves establish a safe production key. The app must not reconstruct event IDs from timestamps or Airtable IDs.

### Media responsibility

The app retrieves/renders Spark media using supplied engagement references and its approved authentication. This repo does not implement another image downloader during setup. The backend supplies selected references and context. Distinguish explicit no-evidence outcomes from pending selection, authorization problems, expired links, and temporary fetch failures. Do not turn a transient app error into A-29's missing marker automatically.

## 2. What the app writes

Proposed dev write object **W**: `jupiter_dev.brianm.triage_manual_results`, a table of manual submissions. The proposed automation-owned projection is `jupiter_dev.brianm.triage_state`. The app does not directly overwrite that projection or arbitrary `demotion_context` columns.

| Submission field | Proposed type | Requirement |
|---|---|---|
| submission_id | STRING | Required; stable unique request ID reused for retries of the same submission |
| event_id | STRING | Required; exact key from R |
| process_key | STRING | Required; exact task process key |
| input_revision | STRING | Required; exact input revision reviewed |
| contract_version | STRING | Required; version governing the payload |
| reviewer_subject | STRING | Required; trusted identity from the authenticated app/backend, not a user-editable impersonation field |
| reviewed_at_utc | TIMESTAMP | Required; trusted UTC submission/review time, not a fixed CST conversion |
| output_payload_json | STRING | Required; JSON text conforming to that process's typed field/enum contract |

JSON text is a portable initial representation proposal, not permission to accept arbitrary unvalidated keys. A typed alternative can be agreed with the platform team before DDL implementation. Use parameterized writes or an approved service interface, not SQL string interpolation of user input.

### Required behavior, not yet implemented

- Append submissions rather than editing automation-owned state. UC MODIFY permission alone does not enforce append-only behavior.
- Same submission ID and same payload is idempotent; same ID with different content is a conflict, not silent replacement. Informational Delta keys alone do not enforce this.
- Validate identity, process/version, fields/types/enums, caller authority, and input revision before applying a result.
- Stale results must be rejected or retained-but-not-applied, not silently applied to changed inputs.
- A correction is a new submission. How competing/corrected submissions supersede prior accepted results remains an explicit backend/platform decision; do not assume largest timestamp is sufficient.
- Only accepted results become inputs to affected automatic rules. Completing one TP does not directly set Investigation Complete, Triage Activities Complete, final classification, operator status, or In Scope.
- A human override of an automation-owned output requires a separately specified override capability; do not infer it from generic form write access.

## 3. Four-part contract by manual process

R and W are the full proposed object names above; they apply to every row. Proposed payload keys are not claims of existing physical DBX fields. The matrix is a draft handoff, not a certification that every manual procedure is complete.

| Process / source alias | Read object | Required inputs beyond common identity | Write object | Required output / pending contract |
|---|---|---|---|---|
| headlands_assessment / TP-1 | R | Path/computed-path, map/position context | W | Pending owner decision: combined headlands_assessment versus breakout pair, complete choices and fallback eligibility |
| spark_engagement_selection / detailed TP-3, alias TP-2 | R | Search reference, available primary/other engagements, event context | W | Proposed selected engagement ID/URL plus explicit selection outcome. Manual missing boundary is confirmed; target normalization is not an already applied A-29 change |
| manual_mask_perception_classification / detailed TP-4 | R | Masking, MAIN set, current secondary set, selected Spark | W | Proposed secondary code selection with explicit add/replace/correction intent. Preserve source-described append behavior as a question; resolve 12.107 unknown case |
| objects_outside_field / TP-7 | R | Selected Spark; conditional map/headlands context | W | vehicle_or_object_outside_field STRING; exact compatibility values below |
| human_detection_details / TP-8 | R | Selected Spark, MAIN 12.24 context | W | Proposed occluded_by_lo and human_detection_details; complete enums/types for the target and missing-value handling still pending |
| vehicle_detection_details / TP-9 | R | Selected Spark; conditional map/headlands, MAIN 12.27 | W | Proposed vehicle_type, vehicle_on_or_off_road, vehicle_parked_or_driving; complete enums/uncertain handling pending |
| vehicle_camera_details / TP-10 | R | Selected Spark/camera metadata, MAIN 12.27 | W | Proposed camera_name; exact metadata property, values, error outcomes and manual-versus-auto ownership pending |
| human_changed_to_vehicle / TP-11 | R | Related-engagement search, original/resolved class context | W | Proposed correction engagement reference/outcome; no-match versus not-reviewed and multiple matches pending |
| nonnavigable_object_misuse_details / detailed TP-15 | R | MAIN 12.29, inside-field assessment, selected Spark | W | Proposed nonnavigable_object_misuse_details choice; full choices/procedure pending, preserving A-31's confirmed two named branch values |

No invented TP renumbering, field enum, or source procedure fills a pending cell. Resolve the specific gap when preparing that process for implementation. Do not reopen the entire A-X capture audit.

## 4. Worked TP-7 handoff

### Read object

R, with proposed process_key `objects_outside_field`, display label TP-7 / Objects Outside Field. Its task filter is not yet implemented. The historical protocol identifies MAIN codes 12.24/12.27/12.29 and bedrock customer/demo/engineering cohorts. Confirm queue rules rather than silently filtering all A-X execution or treating historical gates as runtime ordering guarantees.

### Required inputs

- Opaque event_id, input_revision, contract_version and process_key.
- MAIN code set containing the relevant detected-object classification.
- Selected Spark engagement ID or URL when available; platform app resolves media.
- Explicit evidence-selection status, including an approved no-evidence path rather than treating every absent URL as missing.
- Visualization map and headlands context when Spark evidence is ambiguous, as described by the source protocol. Missing conditional context is not silently treated as proof of outside field.

### Write object

W. Submit only this TP's manual result and the common envelope. Do not write final classification, bug/operator status, investigation/headlands/activities completion, or scope directly from this form.

### Required output

`vehicle_or_object_outside_field`: STRING, exactly one of the compatibility-draft values:

| Stored value | Meaning / constraint |
|---|---|
| Inside Field (OBVIOUS) | Clear inside-field assessment |
| Outside Field (OBVIOUS) | Clear outside-field assessment |
| Outside Field (POTENTIAL) | Supported but uncertain outside-field assessment, not generic missing data |
| Interior Impassible | The exact spelling selected by the captured A-X rules |
| N/A - Spark Error | Explicit no-Spark assessment outcome; do not infer from a transient fetch/auth problem |

Older source text uses Obvious/Potential title case and Impassable. The captured A-X values use OBVIOUS/POTENTIAL and Impassible. Preserve stored values for this draft; friendly UI labels require explicit mapping. Any target enum correction must update affected rules/tests/contracts as an intentional versioned change.

### Synthetic example

This is an illustrative contract record, not production data or an existing table response:

```json
{
  "event_id": "example-event-001",
  "process_key": "objects_outside_field",
  "input_revision": "example-input-revision-1",
  "contract_version": "draft-0.1",
  "main_demotion_codes": ["12.27"],
  "main_spark_engagement_id": "example-engagement-001",
  "spark_selection_status": "selected",
  "headlands_assessment": "h - Headlands Pass"
}
```

Illustrative submission; the real app/backend supplies trusted identity/time and a unique request ID:

```json
{
  "submission_id": "00000000-0000-4000-8000-000000000001",
  "event_id": "example-event-001",
  "process_key": "objects_outside_field",
  "input_revision": "example-input-revision-1",
  "contract_version": "draft-0.1",
  "reviewer_subject": "example-reviewer",
  "reviewed_at_utc": "2026-01-01T00:00:00Z",
  "output_payload_json": "{\"vehicle_or_object_outside_field\":\"Outside Field (OBVIOUS)\"}"
}
```

### Downstream relationship

Accepted object location becomes an input to A-31–A-33 counterparts, still subject to their other conditions. A-31 also requires nonempty object-misuse details. N/A - Spark Error is not in A-33's whitelist. A completed TP-7 review is not proof the investigation or overall activities are complete. Reclassification after later corrections is a target design decision; baseline condition-entry rules do not continuously rerun just because an output/input is edited.

## Acceptance before the platform team relies on this contract

Agree on physical environment bindings/existence/grants; event identity; complete per-TP schema/eligibility and outcomes; media/access ownership; server-side validation; idempotency/stale/correction behavior; and contract version compatibility. These are specific target implementation decisions. Repository setup records the draft accurately and does not create objects or claim platform acceptance.
