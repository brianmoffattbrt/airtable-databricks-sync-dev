# Decisions and Change Register

This small register separates repository choices, proposed target contracts, and actually applied business changes. Git history preserves previous versions; this is not a substitute for live-system change evidence.

| ID | Decision | Status | Scope / consequence |
|---|---|---|---|
| R-01 | Rename the existing repository to brianmoffattbrt/triage-workflows under the same work account | APPLIED: rename verified, repository ID 1362874924 retained | Supersedes the organization-transfer proposal; one GitHub repository and unchanged history |
| R-02 | Keep existing PUBLIC visibility and publish the reviewed baseline/tag | EXPLICITLY APPROVED by Brian | Supersedes private-first proposal; no visibility or protection changes. Secret scanning/push protection verified enabled after rename |
| R-03 | Keep original local files and the existing DBX Git checkout | APPROVED | No workspace pull/re-link/rename/job execution during setup; no private-auth transition introduced; future refresh is not newly validated |
| R-04 | Keep legacy notebook paths/content, isolate imported offline utilities | APPROVED | Root notebooks are compatibility entry points, not the new engine |
| R-05 | Platform team owns the UI/media retrieval; this repo owns backend/contracts | APPROVED | No duplicate app import |
| R-06 | Curate additions, preserve existing Git history | APPROVED | Redact unnecessary new incident/media examples; no retroactive history sanitization or raw export publication |
| C-01 | Shared review-task read view, separate manual-submission write table, backend-owned state | PROPOSED | Names, schema, grants, ingestion and concurrency enforcement are not implemented or accepted by the platform team |
| C-02 | Descriptive process keys with TP aliases | PROPOSED | TP-7 meaning is owner-confirmed; other numbering conflicts remain explicit |
| C-03 | Preserve captured TP-7 output spellings in the compatibility draft | PROPOSED | UI display labels can differ only through explicit mapping; no silent Impassible/Impassable rename |
| A-01 | Prevent late initialization from reopening completed investigations | OPEN TARGET DESIGN | A-1 overwrite remains observed/unmitigated. No gate or new default field was implemented during documentation/Git setup |
| A-02 | Determine ownership/precedence for competing MAIN/operator/classification writers | OPEN TARGET DESIGN | A-number order is not scheduler priority; no silent merge into one guessed winner |
| A-03 | Decide whether A-39 is retained/replaced/retired | OPEN; KEEP pending decision | Complete configuration documentation is not a redundancy proof |
| A-04 | Define manual correction and reclassification semantics | OPEN TARGET DESIGN | Baseline condition-entry rules do not continuously recompute after every manual edit |

## Adding a substantive change

Record affected A-numbers/TPs/fields, baseline behavior, desired behavior, rationale, status, compatibility impact, and the eventual code/test or live-change evidence. Use these statuses consistently:

- **Proposed:** desired design only.
- **Approved design:** accepted behavior/contract; not necessarily deployed.
- **Applied in Airtable:** actual source change, with evidence/currentness identified; update as-is documentation.
- **Implemented in DBX/app contract:** code/spec implementation, not proof of deployment.
- **Deployed/verified:** exact environment/version and observed checks recorded.

Do not label a proposed rule fix as applied because its document was merged. Couple code/contracts/docs when implementation changes them, and coordinate breaking app keys/types/enums with the platform team. Typo corrections need not create a new decision entry. No security-policy changes, data repair, A-39 retirement, or production rollout are authorized by this register alone.
