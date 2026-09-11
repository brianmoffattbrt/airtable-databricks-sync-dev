# Legacy Integration and Planning Context

This is curated context, not another current rule specification. Use [as-is automations](../as-is/automations.md) for captured settings, [manual catalog](../as-is/manual-processes.md) for source status, and [target contracts](../target/platform-app-contract.md) for proposals.

## Systems and ownership

- Existing development history is preserved from airtable-databricks-sync-dev. Its root notebooks remain unchanged compatibility entry points, not the new backend.
- Mesa's [source notebook](https://github.com/BlueRiverTechnology/mesa-autonomy-triage/blob/b277e47f569425e262b53f340f7d7af0a07b46e9/infrastructure/modules/workflows/notebooks/dbx_airtable_sync_notebook.py) belongs to a separately managed integration. That inspected revision uses secret-configured deployment targets. No secret values or current deployed job binding are established here.
- The Mesa repository defines its own Terraform job, hourly schedule, service identity, permissions, and main-branch release workflow. Do not import those resources into this project as a default deployment.
- Local Streamlit/AI prototypes are reference only. Schema readers and declared output mappings do not prove active writeback or identify the platform team's app.

## Immediate data flow

The inspected source selects candidate demotions from `jupiter_prod.jfa_metrics.demotions_stops_hours` and compares VIN, UTC timestamp, and demotion flag against context. It constructs A_UID as `VIN | timestamp` and sends PATCH with performUpsert on A_UID. The function name send_data_to_airtable does not mean every call creates a new row or reruns A-1.

Payloads supply original code/link, preceding stop, and path inputs. Airtable rules then write their captured outputs. Main-sync conversion reads those triage fields, including Investigation Complete, and resolves several linked/lookup fields from their first element. The separate mirror joins linked IDs and defaults to a 100-record dev pull. Neither is a complete event-history proof.

See [mapping distinctions](COLUMN_MAPPING.md), [mirror notes](DEMOTION_TRIAGE_FULL_ARCHITECTURE.md), and [legacy README](legacy-dev-sync.md). The old assertion that separate dev tables guarantee no production impact is withdrawn: shared reference creation and production route-around write paths exist. Setup must not run the notebooks.

## Known documentation corrections retained

- A-2–A-6 write combined assessment/reviewer; A-7–A-13 write breakout position/turn; A-14 writes headlands completion.
- A-26/A-27 use imported code, not MAIN. A-28–A-33 use MAIN.
- A-29 reads MAIN_SparkURL_Manual; the human supplies its marker/reference. The outputs of A-29 are automated.
- A-31 has an initial update followed by one selected branch; it is not one asserted atomic write.
- A-33 includes 12.29 and an explicit three-value location whitelist.
- A-34–A-37 do not have an incomplete-investigation prerequisite. Process lookup membership/exactness is not interchangeable.
- A-38's four criteria/Otherwise and A-40's five-field watcher/ordered scope tree supersede earlier shorthand.
- A_UID is stored text, Investigation Complete a choice, and Confirmed JRM Link a linked field. Older different-base/formula/checkbox/URL descriptions are not this captured workflow.
- Automation-use lists, field names, low populations, and success of one sync do not establish column deletion safety.

## Manual source context not independently recertified

The detailed old migration document described headlands assessment; selecting a main Spark engagement; manual-mask perception classification; object location; human/vehicle details; camera metadata; human-to-vehicle correction; and non-navigable misuse details. Its summary used conflicting TP numbering. Workload percentages, time estimates, old 120-column/36-field counts, and guessed gates are historical, not current validation.

The source-described masked-perception classification mapping was human → 12.24, vehicle → 12.27, route-aroundable classes → 12.X1, false-positive classes → 12.X2, and non-route-aroundable objects → 12.29. A separate unknown row mentioned 12.107 while the output list omitted it. It described adding a classified code to existing secondary links. Preserve these as source-described facts/questions; do not silently implement a replacement/append rule or turn the mapping into an approved automatic classifier.

The old non-navigable detail notes labeled Stationary Object/Equipment as No Misuse, while captured A-31 explicitly selects Stationary Object/Equipment - Potential Error. The new manual contract must resolve that mismatch. Other named source categories included vegetation, water/hole, debris/rock, animal, mapped movable objects, and unmapped movable objects, but a complete current enum/procedure is not certified by those notes.

## Superseded migration/cleanup ideas

Older documents proposed triage_processes/triage_process_status tables, computed views, reviewer-to-email conversion, timestamp conversions, and direct SQL updates. Those are not deployed facts or migration-ready equivalents. Do not execute their SQL or convert choices to timestamps merely because an old table suggested it. Historical snippets retained in the as-is evidence appendix remain labeled non-authoritative; code/comments in retained source files are not silently changed into tested logic.

The known A-1 late reset is documented but unmitigated. The previous 17.0 classification reversals were owner-explained manual policy changes, a different issue. A-39 retirement, initialization gating, field deletion, historic repairs and production cutover require their own approved behavior/data plans.

## Existing Databricks checkout

Read-only setup research found Git folder 2599207419438391 at `/Repos/brian.moffatt@bluerivertech.com/airtable-databricks-sync-dev`, main at `a323693ecffc5964aaaedf6133579c081b3cbe96`. The two notebooks match source HEAD a9e61158c26f5e1251d16bdee77c17ec4ff41681. No direct matching reference was found among 62 visible jobs; visibility and indirect/manual-use limits remain.

The workspace checkout is preserved. Making/transferring the GitHub repository private can require Git access updates before a future pull. No pull/re-link/rename, credential change, validation Git folder, or notebook/job execution is included in this baseline setup. One preserved checkout is not a second GitHub repository.
