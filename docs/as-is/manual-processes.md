# Manual Process Baseline

**Status: source-backed catalog with explicit gaps, not a complete/live manual-workflow certification.** Brian requested a catalog of all documented candidates and a concrete TP-7 handoff, rather than blocking Git setup on a new full manual audit.

The [A-X specification](automations.md) documents automated actions. Manual TP outputs can become their inputs; this does not make A-X actions manual. The future UI is owned by the platform team. Its [proposed DBX contract](../target/platform-app-contract.md) is a separate target specification.

## Identity rules

- Brian explicitly identified TP-7 as Objects Outside Field. Preserve that label.
- A legacy summary renumbered tasks inconsistently: TP-7 there means Vehicle Camera Details, while the detailed source calls that TP-10. Do not silently adopt that summary or change established identifiers.
- Descriptive `process_key` values below are proposed target keys, not claims about existing Airtable IDs or an accepted platform API.
- Preserve source aliases until the owner/platform team agree on target identifiers. Prototype prompt IDs are not proof of manual task identity or live writeback.

## Catalog

The nine rows are documented candidates, not proof of nine currently enabled manual processes. Shared current context is the captured demotion record, its reference lookups, and relevant Spark/map evidence. Older SQL examples naming `demotion_context`/`unique_id` do not certify a deployed read/write/key contract.

| Candidate / proposed key | Source labels | Known inputs | Source-described outputs | Status and exact remaining question |
|---|---|---|---|---|
| Headlands assessment / `headlands_assessment` | Detailed TP-1 | Path/computed-path context; map/field position | Legacy notes name Headlands vs Interior and Headlands Turn; combined assessment is consumed by A-7–A-13 | DRAFT: confirm whether the human writes the combined assessment or breakout values, full choices, and fallback eligibility |
| Spark selection / `spark_engagement_selection` | Detailed TP-3; other sources/summary TP-2 | SparkAI Query URL, available primary/other engagement references | MAIN_SparkURL_Manual: selected reference or missing marker | Manual marker boundary CONFIRMED by Brian; target explicit missing/pending representation and selection contract remain DRAFT |
| Masked-perception classification / `manual_mask_perception_classification` | Detailed TP-4; summary TP-3 | Masking, MAIN, Spark, existing secondary codes | Secondary Demotion Manual code selection; source describes ADD, not replacing earlier code | DRAFT: confirm append/correction behavior, eligibility and unknown case. The source table mentions 12.107 but the output list omits it |
| Objects Outside Field / `objects_outside_field` | TP-7, owner-identified; summary TP-4 | Selected Spark reference; map and headlands context when ambiguous | Vehicle/Object Outside Field | Worked draft target contract exists; source choice spelling/case differs from captured A-X choices |
| Human details / `human_detection_details` | Detailed TP-8; summary TP-5 | Selected Spark reference for MAIN 12.24 | Occluded by LO?; Human Detection Details | DRAFT: complete enum lists, missing/uncertain handling and procedure. Source option cells are blank and vehicle steps are copied |
| Vehicle details / `vehicle_detection_details` | Detailed TP-9; summary TP-6 | Spark; conditional map/headlands for MAIN 12.27 | Vehicle Type; Vehicle On/Off Road; Vehicle Parked/Driving | DRAFT: complete enum lists and missing/uncertain handling; source option cells are blank |
| Camera details / `vehicle_camera_details` | Detailed TP-10; summary TP-7 | Spark reference/metadata for MAIN 12.27 | camera_name | DRAFT: which camera property/allowed values and whether this should be automatic metadata extraction; copied vehicle procedure is not evidence |
| Human-to-vehicle correction / `human_changed_to_vehicle` | Detailed TP-11; summary TP-8 | Related-engagement query/reference for MAIN 12.27 | Human Change to Vehicle reference | DRAFT: how to identify correction, multiple matches, no-match versus not-reviewed; source procedure is copied |
| Non-navigable misuse detail / `nonnavigable_object_misuse_details` | Detailed TP-15; summary TP-9 | MAIN 12.29, inside-field assessment, Spark | NonNavigable Object Misuse Details | DRAFT: complete accepted choices/procedure. A-31 confirms Movable UNMAPPED Object - Misuse and Stationary Object/Equipment - Potential Error; older notes call stationary No Misuse |

## Sources and limitations

- [TP-7 source](../reference/protocols/tp-07-source.md): useful purpose, context and decision matrix; not the authority for exact captured A-X enum spelling.
- [TP-8 source](../reference/protocols/tp-08-source.md), [TP-9 source](../reference/protocols/tp-09-source.md), [TP-10 source](../reference/protocols/tp-10-source.md), [TP-11 source](../reference/protocols/tp-11-source.md): incomplete historical sources, with live examples redacted.
- Other candidates come from the detailed sections of the earlier column/migration working document, summarized in [legacy context](../reference/legacy-context.md) and [source inventory](../reference/source-inventory.md). Old workload percentages, dates, gates, and estimates are not recertified.
- The field worksheet provides selected type/example facts, not complete enum catalogs or deletion proof; see [field contracts](../reference/field-contracts.md).

## Not automatically manual tasks

- The detailed TP-2 Manual Masking Assessment describes the A-15–A-25 automation group, not a human output step to reproduce in the app.
- Historical TP-12/13/14/16/17/18 labels identify A-X predecessors, not new manual procedures.
- The prototype `tp-12` image-quality prompt is a different namespace; it is not automatically a required manual TP or an approved automatic replacement.
- Archived TP-5/6 placeholders are not defined new workflows.
- The OFF automation named TP-1 is separate from the conceptual human headlands task.

## Immediate A-X dependencies

- Headlands assessment values can feed A-7–A-13 and A-14; exact human output ownership must be settled before implementing that TP.
- Manual secondary code selections can feed A-16–A-25 through linked codes/reasons. Preserve sets, not just a first code.
- The manually supplied missing marker feeds A-29; blank/unreviewed is not automatically missing.
- Object location feeds A-31–A-33; non-navigable details feed A-31's two named branches/Otherwise.
- Other manual outputs can serve reporting, metadata enrichment, or future consumers without a direct captured A-X reader. Absence of an A-X reader is not deletion permission.

## What remains outside this baseline

Free-form investigation, final manual overrides, correction/reopening workflows, additional unlisted tasks, app authorization, deployed table bindings, and full manual coverage require later confirmation before Airtable removal. Do not invent new TP numbers for them or call the entire manual workflow complete. Existing source evidence is reused; ask only specific missing contract questions when a TP is implemented.
