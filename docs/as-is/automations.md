# Airtable Automation Specification — Captured A-1 through A-40

## Scope and documentation status

**Repository curation:** This is the versioned copy of the accepted capture, not a fresh Airtable export. Incident records below use redacted case aliases; the 14 raw A_UID examples are omitted. Original owner-held evidence is retained outside Git. Configured reference IDs, field identities, native operators, assignments, and code/choice labels are preserved. Source paths are replaced by portable references; the reference catalog is a snapshot, not a live-deployment certification.

**Authority:** The numbered definitions, shared contracts, dependency catalog, and evidence register ABOVE the preserved-evidence appendix are the authoritative specification of the accepted captured workflow. Companion documents refer here rather than define competing rules.

**Documentation status — reconciliation completed 2026-09-10:** All 40 required captured A-X configurations and their immediate in-scope dependencies are documented against the accepted evidence, with no unresolved material documentation blocker identified. The three OFF entries are inventory-only by explicit agreement. This is a captured-configuration specification, NOT certification that every live published rule still matches it. Brian selected captured-snapshot sign-off and was not sure about live-state equivalence. Runtime correctness, migration readiness, production fixes, A-39 retirement, and column deletion are not certified here.

**Boundary:** A-1 through A-40 are automated processes. A human or external system may supply an input or later edit a field, but no human output step is part of an A-X execution. Immediate field sources/readers/writers are covered; manual playbook internals and the full vehicle-to-dashboard pipeline are not. The three OFF entries below are inventory-only.

**Evidence basis:** Brian's supplied UI captures and saved transcriptions, explicit confirmations, schema/reference snapshots, and qualified local source inspection. No fresh screenshot campaign, production census, automation run, or native-runtime test is required merely to document settings already established by that evidence.

## Inventory and navigation

The supplied inventory identifies 40 numbered rules and three additional OFF entries. Captured enabled-state evidence is retained in the appendix; this is not an independently exhaustive live API enumeration or a new live-status check.

| Group | Canonical rules |
|---|---|
| Initial Creation | [A-1](#a-1) |
| Headlands Assessment | [A-2](#a-2), [A-3](#a-3), [A-4](#a-4), [A-5](#a-5), [A-6](#a-6) |
| Path Position Breakout | [A-7](#a-7), [A-8](#a-8), [A-9](#a-9), [A-10](#a-10), [A-11](#a-11), [A-12](#a-12), [A-13](#a-13), [A-14](#a-14) |
| Confirmed Halt Code | [A-15](#a-15), [A-16](#a-16), [A-17](#a-17), [A-18](#a-18), [A-19](#a-19), [A-20](#a-20), [A-21](#a-21), [A-22](#a-22), [A-23](#a-23), [A-24](#a-24), [A-25](#a-25) |
| Auto-Investigations | [A-26](#a-26), [A-27](#a-27), [A-28](#a-28), [A-29](#a-29), [A-30](#a-30) |
| Perception Demotions | [A-31](#a-31), [A-32](#a-32), [A-33](#a-33) |
| Confirmed Demotion Type | [A-34](#a-34), [A-35](#a-35), [A-36](#a-36), [A-37](#a-37) |
| Triage Activities Complete | [A-38](#a-38) |
| Misuse Checking | [A-39](#a-39) |
| In Scope | [A-40](#a-40) |

| Additional group | Entry | Captured status | Sign-off scope |
|---|---|---|---|
| Triage Protocols | TP-1 Headlands Assessment | OFF, UI and owner-confirmed | Inventory only; internal definition excluded |
| Triage Investigations | JRM-476 | OFF, UI and owner-confirmed | Inventory only; internal definition excluded |
| Triage Investigations | JRM-446 - Bug Assignment | OFF, UI and owner-confirmed | Inventory only; internal definition excluded |

OFF is not deleted or proven obsolete. The disabled JRM-446-named automation is distinct from the JRM-446 reference assigned by A-33. Manual task names/TP aliases are not automatically live Airtable automation identities.

## Shared configuration contracts

These contracts apply to EVERY numbered definition below, so target/source facts are not repeated ambiguously:

- **Base:** Triage Tool Prototype, `app1jXoB1g13R9iOl`.
- **Trigger and action table D:** Demotions_DatabricksSync, `tblSJItXuuUd0lyHP`. All captured actions are Update record actions in D.
- **Action target R:** The triggering record's Airtable record ID. Brian explicitly confirmed this convention; it is not A_UID or a fixed sample record. It applies to every action and branch below.
- **Trigger C:** When a record matches conditions; the UI says it fires when a record starts matching and excludes records already matching. All listed predicates are AND-connected unless an OR or branch grouping is explicitly stated. No additional view/schedule/guard is implied.
- **Created trigger:** A-1 uses When a record is created, including empty creations, with no additional condition/view restriction shown.
- **Updated trigger:** A-38/A-40 use When a record is updated, explicitly excluding creation. Both have no view selected and watch only their five listed fields, not all fields or their own output.
- **Actions:** Unbranched actions explicitly marked Always execute with no further captured action guard. Conditional actions use the exact If/Otherwise-if/Otherwise groups listed; do not replace them with Always.
- **Values/types:** Choice labels below are exact configured selections. Confirmed Demotion Type is a multiple-select field; a single displayed classification means the configured selection contains that one value. Code/JRM name text in linked fields is not a record-ID literal, numeric conversion, wildcard, or direct Jira API operation.
- **Bindings:** A-16–A-18 use direct `R.Halt Code - Import`; A-22/A-23 use direct `R.Secondary Demotion Manual`, with no custom transform, explicitly confirmed by Brian during this documentation audit. A-15 separately projects the linked records' Name property. Backend link resolution/serialization is not a missing selected-source setting and remains a runtime question.
- **Names and identities:** A-numbers identify entries in this accepted inventory, not immutable Airtable UUIDs. Names known only through the inventory or a clipped header are retained as such in the evidence record; an absent UUID, run count, or optional Description does not by itself make a functional definition incomplete.
- **Meaning:** Investigation Complete, Headlands Complete, Triage Activities Complete, In Scope, operator status, and bug/behavior classification are separate fields. Do not harmonize their labels or infer additional writes.
- **Execution boundary:** A dependency arrow or a more-specific condition is not scheduler priority. Native empty/mixed lookup behavior, no-op updates, snapshot timing, retries, and interleavings are not proven by this specification.

### Exact reusable selection sets

The following named sets are literal members of the rule definitions that reference them, not new rules or execution dependencies. DR-X shorthand in conversation denotes these full selected reason-record names.

| Set | Exact members |
|---|---|
| Manual reasons | `DR-1 In-Cab Controls Override`; `DR-2 Human-Triggered Demotion` |
| Interrupted-stop reasons | `DR-4 Perception Internal System Failure`; `DR-6 Gen4/VADC Misc Error`; `DR-7 Perception Image Quality`; `DR-8 Guidance & Geo`; `DR-9 Spark`; `DR-11 Operator Error`; `DR-12 Perception Configuration`; `DR-13 Vehicle Operation Check` |
| DR-3 exclusions | `DR-4 Perception Internal System Failure`; `DR-6 Gen4/VADC Misc Error`; `DR-7 Perception Image Quality`; `DR-8 Guidance & Geo`; `DR-9 Spark`; `DR-11 Operator Error`; `DR-12 Perception Configuration` — NOT DR-13 |
| Accepted completion types | `Intended Manual Demotion`; `Unintended Perception Demotion`; `Unintended Vehicle Demotion`; `Intended Perception Demotion`; `Intended Vehicle Demotion` |

The exact DR-3 value is `DR-3 Perception "Saw Something"`. Preserve `has any of`, `has none of`, and `is exactly` as different operators even when a condition appears redundant.

## Canonical captured rules

### A-1
**Name:** Headlands, Investigation, Activities. **Evidence:** E01.

**Trigger:** Record created in D; includes empty creations. **Action:** Always update R:
- Headlands Assessment Complete = `Headlands Not Complete`.
- Investigation Complete = `Investigation Not Complete`.
- Triage Activities Complete = `Not Complete`.
- In Scope = `Not Yet Determined`.

These are literal assignments, not fill-if-empty/COALESCE defaults. No operator, reviewer, or classification assignment is configured.

### A-2
**Name:** Implement Path - Headlands. **Evidence:** E02.

**Trigger C:** Implement Path Position Type Text **is** `PT_Headland` AND Headlands Assessment Complete **is** `Headlands Not Complete`.

**Action:** Always update R: Headlands Assessment = `h - Headlands Pass`; Headlands Reviewer = linked ID `reccXDh78Z9awPZbW` (captured Name `Automatic `, including one trailing space). Does not write the completion flag.

### A-3
**Name:** Implement Path - In Field. **Evidence:** E03.

**Trigger C:** Implement Path Position Type Text **is** `PT_InField` AND Headlands Assessment Complete **is** `Headlands Not Complete`.

**Action:** Always update R: Headlands Assessment = `i - Interior Pass - No Headlands Turn`; Headlands Reviewer = `reccXDh78Z9awPZbW`. No completion write.

### A-4
**Name:** Implement Path - Turn. **Evidence:** E04.

**Trigger C:** Implement Path Position Type Text **is** `PT_Turn` AND Headlands Assessment Complete **is** `Headlands Not Complete`.

**Action:** Always update R: Headlands Assessment = `t - Interior Pass - Headlands Turn`; Headlands Reviewer = `reccXDh78Z9awPZbW`. No completion write.

### A-5
**Name:** Computed Path - Headlands. **Evidence:** E05.

**Trigger C — all three:**
1. Implement Path Position Type Text **is none of** `PT_Turn`, `PT_InField`, `PT_Headland`.
2. Headlands Assessment Complete **is** `Headlands Not Complete`.
3. Computed Implement Path Position Type Text **is** `PT_Headland`.

**Action:** Always update R: Headlands Assessment = `h - Headlands Pass`; Headlands Reviewer = `reccXDh78Z9awPZbW`. No completion write.

### A-6
**Name:** Computed Path - In Field. **Evidence:** E06.

**Trigger C — all three:**
1. Implement Path Position Type Text **is none of** `PT_Turn`, `PT_InField`, `PT_Headland`.
2. Headlands Assessment Complete **is** `Headlands Not Complete`.
3. Computed Implement Path Position Type Text **is** `PT_InField`.

**Action:** Always update R: Headlands Assessment = `u - Interior - Unknown Turn`; Headlands Reviewer = `reccXDh78Z9awPZbW`. This is NOT A-3's no-turn output; no completion write.

### A-7
**Name:** Headlands Pass. **Evidence:** E07.

**Trigger C:** Headlands Assessment **is** `h - Headlands Pass`.

**Action:** Always update R: Headlands vs Interior = `Headlands Pass`; Headlands Turn = `N/A - Headlands Pass`. Description shown: `Headlands Pass`.

### A-8
**Name:** Interior Pass - No Turn. **Evidence:** E08.

**Trigger C:** Headlands Assessment **is** `i - Interior Pass - No Headlands Turn`.

**Action:** Always update R: Headlands vs Interior = `Interior Pass`; Headlands Turn = `Interior Pass - No Headlands Turn`. Description shown: `Interior Pass - No Turn`.

### A-9
**Name:** Interior Pass - Headlands Turn. **Evidence:** E09.

**Trigger C:** Headlands Assessment **is** `t - Interior Pass - Headlands Turn`.

**Action:** Always update R: Headlands vs Interior = `Interior Pass`; Headlands Turn = `Headlands Turn`. Description shown: `Interior Pass - Headlands Turn`.

### A-10
**Name:** Interior Pass - Headlands Transition. **Evidence:** E10.

**Trigger C:** Headlands Assessment **is** `r - Interior Pass - Headlands Transition`.

**Action:** Always update R: Headlands vs Interior = `Interior Pass`; Headlands Turn = `Headlands Turn`. The Description also says `Interior Pass - Headlands Turn`, not Transition. Preserve the distinction between input label and output; this is not an unrecorded transition output.

### A-11
**Name:** Interior Pass - Interior Boundary. **Evidence:** E11.

**Trigger C:** Headlands Assessment **is** `o - Interior Pass - Internal Obstacle/Boundary`.

**Action:** Always update R: Headlands vs Interior = `Interior Pass`; Headlands Turn = `Interior Boundary/Obstacle`. Description shown: `Interior Pass - Interior Boundary`. Preserve Internal/Interior and the differing word order.

### A-12
**Name:** Not Sure - Headlands vs Interior. **Evidence:** E12.

**Trigger C:** Headlands Assessment **is** `n - Not Sure`.

**Action:** Always update R: Headlands vs Interior = `Not Sure`; Headlands Turn = `Not Sure`. These are nonempty choices, not clears. Captures showed Reconnecting; accepted for the captured snapshot, not as live-publication certification.

### A-13
**Name:** Interior Pass - Unknown Infield. **Evidence:** E13.

**Trigger C:** Headlands Assessment **is** `u - Interior - Unknown Turn`.

**Action:** Always update R: Headlands vs Interior = `Interior Pass`; Headlands Turn = `Not Sure`. Description shown: `Interior Pass - Interior Boundary`; it does NOT change the actual Not Sure assignment. A-6 supplies this assessment automatically.

A-7 through A-13 have no completion-status prerequisite and write neither completion flags nor reviewer. Their r/o/n input values have no producer among the captured A-X assignments; those value inputs cross the external-input boundary.

### A-14
**Name:** Headlands Assessment Complete. **Evidence:** E14.

**Trigger C:** Headlands vs Interior **is not empty** AND Headlands Turn **is not empty**.

**Action:** Always update R: Headlands Assessment Complete = `Headlands Complete`. Description shown: `Interior Pass - Interior Boundary`.

Not Sure values satisfy the nonempty criteria. The rule writes only this flag, with no inverse action to reopen it when inputs later become empty.

### A-15
**Name:** Secondary Demotion Manual. **Evidence:** E15.

**Trigger C — all three:**
1. Secondary Demotion Manual **is empty**.
2. Preceding Stop Code **is not empty**.
3. Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: Secondary Demotion Manual ← **R.Preceding Stop Code → Make a new list of: Name**, explicitly owner-confirmed. This is a linked-field assignment by names, not MAIN/masking/classification. The empty check is a trigger predicate, not a proven atomic write-time guard.

### A-16
**Name:** Manual Initial - N/A Preceding. **Evidence:** E16.

**Trigger C:** Demotion Reason **has any of** Manual reasons AND Secondary Demotion Manual **has any of** `N/A`.

**Action:** Always update R: MAIN Demotion Code ← direct **R.Halt Code - Import**; Manual Demotion Masking = `Intended Manual Demotion - No Mask`.

N/A is a selected linked record, not empty or only-N/A. This rule does not directly test Preceding Stop Code.

### A-17
**Name:** Manual Initial - Manual Secondary. **Evidence:** E17.

**Trigger C:** Demotion Reason **has any of** Manual reasons AND Secondary Demotion Reason **has any of** Manual reasons. The two matches need not be the same member and do not exclude additional reason values.

**Action:** Always update R: MAIN Demotion Code ← direct **R.Halt Code - Import**; Manual Demotion Masking = `Intended Manual Demotion - No Mask`.

### A-18
**Name:** Main Halt Code - Non Manual Initial. **Evidence:** E18.

**Trigger C:** Demotion Reason **has none of** Manual reasons. No separate nonempty-reason condition is configured.

**Action:** Always update R: MAIN Demotion Code ← direct **R.Halt Code - Import**; Manual Demotion Masking = `N/A`; Secondary Demotion Manual = literal linked-record name `N/A` (not a clear).

### A-19
**Name:** Main Halt Code - 12.27. **Evidence:** E19.

**Trigger C:** Secondary Demotion Manual **has any of** `12.27` AND Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: MAIN Demotion Code = literal linked-record name `12.27`; Manual Demotion Masking = `Manual Mask`.

### A-20
**Name:** Main Halt Code - 12.24. **Evidence:** E20.

**Trigger C — all three:** Secondary Demotion Manual **has any of** `12.24`; Demotion Reason **has any of** Manual reasons; Secondary Demotion Manual **has none of** `12.27`.

**Action:** Always update R: MAIN Demotion Code = literal linked-record name `12.24`; Manual Demotion Masking = `Manual Mask`.

### A-21
**Name:** Main Halt Code - 12.29. **Evidence:** E21.

**Trigger C — all three:** Secondary Demotion Manual **has any of** `12.29`; Secondary Demotion Manual **has none of** `12.24`, `12.27`; Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: MAIN Demotion Code = literal linked-record name `12.29`; Manual Demotion Masking = `Manual Mask`.

A-19/A-20/A-21 implement `12.27 > 12.24 > 12.29` predicate precedence within that trio for fixed inputs, not scheduler priority. Their predicates do not exclude N/A, so each can overlap A-16 when N/A accompanies its eligible code and all other predicates hold; this is a configuration observation, not an observed race.

### A-22
**Name:** Main Halt Code - Interrupted Stop Code. **Evidence:** E22.

**Trigger C — all four:**
1. Secondary Demotion Manual **is not empty**.
2. Secondary Demotion Reason **has any of** Interrupted-stop reasons.
3. Secondary Demotion Manual **has none of** `12.24`, `12.27`, `12.29`, `N/A` — exactly four exclusions.
4. Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: MAIN Demotion Code ← direct **R.Secondary Demotion Manual**; Manual Demotion Masking = `Manual Mask`.

The summary's old “and 1 more” did not establish a fifth exclusion; the old transcription omitted condition 4. Source field and direct binding are now confirmed. Display → Name is not evidence of a custom Name projection here.

### A-23
**Name:** Main Halt Code - False Positive. **Evidence:** E23.

**Trigger C — all five:**
1. Secondary Demotion Manual **is not empty**.
2. Secondary Demotion Manual **has none of** `12.24`, `12.27`, `12.29`.
3. Secondary Demotion Reason **is exactly** `DR-3 Perception "Saw Something"`.
4. Secondary Demotion Reason **has none of** DR-3 exclusions.
5. Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: MAIN Demotion Code ← direct **R.Secondary Demotion Manual**; Manual Demotion Masking = `Manual Mask`.

Both the exact DR-3 predicate and the separate seven-reason exclusion are configured. No direct N/A exclusion or separate false-positive adjudication condition is shown.

### A-24
**Name:** Main Halt Code - 12.X1; full sidebar suffix not captured. **Evidence:** E24.

**Trigger C — all six:**
1. Secondary Demotion Manual **is not empty**.
2. Secondary Demotion Manual **has none of** `12.24`, `12.27`, `12.29`.
3. Secondary Demotion Reason **is exactly** `DR-3 Perception "Saw Something"`.
4. Secondary Demotion Reason **has none of** DR-3 exclusions.
5. Demotion Reason **has any of** Manual reasons.
6. Secondary Demotion Manual **has any of** `12.X1`.

**Action:** Always update R: MAIN Demotion Code = literal linked-record name `12.X1`; Manual Demotion Masking = `Manual Mask`.

### A-25
**Name:** Main Halt Code - 12.X2; full sidebar suffix not captured. **Evidence:** E25.

**Trigger C — all six:**
1. Secondary Demotion Manual **is not empty**.
2. Secondary Demotion Manual **has none of** `12.24`, `12.27`, `12.29`.
3. Secondary Demotion Reason **is exactly** `DR-3 Perception "Saw Something"`.
4. Secondary Demotion Reason **has none of** DR-3 exclusions.
5. Demotion Reason **has any of** Manual reasons.
6. Secondary Demotion Manual **has any of** `12.X2`.

**Action:** Always update R: MAIN Demotion Code = literal linked-record name `12.X2`; Manual Demotion Masking = `Manual Mask`.

Brian explicitly confirmed A-25 is A-24 with X2 replacing X1. Neither rule excludes the other's literal code. Both imply A-23 eligibility, and both can qualify if the shared predicates hold with both linked values; no conflicting production runs are certified. A-15 through A-25 do not themselves write investigation completion or confirmed classification.

### A-26
**Name:** Perception Stops as Demotions. **Evidence:** E26.

**Trigger C:** Halt Code - Import **is any of** `12.15`, `12.110`, `12.111`, `12.112`, `12.113`, `12.101` AND Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R:
- Operator Error or Misuse = `No Operator Error or Misuse`.
- Bug or Intended Behavior = `Known Bug`.
- Confirmed Demotion Type = `Unintended Perception Demotion`.
- Investigation Complete = `Investigation Complete`.

This is an imported-code rule, not a MAIN-code rule. Preserve `12.110` distinctly from `12.11`.

### A-27
**Name:** 12.20 and 12.21. **Evidence:** E27.

**Trigger C:** Halt Code - Import **is any of** `12.20`, `12.21` AND Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R:
- Operator Error or Misuse = `No Operator Error or Misuse`.
- Bug or Intended Behavior = `Known Bug`.
- Confirmed Demotion Type = `Unintended Perception Demotion`.
- Investigation Complete = `Investigation Complete`.
- Confirmed JRM Link = literal linked-record name `JRM-613`.

### A-28
**Name:** 12.35. **Evidence:** E28; saved published-policy V2 and later branch captures.

**Trigger C — all three:** MAIN Demotion Code **has any of** `12.35`; Investigation Complete **is** `Investigation Not Complete`; Headlands Assessment Complete **is** `Headlands Complete`.

**Action graph:** One Update record in the If branch, otherwise one Update record in Otherwise. Both target R in D; neither is a globally unconditional Always action.

| Assigned field | If Headlands vs Interior is Headlands Pass | Otherwise: if no other conditions are met |
|---|---|---|
| Operator Error or Misuse | No Operator Error or Misuse | No Operator Error or Misuse |
| Bug or Intended Behavior | Intended Behavior | Known Bug |
| Confirmed Demotion Type | Intended Perception Demotion | Unintended Perception Demotion |
| Investigation Complete | Investigation Complete | Investigation Complete |

Otherwise includes Not Sure/blank/other positions only after all three trigger prerequisites are met. The first branch checks Headlands vs Interior; it is not a fourth trigger predicate. No JRM/headlands-completion assignment is configured.

### A-29
**Name:** Missing Spark. **Evidence:** E29 plus owner-confirmed manual marker input.

**Trigger C — all three:**
1. MAIN Demotion Code **has any of** `12.15`, `12.101`, `12.110`, `12.111`, `12.112`, `12.113`.
2. MAIN_SparkURL_Manual **contains** `missing`.
3. Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R:
- Operator Error or Misuse = `No Operator Error or Misuse`.
- Bug or Intended Behavior = `Known Bug`.
- Confirmed Demotion Type = `Unintended Perception Demotion`.
- Investigation Complete = `Investigation Complete`.
- Confirmed JRM Link = literal linked-record name `JRM-548`.

Contains missing is not an empty-URL or HTTP-failure test. The stored URL/marker is a human-supplied input confirmed by Brian; every output above is automatic. The displayed old test result warned it could be stale and is not used as runtime proof.

### A-30
**Name:** 12.X1, 12.X2. **Evidence:** E30.

**Trigger C:** MAIN Demotion Code **has any of** `12.X1`, `12.X2` AND Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R:
- Operator Error or Misuse = `Potential Operator Error`.
- Bug or Intended Behavior = `Intended Behavior`.
- Confirmed Demotion Type = `Unintended Perception Demotion`.
- Investigation Complete = `Investigation Complete`.

The different intended/unintended labels are exact values on different fields. There is no branch distinguishing X1 from X2 and no JRM assignment.

### A-31
**Name:** 12.29 Intended Perception. **Evidence:** E31.

**Trigger C — all four:**
1. MAIN Demotion Code **has any of** `12.29`.
2. Vehicle/Object Outside Field **is** `Inside Field (OBVIOUS)`.
3. NonNavigable Object Misuse Details **is not empty**.
4. Investigation Complete **is** `Investigation Not Complete`.

**Action graph:** First, Always update R: Confirmed Demotion Type = `Intended Perception Demotion`; Bug or Intended Behavior = `Intended Behavior`. Then execute one selected Update record branch, also targeting R in D:

| Ordered branch / action condition | Operator Error or Misuse | Investigation Complete |
|---|---|---|
| If NonNavigable Object Misuse Details is Movable UNMAPPED Object - Misuse | Misuse | Investigation Complete |
| Otherwise if NonNavigable Object Misuse Details is Stationary Object/Equipment - Potential Error | Potential Operator Error | Investigation Complete |
| Otherwise: if no other conditions are met | No Operator Error or Misuse | Investigation Complete |

Normal execution contains two configured updates: initial classification, then one branch—not four updates or a claimed atomic transaction. Otherwise does not bypass the outer nonempty-details prerequisite. The inputs may be externally supplied; all A-31 outputs are automated. A reconnecting notice in one capture is preserved as a snapshot/currentness caveat, not a requirement for repeat captures.

### A-32
**Name:** 12.24, 12.27 Intended Perception. **Evidence:** E32.

**Trigger C — all three:** MAIN Demotion Code **has any of** `12.24`, `12.27`; Vehicle/Object Outside Field **is** `Inside Field (OBVIOUS)`; Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R: Confirmed Demotion Type = `Intended Perception Demotion`; Bug or Intended Behavior = `Intended Behavior`; Operator Error or Misuse = `Misuse`; Investigation Complete = `Investigation Complete`.

There is no object-misuse-details prerequisite or conditional branch. Do not substitute A-31's tentative/default outcomes.

### A-33
**Name:** 12.24, 12.27 Unintended Perception; actual scope also includes 12.29. **Evidence:** E33.

**Trigger C — all three:**
1. MAIN Demotion Code **has any of** `12.24`, `12.27`, `12.29`.
2. Vehicle/Object Outside Field **is any of** `Outside Field (OBVIOUS)`, `Outside Field (POTENTIAL)`, `Interior Impassible`.
3. Investigation Complete **is** `Investigation Not Complete`.

**Action:** Always update R: Confirmed Demotion Type = `Unintended Perception Demotion`; Bug or Intended Behavior = `Known Bug`; Confirmed JRM Link = literal linked-record name `JRM-446`; Operator Error or Misuse = `No Operator Error or Misuse`; Investigation Complete = `Investigation Complete`.

This is a three-value whitelist, not everything except Inside Field. Blank and the schema choice `N/A - Spark Error` are not selected. A-31/A-32/A-33 do not classify a completed investigation again solely because location is edited.

### A-34
**Name:** Confirmed Manual Demotion. **Evidence:** E34.

**Trigger C:** Manual Demotion Masking **is** `Intended Manual Demotion - No Mask` AND MAIN Demotion Reason **has any of** Manual reasons.

**Action:** Always update R: Operator Error or Misuse = `No Operator Error or Misuse`; Confirmed Demotion Type = `Intended Manual Demotion`; Investigation Complete = `Investigation Complete`.

### A-35
**Name:** Automatic Unintended Perception Demotion. **Evidence:** E35.

**Trigger C:** Triage Process **has any of** `Automatic Unintended Perception Demotion` AND Manual Demotion Masking **is any of** `Manual Mask`, `N/A`.

**Action:** Always update R: Operator Error or Misuse = `No Operator Error or Misuse`; Confirmed Demotion Type = `Unintended Perception Demotion`; Investigation Complete = `Investigation Complete`.

### A-36
**Name:** Automatic Unintended Vehicle Demotion. **Evidence:** E36.

**Trigger C:** Triage Process **is exactly** `Automatic Non-Perception Demotion` AND Manual Demotion Masking **is any of** `Manual Mask`, `N/A`.

**Action:** Always update R: Operator Error or Misuse = `No Operator Error or Misuse`; Confirmed Demotion Type = `Unintended Vehicle Demotion`; Investigation Complete = `Investigation Complete`.

### A-37
**Name:** Automatic Intended Vehicle Demotion. **Evidence:** E37 plus preserved historical run/record evidence.

**Trigger C:** Triage Process **is exactly** `Automatic Intended Vehicle Demotion` AND Manual Demotion Masking **is any of** `Manual Mask`, `N/A`.

**Action:** Always update R: Operator Error or Misuse = `No Operator Error or Misuse`; Confirmed Demotion Type = `Intended Vehicle Demotion`; Investigation Complete = `Investigation Complete`.

A-34 through A-37 have NO Investigation Not Complete prerequisite and do not write bug/JRM/headlands/scope values. A flag-only reset or manual reopening does not make their unchanged trigger predicates newly true. This is not the same eligibility behavior as A-26 through A-33. A-35's any-match process operator is distinct from A-36/A-37's exact-match operators.

### A-38
**Name:** Activities Complete or NOT. **Evidence:** E38.

**Trigger:** Record updated in D; excludes creation; no view selected. Watches exactly: `Confirmed Demotion Type`, `Investigation Complete`, `Headlands Assessment`, `MAIN Demotion Code`, `Headlands Assessment Complete`.

**Ordered action graph; all updates target R in D:**
- **If ALL:** Investigation Complete **is** `Investigation Complete`; Headlands Assessment Complete **is** `Headlands Complete`; Confirmed Demotion Type **has any of** Accepted completion types; MAIN Demotion Code **length ≠ 0** → Triage Activities Complete = `Complete`.
- **Otherwise, if no other conditions are met** → Triage Activities Complete = `Not Complete`.

The action conditions are the branch criteria, not Always. Only the overall activities field is written. Headlands Assessment is watched but not a criterion; linked-list length is not a character-length or exactly-one-code test. Its output, operator/bug/JRM/scope fields, and separate headlands breakout fields are not watched.

### A-39
**Name:** Misuse Checking - Create. **Evidence:** E39 and the saved earlier UI transcription.

**Trigger C:** Misuse Check Required **is exactly** `NOT Required - Misuse Check`. Despite its name, this is not a record-created trigger.

**Action:** Always update R: Operator Error or Misuse = `No Operator Error or Misuse`.

There is no empty-output, completion, MAIN/masking, or initialization guard. The input lookup is through original Halt Code - Linked, not MAIN. Output-only edits do not retrigger the unchanged condition; neither safe retirement nor an actual overwrite is established merely by this configuration.

### A-40
**Name:** In Scope - Updating. **Evidence:** E40.

**Trigger:** Record updated in D; excludes creation; no view selected. Watches exactly: `Operator Error or Misuse`, `Investigation Complete`, `Bug or Intended Behavior`, `Headlands vs Interior`, `Headlands Assessment Complete`.

**Ordered action graph; each branch updates only In Scope on R in D:**
1. **If ANY:** Headlands vs Interior **is any of** `Headlands Pass`, `Not Sure` **OR** Operator Error or Misuse **is** `Misuse` **OR** Bug or Intended Behavior **is** `Out of Scope` → `Outside of Scope`.
2. **Otherwise if ALL:** Headlands vs Interior **is** `Interior Pass`; Operator Error or Misuse **is not** `Misuse`; Operator Error or Misuse **is not empty**; Headlands vs Interior **is not empty** → `In Scope`.
3. **Otherwise, if no other conditions are met** → `Not Yet Determined`.

The first branch wins over the second. The input `Out of Scope` and output `Outside of Scope` are different literal labels. A nonempty `Potential Operator Error` value can satisfy the second branch if the first branch fails. Investigation/headlands completion flags are watched, not prerequisites. In Scope itself is not watched.

## Immediate dependency catalog

### Field identities and reference paths

Evidence S1/S2 below establishes the captured schema relationships; it is not a fresh production schema certification.

| Contract | Captured relationship |
|---|---|
| Demotion identity | Airtable record ID targets a row; `A_UID` is a stored multilineText key constructed as `VIN \| timestamp`, not a formula/MD5. Captured legacy rows include plain and hashed VIN forms; do not normalize them implicitly |
| Original code | `Halt Code - Import` is singleSelect; `Halt Code - Linked` (`fld4qfE6tQ7c7l2mG`) links to Halt Codes (`tblN8uu4Gl1eDZMLs`) |
| Demotion Reason | Lookup through original Halt Code - Linked to reason references |
| Secondary Demotion Reason | Lookup through Secondary Demotion Manual (`fldzCC2DDW9tweN0s`) to linked reason data |
| MAIN Demotion Reason | Lookup through MAIN Demotion Code (`fldw0GEHxF0PFRSof`) to linked reason data |
| Triage Process | Lookup (`fldUTRUIUS22LeCbJ`) through MAIN Demotion Code to linked process data (`fldtQ19seFvs3FSk2`) |
| Misuse Check Required | Lookup through original Halt Code - Linked to `fldn9R876FeC0psJ6`; NOT MAIN-based |
| Code links | Preceding Stop Code, Secondary Demotion Manual, and MAIN Demotion Code link to Halt Codes; single-record UI preference is not a demonstrated runtime cardinality constraint |
| Automatic reviewer | A-2–A-6 assign Team Members record `reccXDh78Z9awPZbW` in `tblHQdtGEVbhNRWMR`; captured Name is `Automatic ` with a trailing space |
| JRM associations | Confirmed JRM Link (`fldFWS6mDaAqFs1Gl`) is multipleRecordLinks to `tbllaxeplHp2Jmrw6`; JRM-613/548/446 are configured linked names, not external issue-creation calls |
| Manual Spark marker | MAIN_SparkURL_Manual (`fldrTkaa23C1V4NHe`) is a stored URL field; Brian confirms a triager supplies the URL or missing marker used by A-29 |
| Assessment input types | Vehicle/Object Outside Field and NonNavigable Object Misuse Details are singleSelect inputs. Their external producers are not new steps inside A-31–A-33 |

### Automated writers and immediate readers

This is a map of the captured A-X boundary, not an exhaustive column-usage/deletion inventory. A field with no A-X reader can still be used by people, interfaces, integrations, and reporting.

| Field | A-X writers | A-X readers/watchers or indirect uses |
|---|---|---|
| Headlands Assessment Complete | A-1; A-14 | A-2–A-6, A-28, A-38; A-40 watches only |
| Investigation Complete | A-1; A-26–A-37 | A-26–A-33, A-38; A-40 watches only; NOT a prerequisite for A-34–A-37 |
| Triage Activities Complete | A-1; A-38 | No direct A-X reader; A-38 does not watch its output |
| In Scope | A-1; A-40 | No direct A-X reader; A-40 does not watch its output |
| Headlands Assessment | A-2–A-6 | A-7–A-13; A-38 watches only |
| Headlands Reviewer | A-2–A-6 | No direct A-X reader shown |
| Headlands vs Interior | A-7–A-13 | A-14, A-28 branch, A-40 watch/criteria |
| Headlands Turn | A-7–A-13 | A-14 |
| Secondary Demotion Manual | A-15; A-18 | A-15/A-16/A-19–A-25; feeds Secondary Demotion Reason including A-17 |
| MAIN Demotion Code | A-16–A-25 | A-28–A-33, A-38; indirectly A-34–A-37 through reason/process lookups |
| Manual Demotion Masking | A-16–A-25 | A-34–A-37 |
| Confirmed Demotion Type | A-26–A-37 | A-38 watch/criteria |
| Operator Error or Misuse | A-26–A-37; A-39 | A-40 watch/criteria; NOT A-38 |
| Bug or Intended Behavior | A-26–A-33 | A-40 watch/criteria |
| Confirmed JRM Link | A-27; A-29; A-33 | No direct A-X reader shown; linked/reference and reporting consumers are outside this table |

### Inputs without a direct A-X writer

| Input field | A-X consumers | Immediate source contract |
|---|---|---|
| Implement Path Position Type Text | A-2–A-6 | Inspected ingestion payload, C1 |
| Computed Implement Path Position Type Text | A-5/A-6 | Inspected ingestion payload, C1 |
| Preceding Stop Code | A-15 trigger and Name projection | Inspected ingestion payload, C1; linked Halt Codes records |
| Halt Code - Import | A-16–A-18 assignments; A-26/A-27 predicates | Inspected ingestion payload, C1; singleSelect |
| Halt Code - Linked | Indirect reason/misuse dependencies | Inspected ingestion payload, C1; original code link |
| Demotion Reason | A-15–A-25 | Original-code reason lookup |
| Secondary Demotion Reason | A-17/A-22–A-25 | Lookup through Secondary Demotion Manual |
| MAIN Demotion Reason | A-34 | Lookup through MAIN Demotion Code |
| Triage Process | A-35–A-37 | Lookup through MAIN Demotion Code |
| Misuse Check Required | A-39 | Original Halt Code - Linked lookup |
| Vehicle/Object Outside Field | A-31–A-33 | External assessment input; actor implementation not certified here |
| NonNavigable Object Misuse Details | A-31 | External assessment input; actor implementation not certified here |
| MAIN_SparkURL_Manual | A-29 | Owner-confirmed manual URL/missing-marker input |

Lookup fields have no direct A-X assignment, but their link/reference inputs can change them indirectly. This table does not classify their source fields as unused or safe to delete.

### External input interfaces and local code boundary

| Interface | Immediate contract and evidence |
|---|---|
| Code/path/preceding-stop ingestion | Inspected Mesa `send_data_to_airtable` and `update_airtable_demotions` write A_UID, original code/link, preceding stop, and path inputs. See C1; local code is not proof of its currently deployed binding |
| r/o/n assessment selections | They are consumed by A-10/A-11/A-12 but not produced by the captured A-X assignments. Treat them as externally supplied values; do not invent an active automatic producer or audit a manual playbook here |
| Object-location/details inputs | A-31–A-33 consume their named assessment fields. External human/integration input is outside A-X execution; mapping declarations in the local app do not prove active writeback |
| A-29 Spark marker | Owner-confirmed manual input boundary; no additional producer hunt needed to document that relationship |
| MAIN/reference changes | Can change reason/process lookup inputs. Exact native propagation timing is deferred runtime behavior, not proof of a new record-level writer |
| Airtable → main context | C1 resolves several linked/lookup fields from their first element into code/name values and reads investigation status. Do not equate this with a lossless list mirror |
| Airtable → dev full mirror | C2 uses a curated mapping, a default 100-record pull, joined linked IDs, a temporary table, and MERGE. Its name is not proof of all records/fields or complete event history |
| Reporting/UI | Separate consumers of persisted triage data. `databricks_dashboard_queries.sql` is not the source of truth for these native automation triggers |

## Evidence and documentation gap register

### Source keys

- **E01–E40:** Supplied conversation UI captures for the corresponding A-number and accepted follow-ups. The original detailed transcriptions are retained as **Evidence record A-N** in the [preserved-evidence appendix](#preserved-evidence-and-historical-material). These local handles are not automation IDs or an API export; no standalone screenshot filenames are invented.
- **O1:** Owner-confirmed shared target record-ID convention.
- **O2:** Owner-confirmed full DR-name shorthand and same-as-except settings, including A-25.
- **O3:** Documentation-audit confirmation that A-16–A-18 and A-22/A-23 use direct fields on the triggering row without custom transforms; A-15's explicit Name projection is separate.
- **O4:** Owner confirmation of A-29's manually supplied URL/missing marker; A-X outputs themselves are automated.
- **S1:** [Selected schema facts](../reference/field-contracts.md) and [source provenance](../reference/source-inventory.md). The owner-held full schema/manifest are not shipped wholesale because unrelated choice lists can contain customer identifiers. Saved timestamps are not verified publication/fetch times; the original manifest explicitly distinguishes capture-time uncertainty.
- **S2:** [Reference labels](../reference/reference-labels.json) and the accepted read-only reference lookup for the Automatic reviewer. Reference labels are not enabled-state evidence.
- **P28:** [Published A-28 V2 policy](../reference/a28-policy.json), owner-confirmed and corroborated by later captures. The A-28 portion of the [initial UI transcription source](../reference/source-inventory.md) is historical and superseded; its A-39 portion remains accepted with later corroboration.
- **C1:** [Mesa source context](../reference/legacy-context.md), inspected at `b277e47f569425e262b53f340f7d7af0a07b46e9`: configuration at 50–60; read conversions in `cast_airtable_format_to_databricks`/`upload_to_temp_table`; PATCH/upsert in `send_data_to_airtable`; update payload in `update_airtable_demotions`. Deployment values come from secrets and were not retrieved.
- **C2:** [Dev sync](../../sync_notebook_dev.py) and [dev mirror](../../sync_triage_full.py), inspected at `a9e61158c26f5e1251d16bdee77c17ec4ff41681`. Separate dev primary tables do not make shared-reference/production route-around paths isolated.

### Per-rule comparison register

Each row covers the full canonical definition, including shared D/R contracts. The per-rule comparison and immediate dependency reconciliation are complete for the accepted evidence. Companion current guidance now points to this authority; superseded prose/SQL remains explicitly historical rather than a second definition. Captured configuration review is separate from runtime proof.

**Documentary verification performed:** 40 unique canonical sections in numeric order, 40 register rows, and 40 preserved capture records; 37 condition-entry triggers, one created trigger, and two updated triggers; exact branch/assignment and input/writer cross-checks; source/reference and local-link/anchor review; Markdown table escaping and seven paired historical-section boundaries; tracked-file diffs and unversioned edit readback. The ten approved documentation/factual-pointer files were changed; raw evidence, runtime code, standalone SQL, and agent permissions/model/query behavior were not. No browser-rendering test, runtime test, sync, or production write was performed or needed for this sign-off.

| Rule | Accepted evidence / distinctive reconciliation | Required configuration gap |
|---|---|---|
| A-1 | E01/O1; created trigger, four literal defaults, supplemental Always/target | None identified |
| A-2 | E02/O1/S2; primary headland and fixed reviewer ID | None identified |
| A-3 | E03/O1; supplemental Always and target-token source | None identified |
| A-4 | E04/O1; primary turn | None identified |
| A-5 | E05/O1; three-condition computed headland fallback | None identified |
| A-6 | E06/O1; unknown-turn fallback, not no-turn | None identified |
| A-7 | E07/O1; two breakout fields only | None identified |
| A-8 | E08/O1; no-turn breakout | None identified |
| A-9 | E09/O1; headlands-turn breakout | None identified |
| A-10 | E10/O1; transition input, turn output, description distinct | None identified |
| A-11 | E11/O1; exact Internal/Interior and Obstacle/Boundary labels | None identified |
| A-12 | E12/O1; explicit Not Sure values; connection notice does not certify live state | None for captured snapshot |
| A-13 | E13/O1; Interior Pass / Not Sure, misleading description retained | None identified |
| A-14 | E14/O1; both nonempty, only headlands-completion write | None identified |
| A-15 | E15/O1; owner-confirmed list of preceding-record Names | None identified |
| A-16 | E16/O1/O3; any linked N/A, direct imported-code binding | Closed by O3 |
| A-17 | E17/O1/O3/S1; two independent manual-reason matches | Closed by O3 |
| A-18 | E18/O1/O3; none-of predicate, literal N/A secondary, supplemental Always/table | Closed by O3 |
| A-19 | E19/O1; fixed 12.27 / Manual Mask | None identified |
| A-20 | E20/O1; explicit 12.27 exclusion | None identified |
| A-21 | E21/O1; excludes both higher-priority codes | None identified |
| A-22 | E22/O1/O2/O3; four predicates, eight reasons, four exclusions, direct source | Closed by selections and O3 |
| A-23 | E23/O1/O2/O3; five predicates including exact DR-3 and exclusion row | Closed by source confirmation/O3 |
| A-24 | E24/O1/O2; six predicates and fixed X1 action | None identified |
| A-25 | E25/O1/O2; explicit equivalence to A-24 except X2 | None identified |
| A-26 | E26/O1; imported codes, four outputs, supplemental Always | None identified |
| A-27 | E27/O1; five outputs including JRM-613 | None identified |
| A-28 | E28/O1/P28; three prerequisites, both branch destinations and four outputs | None identified |
| A-29 | E29/O1/O4; contains marker, JRM-548; stale test not used as runtime proof | Producer boundary confirmed by O4 |
| A-30 | E30/O1; Potential Operator Error / Intended Behavior / Unintended Perception | None identified |
| A-31 | E31/O1; initial update plus three branches; connection caveat retained | None for captured snapshot |
| A-32 | E32/O1; direct Misuse, no detail prerequisite | None identified |
| A-33 | E33/O1/S1; includes 12.29, three-value location whitelist, JRM-446 | None identified |
| A-34 | E34/O1; MAIN reason and no-mask, no investigation prerequisite | None identified |
| A-35 | E35/O1/S1; process has any of, not exact | None identified |
| A-36 | E36/O1/S1; exact Non-Perception process, vehicle output | None identified |
| A-37 | E37/O1; fresh definition plus preserved historical actions | None identified |
| A-38 | E38/O1; updated-only, five watchers, both conditional outputs | None identified |
| A-39 | E39/O1/S1 plus saved UI; original linked-code lookup, no empty guard | None identified |
| A-40 | E40/O1; five watchers, ordered branches, exact Outside of Scope output | None identified |

### Boundaries and non-blocking deferred questions

| Item | Status for this documentation contract |
|---|---|
| Current live published equivalence | Not certified; Brian selected captured-snapshot sign-off after saying he was not sure about currentness |
| Automation UUIDs, clipped optional names/descriptions/counts | Retain available metadata in evidence; not a reason to invent a fresh capture task when A-number/context identifies the rule |
| Native lookup/list/empty/case and link-resolution behavior | Runtime question; selected native operators, fields, and transformations are documented |
| Scheduling, retries, snapshots, actual conflict cohorts | Runtime/operational question; do not promote possible interleavings into observed incidents |
| Human/integration producer internals | Outside A-X execution; external field contracts are documented without inventing human output steps |
| Three OFF automations | Inventory-only by explicit scope decision; internals not certified |
| A-39 removal, column deletion, readiness gate, migration SQL | Not approved or implemented by this documentation sign-off |
| Version control | This curated copy is versioned in triage-workflows. The original unversioned source is retained as owner-held history; Git does not certify or roll back live automation/data state |

## Historical observations and deferred design

- **Observed:** On `CASE-A1-RESET`, supplied history shows A-37 completed investigation and A-1 subsequently reset it. This establishes action/write order, not a second A-1 trigger. No readiness gate has been implemented.
- **Owner-confirmed:** The earlier August 25 intended/unintended reversals were intentional manual policy changes. Preserve that separately from the investigation-reset defect and the later 14-record backfill report/readback.
- **Configured, not an observed race:** A-16 overlaps some N/A-plus-perception-code states; A-23 contains the A-24/A-25 populations; other mixed MAIN/reference states can qualify competing writers. The conditions and assignments establish possibilities, not historical occurrence or a chosen winner.
- **Deferred:** Existing-record preservation, late-input readiness, exact native collection behavior, duplicate-name resolution, A-39 replacement coverage, live version equivalence, and production gate/cutover decisions are not prerequisites to documenting the selected settings.

Historical record details, source limitations, and original SQL/comments remain below for traceability. None of the old executable examples is an approved replacement or an instruction to run a sync, delete a field, replay data, or change a rule.

## Preserved evidence and historical material

**This appendix is not a second current specification.** It retains the earlier detailed capture transcriptions, incident notes, intermediate uncertainty/status statements, and historical SQL/proposals. Some recorded gaps were subsequently closed by the owner confirmations in this document; some old planning requirements were explicitly excluded from this documentation scope. The canonical definitions and register ABOVE govern the captured-snapshot sign-off. Do not interpret historical uses of current, VERIFIED, pending, obsolete, safe, or next steps here as a new verification result or authorization.

The Evidence record A-N headings identify the original rule-specific capture notes. Historical SQL and its original comments are preserved rather than silently edited into a supposedly tested implementation.

### Original working-record introduction

This document tracks each Airtable automation and proposed Databricks behavior.

**Re-audit in progress:** Earlier DOCUMENTED/VERIFIED labels are legacy coverage labels, not proof of a complete, current automation specification or migration readiness. Each automation must be checked against current published configuration, with missing details explicitly recorded. Definition verification and behavioral/migration verification are separate gates. The inventory itself must also be reconciled against all live and disabled automations before migration.

---

#### Record-ID convention

Brian explicitly confirmed that, for the automations being documented here, an action token labeled `Airtable record ID` comes from that automation's trigger. Record this as owner-confirmed provenance; it is not a fixed record ID or A_UID. Expanded source-picker screenshots independently corroborate this for A-1 through A-4. Do not request the same popup repeatedly unless a later action shows a different source, a lookup/repeating-step ambiguity, or a target-table mismatch. This convention does not establish action guards, field assignments, published versions, or runtime behavior; capture those separately.

#### Reason-code shorthand

Brian confirms that DR-X in chat abbreviates the full selected Demotion Reasons record name; for example, DR-3 means `DR-3 Perception "Saw Something"`. Preserve the full verified labels in captured conditions. Summary tables may use DR codes as shorthand, but that does not mean the configured value is only the code or permit replacing exact/membership operators with prefix matching.

**Owner-confirmed equivalence:** When Brian explicitly confirms that an automation is the same as a captured rule except for named changes, record the covered functional settings as owner-confirmed and apply those changes. Do not request duplicate screenshots merely to re-show confirmed, clipped selections. This does not establish matching metadata, published versions, or runtime behavior; ask only about genuinely unresolved differences.

#### Automation Index

| # | Name | Trigger | Category | Status |
|---|------|---------|----------|--------|
| **Initial Creation** |
| A-1 | Headlands, Investigation, Activities | Record Created | Initial Creation | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| **Headlands Assessment** |
| A-2 | Implement Path - Headlands | Record Matches Conditions | Headlands Assessment | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-3 | Implement Path - In Field | Record Matches Conditions | Headlands Assessment | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-4 | Implement Path - Turn | Record Matches Conditions | Headlands Assessment | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-5 | Computed Path - Headlands | Record Matches Conditions | Headlands Assessment | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-6 | Computed Path - In Field | Record Matches Conditions | Headlands Assessment | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| **Headlands Assessment - Path Position Breakout** |
| A-7 | Headlands Pass | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-8 | Interior Pass - No Turn | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-9 | Interior Pass - Headlands Turn | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-10 | Interior Pass - Headlands Transition | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-11 | Interior Pass - Interior Boundary | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-12 | Not Sure - Headlands vs Interior | Record Matches Conditions | Path Position Breakout | UI CONFIGURATION CAPTURED; reconnect/version and behavior validation pending |
| A-13 | Interior Pass - Unknown Infield | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-14 | Headlands Assessment Complete | Record Matches Conditions | Path Position Breakout | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| **Confirmed Halt Code** |
| A-15 | Secondary Demotion Manual | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-16 | Manual Initial - N/A Preceding | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED AS DISPLAYED; source provenance/version and behavior validation pending |
| A-17 | Manual Initial - Manual Secondary | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED AS DISPLAYED; source provenance/version and behavior validation pending |
| A-18 | Main Halt Code - Non Manual Initial | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED AS DISPLAYED; source provenance/version and behavior validation pending |
| A-19 | Main Halt Code - 12.27 | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-20 | Main Halt Code - 12.24 | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-21 | Main Halt Code - 12.29 | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-22 | Main Halt Code - Interrupted Stop Code | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED AS DISPLAYED; token data path/version and behavior validation pending |
| A-23 | Main Halt Code - False Positive | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED AS DISPLAYED; token data path/version and behavior validation pending |
| A-24 | Main Halt Code - 12.X1 | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-25 | Main Halt Code - 12.X2 | Record Matches Conditions | Confirmed Halt Code | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| **Auto-Investigations** |
| A-26 | Perception Stops as Demotions | Record Matches Conditions | Auto-Investigations | CONFIGURATION CAPTURED; header/version and behavior validation pending |
| A-27 | 12.20 and 12.21 | Record Matches Conditions | Auto-Investigations | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-28 | 12.35 | Record Matches Conditions | Auto-Investigations | CONFIGURATION CAPTURED; both branch destinations confirmed, identity/version and behavior validation pending |
| A-29 | Missing Spark | Record Matches Conditions | Auto-Investigations | CONFIGURATION CAPTURED; stale test result noted, identity/version and behavior validation pending |
| A-30 | 12.X1, 12.X2 | Record Matches Conditions | Auto-Investigations | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| **Perception Demotions** |
| A-31 | 12.29 Intended Perception | Record Matches Conditions | Perception Demotions | CONFIGURATION CAPTURED AS DISPLAYED; connection/version and behavior validation pending |
| A-32 | 12.24, 12.27 Intended Perception | Record Matches Conditions | Perception Demotions | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-33 | 12.24, 12.27 Unintended Perception | Record Matches Conditions | Perception Demotions | CONFIGURATION CAPTURED; trigger also includes 12.29; identity/version and behavior validation pending |
| **Confirmed Demotion Type** |
| A-34 | Confirmed Manual Demotion | Record Matches Conditions | Confirmed Demotion Type | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-35 | Automatic Unintended Perception Demotion | Record Matches Conditions | Confirmed Demotion Type | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-36 | Automatic Unintended Vehicle Demotion | Record Matches Conditions | Confirmed Demotion Type | CONFIGURATION CAPTURED; identity/version and behavior validation pending |
| A-37 | Automatic Intended Vehicle Demotion | Record Matches Conditions | Confirmed Demotion Type | CURRENT CONFIGURATION CAPTURED; historical evidence retained, identity/version and broader behavior validation pending |
| **Triage Activities Complete** |
| A-38 | Activities Complete or NOT | Record Updated | Triage Activities Complete | CONFIGURATION CAPTURED; five watched fields and both branches verified, identity/version and runtime pending |
| **Misuse Checking** |
| A-39 | Misuse Checking - Create | Record Matches Conditions | Misuse Checking | CURRENT CONFIGURATION CAPTURED; original-code lookup confirmed, coverage/retirement and runtime pending |
| **In Scope** |
| A-40 | In Scope - Updating | Record Updated | In Scope | CONFIGURATION CAPTURED; five watched fields and ordered branches confirmed, identity/version and runtime pending |

---

#### Evidence record A-1: Headlands, Investigation, Activities

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's supplied screenshots: trigger, execution setting, action table, target record-ID source, and all four assignments. Full identity/published-version metadata remains pending.  
**Behavior/migration status:** A late initialization overwrite is confirmed for CASE-A1-RESET by supplied production record history; remediation and broader behavior/migration validation remain pending. No automation test or production write performed by the agent.  
**Group:** Initial Creation  
**Enabled:** ON in the supplied screenshots  
**Airtable Automation ID:** Not visible; the group name is not an automation ID.  
**Name:** Existing documentation names this Headlands, Investigation, Activities; the full current UI name is truncated in the screenshots.  
**Runs:** Earlier captures displayed 876 this month; the later captures display 910. These are point-in-time UI counts, not measured rates or proof of successful runs.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible in these captures; exact revision/version and effective time have not been captured.

##### Trigger
- **Type:** When a record is created — confirmed in the trigger panel.
- **Table:** Demotions_DatabricksSync — confirmed in the trigger panel.
- **Base:** Triage Tool Prototype as displayed. Previously verified base ID: `app1jXoB1g13R9iOl`; table ID: `tblSJItXuuUd0lyHP`.
- **Creation semantics shown by Airtable:** Includes records that are empty on creation.
- **Conditions/view/schedule:** No additional conditions, view restriction, or schedule are shown for this creation trigger.
- **Existing-record updates:** The shown trigger is creation-based, not an update trigger. Existing-record upserts/backfills must not be assumed to rerun A-1.

##### Action
- **Visible action count/order:** One Update record action directly after the trigger. No branches or additional actions are shown.
- **Action execution setting:** Always — confirmed in the third screenshot. No fill-if-empty guard is shown.
- **Target table:** Demotions_DatabricksSync — confirmed in the third screenshot.
- **Target record:** `When a record is created` → `Airtable record ID`. The expanded source picker shows that trigger step selected and its Airtable record ID value, consistent with the token shown in the action's Record ID setting. The action targets the newly created record, not a fixed record ID or A_UID.
- **Fields Updated:** All four literal assignments are visible:

| Field | Value Set |
|-------|-----------|
| Headlands Assessment Complete | "Headlands Not Complete" |
| Investigation Complete | "Investigation Not Complete" |
| Triage Activities Complete | "Not Complete" |
| In Scope | "Not Yet Determined" |

##### Purpose and dependency implications
Initializes four triage tracking fields when a record is created. The action runs Always and makes explicit literal assignments, not fill-if-empty expressions. A confirmed production counterexample is CASE-A1-RESET (event 2026-09-10 15:34:58.879893 UTC): A-37 added Investigation Complete and Intended Vehicle Demotion, then an A-1-attributed revision explicitly removed Investigation Complete and added Investigation Not Complete. A-1 also assigned Headlands Not Complete and Not Yet Determined scope. Subsequent A-3/A-8/A-14 and A-40 entries show headlands/scope processing, while investigation remains incomplete in the current read. This establishes a late initialization write, NOT that A-1 triggered twice or triggered after A-37; trigger scheduling and action execution order are distinct. Exact run timestamps remain uncaptured (history displays 3h ago). Other affected records require their own history evidence.

A-1 does **not** set Operator Error or Misuse, MAIN Demotion Code, Manual Demotion Masking, or Confirmed Demotion Type in the shown action. It is not a direct replacement for A-39.

Potential downstream consumers, based on existing documentation and still subject to live re-verification: the headlands processing chain reads its completion/default state; A-26's captured trigger requires Investigation Not Complete, and A-28/other investigation-gated rules also consume investigation state; A-38 derives overall activities status; A-40 watches investigation/operator fields to derive scope. Creation-time ordering between A-1, incoming API data, and other automations must be tested rather than assumed.

##### Remaining identity and validation evidence
The trigger/action configuration capture is complete for the workflow shown. Remaining items are tracked separately and do not imply approval to migrate or retire A-1:
1. Full untruncated automation name and immutable automation ID if the UI exposes it; confirm the published configuration/version being reviewed.
2. Representative successful run details, including triggering record, action inputs/outputs, and ordering; required for behavioral validation, not inferred from the run count.

##### Proposed change — NOT current behavior
Brian suggested adding an explicit Not Determined option to Operator Error or Misuse and possibly initializing it in A-1. No option, assignment, or production change has been made by the agent. Treat this as a separate design decision after recording current behavior.

Unknown is not equivalent to No Operator Error or Misuse. Before introducing a nonempty unknown label, re-verify and update consumers that currently interpret nonempty as assessed. The documented A-40 In Scope branch checks operator status is not Misuse and is not empty; Not Determined would pass those checks for Interior Pass records. Review queue filters, other automation conditions, exports, Databricks CASE/NULL logic and metrics as well. Any initializer must also preserve valid incoming/completed assessments and avoid late creation-time overwrites. Stage validation in the isolated dev base after approval rather than changing A-1 during documentation capture.

##### Databricks Equivalent

**Historical sketch only — not an approved equivalent or runnable migration:** The SQL below preserves non-null values with COALESCE, whereas the shown Airtable action assigns fixed values. The action's Always setting is confirmed. Decide the intended handling of prepopulated records before choosing insert defaults versus forced initialization; preserving them would be a deliberate behavior change. Validate target schema separately; the sketch omits one of A-1's four fields.

```sql
-- In the sync job that creates new records in demotion_context
INSERT INTO jupiter_prod.jfa_metrics.demotion_context (
  -- ... other columns ...
  triage_activities_complete,
  investigation_complete,
  in_scope
  -- Note: headlands_assessment_complete is NOT in demotion_context
)
SELECT 
  -- ... other columns ...
  COALESCE(triage_activities_complete, 'Not Complete') AS triage_activities_complete,
  COALESCE(investigation_complete, 'Investigation Not Complete') AS investigation_complete,
  COALESCE(in_scope, 'Not Yet Determined') AS in_scope
FROM new_demotions_to_insert
```

##### Migration Notes and required tests
- The earlier sketch states that Headlands Assessment Complete is absent from demotion_context. Re-verify the chosen destination schema and all four field mappings; do not generalize that old note to every Databricks mirror.
- Do not use a recurring blanket UPDATE to implement a creation-only rule; it could reset reviewed records.
- Explicitly decide whether migration must reproduce overwriting prepopulated fields or intentionally preserve them. Document any intended behavior change separately from Airtable equivalence.
- Required cases: empty record creation; fully populated creation; creation with pre-existing Complete/In Scope values; subsequent update of an existing record; new versus existing upsert; duplicate delivery/retry; other classification actions before/after initialization; target record deleted before the update action.
- Verify initialization happens on the intended new-record identity only, leaves fields outside the four assignments unchanged, and does not reset completed triage on reruns. Where Airtable currently allows a race, record the observation and approve any Databricks ordering improvement explicitly.

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment Complete | Target mapping pending | OUTPUT | Explicit Headlands Not Complete assignment; omitted from historical SQL sketch |
| Investigation Complete | investigation_complete | OUTPUT | Explicit Investigation Not Complete assignment on creation trigger |
| Triage Activities Complete | triage_activities_complete | OUTPUT | Explicit Not Complete assignment on creation trigger |
| In Scope | in_scope | OUTPUT | Explicit Not Yet Determined assignment on creation trigger |

---

#### Evidence record A-2: Implement Path - Headlands

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots; the fixed reviewer reference was resolved with a read-only Airtable lookup.  
**Behavior/migration status:** NOT VERIFIED. The screenshots display successful step-test indicators, but expanded results and production execution history have not been captured. The agent did not run a test.  
**Displayed name:** A-2 Implement Path - Headlands  
**Group:** Headlands Assessment  
**Enabled:** ON in the supplied screenshots  
**Airtable Automation ID:** Not visible; retain A-2 as the inventory label, not an immutable ID.  
**Runs:** 77 this month displayed; earlier notes recorded 56. These are point-in-time UI counts, not proof of successful production runs.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, previously verified as `tblSJItXuuUd0lyHP`; name confirmed in the trigger panel.
- **Conditions:** Both are required, as shown in the full trigger card:
  1. `Implement Path Position Type Text` **is** `PT_Headland`.
  2. **AND** `Headlands Assessment Complete` **is** `Headlands Not Complete`.
- **Native event semantics shown:** Fires when a record starts matching; excludes records that already match. A currently matching row is not evidence that a new run will occur.
- No additional view, schedule, machine-type restriction, or trigger condition is shown. This does not establish the absence of restrictions elsewhere in the workflow.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action will run:** Always.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, confirmed in the expanded source picker. The preview record ID shown in that picker is a sample, not a hardcoded target; A_UID is not selected as the target record ID.
- **Assignments:**

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment | `h - Headlands Pass` | Fixed selection shown in the action |
| Headlands Reviewer | `reccXDh78Z9awPZbW` | Fixed linked-record ID; not the triggering user's identity |

**Reviewer reference:** Read-only lookup in Team Members (`tblHQdtGEVbhNRWMR`) returned record `reccXDh78Z9awPZbW` with exact Name value `"Automatic "` (one trailing space). Preserve that raw label in evidence; do not silently normalize it or confuse the display name with the configured record-ID literal. A separate dev base requires its own corresponding reference record/ID.

##### Purpose and dependency implications
Sets the combined headlands assessment and attributes it to the Automatic reference when the primary path is PT_Headland and the assessment-completion flag is explicitly Headlands Not Complete.

- `Headlands Assessment Complete` is **INPUT ONLY** for A-2; this action does not write it. The earlier INPUT/OUTPUT classification was incorrect.
- The action does not directly set Headlands vs Interior, Headlands Turn, investigation/activities completion, scope, or Operator Error or Misuse.
- Captured configurations establish the dependency: A-1 can set Headlands Not Complete, A-7 consumes `h - Headlands Pass` to set position/turn, and A-14 marks headlands complete when both breakout fields become nonempty. Runtime ordering remains a separate validation requirement; do not call A-6 the completion step.
- Both outputs are literal assignments with no shown fill-if-empty guard. They can replace a current assessment/reviewer when A-2 executes. Guard/event-order behavior, including an assessment completed by another action between trigger and update, needs behavioral testing.

##### Remaining identity and validation evidence
1. Immutable automation ID or stable link if available; published configuration/version and effective time.
2. Expanded View result / Review test results and representative run inputs/outputs. A green Step successful indicator alone does not establish correctness, timing, or complete production coverage.
3. Dependency and migration tests: enter PT_Headland with the exact completion flag; enter the flag after the path is present; already-matching records; blank/Headlands Unknown/Headlands Complete flags; changes away and back; late competing completion; existing manual reviewer/assessment; and missing/renamed Automatic reference in an isolated fixture.

##### Databricks SQL Equivalent

**Historical sketch only — incomplete, not an approved equivalent:** This CASE omits the Headlands Not Complete guard, reviewer assignment, and false-to-true event behavior. It must not be applied repeatedly over all PT_Headland rows as a migration. A complete design must represent both conditions and outputs, preserve existing-record/manual-assessment semantics as agreed, and remap the reviewer reference for dev.
```sql
-- A-2: When path position is PT_Headland, set headlands assessment
CASE 
  WHEN implement_path_position_type_text = 'PT_Headland' 
  THEN 'h - Headlands Pass'
END
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Implement Path Position Type Text | implement_path_position_type_text | INPUT | Exact PT_Headland comparison |
| Headlands Assessment Complete | Target mapping pending | INPUT | Exact Headlands Not Complete comparison; not written by A-2 |
| Headlands Assessment | Target mapping pending | OUTPUT | Fixed h - Headlands Pass assignment |
| Headlands Reviewer | Target mapping pending | OUTPUT | Linked Team Members record reccXDh78Z9awPZbW |

---

#### Evidence record A-3: Implement Path - In Field

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's supplied screenshots: trigger, Always execution setting, action table, target token source, and both assignments. Identity/published-version metadata remains pending.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or production execution history supplied, and no test performed by the agent.  
**Displayed name:** A-3 Implement Path - In Field  
**Group:** Headlands Assessment  
**Enabled:** ON in the screenshots  
**Airtable Automation ID:** Not visible; A-3 is the inventory label.  
**Runs:** 237 this month displayed; earlier notes recorded 125. Point-in-time UI counts do not establish successful execution or coverage.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** Both are required, as shown in the full trigger card:
  1. `Implement Path Position Type Text` **is** `PT_InField`.
  2. **AND** `Headlands Assessment Complete` **is** `Headlands Not Complete`.
- **Native event semantics shown:** Fires when a record starts matching; excludes records already matching. A current match alone does not prove a new run will happen.
- No additional view, schedule, machine-type restriction, or trigger condition is shown. Other workflow restrictions must be documented separately.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or extra actions shown.
- **Action will run:** Always — confirmed in the supplemental unobscured Configuration panel. No additional action-level condition or fill-if-empty guard is shown.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, confirmed in the supplemental expanded source picker showing the A-3 PT_InField trigger. The target is the triggering record, not a fixed record ID or A_UID.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment | `i - Interior Pass - No Headlands Turn` | Fixed selection shown in the action |
| Headlands Reviewer | `reccXDh78Z9awPZbW` | Fixed linked-record ID, matching the A-2 reference |

**Reviewer dependency:** The A-2 read-only lookup resolved this ID in Team Members (`tblHQdtGEVbhNRWMR`) to exact Name `"Automatic "` (one trailing space). This is not a triggering-user assignment or a literal reviewer-name string. Remap the reference record ID for the separate dev base; preserve the raw name in evidence.

##### Purpose and dependency implications
Assigns the combined interior-pass/no-headlands-turn assessment and reviewer reference when the primary path is PT_InField and the completion flag is exactly Headlands Not Complete.

- Headlands Assessment Complete is **INPUT ONLY**, not written by this action. Blank, Headlands Unknown, and Headlands Complete are not the shown trigger value.
- No direct writes to Headlands vs Interior, Headlands Turn, investigation/activities completion, scope, or Operator Error or Misuse are shown.
- Based on existing documentation, A-1 may establish the initial completion flag, A-8 consumes this combined assessment to set position/turn, and A-14 marks headlands complete. Re-verify those rules independently; do not assume atomic ordering.
- Both assignments are fixed values and execution is Always. They can replace an existing assessment/reviewer when the action executes; validate event ordering and competing updates separately.

##### Remaining identity and validation evidence
The trigger/action configuration shown is captured. This is not migration approval.
1. Immutable automation ID/stable link if available; published revision/version and effective time.
2. Representative test/run inputs, outputs, and ordering. Required migration cases: either trigger input arriving first; already-matching records; wrong/blank/unknown/completed flag; path changes away and back; existing manual assessment/reviewer; missing reviewer reference; and a competing completion between trigger and action.

##### Databricks SQL Equivalent

**Historical sketch only — incomplete, not an approved equivalent:** The CASE below omits the completion guard, reviewer assignment, and false-to-true trigger semantics. Do not run it repeatedly over all PT_InField records as a migration. Final field mappings, record identity, initialization order, and preservation of reviewed values require separate validation.
```sql
-- A-3: When path position is PT_InField, set headlands assessment
CASE 
  WHEN implement_path_position_type_text = 'PT_InField' 
  THEN 'i - Interior Pass - No Headlands Turn'
END
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Implement Path Position Type Text | implement_path_position_type_text | INPUT | Exact PT_InField comparison |
| Headlands Assessment Complete | Target mapping pending | INPUT | Exact Headlands Not Complete comparison |
| Headlands Assessment | Target mapping pending | OUTPUT | Fixed i - Interior Pass - No Headlands Turn assignment |
| Headlands Reviewer | Target mapping pending | OUTPUT | Fixed Team Members record reccXDh78Z9awPZbW |

---

#### Evidence record A-4: Implement Path - Turn

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's four supplied screenshots and explicit record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or production execution history supplied, and no test performed by the agent.  
**Displayed name:** A-4 Implement Path - Turn  
**Group:** Headlands Assessment  
**Enabled:** ON in the screenshots  
**Airtable Automation ID:** Not visible; A-4 is the inventory label, not an immutable ID.  
**Runs:** 156 this month displayed; earlier notes recorded 103. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** Both are required, as shown in the full trigger card:
  1. `Implement Path Position Type Text` **is** `PT_Turn`.
  2. **AND** `Headlands Assessment Complete` **is** `Headlands Not Complete`.
- **Native event semantics shown:** Fires when a record starts matching; excludes records already matching. A static match is not a guarantee of a new run.
- No additional view, schedule, machine-type restriction, or trigger condition is shown. Other workflow restrictions must be verified separately.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, shown in the expanded source picker and confirmed by Brian's convention. The action targets the triggering record, not a fixed record or A_UID.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment | `t - Interior Pass - Headlands Turn` | Fixed selection shown in the action |
| Headlands Reviewer | `reccXDh78Z9awPZbW` | Fixed linked-record ID, matching A-2 and A-3 |

**Reviewer dependency:** The read-only A-2 lookup resolved this ID in Team Members (`tblHQdtGEVbhNRWMR`) to exact Name `"Automatic "` (one trailing space). This is not the triggering user's identity. Preserve the configured ID and raw name in evidence; use a separately mapped dev reference record in the new base.

##### Purpose and dependency implications
Assigns the combined interior-pass/headlands-turn assessment and reviewer reference when the primary path is PT_Turn and headlands completion is exactly Headlands Not Complete.

- Headlands Assessment Complete is **INPUT ONLY**. A-4 does not mark the assessment complete; blank, Headlands Unknown, and Headlands Complete do not equal the required trigger value.
- The action does not directly set Headlands vs Interior, Headlands Turn, investigation/activities completion, scope, or Operator Error or Misuse. The combined label is not a direct write to the separate Headlands Turn field.
- A-1 can supply the initial completion flag; downstream breakout and completion automations consume the resulting assessment. Their definitions and ordering remain subject to separate re-verification.
- Both assignments are fixed values and execution is Always. They can replace an existing assessment/reviewer when the action runs. Do not assume an additional blank-field or preserve-manual-value guard.

##### Remaining identity and validation evidence
The core trigger/action configuration is captured, not approved for migration.
1. Immutable automation ID/stable link if available; published revision/version and effective time.
2. Representative test/run inputs, outputs, and ordering. Required cases: either prerequisite arriving first; already-matching records; non-PT_Turn path; blank/unknown/completed flag; path or completion flag leaving/re-entering the condition; existing manual values; missing reviewer reference; and competing completion/classification between trigger and action.

##### Databricks SQL Equivalent

**Historical sketch only — incomplete, not an approved equivalent:** The CASE below omits the Headlands Not Complete guard, fixed reviewer assignment, and event transition semantics. A recurring update over all PT_Turn rows would not reproduce the shown configuration. Any intentional migration improvements must be documented and approved separately.
```sql
-- A-4: When path position is PT_Turn, set headlands assessment
CASE 
  WHEN implement_path_position_type_text = 'PT_Turn' 
  THEN 't - Interior Pass - Headlands Turn'
END
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Implement Path Position Type Text | implement_path_position_type_text | INPUT | Exact PT_Turn comparison |
| Headlands Assessment Complete | Target mapping pending | INPUT | Exact Headlands Not Complete comparison |
| Headlands Assessment | Target mapping pending | OUTPUT | Fixed t - Interior Pass - Headlands Turn assignment |
| Headlands Reviewer | Target mapping pending | OUTPUT | Fixed Team Members record reccXDh78Z9awPZbW |

---

#### Evidence record A-5: Computed Path - Headlands

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED. The trigger displays a test-result indicator, but expanded results and action execution history were not supplied. No test was performed by the agent.  
**Displayed name:** A-5 Computed Path - Headlands  
**Group:** Headlands Assessment  
**Enabled:** ON in the screenshots  
**Airtable Automation ID:** Not visible; A-5 is the inventory label, not an immutable ID.  
**Runs:** 117 this month displayed; earlier notes recorded 71. These point-in-time UI counts do not establish successful execution or coverage.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL three are required, as shown in the full trigger card:
  1. `Implement Path Position Type Text` **is none of** `PT_Turn`, `PT_InField`, `PT_Headland`.
  2. **AND** `Headlands Assessment Complete` **is** `Headlands Not Complete`.
  3. **AND** `Computed Implement Path Position Type Text` **is** `PT_Headland`.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. This is not a scheduled rescan or an action on every edit.
- No additional view, schedule, machine-type restriction, or trigger condition is shown. Other workflow restrictions must be verified separately.
- Preserve the native is none of operator exactly. Whether empty/null primary values satisfy it requires semantic validation; do not assume SQL NOT IN has identical behavior.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention for these automations. A-5's token popup is not independently expanded in these captures; provenance is owner-confirmed, not inferred from a fixed sample ID.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment | `h - Headlands Pass` | Fixed selection shown in the action |
| Headlands Reviewer | `reccXDh78Z9awPZbW` | Fixed linked-record ID, matching A-2 through A-4 |

**Reviewer dependency:** The A-2 read-only lookup resolved this ID in Team Members (`tblHQdtGEVbhNRWMR`) to exact Name `"Automatic "` (one trailing space). This is not the triggering user's identity. Preserve the configured ID/raw label in evidence and remap it to a dev-owned reference record for the separate base.

##### Purpose and dependency implications
This is a **computed-path fallback**: it uses the computed PT_Headland value only when the primary path is none of the three listed standard values and headlands completion is explicitly Headlands Not Complete. It does not override an ordinary PT_Turn/PT_InField/PT_Headland primary value merely because the computed path says PT_Headland.

- Headlands Assessment Complete is **INPUT ONLY**, not written by A-5. Blank, Headlands Unknown, and Headlands Complete are not the required completion value.
- No direct writes to Headlands vs Interior, Headlands Turn, investigation/activities completion, scope, or Operator Error or Misuse are shown.
- Based on existing documentation, A-1 can establish the initial completion flag, A-7 consumes the resulting h - Headlands Pass assessment, and A-14 marks headlands complete. Re-verify downstream rules separately.
- Always execution makes both outputs literal assignments; there is no shown preserve-existing-assessment/reviewer guard.
- A late primary-path update can change eligibility relative to A-2/A-3/A-4. Record asynchronous action ordering and completion gating before migration rather than assuming rule numbers imply execution order.

##### Remaining identity and validation evidence
The core trigger/action configuration is captured, not approved for migration.
1. Immutable automation ID/stable link if available; published revision/version and effective time.
2. Expanded trigger test results, action outputs, and representative run history; the trigger test-result indicator is not proof the action executed correctly.
3. Required cases: each excluded primary value with computed PT_Headland; an allowed nonstandard primary; empty/null primary; non-headland/empty computed values; each completion state; each prerequisite arriving last; already-matching records; leave/re-enter conditions; existing manual values; missing reviewer reference; and delayed primary/computed updates competing with completion/direct-path actions.

##### Databricks SQL Equivalent

**Historical sketch only — incomplete, not an approved equivalent:** The CASE below omits the Headlands Not Complete guard, fixed reviewer assignment, and false-to-true event semantics. SQL NOT IN yields UNKNOWN for NULL; the equivalent Airtable blank behavior must be tested rather than silently adding or omitting a NULL branch. Any intentional behavior improvement belongs in a separate proposal.
```sql
-- A-5: Fallback - When primary path position is non-standard, use computed path position
CASE 
  WHEN implement_path_position_type_text NOT IN ('PT_Turn', 'PT_InField', 'PT_Headland')
    AND computed_implement_path_position_type_text = 'PT_Headland'
  THEN 'h - Headlands Pass'
END
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Implement Path Position Type Text | implement_path_position_type_text | INPUT | Native is none of PT_Turn, PT_InField, PT_Headland |
| Headlands Assessment Complete | Target mapping pending | INPUT | Exact Headlands Not Complete comparison |
| Computed Implement Path Position Type Text | computed_implement_path_position_type_text | INPUT | Exact PT_Headland comparison |
| Headlands Assessment | Target mapping pending | OUTPUT | Fixed h - Headlands Pass assignment |
| Headlands Reviewer | Target mapping pending | OUTPUT | Fixed Team Members record reccXDh78Z9awPZbW |

---

#### Evidence record A-7: Headlands Pass

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or production run history supplied. No test performed by the agent.  
**Displayed name:** A-7 Headlands Pass  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated in the captures).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-7 is the inventory label.  
**Runs:** 211 this month displayed in the supplied A-7 captures; earlier notes recorded 55. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `h - Headlands Pass`. This is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce the two outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown. Do not copy a completion guard from A-2 through A-6 into the description of A-7.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Headlands Pass.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Headlands Pass` | Fixed selection shown in the action |
| Headlands Turn | `N/A - Headlands Pass` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Splits the combined headlands-pass assessment into the two position/turn fields synced to Databricks.

- A-2 and A-5 are confirmed producers of h - Headlands Pass. A manually supplied assessment can also satisfy this condition; A-7 does not independently require A-1's completion/default fields.
- A-7 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- A-14's captured trigger requires both breakout fields to be nonempty and its action marks headlands complete. A-40's existing scope rules use Headlands vs Interior, but its captured five-field update trigger includes that position field; reading a field in a branch does not itself guarantee execution when that field changes.
- The two outputs are unconditional literal assignments when the action executes. There is no shown preserve-manual-value guard. Entering h - Headlands Pass can therefore update them even if headlands assessment was already complete.
- A-8 through A-10 are confirmed competing breakout writers; A-11 is now configuration-captured; A-12 is captured as displayed (fresh published-state confirmation pending); A-13 now has its core configuration captured. Changing the assessment while an earlier action is queued can produce stale writes; the planned initialization gate alone will not serialize those actions.
- Changing only an output while Headlands Assessment remains h - Headlands Pass does not re-enter this trigger. Leaving h - Headlands Pass does not make A-7 clear its outputs; other processing must handle that transition.
- For the proposed, deferred gate, preserve the single business condition and require initialization readiness if approved. Adding a Headlands Not Complete guard would be a separate behavior change, not a faithful transcription of A-7. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, full group label, and published revision/version/effective time.
2. Representative run inputs/outputs and isolated tests: entering/leaving/re-entering h - Headlands Pass, already-matching records, manual output edits, completed versus incomplete headlands flags, inputs present before initialization, and queued actions competing with other breakout rules or downstream completion/scope calculations.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** These CASE expressions represent the two assignments but omit record-transition eligibility and preservation of unaffected rows; an unmatched CASE yields NULL. Do not apply them as an unconditional overwrite of stored triage fields. The original A-6 comment is a legacy numbering error retained verbatim; this rule is A-7.
```sql
-- A-6: When Headlands Assessment is "h - Headlands Pass"
-- Set the two component fields
CASE WHEN headlands_assessment = 'h - Headlands Pass' THEN 'Headlands Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'h - Headlands Pass' THEN 'N/A - Headlands Pass' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact h - Headlands Pass comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Headlands Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed N/A - Headlands Pass assignment |

---

#### Evidence record A-8: Interior Pass - No Turn

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** Incomplete validation. Earlier supplied September 10 record revisions for CASE-A1-RESET attribute changes of the two breakout fields to A-8, corroborating writer identity; full run inputs/outputs and version correspondence remain uncaptured. No test performed by the agent.  
**Displayed name:** A-8 Interior Pass - No Turn  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated in the captures).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-8 is the inventory label.  
**Runs:** 245 this month displayed; earlier notes recorded 60. These point-in-time UI counts are not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `i - Interior Pass - No Headlands Turn`. This is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce the two outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - No Turn.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Interior Pass` | Fixed selection shown in the action |
| Headlands Turn | `Interior Pass - No Headlands Turn` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Splits the combined interior/no-turn assessment into the two position/turn fields synced to Databricks.

- A-3 is a confirmed producer of the trigger value. A-6's computed PT_InField fallback instead produces u - Interior - Unknown Turn, whose configuration-captured consumer is A-13, not A-8.
- A-8 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse. In particular, it cannot repair the investigation flag reset by A-1 in the September 10 example.
- A-14's captured trigger requires both breakout fields to be nonempty and its action marks headlands complete. A-40's existing scope branches use Headlands vs Interior, but its captured five-field update trigger includes that position field; a branch input alone does not guarantee execution on that input's change.
- A-7/A-9/A-10 are confirmed competing writers of these two outputs; A-11 is now configuration-captured; A-12 is captured as displayed (fresh published-state confirmation pending); A-13 now has its core configuration captured. A queued A-8 action could overwrite a newer assessment's breakout values. The initialization barrier alone will not serialize later writers.
- Always execution has no shown preserve-manual-value or completion guard. Entering this assessment value can update outputs even when headlands assessment is already complete. Editing outputs alone while the assessment stays matched does not retrigger A-8; leaving the assessment value does not make A-8 clear its outputs.
- For the proposed, deferred gate, retain the single business condition and add initialization readiness if approved. Do not silently add Headlands Not Complete; that would change the captured behavior. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, full group label, and published revision/version/effective time.
2. Full run inputs/outputs and isolated cases: enter/leave/re-enter the assessment, already-matching records, manual output edits, completed versus incomplete headlands flags, prepopulated assessment before initialization, and delayed competing breakout/completion/scope actions.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** These CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Do not apply them as an unconditional overwrite of stored triage fields. The original A-7 comment is a legacy numbering error retained verbatim; this rule is A-8.
```sql
-- A-7: When Headlands Assessment is "i - Interior Pass - No Headlands Turn"
CASE WHEN headlands_assessment = 'i - Interior Pass - No Headlands Turn' THEN 'Interior Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'i - Interior Pass - No Headlands Turn' THEN 'Interior Pass - No Headlands Turn' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact i - Interior Pass - No Headlands Turn comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Interior Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed Interior Pass - No Headlands Turn assignment |

---

#### Evidence record A-9: Interior Pass - Headlands Turn

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-9. No test performed by the agent.  
**Name:** A-9 Interior Pass - Headlands Turn in the inventory; sidebar label is truncated, while the action description shows Interior Pass - Headlands Turn in full.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-9 is the inventory label.  
**Runs:** 152 this month displayed; earlier notes recorded 35. These point-in-time UI counts are not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `t - Interior Pass - Headlands Turn`. The full trigger card confirms the value cropped in the condition selector; this is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - Headlands Turn.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Interior Pass` | Fixed selection shown in the action |
| Headlands Turn | `Headlands Turn` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Splits the combined interior/headlands-turn assessment into the two position/turn fields synced to Databricks. A Headlands Turn output does not mean Headlands vs Interior should be Headlands Pass; the configured position output is explicitly Interior Pass.

- A-4 is a confirmed producer of t - Interior Pass - Headlands Turn. A manually supplied assessment can also satisfy the condition; A-9 does not independently require A-1's completion/default fields.
- A-9 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- A-14's captured trigger requires both breakout fields to be nonempty and its action marks headlands complete. A-40's existing scope branches use Headlands vs Interior; its captured five-field update trigger includes that position field. Branch input dependencies do not guarantee triggering on every input change.
- A-7/A-8/A-10 are confirmed writers of the same output fields; A-10 assigns the same values as A-9. A-11 is now configuration-captured; A-12 is captured as displayed (fresh published-state confirmation pending); A-13 now has its core configuration captured. Queued actions can apply stale values after another assessment change; initialization gating alone does not serialize later writers.
- Always execution has no shown preserve-manual-value or completion guard. Entering this assessment value can update outputs on an already-completed headlands assessment. Output-only edits while the assessment remains matched do not retrigger A-9; leaving this assessment does not make A-9 clear its outputs.
- For the proposed, deferred gate, retain the single business condition and add initialization readiness if approved. Adding Headlands Not Complete would be a separate behavior change. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated automation/group names, and published revision/version/effective time.
2. Full run inputs/outputs and isolated cases: entering/leaving/re-entering the assessment, already-matching records, manual output edits, completed versus incomplete headlands flags, prepopulated assessment before initialization, and delayed competing breakout/completion/scope actions.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** The CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Do not use them as an unconditional overwrite of stored triage fields. The original A-8 comment is a legacy numbering error retained verbatim; this rule is A-9.
```sql
-- A-8: When Headlands Assessment is "t - Interior Pass - Headlands Turn"
CASE WHEN headlands_assessment = 't - Interior Pass - Headlands Turn' THEN 'Interior Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 't - Interior Pass - Headlands Turn' THEN 'Headlands Turn' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact t - Interior Pass - Headlands Turn comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Interior Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed Headlands Turn assignment |

---

#### Evidence record A-10: Interior Pass - Headlands Transition

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-10. No test performed by the agent.  
**Name:** A-10 Interior Pass - Headlands Transition in the inventory; sidebar label is truncated. Do not confuse the automation's transition input with its action description, which says Headlands Turn.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-10 is the inventory label.  
**Runs:** 129 this month displayed; earlier notes recorded 88. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `r - Interior Pass - Headlands Transition`. The full trigger card confirms the text cropped in the condition selector; this is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce the outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - Headlands Turn (not Headlands Transition), as shown in the Description field and action card.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Interior Pass` | Fixed selection shown in the action |
| Headlands Turn | `Headlands Turn` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
The screenshots confirm that A-10 maps the r transition assessment to the SAME two output values that A-9 assigns for the t headlands-turn assessment. The original assessment is not changed, but the two breakout fields alone no longer distinguish those inputs. Preserve this configured mapping rather than inventing a separate transition output.

- The producer of r - Interior Pass - Headlands Transition has not been established by the A-1 through A-9 captures. Do not infer a live computed-path producer from the historical combined SQL or proposed-automation table. A manually supplied assessment could also satisfy this trigger.
- A-10 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- A-14's captured trigger requires both breakout fields to be nonempty and its action marks headlands complete. A-40's existing scope branches use Headlands vs Interior; its captured five-field update trigger includes that position field; branch input dependencies do not guarantee triggering on every input change.
- A-7 through A-9 are confirmed writers of these outputs; A-11 also has its core configuration captured; A-12's displayed configuration is captured with a connection caveat; A-13 now has its core configuration captured. A-9 writes identical values, whereas other breakout writers can write conflicting values. Queued writes after assessment changes remain an ordering risk; initialization gating alone does not serialize them.
- Always execution has no shown preserve-manual-value or completion guard. Entering this assessment value can update outputs on an already-completed headlands assessment. Output-only edits while the assessment remains matched do not retrigger A-10; leaving the assessment does not make A-10 clear its outputs.
- For the proposed, deferred gate, preserve the single business condition and add initialization readiness if approved. Adding Headlands Not Complete would be a separate behavior change. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated automation/group names, and published revision/version/effective time.
2. Identify actual producers of the r assessment and their ordering relative to initialization.
3. Full run inputs/outputs and isolated cases: enter/leave/re-enter r, already-matching records, t-to-r and r-to-t transitions with identical breakout values, manual output edits, completed versus incomplete headlands flags, prepopulated assessment, and delayed competing breakout/completion/scope actions.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** These CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Do not use them as an unconditional overwrite of stored triage fields. The original A-9 comment is a legacy numbering error retained verbatim; this rule is A-10.
```sql
-- A-9: When Headlands Assessment is "r - Interior Pass - Headlands Transition"
CASE WHEN headlands_assessment = 'r - Interior Pass - Headlands Transition' THEN 'Interior Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'r - Interior Pass - Headlands Transition' THEN 'Headlands Turn' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact r - Interior Pass - Headlands Transition comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Interior Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed Headlands Turn assignment |

---

#### Evidence record A-11: Interior Pass - Interior Boundary

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-11. No test performed by the agent.  
**Name:** A-11 Interior Pass - Interior Boundary in the inventory; sidebar label is truncated, while the action description shows Interior Pass - Interior Boundary in full.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured. The first screenshot includes an address bar, but its identifiers have not been reliably transcribed; A-11 remains the inventory label.  
**Runs:** 2 this month displayed; earlier notes recorded 1. These point-in-time UI counts are not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `o - Interior Pass - Internal Obstacle/Boundary`. The full trigger card confirms the text cropped in the condition selector; this is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - Interior Boundary.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Interior Pass` | Fixed selection shown in the action |
| Headlands Turn | `Interior Boundary/Obstacle` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Splits the combined internal-obstacle/boundary assessment into position and turn-category fields. Preserve the exact distinct labels: the input says Internal Obstacle/Boundary, while the output says Interior Boundary/Obstacle. This is not the Headlands Turn assignment used by A-9/A-10.

- The producer of o - Interior Pass - Internal Obstacle/Boundary has not been established by the A-1 through A-10 captures. A manual assessment can satisfy the condition, but no particular upstream automation or importer is verified as the producer.
- A-11 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- A-14's captured trigger requires both breakout fields to be nonempty and its action marks headlands complete. A-40's existing scope branches use Headlands vs Interior; its captured five-field update trigger includes that position field; reading an input in a branch does not guarantee triggering on every change to it.
- A-7 through A-10 are confirmed writers of these output fields; A-12's displayed configuration is captured with a connection caveat; A-13 now has its core configuration captured. Delayed writes after assessment changes can overwrite a newer breakout value; initialization gating alone does not serialize these writers.
- Always execution has no shown preserve-manual-value or completion guard. Entering this assessment can update outputs on an already-completed headlands assessment. Output-only edits while the assessment remains matched do not retrigger A-11; leaving the assessment does not make A-11 clear its outputs.
- For the proposed, deferred gate, preserve the single business condition and add initialization readiness if approved. Adding Headlands Not Complete would be a separate behavior change. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated automation/group names, and published revision/version/effective time.
2. Identify actual producers of the o assessment and their ordering relative to initialization.
3. Full run inputs/outputs and isolated cases: enter/leave/re-enter o, already-matching records, transitions to/from other assessments, manual output edits, completed versus incomplete headlands flags, prepopulated assessment, and delayed competing breakout/completion/scope actions.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** The CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Do not use them as an unconditional overwrite of stored triage fields. The original A-10 comment is a legacy numbering error retained verbatim; this rule is A-11.
```sql
-- A-10: When Headlands Assessment is "o - Interior Pass - Internal Obstacle/Boundary"
CASE WHEN headlands_assessment = 'o - Interior Pass - Internal Obstacle/Boundary' THEN 'Interior Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'o - Interior Pass - Internal Obstacle/Boundary' THEN 'Interior Boundary/Obstacle' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact o - Interior Pass - Internal Obstacle/Boundary comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Interior Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed Interior Boundary/Obstacle assignment |

---

#### Evidence record A-12: Not Sure - Headlands vs Interior

**Definition status:** CORE CONFIGURATION CAPTURED as displayed in Brian's two supplied screenshots, with owner-confirmed trigger-record-ID convention.  
**Evidence caveat:** Both A-12 screenshots display Reconnecting. A later A-13 screenshot shows Reconnected, establishing connection recovery, but it does not revisit A-12's settings. Fresh A-12 server/published-state confirmation remains pending.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-12. No test performed by the agent.  
**Name:** A-12 Not Sure - Headlands vs Interior in the inventory; sidebar label is truncated. The action card shows Not Sure - Headlands vs Interior.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated).  
**Enabled:** ON as displayed in the screenshots, subject to the connection caveat above.  
**Immutable identity:** No verified automation ID/stable link captured; A-12 is the inventory label.  
**Runs:** 2 this month displayed, also recorded in earlier notes. This is a point-in-time UI count, not an execution-success or coverage measurement.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible. Connection recovery was observed in the subsequent A-13 capture; fresh A-12 settings, exact revision/version, and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, shown in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `n - Not Sure`. This is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown. A blank assessment is not the explicit n - Not Sure value required here.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action card label:** Not Sure - Headlands vs Interior. The Description editor itself is outside the supplied action-panel capture.
- **Action will run:** Always, shown in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, shown in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Not Sure` | Fixed selection shown in the action |
| Headlands Turn | `Not Sure` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Propagates an explicitly uncertain assessment into two explicitly uncertain breakout values. It does not clear these fields or treat Not Sure as a missing value.

- The producer of n - Not Sure has not been established by the A-1 through A-11 captures. A manually supplied assessment could satisfy the condition; the ELSE in historical SQL is not evidence of an equivalent live producer. This automation is not a general fallback for every blank/nonmatching assessment.
- A-12 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- Both outputs are nonempty and satisfy A-14's now-captured two-condition predicate, including when both are Not Sure. An actual run still requires entering the matching state; configuration eligibility is not proof a particular record ran. Uncertainty and assessment completion are separate concepts.
- A-40's captured five-field update trigger watches Headlands vs Interior, and its first branch assigns Outside of Scope for Not Sure regardless of operator/completion values. This closes the old watch-list gap; actual event delivery and scope writes still require run evidence.
- A-7 through A-11 are configuration-captured writers of these output fields; A-13 now has its core configuration captured. Delayed writes after assessment changes can replace newer breakout values; initialization gating alone does not serialize the writers.
- Always execution has no shown preserve-manual-value or completion guard. Entering n - Not Sure can overwrite previously specific outputs even on a completed assessment. Output-only edits while the assessment remains matched do not retrigger A-12; leaving n - Not Sure does not make A-12 clear its outputs.
- For the proposed, deferred gate, preserve the single business condition and add initialization readiness if approved. Adding Headlands Not Complete would be a separate behavior change. No gate has been implemented.

##### Remaining identity and validation evidence
1. Reconnected published-state confirmation, immutable automation ID/stable link, untruncated names, Description editor if needed, and revision/version/effective time.
2. Identify actual producers of n - Not Sure and their ordering relative to initialization.
3. Full run inputs/outputs and isolated cases: blank versus explicit n, enter/leave/re-enter n, already-matching records, transitions from specific assessments, manual output edits, completed versus incomplete flags, prepopulated assessment, and downstream completion/scope behavior with nonempty Not Sure values.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** These CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Preserve literal Not Sure separately from NULL. Do not use this as an unconditional overwrite of stored triage fields. The original A-11 comment is a legacy numbering error retained verbatim; this rule is A-12.
```sql
-- A-11: When Headlands Assessment is "n - Not Sure"
CASE WHEN headlands_assessment = 'n - Not Sure' THEN 'Not Sure' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'n - Not Sure' THEN 'Not Sure' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact n - Not Sure comparison, not a blank check |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed nonempty Not Sure selection |
| Headlands Turn | headlands_turn | OUTPUT | Fixed nonempty Not Sure selection |

---

#### Headlands Assessment - Process (OBSOLETE)

**Status:** Legacy OBSOLETE annotation; the existence and necessity of the two legacy names below have not been re-verified. A later sidebar capture identifies TP-1 Headlands Assessment as OFF under Triage Protocols, plus two OFF entries under Triage Investigations. Do not assume TP-1 is identical to either legacy name; see Additional Disabled Automation Inventory.

Earlier notes described the following as no longer required; that is historical coverage, not retirement approval:
- Headlands Protocol
- Headlands Vis Map Never Arrived

---

#### NEW AUTOMATIONS NEEDED: Computed Path Fallbacks

**Problem Identified:** A-5 only handles `Computed Implement Path Position Type Text = PT_Headland` as a fallback. Records with other computed values fall through and require manual assessment.

**View Filter for Manual Assessment Queue:**
```
WHERE Implement Path Position Type Text NOT IN ('PT_InField', 'PT_Turn', 'PT_Headland')
  AND Computed Implement Path Position Type Text IS NOT NULL
  AND (Headlands Assessment IS EMPTY OR ...)
```

**Historical proposal — not an approved creation list:** The numbering below predates the current inventory. The computed PT_InField fallback already exists as A-6 and is now configuration-captured; A-13 is the unknown-infield breakout, and A-14 is headlands completion. Do not create duplicate rules or reuse these labels based on this table. Other proposed fallbacks still need reconciliation against the live inventory.

**Key Insight:** "Computed" path is the LAST KNOWN position. When actual path is non-standard but computed has a value, we know the general area (Interior vs Headlands) but are UNCERTAIN about specifics (turn type). Therefore computed fallbacks use "Unknown Turn" variants.

| New Automation | Trigger (when primary ≠ standard) | Computed Field Value | → Headlands Assessment | Rationale |
|----------------|-----------------------------------|---------------------|------------------------|-----------|
| A-5 (exists) | Primary NOT IN standard | PT_Headland | h - Headlands Pass | Headlands is certain |
| A-13 (NEW) | Primary NOT IN standard | PT_InField | u - Interior - Unknown Turn | Interior certain, turn uncertain |
| A-14 (NEW) | Primary NOT IN standard | PT_Turn | u - Interior - Unknown Turn | Interior certain, turn uncertain |
| A-15 (NEW) | Primary NOT IN standard | PT_Transition_Implement | u - Interior - Unknown Turn | Interior certain, turn uncertain |
| A-16 (NEW) | Primary NOT IN standard | PT_Unknown | u - Interior - Unknown Turn | Everything uncertain |

**Historical combined SQL — incomplete and not an approved equivalent:** In particular, its computed PT_InField fallback assigns i - Interior Pass - No Headlands Turn, whereas the captured A-6 assigns u - Interior - Unknown Turn. It also omits completion guards, reviewer writes, and trigger-transition semantics. Original SQL/comments remain below as historical material, not a current implementation specification.
```sql
-- Combined logic using COALESCE for primary → computed fallback
CASE 
  WHEN implement_path_position_type_text IN ('PT_Headland') 
    OR (implement_path_position_type_text NOT IN ('PT_InField', 'PT_Turn', 'PT_Headland') 
        AND computed_implement_path_position_type_text = 'PT_Headland')
    THEN 'h - Headlands Pass'
    
  WHEN implement_path_position_type_text IN ('PT_InField') 
    OR (implement_path_position_type_text NOT IN ('PT_InField', 'PT_Turn', 'PT_Headland') 
        AND computed_implement_path_position_type_text = 'PT_InField')
    THEN 'i - Interior Pass - No Headlands Turn'
    
  WHEN implement_path_position_type_text IN ('PT_Turn') 
    OR (implement_path_position_type_text NOT IN ('PT_InField', 'PT_Turn', 'PT_Headland') 
        AND computed_implement_path_position_type_text = 'PT_Turn')
    THEN 't - Interior Pass - Headlands Turn'
    
  WHEN computed_implement_path_position_type_text = 'PT_Transition_Implement'
    THEN 'r - Interior Pass - Headlands Transition'
    
  WHEN computed_implement_path_position_type_text = 'PT_Unknown'
    THEN 'u - Interior - Unknown Turn'
    
  ELSE 'n - Not Sure'
END AS headlands_assessment_computed
```

---

#### Evidence record A-13: Interior Pass - Unknown Infield

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-13. No test performed by the agent.  
**Name:** A-13 Interior Pass - Unknown Infield in the inventory; sidebar label is truncated. The action description instead says Interior Pass - Interior Boundary; preserve this mismatch rather than using the description to infer assignments.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; sidebar group label is truncated).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured. The first screenshot includes an address bar, but its identifiers have not been reliably transcribed; A-13 remains the inventory label.  
**Runs:** 263 this month displayed; earlier notes recorded 52. These point-in-time UI counts are not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Connection/version evidence:** The first screenshot displays Reconnected. No unpublished-change banner is visible, but exact published revision/version and effective time remain uncaptured. This is not a fresh capture of A-12's settings.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Headlands Assessment` **is** `u - Interior - Unknown Turn`. The full trigger card confirms the text cropped in the condition selector; this is the single configured condition shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.
- No Headlands Assessment Complete, Investigation Complete, machine-type, or initialization-ready condition is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - Interior Boundary, as shown in both the Description field and action card. This is not the configured turn assignment.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands vs Interior | `Interior Pass` | Fixed selection shown in the action |
| Headlands Turn | `Not Sure` | Fixed selection shown in the action |

##### Purpose, dependencies, and gating audit
Preserves a known interior position while representing uncertainty about turn status. Unlike A-12, only the turn output is Not Sure; unlike A-11, it does not assign Interior Boundary/Obstacle despite the matching action description.

- A-6 is a confirmed producer of u - Interior - Unknown Turn. Its computed PT_InField fallback feeds this breakout rule, not A-8's no-turn rule. A manually supplied assessment could also satisfy the condition.
- A-13 does not write Headlands Assessment, Headlands Reviewer, Headlands Assessment Complete, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- Interior Pass / Not Sure are both nonempty and satisfy A-14's now-captured predicate. An actual run still requires entering the matching state; a current match is not proof of execution. Unknown turn and incomplete assessment are not interchangeable states.
- A-40's captured scope branches use and watch the Interior Pass position, not the turn field. With a nonempty non-Misuse operator value and no first-branch exclusion, it assigns In Scope even when Headlands Turn is Not Sure. This differs from A-12's Not Sure position, which meets the first Outside of Scope branch. Actual run outcomes remain unverified.
- A-7 through A-12 have displayed configurations captured as other writers of the two output fields, with A-12's fresh published-state confirmation pending. Queued actions after assessment changes can overwrite newer breakout values; initialization gating alone does not serialize these writers.
- Always execution has no shown preserve-manual-value or completion guard. Entering this assessment can update outputs on an already-completed headlands assessment. Output-only edits while the assessment remains matched do not retrigger A-13; leaving the assessment does not make A-13 clear its outputs.
- For the proposed, deferred gate, preserve the single business condition and add initialization readiness if approved. Adding Headlands Not Complete would be a separate behavior change. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated automation/group names, and published revision/version/effective time.
2. Full run inputs/outputs and isolated cases: A-6-to-A-13 handoff, enter/leave/re-enter u, already-matching records, transitions between n/u/i/o assessments, manual output edits, completed versus incomplete flags, prepopulated assessment, delayed competing writers, and downstream completion/scope behavior with Interior Pass / Not Sure.

##### Databricks SQL Equivalent

**Historical value sketch only — not an approved event-equivalent implementation:** The CASE expressions represent the assignments but omit record-transition eligibility and preservation of unaffected rows; unmatched cases yield NULL. Preserve literal Not Sure separately from NULL. Do not use this as an unconditional overwrite of stored triage fields. The original A-12 comment is a legacy numbering error retained verbatim; this rule is A-13.
```sql
-- A-12: When Headlands Assessment is "u - Interior - Unknown Turn"
CASE WHEN headlands_assessment = 'u - Interior - Unknown Turn' THEN 'Interior Pass' END AS headlands_vs_interior,
CASE WHEN headlands_assessment = 'u - Interior - Unknown Turn' THEN 'Not Sure' END AS headlands_turn
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands Assessment | Target mapping pending | INPUT | Exact u - Interior - Unknown Turn comparison |
| Headlands vs Interior | headlands_vs_interior | OUTPUT | Fixed Interior Pass assignment |
| Headlands Turn | headlands_turn | OUTPUT | Fixed nonempty Not Sure selection |

---

#### Evidence record A-6: Computed Path - In Field

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's four supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** NOT VERIFIED. The action UI displays Step successful and Step run 3 days ago, but expanded results and production run history were not supplied. No test performed by the agent.  
**Displayed name:** A-6 Computed Path - In Field  
**Group:** Headlands Assessment  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified machine-readable automation ID/stable link captured; an address bar is visible in the first screenshot but has not been reliably transcribed. A-6 remains the inventory label.  
**Runs:** 211 this month displayed; earlier notes recorded 83. These are point-in-time UI counts, not proof of successful execution or coverage.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL three are required, confirmed by the full trigger card and complementary condition-panel captures:
  1. `Implement Path Position Type Text` **is none of** `PT_Turn`, `PT_InField`, `PT_Headland`.
  2. **AND** `Headlands Assessment Complete` **is** `Headlands Not Complete`.
  3. **AND** `Computed Implement Path Position Type Text` **is** `PT_InField`.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. This is not a scheduled sweep or an action on every edit.
- No additional view, schedule, machine-type restriction, or initialization-ready flag is shown.
- Preserve the native is none of operator; behavior for a blank primary value requires validation rather than assuming equivalence to SQL NOT IN on NULL.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. Provenance is owner-confirmed; no new expanded token popup required.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment | `u - Interior - Unknown Turn` | Fixed selection shown in the action |
| Headlands Reviewer | `reccXDh78Z9awPZbW` | Fixed linked-record ID, matching A-2 through A-5 |

**Reviewer dependency:** The A-2 read-only lookup resolved this record in Team Members (`tblHQdtGEVbhNRWMR`) to exact Name `"Automatic "` (one trailing space). It is not the triggering user's identity. Preserve the configured ID/raw label and remap the reference in a separate dev base.

##### Purpose, dependencies, and gating audit
This computed-path fallback establishes an interior location but leaves turn status unknown. Unlike A-3's primary PT_InField rule, it does NOT assign i - Interior Pass - No Headlands Turn.

- Headlands Assessment Complete is **INPUT ONLY**; A-6 does not mark it complete. It does not directly write Headlands vs Interior, Headlands Turn, Investigation Complete, Triage Activities Complete, In Scope, or Operator Error or Misuse.
- A-1 can supply Headlands Not Complete. This is a headlands-specific prerequisite, not an explicit global initialization barrier; existing/prepopulated values or later edits must not be assumed to prove initialization readiness.
- A-13's captured configuration consumes u - Interior - Unknown Turn and sets Interior Pass / Not Sure. A-14's captured configuration marks headlands complete when both breakout fields become nonempty, including that pair. Unknown turn is not necessarily the same as an incomplete headlands assessment; runtime ordering remains a separate validation requirement.
- A-2 through A-6 are known competing writers of Headlands Assessment and Headlands Reviewer. Their conditions can be disjoint at one instant yet asynchronous runs can overlap after primary/computed inputs change. Always execution provides no shown preserve-existing-value guard.
- For the proposed, deferred gate: retain all three business conditions and add initialization readiness if approved. Readiness must release already-eligible new records without replaying historical records; it will not by itself resolve stale competing path updates. No gate has been implemented.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link and published revision/version/effective time.
2. Expanded test inputs/outputs and production execution history; the displayed success indicator is not full behavioral verification.
3. Isolated cases: each excluded primary value, nonstandard and blank primary, computed PT_InField versus other/blank values, each completion state, each prerequisite arriving last, already-matching records, leave/re-enter conditions, manual assessment/reviewer values, missing reviewer reference, and delayed computed-path actions competing with primary-path or completion updates.

##### Databricks SQL Equivalent

**Historical sketch only — incomplete, not an approved equivalent:** This CASE omits the completion guard, reviewer assignment, and event transition semantics. Blank primary values need explicit equivalence testing. The original A-13 SQL comment is a legacy numbering error retained verbatim; this rule is A-6. The earlier combined SQL also incorrectly assigns the no-turn variant to this computed PT_InField fallback and is flagged separately.
```sql
-- A-13: Fallback - When primary is non-standard but computed is PT_InField
CASE 
  WHEN implement_path_position_type_text NOT IN ('PT_Turn', 'PT_InField', 'PT_Headland')
    AND computed_implement_path_position_type_text = 'PT_InField'
  THEN 'u - Interior - Unknown Turn'
END
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Implement Path Position Type Text | implement_path_position_type_text | INPUT | Native is none of PT_Turn, PT_InField, PT_Headland |
| Headlands Assessment Complete | Target mapping pending | INPUT | Exact Headlands Not Complete comparison |
| Computed Implement Path Position Type Text | computed_implement_path_position_type_text | INPUT | Exact PT_InField comparison |
| Headlands Assessment | Target mapping pending | OUTPUT | Fixed u - Interior - Unknown Turn assignment |
| Headlands Reviewer | Target mapping pending | OUTPUT | Fixed Team Members record reccXDh78Z9awPZbW |

---

#### Evidence record A-14: Headlands Assessment Complete

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention.  
**Behavior/migration status:** Incomplete validation. Earlier supplied September 10 record revisions for CASE-A1-RESET attribute a Headlands Complete assignment to A-14; full run inputs/outputs, version correspondence, and broader behavior remain unverified. No test performed by the agent.  
**Name:** A-14 Headlands Assessment Complete in the inventory; sidebar label is truncated. The action description instead says Interior Pass - Interior Boundary; preserve the description but do not infer its assignments from that label.  
**Group:** Headlands Assessment - Path Position Breakout (inventory name; group label is not fully visible in these captures).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-14 is the inventory label.  
**Runs:** 341 this month displayed. This is a point-in-time UI count, not an execution-success or coverage measurement.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

##### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required, confirmed in the trigger card and condition panel:
  1. `Headlands vs Interior` **is not empty**.
  2. **AND** `Headlands Turn` **is not empty**.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously recompute completion.
- No check of the combined Headlands Assessment, reviewer, existing completion status, investigation status, classification, machine type, or initialization-ready flag is shown. No Not Sure exclusion or cross-field consistency check is shown.

##### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Interior Pass - Interior Boundary, as shown in the Description field and action card.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention. No separate source-picker capture requested.

| Field | Assigned value | Value source/type |
|-------|----------------|-------------------|
| Headlands Assessment Complete | `Headlands Complete` | Fixed selection; the only field in the full action capture |

##### Purpose, dependencies, and gating audit
Marks the headlands assessment complete when both breakout selections are populated. This measures populated assessment fields, not certainty about position/turn or completion of the overall investigation.

- Not Sure is a nonempty selection. Consequently, the configured predicate accepts both A-12's Not Sure / Not Sure pair and A-13's Interior Pass / Not Sure pair. This settles configuration eligibility, not whether a particular record entered the condition or its run succeeded. Do not silently replace this with a known-value-only condition in migration.
- A-7 through A-13 are captured producers of the two inputs (A-12 retains its fresh published-state caveat). Manual/prepopulated values can also satisfy the predicate; A-14 does not verify their source or agreement with the combined assessment.
- A-14 writes ONLY Headlands Assessment Complete. It does not write Investigation Complete, Triage Activities Complete, In Scope, reviewer, classification, or either breakout input. It cannot repair the investigation flag reset by A-1.
- A-1 is another confirmed writer of Headlands Assessment Complete and assigns Headlands Not Complete. A late A-1 write could reset A-14's output while both trigger inputs remain populated; changing only the completion flag would not re-enter A-14's predicate. This analogous headlands race is a configuration-derived risk, not a separately observed failure in the September 10 record, whose history shows headlands completion recovering.
- Clearing either input makes the trigger false but does not run an inverse action here. Therefore A-14 alone does not clear/reopen an existing Headlands Complete status when a breakout field becomes empty. Changing one nonempty pair to another also does not necessarily create a new matching transition.
- If an input is cleared after the trigger but before its queued Always update, A-14 may still write completion; runtime input rechecking/ordering needs validation. The proposed initialization barrier does not resolve every later edit race.
- A-2 through A-6 read this flag as part of their exact Headlands Not Complete prerequisites; A-28's captured trigger instead requires Headlands Complete before classifying MAIN 12.35. A-38's captured update trigger watches this flag and its Complete branch requires Headlands Complete alongside the other completion criteria; its Otherwise branch sets overall activities Not Complete.
- For the proposed, deferred gate, preserve BOTH nonempty conditions and require initialization readiness if approved. Any change to uncertainty handling, automatic reopening, or reassertion after a reset is a separate behavior change. No gate has been implemented.

##### Headlands Assessment Chain
1. **A-2 through A-6:** Set Headlands Assessment and the Automatic reviewer reference; core configurations captured. These do not establish the producers of every manually available assessment label.
2. **A-7 through A-13:** Set Headlands vs Interior and Headlands Turn; all seven displayed configurations captured, with fresh A-12 published-state confirmation still pending.
3. **A-14:** Set Headlands Assessment Complete = Headlands Complete when both breakout fields become nonempty; core configuration now captured.

This is a dependency outline, not a guarantee of ordered execution between separate automations. The previous outline swapped A-6 and A-13. Identity/version and broader runtime validation remain separate for the chain.

##### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated automation/group names, and published revision/version/effective time.
2. Full run inputs/outputs and isolated cases: each input arriving last, either/both blank, Not Sure pairs, no combined assessment/reviewer, prepopulated inputs before initialization, already-matching records, nonempty-to-nonempty changes, clearing/repopulating inputs, manual flag changes, delayed A-1 or A-14 writes, and downstream A-38 handling.

##### Databricks SQL Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** A recurring UPDATE over all populated rows would reassert completion without a new trigger transition and could repair resets that Airtable leaves untouched. The target column/mapping is not validated by this sketch. Preserve literal Not Sure as populated and do not add an inverse reset for blank inputs without separately approving the behavior change. Original SQL/comment retained below.
```sql
-- A-14: When both headlands fields are populated, mark assessment complete
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET headlands_assessment_complete = 'Headlands Complete'
WHERE headlands_vs_interior IS NOT NULL 
  AND LENGTH(headlands_vs_interior) > 0
  AND headlands_turn IS NOT NULL 
  AND LENGTH(headlands_turn) > 0;
```

##### Columns Used
| Airtable Column | DBX Column | Direction | Notes |
|-----------------|------------|-----------|-------|
| Headlands vs Interior | headlands_vs_interior | INPUT | Native is not empty; includes Not Sure |
| Headlands Turn | headlands_turn | INPUT | Native is not empty; includes Not Sure |
| Headlands Assessment Complete | Target mapping pending | OUTPUT | Fixed Headlands Complete assignment |

---

#### Confirmed Halt Code Automations (A-15 through A-25)

**Status:** CURRENT RE-AUDIT IN PROGRESS. The earlier ALL VERIFIED label (2026-09-07) described legacy coverage, not a complete current specification. A-15's core configuration is captured, including its Name projection. A-16/A-17 configurations are captured as displayed, with dynamic source-step provenance/link conversion still unverified. A-18's displayed configuration now includes confirmed Always execution and target table; its dynamic source provenance/link resolution remain pending. A-19's core configuration and literal 12.27 assignment are captured. A-20's core configuration, literal 12.24 assignment, and 12.27 exclusion are captured. A-21's core configuration, literal 12.29 assignment, and 12.24/12.27 exclusions are captured. A-22's visible configuration is captured, including its four-condition trigger and Secondary Demotion Manual source token. Display Name is observed, but the token's data path/projection and resolved value remain unverified. A-23's displayed configuration is captured, including its five-condition trigger and confirmed Secondary Demotion Manual source token. Its resolved data path/link conversion remain unverified. A-24's complete configuration is captured, including its six-condition trigger and Always action assigning literal 12.X1 / Manual Mask. A-25's configuration is captured from screenshots and Brian's explicit same-as-A-24-except-12.X2 confirmation. All eleven A-15 through A-25 visible configurations are now captured, with the noted data-path gaps retained. Identity/version and runtime validation remain separate.

**Key Question:** When the operator manually demoted (DR-1/DR-2), was the machine already stopped due to a perception/system issue?

##### Quick Reference Table

| # | Name | Trigger Summary | MAIN Demotion Code | Manual Demotion Masking |
|---|------|-----------------|-------------------|------------------------|
| A-15 | Secondary Demotion Manual | Empty + Preceding exists + DR-1/DR-2 | *(not set)* | *(not set)* |
| A-16 | Manual Initial - N/A Preceding | Reason has DR-1/DR-2 + Secondary includes N/A | Halt Code - Import token | Intended Manual Demotion - No Mask |
| A-17 | Manual Initial - Manual Secondary | Reason has DR-1/DR-2 + secondary reason has DR-1/DR-2 | Halt Code - Import token | Intended Manual Demotion - No Mask |
| A-18 | Non Manual Initial | Reason has none of DR-1/DR-2; no separate nonempty guard | Halt Code - Import token | N/A |
| A-19 | 12.27 | Secondary includes 12.27 + Reason has DR-1/DR-2 | Literal 12.27 name | Manual Mask |
| A-20 | 12.24 | Secondary includes 12.24, excludes 12.27 + Reason has DR-1/DR-2 | Literal 12.24 name | Manual Mask |
| A-21 | 12.29 | Secondary includes 12.29, excludes BOTH 12.24/12.27 + Reason has DR-1/DR-2 | Literal 12.29 name | Manual Mask |
| A-22 | Interrupted Stop Code | Secondary nonempty + secondary DR-4/6/7/8/9/11/12/13 + excludes 12.24/12.27/12.29/N/A + primary DR-1/DR-2 | Secondary Demotion Manual token (resolved representation pending) | Manual Mask |
| A-23 | False Positive | Secondary nonempty + excludes 12.24/12.27/12.29 + secondary exactly DR-3 + excludes seven secondary reasons + primary DR-1/DR-2 | Secondary Demotion Manual token (resolved representation pending) | Manual Mask |
| A-24 | 12.X1 | All five A-23 predicates + Secondary includes linked 12.X1 | Literal 12.X1 name | Manual Mask |
| A-25 | 12.X2 | All five A-23 predicates + Secondary includes linked 12.X2; owner confirms otherwise same as A-24 | Literal 12.X2 name | Manual Mask |

**Captured predicate precedence within A-19/A-20/A-21:** 12.27 > 12.24 > 12.29 for a qualifying manual reason and a fixed secondary-link set. A-20 excludes 12.27; A-21 excludes BOTH 12.24 and 12.27. This establishes mutually exclusive eligibility within the trio, not automation execution order or priority over all other masking rules. Each can still overlap A-16 when N/A accompanies its eligible code.

This group of automations determines:
1. **Manual Demotion Masking** - Whether a manual demotion was masking an underlying issue
2. **MAIN Demotion Code** - Updates to secondary code when masking is detected
3. **Secondary Demotion Manual** - Links the secondary demotion when applicable

##### Key Fields

| Field | Values | Purpose |
|-------|--------|---------|
| `manual_demotion_masking` | "N/A", "Intended Manual Demotion - No Mask", "Manual Mask" | Indicates if manual demotion was masking a perception/system issue |
| `main_demotion_code` | Halt code (e.g., "12.27") | The confirmed root cause halt code |
| `secondary_demotion_manual` | Linked halt code or "N/A" | The underlying/secondary halt code |

##### Demotion Reason Categories

| DR Code | Name | Type |
|---------|------|------|
| DR-1 | In-Cab Controls Override | Manual |
| DR-2 | Human-Triggered Demotion | Manual |
| DR-3 | Perception "Saw Something" | Perception (False Positive) |
| DR-4 | Perception Internal System Failure | Perception |
| DR-6 | Gen4/VADC Misc Error | System |
| DR-7 | Perception Image Quality | Perception |
| DR-8 | Guidance & Geo | Vehicle |
| DR-9 | Spark | System |
| DR-11 | Operator Error | Manual |
| DR-12 | Perception Configuration | Perception |
| DR-13 | Vehicle Operation Check | Vehicle |

---

#### Evidence record A-15: Secondary Demotion Manual

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's screenshots and explicit confirmation that the dynamic assignment uses Name. Trigger, execution setting, target table/record, destination, source step/field, and Name projection are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-15. No test performed by the agent.  
**Name:** A-15 Secondary Demotion Manual in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed for the group).  
**Enabled:** ON in the screenshots  
**Immutable identity:** Address bars are visible, but no verified machine-readable automation ID/stable link has been transcribed; A-15 remains the inventory label.  
**Runs:** 672 this month displayed; earlier notes recorded 216/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL three are required; the full trigger card reveals both reason labels cropped in the selector:
  1. `Secondary Demotion Manual` **is empty**.
  2. **AND** `Preceding Stop Code` **is not empty**.
  3. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- The reason predicate is any-match, not an exact-only comparison of the complete lookup result, and uses Demotion Reason rather than MAIN Demotion Reason.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously copy changes to the preceding code.
- No completion, machine-type, masking, or initialization-ready condition is shown. The DR-1/DR-2 selection must not be expanded to every reason described elsewhere as manual.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Empty; the Description editor shows its Enter a description placeholder.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** `When a record matches conditions` → `Airtable record ID`, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Evidence status |
|-------|------------------|-----------------|
| Secondary Demotion Manual | `When a record matches conditions` → `Preceding Stop Code` → `Make a new list of: Name` | Source step/field captured in the picker and tooltip; Name projection explicitly confirmed by Brian and shown in the supplemental picker. |

Brian confirmed: it uses the name. The action supplies the Name properties of the preceding linked records to the destination linked-record field, using name-based link resolution rather than directly supplying their IDs. This Name property is not evidence that the separate Halt Codes column Code Name was selected. The target demotion's Airtable record ID is a different token and remains sourced from the trigger. The earlier ambiguity about the shaded Name row is resolved by Brian's explicit confirmation.

###### Field types and dependencies
The earlier read-only production schema response identifies:
- Preceding Stop Code: multipleRecordLinks, field fldkMQXjugFZoR0ED, linked to Halt Codes (tblN8uu4Gl1eDZMLs), prefersSingleRecordLink = true.
- Secondary Demotion Manual: multipleRecordLinks, field fldzCC2DDW9tweN0s, linked to the same Halt Codes table, prefersSingleRecordLink = false.
- Demotion Reason: multipleLookupValues with a linked-record result.

The single-record preference is not proof every historical/imported value has exactly one element. The configured projection supplies a list of Names; preserve cardinality and validate destination name resolution. Duplicate names, renamed records, whitespace/case differences, and missing matches require isolated validation; the captures do not establish whether ambiguous/missing names fail, select a particular record, or create records. This is a dependency/risk, not evidence A-15 caused the earlier duplicate-halt-code incident. Switching to ID-based assignment would be a separate proposed behavior change, not a faithful transcription of the current configuration.

###### Purpose and gating audit
The documented intent is to seed an empty manual-secondary link from the preceding stop for DR-1/DR-2 demotions, making that candidate available to later masking/main-code rules. It does not itself establish that masking occurred.

- A-15 does NOT write MAIN Demotion Code, Manual Demotion Masking, Confirmed Demotion Type, investigation/headlands/activities completion, reviewer, scope, or operator-error status.
- A-16's captured trigger matches any secondary-link set containing N/A, not only an N/A-only set. A-17's captured trigger reads Secondary Demotion Reason, whose schema-confirmed source is Secondary Demotion Manual. A-18 is now captured as another writer of Secondary Demotion Manual, assigning the literal N/A name. Dynamic MAIN-source provenance/link conversion validation remains pending for A-16 through A-18; A-19's captured rule consumes secondary links including 12.27; A-20's captured rule consumes secondary links including 12.24 and excluding 12.27; A-21's captured rule consumes secondary links including 12.29 and excluding BOTH 12.24/12.27; A-22 through A-25 still need current rule/source re-verification. Do not assume rule numbers define execution order.
- The empty-destination check is in the trigger, while the action executes Always. It is not a proven action-time protection against a manual/automated fill after triggering but before the queued update; assignment/overwrite behavior must be tested.
- If the assignment fills the destination, the trigger becomes false. Subsequent preceding-code changes alone will not qualify while the destination remains populated. Clearing the secondary link can re-enter the condition if the other predicates hold, including after a linked-record deletion; do not attribute any past incident to that mechanism without evidence.
- A linked placeholder named N/A is not an empty link. Validate this case separately from missing data before changing fallback or masking behavior.
- For the proposed, deferred gate, retain all three predicates and add initialization readiness if approved. Preserve the destination-empty condition and audit downstream cascades before releasing historical records. No gate has been implemented.

###### Remaining identity and validation evidence
The core trigger/action configuration, including Name projection, is captured; this is not migration approval.
1. Immutable automation ID/stable link, untruncated name, and published revision/version/effective time.
2. Historical resolved action inputs/outputs and isolated cases: each prerequisite arriving last, already-matching records, nonempty destination, mixed reason lookups, empty versus linked N/A preceding code, multiple linked values, duplicate/renamed/unmatched names, whitespace/case behavior, later source edits, destination clearing, concurrent manual fill, and downstream routing.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT/OUTPUT | Empty predicate and sole action destination |
| Preceding Stop Code | INPUT | Nonempty predicate and confirmed dynamic source field; supplies the list of Names |
| Demotion Reason | INPUT | Has any of the two specified manual reasons |

---

#### Evidence record A-16: Manual Initial - N/A Preceding

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED from Brian's two supplied screenshots: both trigger predicates, Always setting, target table/record token, and both assignments. The dynamic field token is fully readable; its source-step picker and runtime link conversion have not been independently inspected.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-16. No test performed by the agent.  
**Name:** A-16 Manual Initial - N/A Preceding in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-16 is the inventory label.  
**Runs:** 607 this month displayed; earlier notes recorded 164/month. These point-in-time UI counts are not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms labels cropped in the selector:
  1. `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
  2. **AND** `Secondary Demotion Manual` **has any of** `N/A`.
- Demotion Reason is used, not MAIN Demotion Reason. The first predicate is an any-match on the lookup, not an exact-only reason-set comparison.
- N/A is a linked-record selection here, not an empty field. Has any of N/A does not require that N/A is the ONLY secondary link. The rule does not directly test Preceding Stop Code despite its name.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce MAIN or masking.
- No current MAIN-empty check, existing-masking guard, completion, machine-type, or initialization-ready condition is shown.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description evidence:** No description text appears on the action card; the Description editor is outside the supplied action-panel capture.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `Halt Code - Import` | Fully visible dynamic field token; source-step picker not expanded |
| Manual Demotion Masking | `Intended Manual Demotion - No Mask` | Fixed selection shown in the action |

###### Field types and link resolution
The earlier read-only production schema identifies Halt Code - Import as a singleSelect (fldC0SRCo4mm8OHEV), whereas MAIN Demotion Code is multipleRecordLinks (fldw0GEHxF0PFRSof) pointing to Halt Codes (tblN8uu4Gl1eDZMLs), with prefersSingleRecordLink = true. Thus the old description of the SOURCE as a linked record was inaccurate: this is a single-select-field token assigned into a linked destination, not a demonstrated direct copy of a Halt Codes record ID.

Preserve the visible Halt Code - Import token selection. Do not import A-15's list-of-Names projection into A-16 by assumption, or confuse a single-select choice ID with a Halt Codes record ID. Source-step provenance, resolved runtime value, and destination lookup behavior can be validated with the picker or an existing successful run. Duplicate/unmatched code labels, reference renames, and link cardinality remain migration-validation concerns.

###### Purpose, dependencies, and gating audit
The configured rule treats a DR-1/DR-2 demotion whose secondary links include N/A as no-mask, retaining the imported halt code as MAIN. This describes the rule's assignment; it is not independent evidence that no underlying stop existed, especially for mixed secondary-link sets.

- A-15 can seed Secondary Demotion Manual from the preceding stop's Name list, including a linked N/A placeholder. That is a possible dependency, not proof A-15 populated every qualifying record.
- A-16 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not write Secondary Demotion Manual, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope.
- A-34's captured rule consumes the no-mask value and MAIN Demotion Reason any of DR-1/DR-2 to assign Intended Manual Demotion, No Operator Error or Misuse, and Investigation Complete, without an incomplete-investigation prerequisite. Do not attribute those downstream assignments directly to A-16; actual eligibility/order remains separate.
- A-17 is now a configuration-captured MAIN/masking writer with the same assignments as A-16 but a different secondary predicate. A-18 is now captured as displayed, including its secondary N/A assignment; A-19's literal 12.27 / Manual Mask assignments are captured; A-20's 12.24 / Manual Mask assignments and 12.27 exclusion are captured; A-21's 12.29 / Manual Mask assignments and 12.24/12.27 exclusions are captured; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending. Captured predicate overlaps include A-19 for N/A + 12.27, A-20 for N/A + 12.24 WITHOUT 12.27, and A-21 for N/A + 12.29 WITHOUT either 12.24 or 12.27, each with a DR-1/DR-2 reason. Those sets satisfy A-16 and the respective perception-code rule, with opposing no-mask versus Manual Mask assignments. This is a configuration-level conflict, not proof such a record or conflicting runs have been observed; do not assume mutual exclusivity or execution priority.
- Always execution has no shown preserve-existing-MAIN/masking guard. A queued A-16 action may apply its no-mask result after inputs or another writer have changed. Initialization gating alone does not serialize these later writers.
- A-16's own outputs are not its trigger inputs. Editing only MAIN/masking while the two predicates remain true does not re-enter the trigger; changes to secondary links/reasons that leave and re-enter the condition can reapply the assignments.
- For the proposed, deferred gate, retain both any-match predicates and add initialization readiness if approved. Replacing includes N/A with only N/A or an empty check is a separate policy change. No gate has been implemented.

###### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated name, Description editor if needed, and published revision/version/effective time.
2. Confirm the dynamic source-step provenance and resolved Halt Code - Import value/link conversion without changing the selection; do not assume linked IDs from the destination field's type.
3. Isolated cases: each predicate arriving last, already-matching records, blank secondary versus N/A-only versus mixed N/A/real codes, mixed reason lookups, existing MAIN/masking values, missing/duplicate imported-code matches, later import-only edits, manual overrides, and competing masking/classification rules. No migration implementation is approved by configuration capture alone.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Demotion Reason | INPUT | Has any of the two specified manual reasons |
| Secondary Demotion Manual | INPUT | Includes linked N/A; not an empty/only-N/A check |
| Halt Code - Import | INPUT | Visible dynamic single-select-field token assigned to MAIN |
| MAIN Demotion Code | OUTPUT | Linked destination populated by the token |
| Manual Demotion Masking | OUTPUT | Fixed Intended Manual Demotion - No Mask selection |

---

#### Evidence record A-17: Manual Initial - Manual Secondary

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED from Brian's two supplied screenshots: both predicates, Always setting, target table/record token, description, and both assignments. The Halt Code - Import token is fully readable; source-step picker and runtime link conversion have not been independently inspected for A-17.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-17. No test performed by the agent.  
**Name:** A-17 Manual Initial - Manual Secondary in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-17 is the inventory label.  
**Runs:** 4 this month displayed; earlier notes recorded 1/month and called it rare. These point-in-time UI counts do not establish frequency, execution success, or coverage.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms both complete reason lists:
  1. `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
  2. **AND** `Secondary Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- These are two independent any-match predicates, not exact-only comparisons or a requirement that the same reason appears in both. For example, primary DR-1 and secondary DR-2 satisfy the listed comparisons.
- The first field is Demotion Reason, not MAIN Demotion Reason. The second field is the secondary-reason lookup, not a direct comparison of Secondary Demotion Manual code labels.
- No exclusion of additional nonmanual reasons, N/A-only test, current MAIN-empty check, existing-masking guard, completion, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce MAIN or masking.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description:** Empty; the editor shows Enter a description.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `Halt Code - Import` | Fully visible dynamic field token; source-step picker not expanded |
| Manual Demotion Masking | `Intended Manual Demotion - No Mask` | Fixed selection shown in the action |

###### Field types and dependencies
The earlier read-only production schema identifies Secondary Demotion Reason (fld23MZ4hKOoXoDit) as multipleLookupValues, using recordLinkFieldId fldzCC2DDW9tweN0s: Secondary Demotion Manual. It reads the reason-reference field fldHZEJ61WQUe9IWd on those linked Halt Codes records. This establishes that the secondary predicate is fed through the manual-secondary links, not merely inferred from the automation name.

A-15 can populate those links from the preceding stop's Name list. Manual link edits or changes to linked reason data can also change the lookup result; actual trigger propagation and historical input state require validation. Current linkage does not prove which writer populated a particular record.

As established in the schema check for A-16, Halt Code - Import is singleSelect, while MAIN Demotion Code is a linked field targeting Halt Codes. Preserve the visible source token rather than calling it a direct linked-ID copy. A-15's list-of-Names projection is not automatically established for this different source type. The resolved token value and destination link conversion remain runtime/provenance validation items.

###### Purpose and gating audit
Assigns the imported code as MAIN and no-mask status when BOTH reason lookups contain at least one of the two specified manual reasons. The legacy statement that all reasons are manual and no system stop was masked was stronger than the actual predicates: mixed manual/nonmanual reason sets are not excluded by these two conditions.

- A-17 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not write either reason field, Secondary Demotion Manual, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope.
- A-16 is a configuration-captured writer with the same two assignments but a different secondary predicate. A-18 is now captured as displayed, including its secondary N/A assignment; A-19's literal 12.27 / Manual Mask assignments are captured; A-20's 12.24 / Manual Mask assignments and 12.27 exclusion are captured; A-21's 12.29 / Manual Mask assignments and 12.24/12.27 exclusions are captured; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending; inspect their exclusions before assuming mixed secondary sets cannot qualify for a competing result.
- A-34's captured rule consumes the no-mask value and MAIN Demotion Reason any of DR-1/DR-2, assigning intended manual classification, no operator error/misuse, and investigation completion without an incomplete-investigation prerequisite. A-17 itself does not perform those writes or establish that downstream execution occurred.
- Always execution has no shown preserve-existing-MAIN/masking guard. An action queued under earlier reason values can potentially overwrite a later decision; initialization gating alone does not serialize these writers.
- Editing only MAIN/masking while the two reason predicates remain true does not re-enter this trigger. Reason/link changes that make the predicate false and then true can cause another assignment, including on an existing record.
- For the proposed, deferred gate, retain both any-match predicates and add initialization readiness if approved. Requiring only manual reasons or adding explicit priority/exclusions would be a separate policy change. No gate has been implemented.

###### Remaining identity and validation evidence
1. Immutable automation ID/stable link, untruncated name, and published revision/version/effective time.
2. Dynamic source-step provenance and resolved Halt Code - Import value/link conversion, using the picker or an existing run without altering the configuration.
3. Isolated cases: DR-1/DR-2 cross-combinations, mixed manual/nonmanual reason sets, empty primary/secondary lookup, multiple secondary links, changed linked reason metadata, each predicate arriving last, already-matching records, existing MAIN/masking, missing/duplicate imported-code matches, manual overrides, and overlapping masking/classification rules.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Demotion Reason | INPUT | Any of the two specified manual reasons |
| Secondary Demotion Reason | INPUT | Independent any-match against the same two reasons |
| Secondary Demotion Manual | INDIRECT INPUT | Schema-confirmed source links for Secondary Demotion Reason |
| Halt Code - Import | INPUT | Visible dynamic single-select-field token assigned to MAIN |
| MAIN Demotion Code | OUTPUT | Linked destination populated by the token |
| Manual Demotion Masking | OUTPUT | Fixed Intended Manual Demotion - No Mask selection |

---

#### Evidence record A-18: Main Halt Code - Non Manual Initial

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED from Brian's supplied screenshots, including the supplemental full action panel. Trigger, Always setting, target table/record token, and all three assignments are captured. Dynamic source-step provenance and link conversion remain unverified, as for A-16/A-17.  
**Behavior/migration status:** NOT VERIFIED; full A-18 run inputs/outputs and version correspondence are not captured. No test performed by the agent.  
**Name:** A-18 Main Halt Code - Non Manual Initial in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-18 is the inventory label.  
**Runs:** 485 this month displayed; earlier notes recorded 84/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition:** `Demotion Reason` **has none of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`. The full trigger card confirms both names; this is the single configured condition shown.
- This uses Demotion Reason, not MAIN Demotion Reason. It excludes the two listed reasons, not every possible category described elsewhere as manual/operator-related. A mixed lookup containing either excluded reason fails the predicate even if it also contains other reasons.
- No separate Demotion Reason is not empty condition is shown. Empty/unresolved lookup behavior must be validated; do not assume absence of DR-1/DR-2 proves reference data has finished loading or identifies a known nonmanual reason.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.
- No current MAIN-empty, existing-masking, existing-secondary, completion, machine-type, or initialization-ready condition is shown.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action will run:** Always, confirmed in the supplemental action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in that same action panel; no longer inferred from the trigger.
- **Description evidence:** No description text on the action card; Description editor is outside the supplied capture.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `Halt Code - Import` | Fully visible dynamic field token; source-step picker not expanded |
| Manual Demotion Masking | `N/A` | Fixed single-select choice |
| Secondary Demotion Manual | `N/A` | Literal name text entered in the linked-record field; NOT a blank/clear operation or a visible record-ID literal |

###### Field types and link resolution
Earlier production schema reads identify Halt Code - Import as singleSelect, MAIN Demotion Code as a link to Halt Codes, and Secondary Demotion Manual as another link to that table. Preserve the distinction between the source token, the N/A masking choice, and the literal N/A used for linked-record resolution.

Do not describe the imported source as a linked record or assume A-15's Name-list projection applies. Source-step provenance and actual imported-code link conversion remain pending, as for A-16/A-17. The configured Secondary Demotion Manual assignment uses the N/A name; exact resolved record identity and behavior for missing/duplicate names require validation. No record creation, deletion, or incident attribution is established by the screenshot.

###### Purpose and gating audit
The displayed rule retains the imported code as MAIN and assigns N/A to masking/manual-secondary when the reason lookup has neither DR-1 nor DR-2. This does not independently classify the demotion as intended/unintended or establish that input/reference data is complete.

- A-18 writes MAIN Demotion Code, Manual Demotion Masking, and Secondary Demotion Manual. It does not directly write Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope.
- A-15 is another confirmed writer of Secondary Demotion Manual. A-16/A-17 write MAIN/masking with the same imported-code token but a DIFFERENT masking value: Intended Manual Demotion - No Mask. A-19's literal 12.27 / Manual Mask assignments are captured; A-20's 12.24 / Manual Mask assignments and 12.27 exclusion are captured; A-21's 12.29 / Manual Mask assignments and 12.24/12.27 exclusions are captured; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending.
- A-16's secondary predicate accepts a linked N/A. A-17's Secondary Demotion Reason lookup is sourced through Secondary Demotion Manual. This makes A-18's secondary assignment relevant to downstream eligibility if primary reasons later change; a fixed name is not equivalent to no link.
- A-18's reason condition is complementary to the manual-reason predicate used by A-15/A-16/A-17 at a fixed, settled input state. That does not guarantee queued actions cannot overlap after lookup/link changes. Always execution is now confirmed; historical ordering still needs evidence before attributing an overwrite.
- Reference/readiness matters in addition to A-1 initialization. If empty/unresolved lookups satisfy has none of, an early run could be queued before a later manual reason arrives. This is a hypothesis to test, not a demonstrated cause; a generic initialized flag alone may not establish lookup readiness.
- Always execution and the absence of a fill-if-empty guard mean the action can replace existing MAIN, masking, and secondary selections when it executes. No preserve-existing-output condition is shown.
- Editing only outputs while the reason predicate remains true does not re-enter the trigger. Changing source links/reason metadata can change eligibility; validate lookup propagation rather than assuming automation numbers imply execution order.
- For the proposed, deferred gate, preserve the has none of business predicate and gate all writes after initialization if approved. Adding a nonempty-reason requirement or preserving existing secondary links is a separate behavior change. No gate has been implemented.

###### Remaining identity and validation evidence
The visible trigger/action configuration is captured; this is not migration approval.
1. Immutable automation ID/stable link, untruncated name, Description editor if needed, and published revision/version/effective time.
2. Dynamic source-step provenance, imported-code link conversion, and resolved linked N/A identity from the picker or an existing successful run.
3. Isolated cases: empty/unresolved reason, each excluded reason, mixed reason sets, other reasons, lookup arrival/change timing, already-matching records, populated outputs, missing/duplicate N/A or imported-code names, and queued manual/nonmanual rules during input changes.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Demotion Reason | INPUT | Has none of the two specified manual reasons; no separate nonempty check |
| Halt Code - Import | INPUT | Visible dynamic token assigned to MAIN |
| MAIN Demotion Code | OUTPUT | Linked destination populated by the token |
| Manual Demotion Masking | OUTPUT | Fixed N/A single-select choice |
| Secondary Demotion Manual | OUTPUT | Literal N/A name assigned to a linked field |

---

#### Evidence record A-19: Main Halt Code - 12.27

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three supplied screenshots and owner-confirmed trigger-record-ID convention. Both predicates, Always setting, target table/record token, and both literal assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-19. No test performed by the agent.  
**Displayed name:** A-19 Main Halt Code - 12.27  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-19 is the inventory label.  
**Runs:** 2 this month displayed. This is a point-in-time UI count, not an execution-success or coverage measurement.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms all labels cropped in the condition panel:
  1. `Secondary Demotion Manual` **has any of** `12.27`.
  2. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- The first predicate includes the selected linked 12.27 record; it is not an only-12.27 or free-text substring condition. The second is an any-match on Demotion Reason, not MAIN Demotion Reason or an exact-only reason-set comparison.
- No exclusion of N/A or other secondary codes, current MAIN-empty check, existing-masking guard, completion, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce MAIN or masking.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action card subtitle:** Manual Demotion Masking and MAIN Demotion Code.
- **Description editor:** Shows Enter a description; no populated description text is visible. Keep this separate from the card subtitle rather than inferring they are the same property.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `12.27` | Fixed literal name text entered in the linked-record field; not a dynamic secondary-code token or visible record-ID literal |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

MAIN Demotion Code is a link to Halt Codes in the earlier production schema. Preserve the literal 12.27 name and its linked-record resolution; do not reinterpret it as a floating-point number or directly supplied record ID. Actual resolved identity and behavior for duplicate, renamed, or missing matches remain validation items. Name-based assignment is not proof of any past duplicate-record creation or incident cause.

###### Purpose and gating audit
When the selected secondary links include 12.27 and the raw demotion-reason lookup includes DR-1/DR-2, the rule promotes 12.27 to MAIN and assigns Manual Mask. It does not remove the secondary links or rewrite the imported halt code.

- A-15 can supply the manual-secondary links from preceding-stop Names. Manual changes or other writers can also populate them; do not assume A-15 ran for every qualifying record.
- A-19 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not directly write Secondary Demotion Manual, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope. Derived MAIN-reason/routing changes and downstream classification rules must be traced separately.
- A-16 through A-18 are captured writers of MAIN/masking; A-18 also writes Secondary Demotion Manual. A-20's 12.24 / Manual Mask assignments and 12.27 exclusion are captured; A-21's 12.29 / Manual Mask assignments and 12.24/12.27 exclusions are captured; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending. Always execution has no shown preserve-existing-value guard.
- **Confirmed predicate overlap with A-16:** A record with Secondary Demotion Manual containing BOTH N/A and 12.27, and Demotion Reason containing DR-1 or DR-2, satisfies both captured rules. A-16 assigns MAIN from Halt Code - Import and Intended Manual Demotion - No Mask; A-19 assigns literal 12.27 and Manual Mask. This is a configuration-level conflict, not a claim that such a record or competing execution has been observed. Actual firing still requires condition entry.
- Mixed secondary/reason sets may also interact with other manual-secondary rules; verify exact exclusions and dependencies rather than assuming the 12.27 label gives this action scheduler priority.
- Editing only MAIN/masking while the predicates remain true does not re-enter the trigger. Removing/re-adding qualifying secondary links or changing reason membership can re-enter it. Queued writes based on earlier conditions can overwrite a later decision; initialization gating alone does not serialize those writes.
- For the proposed, deferred gate, retain both any-match predicates and require initialization readiness if approved. Adding mutual exclusions, preserving manual overrides, or establishing a single classification writer is a separate behavior change. No gate has been implemented.

###### Priority evidence
Captured A-20 excludes 12.27, and captured A-21 excludes BOTH 12.24 and 12.27. Together with A-19's positive 12.27 predicate, this establishes 12.27 > 12.24 > 12.29 eligibility within the trio for fixed inputs and a qualifying manual reason. It does not establish queued-action order or full-workflow priority, and it does not resolve their demonstrated predicate overlaps with A-16. A-22 through A-25 still require current re-verification.

###### Remaining identity and validation evidence
1. Immutable automation ID/stable link and published revision/version/effective time; clarify the description/subtitle distinction if needed.
2. Historical resolved MAIN link identity/action outputs, preserving the fixed 12.27 assignment.
3. Isolated cases: 12.27-only versus mixed secondary links (especially N/A + 12.27), other/empty secondary values, DR-1/DR-2 cross/mixed reason sets, each predicate arriving last, already-matching records, populated outputs, duplicate/renamed/missing 12.27 name matches, manual overrides, and concurrent competing masking rules.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Includes linked 12.27; other secondary values are not excluded |
| Demotion Reason | INPUT | Any of the two specified manual reasons |
| MAIN Demotion Code | OUTPUT | Fixed 12.27 name in linked destination |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-20: Main Halt Code - 12.24

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's two supplied screenshots and owner-confirmed trigger-record-ID convention. All three predicates, Always setting, target table/record token, and both literal assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-20. No test performed by the agent.  
**Displayed name:** A-20 Main Halt Code - 12.24  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-20 is the inventory label.  
**Runs:** 2 this month displayed. This is a point-in-time UI count, not an execution-success or coverage measurement.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL three are required, in displayed order; the full trigger card confirms labels cropped in the condition panel:
  1. `Secondary Demotion Manual` **has any of** `12.24`.
  2. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
  3. **AND** `Secondary Demotion Manual` **has none of** `12.27`.
- These are linked-record membership predicates and an any-match on Demotion Reason, not free-text substring checks or an exact-only reason-set comparison. The first positive predicate requires 12.24, so an empty secondary set cannot satisfy the complete conjunction.
- No exclusion of N/A or other secondary codes besides 12.27, current MAIN-empty check, existing-masking guard, completion, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce MAIN or masking.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action card subtitle:** Manual Demotion Masking and MAIN Demotion Code. The Description editor is outside the supplied action-panel capture.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `12.24` | Fixed literal name text entered in the linked-record field; not a dynamic secondary-code token or visible record-ID literal |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

MAIN Demotion Code is a link to Halt Codes in the earlier production schema. Preserve the literal 12.24 name and its linked-record resolution; do not reinterpret it as a floating-point number or directly supplied record ID. Actual resolved identity and duplicate/renamed/missing-name behavior remain validation items. The captured configuration does not establish any past duplicate-record creation or incident cause.

###### Purpose and gating audit
For a DR-1/DR-2 demotion with secondary links including 12.24 but not 12.27, assigns 12.24 as MAIN and Manual Mask. The imported halt code and secondary links are not changed by this action.

- A-15 can supply the manual-secondary links from preceding-stop Names; manual edits and other writers can also populate them. Do not assume a particular producer from current values alone.
- A-20 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not directly write Secondary Demotion Manual, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope. Downstream routing/classification effects require separate tracing.
- **Captured precedence versus A-19:** On the same settled secondary-link set, A-19 requires 12.27 present and A-20 requires it absent. With both 12.24 and 12.27 present and a qualifying manual reason, A-19 is eligible and A-20 is not. This establishes predicate precedence of 12.27 over 12.24 between these two rules, not a scheduler ordering guarantee or full-workflow priority.
- An A-20 action queued while 12.27 was absent can potentially finish after the secondary set changes and A-19 becomes eligible. Always execution does not establish current-input rechecking; historical runs/isolated tests are needed before claiming a race occurred.
- **Confirmed predicate overlap with A-16:** Secondary links containing N/A AND 12.24, with NO 12.27, plus a DR-1/DR-2 reason satisfy both captured rules. A-16 assigns the imported MAIN code and Intended Manual Demotion - No Mask; A-20 assigns literal 12.24 and Manual Mask. This proves configuration overlap, not an observed record/cohort or conflicting execution. Actual firing still requires condition entry.
- A-16 through A-19 are captured MAIN/masking writers; A-21's 12.29 / Manual Mask assignments and 12.24/12.27 exclusions are captured; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending. Mixed secondary/reason sets require explicit exclusion/precedence analysis across all writers. The 12.27 exclusion alone does not resolve the A-16 overlap.
- Always execution has no shown preserve-existing-value guard. Output-only edits while the predicates remain true do not re-enter this trigger; secondary/reason changes that leave and re-enter the condition can reapply it. Initialization gating alone does not serialize these later writes.
- For the proposed, deferred gate, preserve all three predicates and require initialization readiness if approved. Changing exclusions, precedence, or manual-override protection is a separate behavior change. No gate has been implemented.

###### Remaining identity and validation evidence
1. Immutable automation ID/stable link, Description editor if needed, and published revision/version/effective time.
2. Historical resolved MAIN link identity/action outputs, preserving the fixed 12.24 assignment.
3. Isolated cases: 12.24-only, 12.24 + 12.27, N/A + 12.24 with/without 12.27, other/empty secondary links, DR-1/DR-2 and mixed reasons, each predicate arriving last, already-matching records, populated outputs, duplicate/renamed/missing 12.24 matches, manual overrides, and 12.27 added/removed while actions are queued.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Includes 12.24 and excludes 12.27; N/A is not excluded |
| Demotion Reason | INPUT | Any of the two specified manual reasons |
| MAIN Demotion Code | OUTPUT | Fixed 12.24 name in linked destination |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-21: Main Halt Code - 12.29

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's two supplied screenshots and owner-confirmed trigger-record-ID convention. All three predicates, Always setting, target table/record token, and both literal assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-21. No test performed by the agent.  
**Displayed name:** A-21 Main Halt Code - 12.29  
**Group:** Confirmed Halt Code, shown in the sidebar (11 active displayed).  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-21 is the inventory label.  
**Runs:** 3 this month displayed; earlier notes recorded 2/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL three are required, in displayed order; the full trigger card confirms the lists cropped in the condition panel:
  1. `Secondary Demotion Manual` **has any of** `12.29`.
  2. **AND** `Secondary Demotion Manual` **has none of** `12.24`, `12.27`.
  3. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- The exclusion requires BOTH higher-priority values to be absent. These are linked-record membership predicates, not substring or numeric-range checks. The reason test uses Demotion Reason, not MAIN Demotion Reason, and does not require an exact-only reason set.
- The positive 12.29 predicate means an empty secondary set cannot satisfy the full conjunction. No exclusion of N/A or other codes besides 12.24/12.27, current MAIN-empty check, existing-masking guard, completion, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce MAIN or masking.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Action card subtitle:** Manual Demotion Masking and MAIN Demotion Code. The Description editor is outside the supplied action-panel capture.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `12.29` | Fixed literal name text entered in the linked-record field; not a dynamic secondary-code token or visible record-ID literal |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

MAIN Demotion Code is a link to Halt Codes in the earlier production schema. Preserve the literal 12.29 name and linked-record resolution; do not reinterpret it as a floating-point number or directly supplied record ID. Actual resolved identity and duplicate/renamed/missing-name behavior remain validation items, not demonstrated incident causes.

###### Predicate precedence across A-19/A-20/A-21
For a qualifying DR-1/DR-2 reason and the same fixed secondary-link set, the captured code-membership conditions produce the following eligibility:

| Secondary-code membership | Eligible rule within this trio |
|---------------------------|--------------------------------|
| Includes 12.27 | A-19, even if 12.24 and/or 12.29 are also present |
| Includes 12.24, excludes 12.27 | A-20, even if 12.29 is also present |
| Includes 12.29, excludes BOTH 12.24 and 12.27 | A-21 |
| Includes none of these three | None of A-19/A-20/A-21 |

This establishes 12.27 > 12.24 > 12.29 at the predicate level within these three rules. It does NOT establish execution order, cancellation of queued actions after inputs change, priority over every other rule, or proof a currently eligible record has run. Reference identities and actual run behavior remain separate validation concerns.

###### Purpose and gating audit
Promotes the selected 12.29 secondary code to MAIN and assigns Manual Mask when the higher-priority codes are absent and a manual reason is present. It does not remove secondary links or change the imported halt code.

- A-15 can populate manual-secondary links from preceding-stop Names; manual edits and other writers can also supply them. Current values do not establish their producer.
- A-21 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not directly write Secondary Demotion Manual, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope. A-31's now-captured classifier consumes MAIN 12.29 plus inside-field assessment, nonempty object-misuse details, and Investigation Not Complete; those additional inputs/timing determine eligibility rather than A-21's write alone.
- **Confirmed predicate overlap with A-16:** N/A + 12.29 in secondary links, with NEITHER 12.24 NOR 12.27, and a DR-1/DR-2 reason satisfy both rules. A-16 assigns imported MAIN / Intended Manual Demotion - No Mask; A-21 assigns literal 12.29 / Manual Mask. This is a configuration conflict, not an observed matching cohort or race. Actual firing still requires condition entry.
- A-16 through A-20 are captured MAIN/masking writers; A-22 through A-25 now have displayed configurations captured; their record-specific runtime/identity validation remains pending. Pairwise exclusivity within the perception-code trio does not remove overlaps with other writers or mixed reason sets.
- An A-21 action queued before a higher-priority code arrives can potentially finish after another rule becomes eligible. Always execution has no shown preserve-existing-value guard or action-time condition recheck. Initialization gating alone does not serialize these later actions.
- Output-only edits while the predicates remain true do not re-enter this trigger. Changes to secondary/reason membership that leave and re-enter the condition can reapply it.
- For the proposed, deferred gate, retain all three predicates and require initialization readiness if approved. Changes to exclusions, priority enforcement, or manual-override protection are separate behavior changes. No gate has been implemented.

###### Remaining identity and validation evidence
1. Immutable automation ID/stable link, Description editor if needed, and published revision/version/effective time.
2. Historical resolved MAIN link identity/action outputs, preserving the fixed 12.29 assignment.
3. Isolated cases: all combinations of 12.27/12.24/12.29; N/A + 12.29 with/without higher-priority codes; empty/other secondary links; mixed reason sets; each prerequisite arriving last; already-matching records; populated outputs; duplicate/renamed/missing 12.29 matches; manual overrides; and higher-priority codes added/removed while actions are queued.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Includes 12.29 and excludes BOTH 12.24 and 12.27; N/A is not excluded |
| Demotion Reason | INPUT | Any of the two specified manual reasons |
| MAIN Demotion Code | OUTPUT | Fixed 12.29 name in linked destination |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-22: Main Halt Code - Interrupted Stop Code

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED from Brian's screenshots and explicit exclusion-list confirmation. All four predicates/lists, Always setting, target table/record token, and both assignments are captured; the supplemental tooltip confirms Secondary Demotion Manual as the MAIN source field. The source-step path, any data projection/modification, and resolved runtime value representation remain unverified. Display Name is recorded only as the visible editor setting.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-22. No test performed by the agent.  
**Name:** A-22 Main Halt Code - Interrupted Stop Code in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code in the inventory; group header is outside the supplied captures.  
**Enabled:** ON in the screenshots  
**Immutable identity:** No verified automation ID/stable link captured; A-22 is the inventory label.  
**Runs:** 112 this month displayed; earlier notes recorded 35/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Condition structure:** FOUR AND-connected predicates, with complete selections now confirmed in the supplemental panels/pickers:
  1. `Secondary Demotion Manual` **is not empty**.
  2. **AND** `Secondary Demotion Reason` **has any of** these eight selected reason records:
     - DR-4 Perception Internal System Failure
     - DR-6 Gen4/VADC Misc Error
     - DR-7 Perception Image Quality
     - DR-8 Guidance & Geo
     - DR-9 Spark
     - DR-11 Operator Error
     - DR-12 Perception Configuration
     - DR-13 Vehicle Operation Check
  3. **AND** `Secondary Demotion Manual` **has none of** exactly `12.24`, `12.27`, `12.29`, `N/A`, confirmed by the expanded panel and Brian's explicit text.
  4. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`, confirmed in the expanded primary-reason picker.
- **Correction to legacy evidence:** There are four excluded values, not an unidentified fifth. The summary's and 1 more abbreviated the configuration containing the fourth primary-reason condition omitted from the old entry. The complete trigger no longer has a selected-list gap.
- The expanded reason cards also display related halt_codes. Those are properties of the selected reason records, not additional directly selected code predicates; do not substitute the visible example codes for the reason-based condition.
- Both reason conditions are any-match lookup predicates. They do not require all linked secondary codes to have an allowed reason or all primary reasons to be manual. Primary Demotion Reason and Secondary Demotion Reason are distinct inputs.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. No separate completion, current MAIN-empty, existing-masking, machine-type, or initialization-ready condition is shown.

###### Action
- **Order/count:** One Update record action directly after the trigger; no branches or additional actions shown.
- **Description evidence:** No description text on the action card; Description editor is outside the supplied capture.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention.

| Field | Assignment shown | Evidence status |
|-------|------------------|-----------------|
| MAIN Demotion Code | Dynamic `Secondary Demotion Manual` field token | Full field name confirmed by the supplemental tooltip; context menu shows Display → Name. Source-step/data-projection and resolved value format remain unverified. |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

The supplemental tooltip resolves the formerly truncated field name to Secondary Demotion Manual. The context menu exposes Edit token, Display → Name, and Modify; it does not show a selected Make a new list of → Name data projection. Record Display → Name as an editor display setting, not proof that the action transmits linked-record names rather than IDs or another linked-field representation. This differs from A-15, where Brian explicitly confirmed the Name projection. No further configuration screenshots are requested at this stage; an existing run's resolved action inputs or a later source-token inspection can establish the data path and representation. The trigger-record-ID convention covers the update target, not this assignment's internal data path.

###### Purpose, dependencies, and gating audit
The rule handles nonempty secondary links with any of the eight listed secondary reasons, excludes 12.24/12.27/12.29/N/A, and requires a primary DR-1/DR-2 reason. The old non-perception-only description was inaccurate: DR-4, DR-7, and DR-12 explicitly include perception-related failures/configuration.

- A-15 and A-18 are captured writers of Secondary Demotion Manual. The previously read schema confirms Secondary Demotion Reason is looked up through those manual-secondary links. Actual source/reference changes and trigger propagation need runtime validation.
- A-22 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not directly write secondary links, Confirmed Demotion Type, operator-error status, reviewer, investigation/headlands/activities completion, or scope.
- The confirmed exclusion of N/A prevents the particular fixed-input A-16 overlap found for A-19 through A-21. Excluding 12.24/12.27/12.29 likewise rules out simultaneous fixed-input eligibility with those three positive-code predicates. The confirmed primary DR-1/DR-2 any-match is incompatible with A-18's has-none predicate on the same settled primary-reason state. None of this establishes ordering of already-queued actions after inputs change.
- Full-workflow exclusivity is NOT established: a secondary-reason set containing DR-1/DR-2 AND one of A-22's eight allowed reasons can satisfy A-17 and A-22 if the secondary links are nonempty, avoid all four exclusions, and the primary reason qualifies. They assign opposing no-mask/Manual Mask values. This is a predicate-level overlap for such a mixed set, not evidence of an observed cohort or conflicting execution; MAIN's resolved payload representation is still unverified. A-23 through A-25 have displayed configurations captured; runtime/identity validation remains separate.
- The source field is Secondary Demotion Manual. If the entire linked list is supplied, the secondary-reason any-match does not itself filter the assignment down to only reason-matching members. Validate data projection/modification and cardinality before deciding which codes are promoted; MAIN's single-record preference is not proof of runtime truncation or selection.
- Always execution has no shown preserve-existing-MAIN/masking guard. Current output edits alone do not re-enter the shown input conditions; later source/reason changes can. Initialization gating alone does not serialize competing classification writes.
- For the proposed, deferred gate, retain the FOUR now-captured business predicates and require initialization readiness if approved. Do not drop the primary-reason row or invent an extra exclusion. No gate has been implemented.

###### Remaining identity and validation evidence
Visible configuration capture is complete; data-path/runtime verification and migration approval remain separate.
1. Establish the token's source-step path, any data projection/modification, and resolved action value from an existing run or later token inspection. Do not equate Display Name with a Name data projection.
2. Immutable automation ID/stable link, untruncated name/group, Description editor if needed, and published revision/version/effective time.
3. Validate missing/excluded links, mixed secondary reasons (including A-17 overlap), all primary-reason cases, N/A coexistence, each input arriving last, already-matching records, full-list versus filtered promotion, duplicate/renamed link values, populated outputs, and queued competing writers.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Nonempty and four exclusions; tooltip-confirmed MAIN source field |
| Secondary Demotion Reason | INPUT | Any of the eight reason records confirmed in the expanded picker |
| Demotion Reason | INPUT | Fourth predicate, confirmed as any of DR-1/DR-2; omitted from legacy entry |
| MAIN Demotion Code | OUTPUT | Dynamic Secondary Demotion Manual token; Display Name setting observed, resolved data representation pending |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-23: Main Halt Code - False Positive

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED. Brian's screenshots and text confirm all five trigger predicates/selections, Always execution, target table/record token, and both assignments. The supplemental tooltip and explicit owner confirmation establish Secondary Demotion Manual as the dynamic MAIN source field. Source-step/data representation, link conversion, and runtime validation remain separate outstanding items.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-23. No test performed by the agent.  
**Name:** A-23 Main Halt Code - False Positive in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Halt Code in the inventory; group label is truncated in the screenshot.  
**Enabled:** ON in the screenshot  
**Immutable identity:** No verified automation ID/stable link captured; A-23 is the inventory label.  
**Runs:** 105 this month displayed; earlier notes recorded 16/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL FIVE are required, in displayed order, with selections confirmed by Brian's text and expanded record pickers:
  1. `Secondary Demotion Manual` **is not empty**.
  2. **AND** `Secondary Demotion Manual` **has none of** `12.24`, `12.27`, `12.29`.
  3. **AND** `Secondary Demotion Reason` **is exactly** `DR-3 Perception "Saw Something"`.
  4. **AND** `Secondary Demotion Reason` **has none of** these seven reason records:
     - DR-4 Perception Internal System Failure
     - DR-6 Gen4/VADC Misc Error
     - DR-7 Perception Image Quality
     - DR-8 Guidance & Geo
     - DR-9 Spark
     - DR-11 Operator Error
     - DR-12 Perception Configuration
  5. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- **Legacy correction:** The old and 2 more conditions abbreviation concealed the secondary-reason exclusion row and the primary DR-1/DR-2 row. Both are now explicitly captured; do not omit them in migration.
- Preserve is exactly DR-3 AND the separate has none of row. They are different configured operators; apparent redundancy is not authorization to remove a condition. Exact-match semantics for this lookup, including multiple linked codes sharing DR-3, must be validated.
- DR-13 is NOT in the explicit seven-reason exclusion list. That does not mean DR-3 + DR-13 is allowed: the separate is exactly DR-3 predicate still applies. Do not add DR-13 by copying A-22's allowed-reason list, or broaden exact-match into has any of.
- N/A is NOT explicitly excluded by the secondary-code row, unlike A-22. Any eligibility with an N/A-containing list depends on the full conjunction, including the secondary-reason lookup's exact-match behavior and N/A reference data.
- The halt_codes displayed inside reason selection cards are record metadata, not additional directly configured code conditions.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. No completion, initialization-ready, existing MAIN/masking, or separate false-positive adjudication condition is shown in the five-row trigger.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Action will run:** Always, visible above the Table setting in the supplemental capture.
- **Target table:** Demotions_DatabricksSync, confirmed in that action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention. No repeated source popup needed for this target token.
- **Description evidence:** No description text on the action card; Description editor is outside the capture.

| Field | Assignment shown | Evidence status |
|-------|------------------|-----------------|
| MAIN Demotion Code | Dynamic `Secondary Demotion Manual` field token | Full field name confirmed by tooltip and Brian's explicit confirmation; source-step/data representation and link resolution remain unverified |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice confirmed in the supplemental capture |

The supplemental tooltip resolves the source field to Secondary Demotion Manual, and Brian explicitly confirms it. This identifies the configured field without inferring it from A-22. It does not establish a Name/ID data projection, source-step path, or resolved runtime payload. No more configuration screenshots are requested at this stage; retain these data-path/link-conversion checks for existing-run review or later validation. Do not treat a token Display setting as proof of a data projection.

###### Purpose, dependencies, and gating audit
The captured trigger identifies a manual primary reason and a populated secondary set passing the DR-3 exact-match and exclusion tests. The False Positive title and old purpose statement are not independent evidence that a particular stop was adjudicated false-positive; no separate adjudication input appears in the trigger.

- A-15/A-18 are captured writers of Secondary Demotion Manual. Previously read schema identifies Secondary Demotion Reason as a lookup through that linked field. Linked-record/reference edits can change predicate inputs; their actual trigger propagation requires validation.
- The three code exclusions rule out fixed-input eligibility alongside A-19/A-20/A-21's positive code predicates. The primary manual-reason condition is incompatible with A-18's settled has-none primary condition. Neither establishes action execution order after input changes.
- A-16 overlap cannot be decided solely from the absence of an explicit N/A exclusion here. Check N/A's reason mapping and the exact DR-3 lookup comparison; do not declare an overlap or add a new exclusion without establishing the full case.
- A-22 accepts eight secondary reason categories; A-23 explicitly excludes seven of them and additionally requires exactly DR-3. Validate the exact-match behavior rather than inferring DR-13 coexistence from the missing explicit exclusion.
- A-24's six captured predicates are ALL FIVE A-23 predicates plus Secondary Demotion Manual has any of 12.X1. Therefore A-24 eligibility implies A-23 eligibility on the same input state. A-24's now-captured Always action writes literal 12.X1 to MAIN, unlike A-23's dynamic Secondary Demotion Manual token; both write Manual Mask. Resolved outcomes can agree or differ depending on the secondary set and runtime token handling; no conflicting runs are established. A-25 is now captured with these same five predicates plus includes 12.X2 and an Always action assigning fixed 12.X2 / Manual Mask. Its eligibility also implies A-23 eligibility. More-specific conditions do not confer scheduler priority.
- The full field list now confirms A-23 writes ONLY MAIN Demotion Code and Manual Demotion Masking, not secondary links, classification, completion, reviewer, operator-error status, or scope. Always execution has no shown preserve-existing-output guard. Runtime overwrites and downstream effects still require evidence; initialization gating alone will not serialize competing actions.
- For the proposed, deferred gate, preserve ALL FIVE predicates and require initialization readiness if approved. Changing exact-match semantics, removing a seemingly redundant exclusion, or adding new exclusions is a separate behavior change. No gate has been implemented.

###### Remaining identity and validation evidence
Visible configuration capture is complete; this is not migration approval.
1. Immutable automation ID/stable link, untruncated name/group, Description editor if needed, and published revision/version/effective time.
2. Validate the token's source-step/data representation, link resolution/cardinality, exact DR-3 lookup behavior with one/multiple codes, duplicate DR-3 lookup results, mixed DR-3/DR-13 or excluded reasons, N/A combinations, each code exclusion, primary reason combinations, input arrival timing, already-matching records, and overlaps/queued writes involving A-24/A-25. A reason predicate does not by itself filter the source list to selected members; verify what is actually assigned to MAIN.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Nonempty/exclusion predicates and confirmed dynamic MAIN source field |
| Secondary Demotion Reason | INPUT | Exactly DR-3 AND none of the seven specified reasons |
| Demotion Reason | INPUT | Any of DR-1/DR-2 |
| MAIN Demotion Code | OUTPUT | Dynamic Secondary Demotion Manual token; resolved representation remains pending |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-24: Main Halt Code - 12.X1

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's screenshots and explicit selection lists. All six trigger predicates, Always setting, target table/record token, and both literal assignments are captured, including the supplemental full action panel. Identity/version and runtime validation remain separate.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-24. No test performed by the agent.  
**Name:** A-24 Main Halt Code - 12.X1 in the inventory; the sidebar label continues with Int… and is truncated. Do not reconstruct the unseen full name.  
**Group:** Confirmed Halt Code in the inventory; the breadcrumb/group label is truncated in the screenshot.  
**Enabled:** ON in the screenshot  
**Immutable identity:** No verified automation ID/stable link captured; A-24 is the inventory label.  
**Runs:** 27 this month displayed; earlier notes recorded 4/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL SIX are required, in displayed order. Brian's DR-code shorthand denotes the full selected reason names:
  1. `Secondary Demotion Manual` **is not empty**.
  2. **AND** `Secondary Demotion Manual` **has none of** `12.24`, `12.27`, `12.29`.
  3. **AND** `Secondary Demotion Reason` **is exactly** `DR-3 Perception "Saw Something"`.
  4. **AND** `Secondary Demotion Reason` **has none of**:
     - DR-4 Perception Internal System Failure
     - DR-6 Gen4/VADC Misc Error
     - DR-7 Perception Image Quality
     - DR-8 Guidance & Geo
     - DR-9 Spark
     - DR-11 Operator Error
     - DR-12 Perception Configuration
  5. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
  6. **AND** `Secondary Demotion Manual` **has any of** `12.X1`.
- The fourth row's UI operator is has none of; preserve that membership operator despite conversational is none of shorthand. The old and 3 more conditions abbreviation concealed rows 4–6.
- 12.X1 is a selected linked-record label, not a wildcard/pattern condition over all codes ending in 1. Preserve the capital X and literal label; any upstream grouping that produces this linked value requires separate evidence.
- Has any of 12.X1 is not only 12.X1. Other secondary links, including N/A or 12.X2, are not explicitly excluded by the code predicates, although the entire reason conjunction must still hold.
- Preserve exactly DR-3 and the separate seven-reason exclusion. DR-13 is not in the explicit exclusion list, but the exact-match predicate still applies; do not infer mixed DR-3/DR-13 eligibility or remove an apparently redundant condition without validating lookup semantics.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. No completion, initialization-ready, current MAIN/masking, explicit headlands/interior, or separate false-positive adjudication condition is shown among these six predicates.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Card subtitle:** Manual Demotion Masking and MAIN Demotion Code, fully visible in the supplemental capture. Description editor is outside the capture.
- **Action will run:** Always, visible above the Table setting.
- **Target table:** Demotions_DatabricksSync, confirmed in the supplemental action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's explicit convention. No repeated target-token popup needed.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `12.X1` | Fixed literal name text in the linked-record field; not a dynamic secondary-code token or visible record-ID literal |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

The previously documented assignments are now corroborated by the current action capture. MAIN links to Halt Codes in the reviewed schema; preserve the literal 12.X1 name and validate its resolved record identity. It is not a wildcard or numeric conversion. Missing/duplicate/renamed-name behavior remains a validation concern, not an established incident cause.

###### Purpose, dependencies, and gating audit
The trigger narrows A-23's DR-3/manual-primary population to secondary links including 12.X1; the action assigns that fixed code to MAIN and Manual Mask to masking. It does not establish a separate adjudicated false-positive outcome.

- **Confirmed trigger containment:** A-24 has every captured A-23 predicate plus 12.X1 membership. A fixed input state satisfying A-24 also satisfies A-23. Both actions are Always, but actual firing depends on entering their respective conditions: A-24 can become newly eligible while A-23 was already matching. Overlapping eligibility does not prove both ran or that a conflict occurred.
- **Confirmed assignment distinction:** A-23 uses a dynamic Secondary Demotion Manual token for MAIN; A-24 writes literal 12.X1. Both write Manual Mask. Results may agree for a sole 12.X1 link, but can differ with multiple secondary links or different runtime token/link handling. Validate resolved outputs before asserting an actual conflicting write.
- More-specific conditions or a higher automation number do not confer scheduler priority, suppress A-23, or cancel a queued action. Initialization gating alone would not make these predicates mutually exclusive.
- A-15/A-18 are captured writers of Secondary Demotion Manual, which also feeds the Secondary Demotion Reason lookup. Any source assigning the particular 12.X1 link and its reference reason mapping remains to be traced.
- Code exclusions prevent fixed-input eligibility alongside A-19/A-20/A-21; the primary manual predicate is incompatible with A-18's settled has-none predicate. A-16/N/A behavior still depends on the full exact-reason comparison and reference data.
- A-25 is now captured, with owner-confirmed identical conditions except it requires 12.X2 and assigns fixed MAIN 12.X2. If the shared five predicates hold and both X1/X2 links are present, A-24 and A-25 (and A-23) are eligible together. The two specific rules assign different MAIN literals; this is conditional configuration overlap, not an observed qualifying cohort or conflict. Neither excludes the other's code.
- A-24 writes ONLY MAIN Demotion Code and Manual Demotion Masking, not secondary links, Confirmed Demotion Type, operator-error status, reviewer, completion flags, or scope. Always execution has no shown preserve-existing-MAIN/masking guard. Editing only outputs while inputs remain matched does not re-enter the trigger.
- A-30's captured trigger consumes MAIN 12.X1/12.X2 while investigation is incomplete, then assigns Potential Operator Error, Intended Behavior, Unintended Perception Demotion, and Investigation Complete. Those are downstream A-30 assignments, not direct A-24 writes or proof every A-24 result was processed.
- For the deferred initialization gate, retain ALL SIX business predicates if approved; any precedence, exclusivity, or existing-value protection changes require separate approval. No gate has been implemented.

###### Remaining identity and validation evidence
Visible configuration capture is complete; this is not migration approval.
1. Immutable automation ID/stable link, full untruncated name/group, Description if needed, and published revision/version/effective time.
2. Validate the 12.X1 reference identity/reason mapping, actual producer, name-based resolution, single/multiple secondary links, 12.X1 + 12.X2, exact DR-3/excluded-reason behavior, N/A combinations, input transitions, populated outputs, and resolved A-23/A-24/A-25 outputs and execution ordering.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Nonempty, excludes 12.24/12.27/12.29, includes literal linked 12.X1 |
| Secondary Demotion Reason | INPUT | Exactly DR-3 AND none of the seven specified reasons |
| Demotion Reason | INPUT | Any of DR-1/DR-2 |
| MAIN Demotion Code | OUTPUT | Fixed literal 12.X1 name in linked destination |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

#### Evidence record A-25: Main Halt Code - 12.X2

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and explicit confirmation that A-25 is the same as captured A-24 except 12.X2 replaces 12.X1. This confirms the clipped selection lists without requesting duplicate screenshots.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific run evidence supplied for A-25. No test performed by the agent.  
**Name:** A-25 Main Halt Code - 12.X2 in the inventory; sidebar name continues with Fa… and is truncated. Full name is not reconstructed.  
**Group:** Confirmed Halt Code in the inventory; breadcrumb/group label is truncated.  
**Enabled:** ON in the screenshot  
**Immutable identity:** No verified automation ID/stable link captured; A-25 is the inventory label.  
**Runs:** 17 this month displayed; earlier notes recorded 5/month. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Last Updated By:** Brian Moffatt, as displayed.  
**Published-version evidence:** No unpublished-change or reconnecting banner is visible; exact revision/version and effective time remain uncaptured.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL SIX are required. Screenshots show the structure and 12.X2 selection; Brian's same-as-A-24 confirmation establishes the complete matching reason lists:
  1. `Secondary Demotion Manual` **is not empty**.
  2. **AND** `Secondary Demotion Manual` **has none of** `12.24`, `12.27`, `12.29`.
  3. **AND** `Secondary Demotion Reason` **is exactly** `DR-3 Perception "Saw Something"`.
  4. **AND** `Secondary Demotion Reason` **has none of** `DR-4 Perception Internal System Failure`, `DR-6 Gen4/VADC Misc Error`, `DR-7 Perception Image Quality`, `DR-8 Guidance & Geo`, `DR-9 Spark`, `DR-11 Operator Error`, `DR-12 Perception Configuration`.
  5. **AND** `Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
  6. **AND** `Secondary Demotion Manual` **has any of** `12.X2`.
- Preserve literal linked-record membership for 12.X2, not wildcard matching of codes ending in 2. Includes 12.X2 does not mean only 12.X2; no explicit 12.X1 or N/A exclusion is shown/owner-confirmed.
- The first five predicates match A-23/A-24. Preserve exactly DR-3 and the separate seven-reason exclusion; do not simplify them or infer mixed-reason eligibility without validating lookup semantics.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. No completion, initialization-ready, current MAIN/masking, explicit headlands/interior, or separate adjudication condition is configured in the confirmed six-predicate set.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Card subtitle:** Truncated Manual Demotion Masking and MAIN …; Description editor is outside the captures.
- **Action will run:** Always, confirmed in the action panel.
- **Target table:** Demotions_DatabricksSync, confirmed in that panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| MAIN Demotion Code | `12.X2` | Fixed literal name text in the linked-record field, not a dynamic token or visible record-ID literal |
| Manual Demotion Masking | `Manual Mask` | Fixed single-select choice |

MAIN links to Halt Codes in the reviewed schema. Preserve the literal 12.X2 name; validate resolved reference identity and duplicate/renamed/missing-name behavior separately. Configuration capture does not establish a past link-resolution failure or incident cause.

###### Purpose, dependencies, and gating audit
A-25 narrows the shared DR-3/manual-primary trigger to secondary links including 12.X2 and assigns that fixed MAIN value with Manual Mask. The only confirmed functional differences from A-24 are the final membership value and the MAIN literal, both 12.X2 instead of 12.X1.

- A-25 eligibility implies A-23 eligibility on the same fixed input state because it adds one requirement to A-23's five predicates. Both actions are Always; actual firing still depends on entering the respective condition, so this does not prove both run on every edit.
- A-23 uses a dynamic Secondary Demotion Manual token; A-25 uses fixed 12.X2. They share Manual Mask. Resolved MAIN results can agree or differ depending on the source set/token behavior; no conflicting execution is established.
- **Conditional A-24/A-25 overlap:** If the shared five predicates hold and Secondary Demotion Manual contains BOTH 12.X1 and 12.X2, A-24, A-25, and A-23 are all eligible. A-24 and A-25 assign different literal MAIN values, while both assign Manual Mask. This is a configuration-level competing assignment, not proof that such a qualifying record or conflicting run exists. Validate both reference reason mappings and exact-lookup behavior.
- Neither A-24 nor A-25 excludes the other's code. More-specific names, numbering, or the X1/X2 labels do not imply mutual exclusivity or scheduler priority. Initialization gating alone would not resolve this overlap.
- A-15/A-18 can write manual-secondary links, which feed the secondary-reason lookup. Actual producers of the specific 12.X2 link and the linked reference mapping remain to be traced.
- A-25 writes ONLY MAIN Demotion Code and Manual Demotion Masking. It does not write the imported code, secondary links, Confirmed Demotion Type, operator-error status, reviewer, completion flags, or scope. Always execution has no shown preserve-existing-output guard.
- A-30's captured trigger accepts MAIN 12.X1 or 12.X2 with Investigation Not Complete and assigns the same four classification/completion values for either code. This establishes a dependency, not proof of an actual run or a different classifier for X2 versus X1.
- Output-only edits while inputs remain matched do not re-enter the trigger. Later input changes can re-enter it, and queued actions can finish after newer state arrives; no runtime ordering guarantee has been established.
- For the deferred initialization gate, preserve ALL SIX confirmed predicates if approved. Any exclusion, precedence, or existing-value protection change requires separate approval. No gate has been implemented.

###### Remaining identity and validation evidence
Visible configuration capture is complete; no more A-25 screenshots are requested. This is not migration approval.
1. Immutable automation ID/stable link, full name/group, Description if needed, and published revision/version/effective time.
2. Validate the 12.X2 reference identity/reason mapping, actual producer, name-based resolution, single/multiple secondary links including X1 + X2, exact DR-3 behavior, N/A combinations, input transitions, manual overrides, and resolved A-23/A-24/A-25 outcomes/order.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Secondary Demotion Manual | INPUT | Nonempty; excludes 12.24/12.27/12.29; includes linked 12.X2 |
| Secondary Demotion Reason | INPUT | Exactly DR-3 AND none of seven specified reasons |
| Demotion Reason | INPUT | Any of DR-1/DR-2 |
| MAIN Demotion Code | OUTPUT | Fixed literal 12.X2 name in linked destination |
| Manual Demotion Masking | OUTPUT | Fixed Manual Mask selection |

---

##### Databricks SQL Equivalent

**Historical sketch — NOT an approved equivalent of the captured A-15 through A-25 rules:** The SQL below treats lookup/link inputs as scalar values, omits multiple captured guards/exclusions and the A-15/A-18 secondary-link writes, and imposes CASE ordering not guaranteed by independent Airtable automations. It also mixes full reason names with bare DR identifiers and does not establish the actual list/name resolution of MAIN assignments. Preserve native exact-versus-any/none semantics, literal X1/X2 references, and event transitions; do not silently resolve the documented rule overlaps through CASE priority. Reconcile schema/identity, behavior, and an approved precedence policy before implementation. Original SQL and comments remain unchanged below.

```sql
-- Combined Confirmed Halt Code / Manual Masking Logic
WITH demotion_classification AS (
  SELECT 
    unique_id,
    demotion_reason,
    secondary_demotion_reason,
    secondary_demotion_manual,
    halt_code_import,
    
    -- Determine if main demotion is manual
    CASE 
      WHEN demotion_reason IN ('DR-1 In-Cab Controls Override', 'DR-2 Human-Triggered Demotion')
      THEN TRUE ELSE FALSE 
    END AS is_manual_demotion,
    
    -- Determine if secondary is also manual
    CASE 
      WHEN secondary_demotion_reason IN ('DR-1 In-Cab Controls Override', 'DR-2 Human-Triggered Demotion')
      THEN TRUE ELSE FALSE 
    END AS is_secondary_manual
    
  FROM demotion_context
)
SELECT
  unique_id,
  
  -- Manual Demotion Masking
  CASE 
    -- Non-manual demotion
    WHEN NOT is_manual_demotion THEN 'N/A'
    
    -- Manual with no secondary or secondary also manual
    WHEN is_manual_demotion AND (secondary_demotion_manual = 'N/A' OR is_secondary_manual) 
      THEN 'Intended Manual Demotion - No Mask'
    
    -- Manual masking specific perception codes
    WHEN is_manual_demotion AND secondary_demotion_manual IN ('12.24', '12.27', '12.29', '12.X1', '12.X2')
      THEN 'Manual Mask'
    
    -- Manual masking system/perception failures (DR-3, DR-4, DR-6, DR-7, DR-8, DR-9, DR-11, DR-12, DR-13)
    WHEN is_manual_demotion AND secondary_demotion_reason IN (
      'DR-3 Perception "Saw Something"',
      'DR-4 Perception Internal System Failure',
      'DR-6 Gen4/VADC Misc Error',
      'DR-7 Perception Image Quality',
      'DR-8 Guidance & Geo',
      'DR-9 Spark',
      'DR-11 Operator Error',
      'DR-12 Perception Configuration',
      'DR-13 Vehicle Operation Check'
    ) THEN 'Manual Mask'
    
    ELSE 'N/A'
  END AS manual_demotion_masking_computed,
  
  -- Main Demotion Code
  CASE
    WHEN secondary_demotion_manual IN ('12.24', '12.27', '12.29', '12.X1', '12.X2')
      THEN secondary_demotion_manual
    WHEN is_manual_demotion AND secondary_demotion_reason IN ('DR-3', 'DR-4', 'DR-6', 'DR-7', 'DR-8', 'DR-9', 'DR-11', 'DR-12', 'DR-13')
      THEN secondary_demotion_manual
    ELSE halt_code_import
  END AS main_demotion_code_computed

FROM demotion_classification
```

---

#### Auto-Investigations — Current Re-Audit

#### Evidence record A-26: Perception Stops as Demotions

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's supplied screenshots, including the supplemental action panel confirming Always. Both trigger predicates, execution setting, target table/record token, and all four assignments are captured; header identity/version and runtime validation remain separate.  
**Behavior/migration status:** NOT VERIFIED. Test-result/check indicators are visible, but expanded inputs/outputs and production run history are not supplied. No test performed by the agent.  
**Identity/context:** A-26 Perception Stops as Demotions in the inventory, under Auto-Investigations; its original captures crop the full automation header and complete run count.  
**Enabled:** ON, subsequently visible for A-26 in the supplied A-27 sidebar capture. The full untruncated A-26 name/count remain uncaptured.  
**Immutable identity/version:** No verified automation ID/stable link or published revision/effective time captured. Brian Moffatt is displayed as last updater.  
**Prior documentation:** A-26 previously appeared only in this file's index, despite its DOCUMENTED label; this section records the supplied definition, not a newly created automation.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms the values clipped in the condition selector:
  1. `Halt Code - Import` **is any of** `12.15`, `12.110`, `12.111`, `12.112`, `12.113`, `12.101`.
  2. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- Preserve these six exact single-select labels and displayed order. They are not a 12.11-family wildcard; do not convert 12.110 to the numeric/string value 12.11.
- The rule reads the imported halt code, NOT MAIN Demotion Code, Demotion Reason, or Triage Process. Blank investigation status is not the required Investigation Not Complete value.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.
- No masking, MAIN-code, headlands, machine-type, initialization-ready, or existing classification/operator/bug-value restriction is shown in the trigger.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Action will run:** Always, confirmed by the supplemental Configuration panel. No additional action-level guard is shown.
- **Target table:** Demotions_DatabricksSync, visible at the top of the action capture.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 1 more field. The full panel identifies the fourth field as Bug or Intended Behavior; Description editor is not shown.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Bug or Intended Behavior | `Known Bug` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Purpose, dependencies, and gating audit
Classifies the six imported halt-code values as unintended perception demotions with Known Bug and No Operator Error or Misuse, and marks the investigation complete. These are configured assignments, not independent evidence establishing the cause of a specific event.

- A-26 directly writes four fields, including Bug or Intended Behavior; it does not directly write MAIN, Manual Demotion Masking, secondary links, headlands assessment/completion, reviewer, overall triage completion, or scope. The title alone does not establish that it changes an upstream event/demotion flag.
- A-1's captured initializer writes Investigation Not Complete. Unlike A-37's documented trigger, A-26 explicitly reads that value: when code eligibility is already present, a transition into Investigation Not Complete can make A-26 newly eligible.
- A successful assignment of Investigation Complete makes this trigger false. A later reset to Investigation Not Complete, while the imported code still qualifies, can make it true again. This differs from the flag-only reset that did not re-enter A-37's process/masking predicate. Always execution is now confirmed, but this remains eligibility analysis, not proof of a particular rerun or guaranteed repair.
- A manual reopening can likewise create a new eligible transition. The Always action has no shown preserve-existing-value guard and can reassign classification, operator-error, bug, and investigation values when it executes. An actual overwrite, timing, or retry outcome still requires record/run evidence.
- Import-code changes versus MAIN-code/routing changes are distinct. A-26 has no shown MAIN/masking restriction, so do not assume those downstream decisions take precedence over this raw-code rule. A-29's captured rule tests the same six-code set on MAIN plus a missing-marker condition and adds JRM-548. A-26 can potentially complete investigation before those additional inputs arrive, blocking a later A-29 run unless investigation becomes incomplete again; no such production miss is proven. A-34 through A-37 and other investigation writers still require current re-verification/ordering analysis.
- A-38 is documented as watching classification/investigation fields to set overall activities completion. A-40 is documented as watching investigation/operator fields and using Bug or Intended Behavior in scope branches. A-38's five-field update trigger and branches are now captured; A-40's five-field trigger and scope branches are now captured, with runtime validation pending. A-26 does not directly assign their outputs.
- For the deferred initialization gate, preserve BOTH original trigger predicates, including Investigation Not Complete, and add readiness only if approved. Initialization readiness is not a replacement for this business-state guard, and would not by itself prevent automatic reprocessing after a manual reopen. No gate has been implemented.

###### Remaining identity and validation evidence
Core trigger/action capture is complete; no repeated configuration screenshots are requested at this stage. This is not migration approval.
1. Complete automation header/name, run count, immutable ID/stable link, Description if needed, and published revision/version/effective time. ON status is now corroborated by the later A-27 sidebar capture.
2. Validate each exact code versus nearby unlisted labels, blank/not-complete/complete statuses, either prerequisite arriving last, already-matching records, completed-then-reset investigations, manual reopening/overrides, late A-1 or competing classification writes, and downstream activities/scope updates.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Halt Code - Import | INPUT | Is any of the six exact code labels |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Bug or Intended Behavior | OUTPUT | Fixed Known Bug |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion selection |

---

#### Evidence record A-27: 12.20 and 12.21

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. Both predicates, Always setting, target table/record token, and all five assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-27. No test performed by the agent.  
**Displayed name:** A-27 12.20 and 12.21  
**Group:** Auto-Investigations, shown with 5 active automations.  
**Enabled:** ON in the screenshot  
**Runs:** 34 this month displayed; a point-in-time UI count, not an execution-success or coverage measurement.  
**Identity/version:** No verified automation ID/stable link or published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.  
**Prior documentation:** Previously only an index entry existed for A-27 in this file; this section records the supplied configuration, not a new automation.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required:
  1. `Halt Code - Import` **is any of** `12.20`, `12.21`.
  2. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- Preserve the exact code labels; 12.20 is not a numeric normalization to 12.2 or a wildcard family. The input is the imported single-select halt code, not MAIN Demotion Code or a reason/routing field.
- Blank investigation status does not equal Investigation Not Complete. No current classification/operator/bug/JRM-link preservation condition, MAIN/masking restriction, headlands condition, machine-type restriction, or initialization-ready flag is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 2 more fields. The full field capture identifies Bug or Intended Behavior and Confirmed JRM Link; Description editor is not shown.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Bug or Intended Behavior | `Known Bug` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |
| Confirmed JRM Link | `JRM-613` | Fixed literal name text in a linked-record field, not a dynamic token, record-ID literal, or visible Jira API/create action |

###### JRM reference dependency
The previously read production schema identifies Confirmed JRM Link (fldFWS6mDaAqFs1Gl) as multipleRecordLinks targeting Airtable table tbllaxeplHp2Jmrw6, with prefersSingleRecordLink = false. The action supplies JRM-613 as a name to that linked field. Exact resolved record identity, duplicates/renames/missing matches, and preservation versus replacement of existing links remain validation items. Do not describe this as append-only or assume it creates/updates an external Jira issue; no direct external issue action is shown, and downstream integration side effects are not established here.

###### Purpose, dependencies, and gating audit
For the two imported codes while investigation is explicitly incomplete, assigns the same four classification/completion values as A-26 PLUS the fixed JRM-613 association. These are configured classifications/references, not independent verification of a particular event's cause or issue relevance.

- A-1 can initialize Investigation Not Complete, making A-27 eligible once a listed code is present. Assigning Investigation Complete makes the predicate false. A later reset/manual reopen can re-enter it while the code still qualifies; this differs from A-37's documented process/masking-only predicate.
- Always execution has no shown preserve-existing-value guard. A new qualifying run can reapply all five assignments, including replacing manually chosen classification, bug/operator values, or issue associations depending on linked-field update behavior. Actual reruns/overwrites are not established by current configuration alone.
- A-26 and A-27 have disjoint imported single-select code sets, so they do not match the same settled imported-code value. That does not guarantee order after code changes or establish exclusivity with MAIN/reason-based classification writers.
- A-26 does not write Confirmed JRM Link. Moving a record out of A-27's code set does not invoke a clearing action here; do not assume JRM-613 is automatically removed or that other classifiers manage the link.
- A-27 writes only the five listed fields. It does not directly write MAIN, masking, secondary links, headlands assessment/completion, reviewer, overall triage completion, or scope. A-38/A-40 are documented downstream consumers, with A-38 now configuration-captured and A-40's current configuration also captured (runtime validation remains separate).
- A-34 through A-37 and other investigation/classification writers require complete predicate/ordering review. Imported-code logic is not interchangeable with MAIN-code logic, and an initialization barrier alone does not protect against every later stale write or manual reopening.
- For the deferred gate, preserve BOTH predicates including Investigation Not Complete and add readiness only if approved. Changes to reopening behavior, issue-link preservation, or classification precedence require separate approval. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no additional A-27 screenshots are requested at this stage. This is not migration approval.
1. Immutable automation ID/stable link, Description if needed, published revision/version/effective time, and the resolved JRM-613 reference identity.
2. Validate both exact codes versus unlisted labels, blank/not-complete/complete investigation states, either prerequisite arriving last, already-matching records, manual reopening/overrides, late competing writes, existing/multiple JRM links, missing/duplicate JRM-613 names, code changes leaving the rule, and downstream activities/scope/integration behavior.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Halt Code - Import | INPUT | Is any of exact 12.20/12.21 labels |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Bug or Intended Behavior | OUTPUT | Fixed Known Bug |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion |
| Confirmed JRM Link | OUTPUT | Fixed JRM-613 name in linked destination |

---

#### Evidence record A-28: 12.35

**Definition status:** CORE CONFIGURATION CAPTURED. Brian's three current screenshots corroborate the previously owner-confirmed published policy and close the branch action-setting/table/target-token gaps.  
**Behavior/migration status:** NOT VERIFIED; current configuration does not establish representative run outcomes, ordering, backfill, or absence of other writers. No test performed by the agent.  
**Displayed name:** A-28 12.35  
**Group:** Auto-Investigations, shown with 5 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 10 this month displayed; a point-in-time UI count, not an execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.  
**Prior evidence:** [a28-policy.json](../reference/a28-policy.json) records owner-confirmed publication of A28_HEADLANDS_COMPLETE_OTHERWISE_V2. That is a local audit-policy label, not an Airtable revision ID. Preserve that historical artifact; these newer screenshots close its action-destination evidence gap in this specification without rewriting the old snapshot.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL THREE are required:
  1. `MAIN Demotion Code` **has any of** `12.35`.
  2. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
  3. **AND** `Headlands Assessment Complete` **is** `Headlands Complete`.
- The input is MAIN's linked 12.35 selection, NOT Halt Code - Import. Membership does not require 12.35 to be the only MAIN link.
- Blank investigation/headlands status does not equal either required status. The trigger has no separate masking, operator-error, current confirmed-type/bug-value, raw-code, or machine-type condition.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. Headlands vs Interior determines the branch, but is not an additional trigger predicate.

###### Conditional actions
The workflow shows one If group followed by Otherwise, with one Update record action in each. These are mutually exclusive branches within a qualifying run, not two unconditional Always updates.

| Setting | Headlands Pass branch | Otherwise branch |
|---------|-----------------------|------------------|
| Branch condition | Headlands vs Interior is Headlands Pass | Otherwise |
| Action will run | If Headlands vs Interior is Headlands Pass | If no other conditions are met |
| Target table | Demotions_DatabricksSync | Demotions_DatabricksSync |
| Target record | Trigger's Airtable record ID | Trigger's Airtable record ID |

Both action panels confirm their table and target token; the token provenance follows Brian's explicit convention. Card subtitles summarize the four fields, while Description editors are outside the captures.

| Assigned field | Headlands Pass branch | Otherwise branch |
|----------------|-----------------------|------------------|
| Operator Error or Misuse | No Operator Error or Misuse | No Operator Error or Misuse |
| Bug or Intended Behavior | Intended Behavior | Known Bug |
| Confirmed Demotion Type | Intended Perception Demotion | Unintended Perception Demotion |
| Investigation Complete | Investigation Complete | Investigation Complete |

All assignments are fixed choices, with one multiple-select value shown for Confirmed Demotion Type. Neither branch writes a JRM link, reviewer, MAIN, masking, secondary links, headlands fields/completion, overall triage completion, or scope.

###### Otherwise and readiness semantics
- Otherwise is not limited to Interior Pass: it covers Not Sure, blank, and any other non-Headlands-Pass value, but ONLY after all three trigger predicates are satisfied. This matches the previously published owner-confirmed policy; do not revert to an interior-only branch or a no-action gap for uncertainty.
- A-12's displayed Not Sure / Not Sure outputs and A-13's Interior Pass / Not Sure outputs satisfy A-14's captured nonempty-field predicate. Their resulting headlands completion can therefore make a MAIN-12.35 incomplete investigation eligible for A-28's Otherwise branch. This is configuration-level eligibility, not proof of actual execution for a particular record.
- Although A-14 normally marks completion after populated breakout values, it does not reopen the flag when inputs are later cleared. A stale/manually supplied Headlands Complete flag can coexist with blank position. Thus the otherwise-blank case must not be silently discarded as impossible.
- The policy classifies uncertainty as unintended perception only once the headlands-completion prerequisite is met. It does not treat missing/incomplete headlands status as ready.

###### Dependencies and gating audit
- MAIN writers A-16 through A-25 can affect 12.35 membership; A-7 through A-13 supply position/turn; A-14 supplies headlands completion; A-1 initializes investigation/headlands status. No particular producer or execution order is established solely from current values.
- A-28 has an existing stage prerequisite (Headlands Complete) and business-state prerequisite (Investigation Not Complete), but no dedicated global initialization-ready flag. Preserve both when designing a gate.
- Either branch completing the investigation makes the trigger false. A later reset/manual reopening can re-enter eligibility only if MAIN still includes 12.35 AND headlands is complete. Unlike A-26/A-27, an A-1 reset of BOTH status fields can leave A-28 waiting for headlands completion to be restored; A-14 does not continuously reassert its output.
- Changing Headlands vs Interior alone does not necessarily re-enter the three trigger predicates, especially after investigation is complete. It is a branch input, not a subscription guaranteeing reclassification on every later position edit. Validate snapshot/current-value behavior if it changes while a run is queued.
- Both branches assign No Operator Error or Misuse and overwrite classification/bug choices when they execute; no preserve-manual-value condition is shown. Reopening investigation may reapply these assignments. This conditional coverage does not prove A-39 is redundant for records waiting on headlands or otherwise outside A-28 eligibility.
- A-26/A-27 use raw imported codes while A-28 uses MAIN. A state with an A-26/A-27 raw code, MAIN including 12.35, Investigation Not Complete, and Headlands Complete can satisfy both types of rules. In Headlands Pass, their configured intended/bug assignments differ. This is a conditional configuration overlap, not an observed qualifying cohort or conflicting run. A-27's JRM association is not cleared by A-28.
- A-34 through A-37 and other classifiers remain subjects of the current audit. A-38/A-40 are documented consumers of the resulting classification/investigation/operator/bug values; both current configurations are now captured, while downstream completion/scope outcomes still require run validation.
- Adding an initialization prerequisite will not by itself serialize competing classifiers, reconcile stale headlands values, or protect manual reopenings. Any changes to branch policy, prerequisite semantics, or write ownership require separate approval. No gate or production policy change has been implemented by the agent.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-28 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, published revision/effective time, optional Descriptions, and resolved MAIN 12.35 reference identity.
2. Validate Headlands Pass, Interior Pass, Not Sure, and blank position with complete versus incomplete headlands; blank/incomplete/complete investigation; MAIN membership including mixed links; each prerequisite arriving last; already-matching records; manual reopening; late A-1/status resets; position changes while queued; raw-versus-MAIN classifier overlaps; and downstream activities/scope results.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes linked 12.35 |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; both branches assign Investigation Complete |
| Headlands Assessment Complete | INPUT | Requires Headlands Complete; not written here |
| Headlands vs Interior | BRANCH INPUT | Headlands Pass versus Otherwise |
| Operator Error or Misuse | OUTPUT | Both branches assign No Operator Error or Misuse |
| Bug or Intended Behavior | OUTPUT | Intended Behavior versus Known Bug |
| Confirmed Demotion Type | OUTPUT | Intended versus Unintended Perception Demotion |

---

#### Evidence record A-29: Missing Spark

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's five screenshots and owner-confirmed trigger-record-ID convention. All three predicates, Always setting, target table/record token, and five assignments are captured.  
**Behavior/migration status:** NOT VERIFIED. The trigger test panel shows Step successful / Step run 4 days ago, but explicitly warns that the configuration OR inputs changed since the test and results may be out of date. The found-record preview is not proof of current eligibility, current action outputs, or a production run. No test performed by the agent.  
**Displayed name:** A-29 Missing Spark  
**Group:** Auto-Investigations, shown with 5 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 5 this month displayed; a point-in-time count, not an execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater. No unpublished-change or reconnecting banner is visible; the stale test-result warning does not itself establish an unpublished configuration change.  
**Prior documentation:** Previously only an index entry existed for A-29 in this file; this section records an existing automation, not a new one.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL THREE are required; the expanded trigger card confirms the complete code list:
  1. `MAIN Demotion Code` **has any of** `12.15`, `12.101`, `12.110`, `12.111`, `12.112`, `12.113`.
  2. **AND** `MAIN_SparkURL_Manual` **contains** `missing`.
  3. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- Preserve the exact linked-code labels, including trailing zeros; do not turn 12.110 into 12.11. MAIN membership does not require a single MAIN link or refer to Halt Code - Import.
- Contains missing is a text/substring predicate on the stored field, not an empty-field check, equality to missing, media-fetch failure, or HTTP availability test. Case and formatting behavior must be validated rather than assumed during migration. A blank value is not evidence that this literal marker is present.
- Blank investigation status is not Investigation Not Complete. No headlands-completion, masking, raw-code, existing classification/operator/bug/JRM-link, machine-type, or initialization-ready guard is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Description:** Empty; the Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the full action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 2 more fields. The full field capture identifies Bug or Intended Behavior and Confirmed JRM Link.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Bug or Intended Behavior | `Known Bug` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |
| Confirmed JRM Link | `JRM-548` | Fixed literal name text in the linked-record field; not a dynamic token, record-ID literal, or direct external Jira action |

###### Stored-input and reference dependencies
The earlier read-only production schema identifies MAIN_SparkURL_Manual (fldrTkaa23C1V4NHe) as a stored URL field, not a formula/lookup. Its actual producer and the timing/meaning of the missing marker are not established by these automation captures. Do not assume that a MAIN-code update populates it atomically, or infer the marker from a missing URL without a separately approved rule.

Confirmed JRM Link (fldFWS6mDaAqFs1Gl) is multipleRecordLinks to Airtable table tbllaxeplHp2Jmrw6. Preserve JRM-548 as the configured name. Its resolved record identity, duplicate/renamed/missing-name behavior, existing-link preservation versus replacement, and any downstream integration effects remain unverified. No direct external issue creation/update is shown.

###### Purpose, dependencies, and gating audit
For eligible MAIN codes with the literal missing marker and an explicitly incomplete investigation, assigns the four classification/completion values and the JRM-548 association. The name Missing Spark is not independent verification of an actual missing media artifact.

- A-29 writes ONLY the five listed fields. It does not write MAIN, the Spark URL/marker, masking, secondary links, headlands state, reviewer, overall triage completion, or scope.
- A-1 can initialize Investigation Not Complete. A-29 completing investigation makes the predicate false; a later reset/manual reopen can re-enter eligibility only if MAIN and the missing-marker condition still qualify. Always execution has no shown preservation guard and can reapply all five assignments; actual reruns/overwrites require evidence.
- **Overlap and timing dependency with A-26:** The MAIN-code set here is the same set A-26 tests on the raw imported code. If both code fields qualify, the marker is present, and investigation is incomplete, both rules can be eligible. Their four shared assignments agree, but only A-29 writes JRM-548.
- **Conditional late-input gap:** If A-26 completes investigation before MAIN/marker conditions make A-29 newly eligible, later marker/MAIN arrival alone will not satisfy A-29 because investigation is already complete. This can leave the JRM association unapplied by A-29. It is a configuration-derived scenario, not an observed missed run; establish actual input producers/timestamps before attributing a case. An initialization flag alone does not guarantee all enrichment inputs have arrived.
- A-27 can also be eligible if the raw code is 12.20/12.21 while MAIN qualifies for A-29 and the other predicates hold. It assigns JRM-613 instead of JRM-548. This is a conditional competing issue-link assignment, not an observed cohort or proven final link result; validate both routing and linked-field update behavior.
- With multiple MAIN links including 12.35 and one of this rule's codes, A-28 can conditionally overlap if headlands is complete. Its Headlands Pass branch differs in intended/bug classification. MAIN's single-record preference is not proof such combinations are impossible; no actual matching records or conflicting runs are established here.
- Removing missing from the URL, clearing the URL, or changing MAIN so the predicate becomes false does not invoke an inverse/clearing action here. Do not assume JRM-548 or the classification is automatically removed when inputs change.
- A-38/A-40 are documented downstream consumers of classification/investigation/operator/bug fields; A-38 is now configuration-captured and A-40's five-field trigger and scope branches are now captured, with runtime validation pending. A-29 does not directly complete overall triage or set scope.
- For the deferred gate, preserve all three predicates if approved. Deciding whether issue enrichment should occur after investigation completion, defining missing-input semantics, changing precedence, or protecting manual/JRM values is a separate policy/design change. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-29 screenshots are requested at this stage. This is not migration approval.
1. Immutable automation ID/stable link, published revision/effective time, and resolved JRM-548/MAIN reference identities.
2. Review existing run history or later isolated tests rather than relying on the explicitly stale preview. Validate all code labels, raw-versus-MAIN differences, stored marker producer/timing, blank/equal/substring/case variants, incomplete/complete/blank investigation, each prerequisite arriving last, manual reopening, existing/multiple issue links, competing A-26/A-27/A-28 writes, stale marker removal, and downstream completion/scope behavior.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes any of six exact linked-code labels |
| MAIN_SparkURL_Manual | INPUT | Stored URL field contains literal missing |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Bug or Intended Behavior | OUTPUT | Fixed Known Bug |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion |
| Confirmed JRM Link | OUTPUT | Fixed JRM-548 name in linked destination |

---

#### Evidence record A-30: 12.X1, 12.X2

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. Both trigger predicates, Always setting, target table/record token, and all four literal assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-30. No test performed by the agent.  
**Displayed name:** A-30 12.X1, 12.X2  
**Group:** Auto-Investigations, shown with 5 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 30 this month displayed; a point-in-time UI count, not an execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.  
**Prior documentation:** A-30 previously had only an index entry in this file; this section records the existing automation, not a newly created rule.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms both code selections:
  1. `MAIN Demotion Code` **has any of** `12.X1`, `12.X2`.
  2. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- MAIN is the linked-code field, not Halt Code - Import. These are literal selected reference labels, not wildcard matches for numeric codes ending in 1/2. Membership does not require MAIN to contain only one of them.
- Blank investigation status does not equal Investigation Not Complete. No headlands-completion/position, masking, raw-code, current operator/bug/classification, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. There is no branch distinguishing X1 from X2.

###### Action
- **Visible structure:** One Update record action; no additional branches/actions shown.
- **Description:** Empty; the Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 1 more field. The full field capture identifies Bug or Intended Behavior as the fourth field.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `Potential Operator Error` | Fixed single-select choice |
| Bug or Intended Behavior | `Intended Behavior` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Meaning and dependency distinctions
- Preserve ALL four assignments together. Intended Behavior in one field is not an instruction to change the separate Confirmed Demotion Type to Intended Perception Demotion; the displayed type is explicitly Unintended Perception Demotion.
- Potential Operator Error is neither confirmed Operator Error/Misuse nor No Operator Error or Misuse. The rule assigns that tentative label while marking investigation complete; this is the configured policy, not independent evidence of actual operator fault or completion of every manual-review activity.
- A-24/A-25 are captured MAIN producers assigning fixed 12.X1/12.X2; A-23's dynamic manual-secondary token can also be relevant depending on the source set and runtime link resolution. Manual/other writers can affect MAIN; current values alone do not establish their producer.
- A-24 versus A-25's different MAIN literals satisfy the SAME A-30 code predicate and select the same action if the investigation prerequisite also holds. This does not make their own competing MAIN assignments equivalent for other consumers/reporting or prove an A-30 run occurred.
- A-30 writes ONLY the four listed fields. It does not write MAIN, masking, secondary links, JRM links, reviewer, headlands status, overall triage completion, or scope. Existing JRM associations are not cleared by this rule.

###### Gating and competing-writer audit
- A-1 can initialize Investigation Not Complete. Successful completion by A-30 makes its predicate false; a later reset/manual reopen can make it eligible again if MAIN still includes X1/X2. Always execution has no shown preservation guard, so all four assignments can be reapplied. Actual reruns/overwrites require record history or isolated validation.
- Changing MAIN from X1 to X2 while the rule remains matched does not create a new matching transition by itself. MAIN changes after investigation is complete likewise do not satisfy the incomplete-investigation prerequisite unless it is reopened/reset.
- A-26/A-27 classify raw imported-code sets, whereas A-30 classifies MAIN. Conditional overlap is possible if those raw/MAIN states coexist while investigation is incomplete: A-26/A-27 assign No Operator Error or Misuse and Known Bug, whereas A-30 assigns Potential Operator Error and Intended Behavior. No qualifying cohort or conflicting run is established.
- A-28/A-29 can conditionally overlap on mixed MAIN links if their additional prerequisites hold. Do not infer mutually exclusive populations merely from different code lists when MAIN can contain multiple linked values. An earlier classifier completing investigation can also prevent a later-ready classifier from entering its condition; the applicable precedence/readiness policy remains to be specified.
- **A-39 review dependency:** Its current captured rule exactly matches NOT Required - Misuse Check via the original Halt Code - Linked lookup, then Always assigns No Operator Error or Misuse without an empty-output guard. A-30 assigns Potential Operator Error. Actual shared eligibility depends on reference/data mappings; ordering, overwrites, and redundancy remain unverified. No incident attribution or retirement decision follows from the differing assignments alone.
- A-38/A-40 are documented consumers of investigation/classification/operator/bug fields, with A-38 now configuration-captured and A-40's current configuration also captured (runtime validation remains separate). Do not infer overall triage completion or scope solely from A-30's investigation flag or the word Intended.
- The rule does not wait for Headlands Complete, unlike A-28. For the deferred initialization gate, preserve BOTH existing predicates and require readiness only if approved; adding headlands gating, changing labels, or protecting manual overrides is a separate policy change. Initialization gating alone does not serialize competing classifiers. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-30 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, published revision/effective time, and resolved MAIN X1/X2 reference identities.
2. Validate X1-only/X2-only/both/mixed MAIN sets, no wildcard expansion, raw-versus-MAIN differences, blank/incomplete/complete investigation, each prerequisite arriving last, already-matching records, manual reopening/overrides, late A-1 resets, competing classification/operator writers including the eventual A-39 definition, unchanged JRM links, and downstream activities/scope behavior.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes linked literal 12.X1 or 12.X2 |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Operator Error or Misuse | OUTPUT | Fixed Potential Operator Error |
| Bug or Intended Behavior | OUTPUT | Fixed Intended Behavior |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion |

---

#### Perception Demotions — Current Re-Audit

#### Evidence record A-31: 12.29 Intended Perception

**Definition status:** CORE CONFIGURATION CAPTURED AS DISPLAYED from Brian's six screenshots and owner-confirmed trigger-record-ID convention. Four trigger predicates, the initial Always update, all three conditional branch actions, destinations, and assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-31. No test performed by the agent.  
**Displayed name:** A-31 12.29 Intended Perception  
**Group:** Perception Demotions, shown with 3 active automations.  
**Enabled:** ON as displayed  
**Runs:** 5 this month displayed; a point-in-time UI count, not execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater. The first capture shows Reconnecting; subsequent action captures do not show that banner, but current server revision is not independently verified. Preserve this evidence caveat without requesting repeat captures now.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL FOUR are required:
  1. `MAIN Demotion Code` **has any of** `12.29`.
  2. **AND** `Vehicle/Object Outside Field` **is** `Inside Field (OBVIOUS)`.
  3. **AND** `NonNavigable Object Misuse Details` **is not empty**.
  4. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- MAIN is a linked-code membership test, not Halt Code - Import or an only-12.29 condition. Vehicle/Object Outside Field is a separate assessment field, not Headlands vs Interior; do not substitute Interior Pass for Inside Field (OBVIOUS).
- The reviewed production schema identifies Vehicle/Object Outside Field and NonNavigable Object Misuse Details as singleSelect fields. Their actual producers/timing are not established by the screenshots.
- Blank object-misuse details or blank investigation status do not meet the shown trigger. No Headlands Complete, masking, raw-code, existing classification/operator/bug-value, or initialization-ready restriction is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.

###### Workflow structure and initial action
The workflow contains FOUR Update record cards: one initial Always action followed by an If / Otherwise if / Otherwise group with one action per branch. The normal successful path executes the initial action and one selected branch, not all four cards.

- **Initial action will run:** Always.
- **Initial target table:** Demotions_DatabricksSync.
- **Initial target record:** Trigger's Airtable record ID, following Brian's convention.
- **Initial card subtitle:** Confirmed Demotion Type and Bug or Intended Behavior; Description editor is not shown.

| Initial assigned field | Value |
|------------------------|-------|
| Confirmed Demotion Type | Intended Perception Demotion |
| Bug or Intended Behavior | Intended Behavior |

The initial action does NOT complete investigation or assign operator status. These assignments precede a separate branch action; do not model the workflow as a single atomic update or assume other automations cannot observe an intermediate state.

###### Conditional actions
All three branch panels independently show target table Demotions_DatabricksSync and an Airtable record ID token, sourced from the trigger by Brian's convention. All choices below are fixed values. Branch card subtitles identify Operator Error or Misuse and Investigation Complete; Description editors are not shown.

| Branch | Condition / Action will run | Operator Error or Misuse | Investigation Complete |
|--------|-----------------------------|-------------------------|------------------------|
| If | NonNavigable Object Misuse Details is Movable UNMAPPED Object - Misuse | Misuse | Investigation Complete |
| Otherwise if | NonNavigable Object Misuse Details is Stationary Object/Equipment - Potential Error | Potential Operator Error | Investigation Complete |
| Otherwise | If no other conditions are met | No Operator Error or Misuse | Investigation Complete |

Preserve the exact distinction between the branch option Stationary Object/Equipment - Potential Error and its output Potential Operator Error. The first option is Movable UNMAPPED Object - Misuse, with the shown spelling/capitalization.

###### Otherwise and outcome semantics
- Otherwise covers other values only after the outer four-predicate trigger is satisfied. It is NOT a general fallback that permits a new run with blank misuse details; that trigger explicitly requires nonempty details. A value cleared after triggering is a separate snapshot/current-value timing case to validate.
- New nonempty detail options would fall through to Otherwise unless one of the two exact branch values matches. Do not infer an explicit no-misuse whitelist that is not configured.
- Every normal branch completes investigation, including the Misuse and Potential Operator Error branches. Investigation Complete therefore does not imply No Operator Error or Misuse or resolution of every other review task.
- All branch outcomes share the initial Intended Perception Demotion / Intended Behavior assignments. A-31 does not directly write MAIN, masking, secondary links, either object-assessment input, headlands state, JRM links, reviewer, overall triage completion, or scope.

###### Dependencies and gating audit
- A-21 can assign fixed MAIN 12.29; other MAIN writers/manual edits may also produce that membership. The additional object-location and misuse-detail inputs must arrive as well; current values do not establish who populated them.
- A-1 can initialize Investigation Not Complete. A branch completing investigation makes A-31's predicate false; reset/manual reopening can re-enter eligibility only while MAIN, inside-field assessment, and nonempty misuse details still qualify. There is no Headlands Complete prerequisite, unlike A-28.
- Changing one nonempty misuse-detail selection to another does not by itself turn the outer nonempty predicate false and true. After completion, such an edit also does not satisfy the investigation prerequisite. Do not assume A-31 continuously reclassifies operator status on every detail change.
- The initial update and branch update are separate configured steps. Validate intermediate visibility, failure between steps, and stale/current values used for branch evaluation; do not infer whole-workflow atomicity from the shared record ID.
- Earlier completion by another classifier can prevent later-arriving location/details from making A-31 eligible, since Investigation Not Complete is required. Conversely, a queued run can apply decisions after newer inputs arrive. These are scenarios to validate, not observed production incidents.
- Mixed MAIN sets or raw-versus-MAIN differences can conditionally overlap other captured classifiers. Their guards and completion writes do not establish global precedence. A dedicated initialization barrier alone does not serialize these later decisions.
- A-39's now-captured original-linked-code lookup trigger and unguarded Always No Operator Error or Misuse assignment differ from A-31's Misuse/Potential branches. Actual shared cohorts, reference mappings, and execution ordering still need validation before attributing an overwrite or deciding redundancy/removal.
- A-38's captured five-field watcher includes Confirmed Demotion Type and Investigation Complete, so A-31's separate initial/branch changes can trigger separate evaluations when those values change. Operator/bug values are not themselves watched by A-38. A-40 now has all five watched fields and ordered scope branches captured, including operator/bug/position inputs. Actual interleaving and final outputs still require runtime validation.
- For the deferred initialization gate, preserve all FOUR trigger predicates and the initial-plus-branch structure if approved. Changing detail-edit responsiveness, fallback treatment, branch outputs, atomicity, or manual-override protection is a separate behavior/design change. No gate has been implemented.

###### Remaining identity and validation evidence
Visible configuration capture is complete; no more A-31 screenshots are requested at this stage. This is not migration approval.
1. Immutable automation ID/stable link, published revision/effective time/current server-state confirmation following the connection caveat, optional Descriptions, and resolved 12.29 reference identity.
2. Validate inside versus other/blank location, empty/nonempty detail values, both exact branches and other values, investigation states, each prerequisite arriving last, already-matching records, manual reopening/detail edits, changed values between initial and branch actions, partial failures/interleaving, competing classifiers/operator writers, and downstream activities/scope.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes linked 12.29 |
| Vehicle/Object Outside Field | INPUT | Exactly Inside Field (OBVIOUS) |
| NonNavigable Object Misuse Details | INPUT/BRANCH INPUT | Nonempty prerequisite; two exact options and Otherwise |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; every branch assigns Investigation Complete |
| Confirmed Demotion Type | OUTPUT | Initial Always action assigns Intended Perception Demotion |
| Bug or Intended Behavior | OUTPUT | Initial Always action assigns Intended Behavior |
| Operator Error or Misuse | OUTPUT | Branch assigns Misuse, Potential Operator Error, or No Operator Error or Misuse |

---

#### Evidence record A-32: 12.24, 12.27 Intended Perception

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. All three predicates, Always setting, target table/record token, and four assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-32. No test performed by the agent.  
**Name:** A-32 12.24, 12.27 Intended Perception in the inventory; sidebar/top labels are truncated.  
**Group:** Perception Demotions, shown with 3 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 14 this month displayed; a point-in-time UI count, not execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL THREE are required; the full trigger card confirms both code labels:
  1. `MAIN Demotion Code` **has any of** `12.24`, `12.27`.
  2. **AND** `Vehicle/Object Outside Field` **is** `Inside Field (OBVIOUS)`.
  3. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- MAIN is a linked-code membership test, not Halt Code - Import or an only-one-code requirement. Vehicle/Object Outside Field is the separate single-select assessment field, not Headlands vs Interior or an interchangeable Interior Pass value.
- Unlike A-31, there is NO NonNavigable Object Misuse Details prerequisite or branch. Blank details do not block A-32 if its actual three predicates hold.
- Blank location or investigation status do not equal the required selections. No Headlands Complete, masking, raw-code, existing classification/operator/bug-value, machine-type, or initialization-ready restriction is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.

###### Action
- **Visible structure:** One Update record action; no conditional groups or additional actions shown. Unlike A-31's initial-plus-branch path, these four values are assigned by one configured update.
- **Description:** Empty; the Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 1 more field. The complete field capture identifies Bug or Intended Behavior as the fourth field.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Confirmed Demotion Type | `Intended Perception Demotion` | One fixed multiple-select choice shown |
| Bug or Intended Behavior | `Intended Behavior` | Fixed single-select choice |
| Operator Error or Misuse | `Misuse` | Fixed single-select choice; not Potential Operator Error or No Operator Error or Misuse |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Meaning and dependencies
- Every qualifying execution of this configured action assigns Misuse directly. It does not consult object-misuse details to choose among A-31's three operator outcomes. This is the recorded policy, not independent evidence of actual operator fault for a specific event.
- Intended Perception Demotion, Intended Behavior, Misuse, and Investigation Complete are separate fields assigned together. Completion does not mean absence of misuse or completion of all other triage activities.
- A-19/A-20 are captured MAIN producers for 12.27/12.24; other MAIN writers/manual changes can also supply the links. The inside-field assessment and incomplete-investigation state must also hold; a MAIN assignment alone does not establish a run.
- A-32 writes ONLY these four fields. It does not write MAIN, masking, secondary links, either object-assessment field, headlands state, JRM links, reviewer, overall triage completion, or scope.

###### Gating and competing-writer audit
- A-1 can initialize Investigation Not Complete. Completion by A-32 makes the trigger false; a later reset/manual reopening can re-enter eligibility only if MAIN and Inside Field (OBVIOUS) still qualify. Always execution has no shown preserve-existing-value guard and can reapply Misuse/classification/bug state.
- A later location edit is not continuous reclassification: leaving Inside Field makes this trigger false but does not invoke a clearing/reversal action. A-33's now-captured outside/potential-outside/Interior Impassible rule also requires Investigation Not Complete, so changing location or MAIN while investigation stays complete does not itself enable it. A-33 writes JRM-446, while A-32 does not clear/manage JRM links if a later reopened investigation is reclassified inside.
- Earlier completion by another classifier can block later-arriving location evidence from making A-32 eligible. A queued A-32 action may also finish after newer inputs arrive. These are validation scenarios, not observed incidents; initialization gating alone does not establish readiness/precedence for all later inputs.
- A-31 targets 12.29 and A-32 targets 12.24/12.27. With one MAIN code their code predicates are disjoint, but a mixed MAIN set can satisfy both if the remaining prerequisites hold. A-31's Potential Operator Error or Otherwise branch differs from A-32's fixed Misuse; its Movable UNMAPPED branch agrees. No actual mixed cohort or conflicting execution is established.
- Other raw-code or mixed-MAIN classifiers can conditionally overlap; do not assume code-list differences imply exclusivity for every record representation. The reviewed MAIN field's single-record preference is not proof of a hard cardinality constraint.
- A-39's current captured rule Always assigns No Operator Error or Misuse when its original-linked-code lookup exactly matches NOT Required - Misuse Check, without an empty-output guard. This differs from A-32's Misuse assignment, but actual shared eligibility, reference mappings, ordering, and redundancy still need validation.
- A-38/A-40 are documented downstream consumers. In particular, the legacy scope rule references Misuse, but A-32 itself does not set scope and its actual downstream result remains unverified until those live rules are captured.
- For the deferred initialization gate, preserve all THREE predicates if approved. Adding an A-31-style details prerequisite, changing Misuse to a tentative/default label, or adding location-change responsiveness is a separate behavior change requiring approval. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-32 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, full name, published revision/effective time, and resolved 12.24/12.27 reference identities.
2. Validate either/both/mixed MAIN codes, inside versus other/blank location, blank versus populated misuse details without inventing a prerequisite, investigation states, each input arriving last, already-matching records, manual reopening/overrides, location/code changes while complete, competing classifiers/operator writers, and downstream activities/scope.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes linked 12.24 or 12.27 |
| Vehicle/Object Outside Field | INPUT | Exactly Inside Field (OBVIOUS) |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Confirmed Demotion Type | OUTPUT | Fixed Intended Perception Demotion |
| Bug or Intended Behavior | OUTPUT | Fixed Intended Behavior |
| Operator Error or Misuse | OUTPUT | Fixed Misuse |

---

#### Evidence record A-33: 12.24, 12.27 Unintended Perception

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. All three predicates with complete code/location selections, Always setting, target table/record token, and five assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-33. No test performed by the agent.  
**Name/scope:** A-33 12.24, 12.27 Unintended Perception in the inventory/sidebar (truncated). The actual trigger also includes 12.29; do not infer scope from the shorter name.  
**Group:** Perception Demotions, shown with 3 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 15 this month displayed; a point-in-time UI count, not execution-success or coverage measurement.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** ALL THREE are required; the full trigger card confirms the lists clipped in the condition selector:
  1. `MAIN Demotion Code` **has any of** `12.24`, `12.27`, `12.29`.
  2. **AND** `Vehicle/Object Outside Field` **is any of** `Outside Field (OBVIOUS)`, `Outside Field (POTENTIAL)`, `Interior Impassible`.
  3. **AND** `Investigation Complete` **is** `Investigation Not Complete`.
- MAIN is a linked-code membership test, not Halt Code - Import or an only-one-code requirement. Vehicle/Object Outside Field is a separate single-select assessment, not Headlands vs Interior.
- Preserve the spelling Interior Impassible, corroborated by the earlier production schema. It is an explicit accepted value despite not being labeled Outside Field. Outside Field (POTENTIAL) is also accepted; certainty is not required by that selection.
- This is a three-value whitelist, NOT is not Inside Field. The reviewed schema also contains N/A - Spark Error, which is not selected here. Neither that value nor blank location meets the captured condition. Blank investigation status is not Investigation Not Complete.
- No NonNavigable Object Misuse Details, Headlands Complete, masking, raw-code, current classification/operator/bug/JRM-value, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records.

###### Action
- **Visible structure:** One Update record action; no conditional branches or additional actions shown.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse, Investigation Complete, and 2 more fields. The full field captures identify Bug or Intended Behavior and Confirmed JRM Link. Description editor is outside the captures.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Bug or Intended Behavior | `Known Bug` | Fixed single-select choice |
| Confirmed JRM Link | `JRM-446` | Fixed literal name in the linked-record field, not a dynamic token, record-ID literal, or direct external Jira action |
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

Confirmed JRM Link is a multipleRecordLinks field targeting tbllaxeplHp2Jmrw6 in the previously read production schema. Preserve the JRM-446 name. Resolved identity, missing/duplicate/renamed-name behavior, preservation versus replacement of existing associations, and downstream integration effects remain validation items; this is not evidence of an external issue creation/update.

###### Comparison with A-31/A-32
For Investigation Not Complete and the relevant MAIN membership:

| MAIN code | Vehicle/Object Outside Field | Rule and additional prerequisite |
|-----------|------------------------------|----------------------------------|
| 12.29 | Inside Field (OBVIOUS) | A-31 additionally requires nonempty NonNavigable Object Misuse Details; branch determines operator status |
| 12.24 or 12.27 | Inside Field (OBVIOUS) | A-32 directly assigns Misuse; no details prerequisite |
| 12.24, 12.27, or 12.29 | Any of A-33's three listed values | A-33 assigns unintended perception, Known Bug, No Operator Error or Misuse, completion, and JRM-446 |
| Any of these codes | Blank or N/A - Spark Error | None of these three rules qualifies on that location value |

Inside 12.29 with blank details also fails this trio's full predicates. These are coverage statements within A-31/A-32/A-33, not proof no other workflow handles such records. Because location is singleSelect, A-33's accepted values are disjoint from A-31/A-32's Inside Field value at a fixed state, even if MAIN has multiple codes. This does not serialize runs after location changes.

###### Dependencies and gating audit
- A-19/A-20/A-21 can assign MAIN 12.27/12.24/12.29; other writers/manual changes can also supply those links. The location assessment's actual producer/timing still needs tracing; MAIN alone does not establish a run.
- A-1 can initialize Investigation Not Complete. A-33's completion write makes the predicate false; a later reset/manual reopening can re-enter it only if MAIN and a listed location still qualify. Always execution has no shown preservation guard and can reapply all five assignments, including the issue association.
- A location correction after investigation is complete does not by itself enable A-31/A-32/A-33, because each requires Investigation Not Complete. Leaving A-33's location set invokes no clearing action here. A-31/A-32 do not write JRM links, so do not assume a later intended classification removes JRM-446.
- A queued run can act after newer inputs arrive, and an earlier completion writer can block a later-ready classifier. These are validation scenarios, not observed misclassifications. Initialization gating alone does not enforce location readiness or cross-rule precedence.
- Mixed MAIN sets or raw-versus-MAIN differences can conditionally overlap other classifiers outside this trio. A-27/A-29 also assign fixed JRM names for their own conditions; investigate actual shared eligibility and link-update semantics before attributing an issue-link conflict.
- A-33 writes ONLY its five listed fields. It does not write MAIN, masking, secondary links, object-assessment inputs, headlands state, reviewer, overall triage completion, or scope. Known Bug and No Operator Error or Misuse are configured outputs, not independent evidence of an event's cause.
- A-38/A-40 are documented downstream consumers, with A-38 now configuration-captured and A-40's current configuration also captured (runtime validation remains separate). Do not equate Investigation Complete with overall triage completion or infer dashboard inclusion solely from this action.
- For the deferred initialization gate, preserve all THREE predicates and the explicit three-value location whitelist if approved. Broadening it to every non-inside/blank value, changing issue-link preservation, or adding automatic reclassification on later location edits is a separate behavior change. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-33 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, full name, optional Description, published revision/effective time, and resolved MAIN/JRM-446 reference identities.
2. Validate each code/location combination, blank/N/A - Spark Error, inside 12.29 with/without details, incomplete/complete/blank investigation, each input arriving last, already-matching records, manual reopening/location corrections, single/mixed MAIN sets, existing/multiple JRM links, name resolution, queued competing classifiers, and downstream activities/scope.

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| MAIN Demotion Code | INPUT | Includes 12.24, 12.27, OR 12.29 |
| Vehicle/Object Outside Field | INPUT | Explicit three-value whitelist |
| Investigation Complete | INPUT/OUTPUT | Requires Investigation Not Complete; assigns Investigation Complete |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion |
| Bug or Intended Behavior | OUTPUT | Fixed Known Bug |
| Confirmed JRM Link | OUTPUT | Fixed JRM-446 linked-record name |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |

---

#### Confirmed Demotion Type Automations (A-34 through A-37)

These automations set the `Confirmed Demotion Type` and related fields based on masking and MAIN-reason/process lookups. A-34 through A-37 now have current core configurations captured: all four use Always Update record, assign No Operator Error or Misuse and Investigation Complete, and set their respective confirmed type. None has an Investigation Not Complete prerequisite. Their field-output reset behavior must not be confused with the investigation-gated A-26 through A-33 rules; runtime/version validation and the approved initialization-gate design remain separate.

---

#### Evidence record A-34: Confirmed Manual Demotion

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. Both predicates, Always setting, target table/record token, and all three assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-34. No test performed by the agent.  
**Name:** A-34 Confirmed Manual Demotion in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Demotion Type, shown with 4 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 611 this month displayed; earlier notes recorded 231. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms labels cropped in the condition selector:
  1. `Manual Demotion Masking` **is** `Intended Manual Demotion - No Mask`.
  2. **AND** `MAIN Demotion Reason` **has any of** `DR-1 In-Cab Controls Override`, `DR-2 Human-Triggered Demotion`.
- The lookup is MAIN Demotion Reason, NOT Demotion Reason or Secondary Demotion Reason. Has any of does not require all MAIN reasons to be manual or one particular reason to be the sole result.
- No Investigation Not Complete, headlands-completion, existing classification/operator-value, raw-code, machine-type, or initialization-ready guard is shown. The masking value N/A is not the same as Intended Manual Demotion - No Mask.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It is not an action on every edit or a recurring enforcement of these outputs.

###### Action
- **Visible structure:** One Update record action; no branches or additional actions shown.
- **Description:** Empty; the Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse and Investigation Complete. The full action capture confirms exactly those three fields.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Confirmed Demotion Type | `Intended Manual Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Meaning, dependencies, and gating audit
Classifies records already labeled no-mask and having at least one MAIN manual reason as intended manual demotions, with no operator error/misuse and completed investigation. These are configured assignments; the rule does not independently verify that the no-mask decision or real-world operator behavior was correct.

- A-16/A-17 can supply the no-mask value and an imported-code MAIN link. Their triggers read primary/secondary reasons; A-34 instead evaluates the resulting MAIN reason. Do not assume a producer's qualifying raw reason proves the selected MAIN lookup has the same value, particularly with name resolution or mixed links.
- A-34 writes ONLY the three listed fields. It does not change masking, MAIN, secondary links, Bug or Intended Behavior, JRM links, reviewer, headlands state, overall triage completion, or scope. Existing bug/JRM associations are not cleared here.
- **A-1 ordering risk:** A-34 can mark investigation complete without first requiring the Investigation Not Complete value initialized by A-1. If a late A-1 action resets that flag while masking and MAIN reason remain matched, the flag-only change does NOT re-enter A-34's trigger. This is the same class of risk as the observed A-37/A-1 overwrite, but no A-34-specific incident is established.
- Manual reopening of Investigation Complete alone likewise does not rerun A-34 while its trigger inputs remain unchanged. Conversely, a masking/MAIN-reason transition that newly matches can run A-34 even on an already-completed investigation; it has no completion guard.
- Always execution has no shown preserve-existing-operator/classification guard. A newly eligible or queued action can replace prior values. A subsequent output-only manual edit does not itself cause A-34 to reassert them.
- A-35/A-36 both have captured masking predicates accepting Manual Mask or N/A, disjoint from A-34's no-mask value at a fixed state. A-37 now has those same masking choices confirmed in its current capture. Disjoint settled masking states do not order actions already queued before masking/reason changes.
- Captured A-16 overlaps with several masking writers can change which classification path becomes eligible. If an upstream no-mask assignment is incorrect, A-34 can propagate that decision into classification/operator/completion fields. This is dependency analysis, not attribution of a past incident.
- A-26 through A-33 use other combinations of raw/MAIN code, location, and investigation prerequisites. No A-34 masking/MAIN-reason predicate establishes global priority over those classifiers; validate any actual shared input states and ordering separately.
- A-38/A-40 are documented downstream consumers of the output fields; A-38 is now configuration-captured and A-40's five-field trigger and scope branches are now captured, with runtime validation pending. Investigation Complete alone does not establish overall triage completion or scope.
- For the deferred initialization gate, preserve BOTH captured predicates and add readiness only if approved. Adding Investigation Not Complete as a shortcut would change A-34's eligibility for already-completed records and manual reopening; it is not a faithful transcription or an approved fix. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-34 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, full name, published revision/effective time, and MAIN/reason reference identities.
2. Validate each predicate arriving last, no-mask versus N/A/Manual Mask, raw-versus-MAIN differences, mixed MAIN reasons, already-matching records, completed investigations becoming eligible, output-only changes/reopening, late A-1 resets, upstream masking changes, competing classifier writes, unchanged bug/JRM fields, and downstream activities/scope.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** This recurring UPDATE would reassert outputs on already-matching rows and can erase later manual edits or repair resets that the Airtable event trigger leaves untouched. Scalar IN also does not establish equivalence to the native any-match lookup predicate. Validate schema, list semantics, and approved write precedence before implementation; original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET 
  operator_error_or_misuse = 'No Operator Error or Misuse',
  confirmed_demotion_type = 'Intended Manual Demotion',
  investigation_complete = 'Investigation Complete'
WHERE manual_demotion_masking = 'Intended Manual Demotion - No Mask'
  AND main_demotion_reason IN ('DR-1 In-Cab Controls Override', 'DR-2 Human-Triggered Demotion');
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Manual Demotion Masking | INPUT | Exact Intended Manual Demotion - No Mask |
| MAIN Demotion Reason | INPUT | Any of DR-1/DR-2 full reason records |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Confirmed Demotion Type | OUTPUT | Fixed Intended Manual Demotion |
| Investigation Complete | OUTPUT | Fixed Investigation Complete; not a trigger predicate |

---

#### Evidence record A-35: Automatic Unintended Perception Demotion

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention. Both predicates, Always setting, target table/record token, and all three assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-35. No test performed by the agent.  
**Name:** A-35 Automatic Unintended Perception Demotion in the inventory; sidebar/top labels are truncated.  
**Group:** Confirmed Demotion Type, shown with 4 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 93 this month displayed; earlier notes recorded 28. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms the labels clipped in the selector:
  1. `Triage Process` **has any of** `Automatic Unintended Perception Demotion`.
  2. **AND** `Manual Demotion Masking` **is any of** `Manual Mask`, `N/A`.
- Preserve has any of for the process lookup, not is exactly. Additional process values are not explicitly excluded. Masking is membership in the two single-select choices; Intended Manual Demotion - No Mask does not qualify.
- No Investigation Not Complete, headlands-completion, raw-code, existing classification/operator-value, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. Output-only changes do not automatically retrigger it.

###### Action
- **Visible structure:** One Update record action; no branches or additional actions shown.
- **Description:** Empty; the Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the action Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse and Investigation Complete; the full field panel confirms exactly those three assignments.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Perception Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Process lookup and upstream evidence
The earlier production schema identifies Triage Process (fldUTRUIUS22LeCbJ) as multipleLookupValues through MAIN Demotion Code (recordLinkFieldId fldw0GEHxF0PFRSof), reading linked Halt Codes field fldtQ19seFvs3FSk2. Its result is linked-record-valued, not a directly writable process label on the demotion row. MAIN/reference changes can change that lookup and eligibility; actual trigger propagation and timing require validation.

The old description asserted that TP-12/TP-13/TP-14 were upstream automations setting this field. That provenance has not been verified and must not be treated as an established writer chain. Trace the actual reference field/metadata producers rather than assuming those labels identify live automations.

###### Meaning, dependencies, and gating audit
Completes/classifies records whose process lookup includes the selected automatic-unintended-perception process and whose masking is Manual Mask or N/A. The old non-manual-only description was too narrow: the captured rule explicitly accepts Manual Mask and has no raw manual-reason exclusion.

- A-16 through A-25 can affect MAIN/masking; the resulting MAIN-linked reference data determines Triage Process. Current values alone do not identify which upstream action or reference edit made this rule eligible.
- A-35 writes ONLY the three listed fields. It does not set Bug or Intended Behavior, JRM links, MAIN, masking, secondary links, reviewer, headlands state, overall triage completion, or scope. Unintended Perception Demotion does not imply that this action also wrote Known Bug; prior bug/JRM values remain unmanaged here.
- **A-1 ordering risk:** With no incomplete-investigation prerequisite, A-35 can complete investigation before an A-1 initialization action finishes. A later flag-only reset does not re-enter the unchanged process/masking predicate. This is the risk class observed for A-37/A-1, not proof of an A-35-specific incident.
- Manual reopening of investigation alone likewise does not rerun A-35 while process/masking stay matched. Conversely, newly matching process/masking can run it on an already-completed investigation. Always execution has no shown preserve-existing-classification/operator guard.
- A-34 requires the different no-mask selection, so A-34/A-35 are disjoint on the settled masking value. Changes over time can still leave queued actions with different classifications; disjoint current predicates are not scheduler priority.
- A-36's captured process predicate is exactly Automatic Non-Perception Demotion, unlike A-35's any-match for Automatic Unintended Perception Demotion. A-37's current exact-match Automatic Intended Vehicle Demotion predicate and Always action are now captured. Multiple MAIN links or reference process values require native exact/any-match validation rather than assuming either common semantics or global exclusivity.
- If another classifier sharing an eligible record needs later-arriving context and Investigation Not Complete, A-35 completing first can prevent that later rule from entering its condition. It can also be queued alongside another writer and finish later. These are conditional scenarios, not observed missed runs or overwrites.
- This rule's conditional No Operator Error or Misuse coverage does not establish A-39 redundancy. The full set of relevant writers, their eligible populations, and timing still need review.
- A-38's current configuration is captured; A-40's five-field trigger and scope branches are now captured, with runtime validation pending. Both are downstream consumers, with actual run outcomes still unverified. Investigation Complete here does not establish overall triage completion or scope.
- For the deferred initialization gate, preserve BOTH predicates, including any-match process semantics, and add readiness only if approved. Adding Investigation Not Complete or an existing-value guard is a separate behavior change, not an already-approved fix. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-35 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, full name, published revision/effective time, and resolved process/reference identities and producer chain.
2. Validate mixed/empty process lookups, MAIN/reference changes, both allowed masking values versus no-mask, each predicate arriving last, already-matching records, completed investigations becoming eligible, output-only edits/reopening, late A-1 resets, competing context-dependent classifiers, unchanged bug/JRM fields, and downstream activities/scope.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** Scalar process equality does not establish equivalence to the captured lookup has-any predicate, and a recurring UPDATE can overwrite later manual values or repair flag resets that the native event trigger leaves untouched. Validate schema, lookup/reference semantics, and approved write precedence before implementation. Original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET 
  operator_error_or_misuse = 'No Operator Error or Misuse',
  confirmed_demotion_type = 'Unintended Perception Demotion',
  investigation_complete = 'Investigation Complete'
WHERE triage_process = 'Automatic Unintended Perception Demotion'
  AND manual_demotion_masking IN ('Manual Mask', 'N/A');
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Triage Process | INPUT | Has any of Automatic Unintended Perception Demotion |
| Manual Demotion Masking | INPUT | Is any of Manual Mask, N/A |
| MAIN Demotion Code | INDIRECT INPUT | Schema-confirmed source link for Triage Process |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Perception Demotion |
| Investigation Complete | OUTPUT | Fixed Investigation Complete; not a trigger predicate |

---

#### Evidence record A-36: Automatic Unintended Vehicle Demotion

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots, including the supplemental action settings, and owner-confirmed trigger-record-ID convention. Both predicates, Always setting, target table/record token, and all three assignments are captured.  
**Behavior/migration status:** NOT VERIFIED; no expanded test results or record-specific production run evidence supplied for A-36. No test performed by the agent.  
**Name:** A-36 Automatic Unintended Vehicle Demotion in the inventory; sidebar/top labels are truncated. The selected PROCESS name is Automatic Non-Perception Demotion, not a replacement inferred from the automation name.  
**Group:** Confirmed Demotion Type, shown with 4 active automations.  
**Enabled:** ON in the screenshots  
**Runs:** 214 this month displayed; earlier notes recorded 79. These are point-in-time UI counts, not execution-success or coverage measurements.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms the labels cropped in the selector:
  1. `Triage Process` **is exactly** `Automatic Non-Perception Demotion`.
  2. **AND** `Manual Demotion Masking` **is any of** `Manual Mask`, `N/A`.
- Preserve is exactly for the process lookup. A-35 uses has any of for its different process selection; do not normalize these operators into one another. Validate multiple/distinct/duplicate lookup values rather than silently accepting any matching member for A-36.
- Masking accepts both Manual Mask and N/A, not Intended Manual Demotion - No Mask. The old description excluding manual masking contradicted this captured condition and is superseded.
- No Investigation Not Complete, headlands-completion, raw-code/reason, current classification/operator-value, machine-type, or initialization-ready condition is shown.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce its outputs.

###### Action
- **Visible structure:** One Update record action; no branches or additional actions shown.
- **Description:** Empty; the supplemental Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the supplemental Configuration panel.
- **Target table:** Demotions_DatabricksSync, confirmed in the action captures.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse and Investigation Complete. The earlier full field capture and supplemental settings together confirm exactly those three fields.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Confirmed Demotion Type | `Unintended Vehicle Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

###### Process/reference dependency
As established by the production schema read for A-35, Triage Process is a multipleLookupValues field through MAIN Demotion Code to linked Halt Codes process data. It is not a directly assigned label on this demotion row. MAIN/reference changes can affect eligibility; the actual reference producer and propagation/trigger timing require validation.

Automatic Non-Perception Demotion is the selected process label; Unintended Vehicle Demotion is the assigned classification label. Preserve both without renaming one to match the other. Exact-match semantics for the linked-record-valued lookup and resolved process identity remain validation items.

###### Meaning, dependencies, and gating audit
Classifies the exact non-perception process with either Manual Mask or N/A as unintended vehicle demotion, no operator error/misuse, and completed investigation. This includes qualifying manually masked events and is not independent evidence of the cause or operator behavior of a particular event.

- A-16 through A-25 can affect MAIN/masking; MAIN-linked reference data supplies the process lookup. Current values do not identify the upstream writer or historical values at trigger time.
- A-36 writes ONLY the three listed fields. It does not set Bug or Intended Behavior, JRM links, MAIN, masking, secondary links, reviewer, headlands state, overall triage completion, or scope. Existing bug/JRM associations remain unmanaged here.
- **A-1 ordering risk:** Investigation status is an output, not a trigger prerequisite. A-36 can complete investigation before a delayed A-1 initialization write; resetting the completion flag alone does not re-enter an unchanged process/masking predicate. This is the risk class observed for A-37/A-1, not a separately observed A-36 failure.
- Manual reopening of investigation alone likewise does not rerun A-36 while the trigger inputs remain matched. A newly matching process/masking state can classify an already-completed investigation. Always execution has no shown preserve-existing-operator/classification guard.
- A-34's no-mask value is disjoint from A-36's allowed masking values on a fixed state. A-35 shares A-36's masking choices but has a different process and any-match rather than exact-match. Do not infer general multi-value exclusivity or priority solely from different labels; preserve and validate the native operators. A-37's current exact-match Automatic Intended Vehicle Demotion predicate and Always action are now captured.
- Queued actions may finish after masking/reference inputs change. Earlier completion can also prevent a more context-dependent rule requiring Investigation Not Complete from becoming eligible later, if its other inputs arrive afterward. These are conditional scenarios, not proven cohorts, missed runs, or overwrites.
- Conditional No Operator Error or Misuse coverage here does not prove A-39 redundancy or safe removal. Complete writer/population/timing analysis remains outstanding.
- A-38/A-40 are documented downstream consumers with A-38 now configuration-captured and A-40's current configuration also captured (runtime validation remains separate). Investigation Complete does not establish overall triage completion or scope.
- For the deferred initialization gate, preserve BOTH predicates and add readiness only if approved. Adding Investigation Not Complete or changing exact-match to any-match would alter current behavior and is not an already-approved fix. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-36 screenshots are required at this stage. This is not migration approval.
1. Immutable automation ID/stable link, full name, published revision/effective time, and process/reference identity and producer chain.
2. Validate empty/single/multiple/duplicate process results, exact versus any-match behavior, both masking choices versus no-mask, each predicate arriving last, already-matching records, completed investigations becoming eligible, output-only edits/reopening, late A-1 resets, reference changes, competing context-dependent classifiers, unchanged bug/JRM fields, and downstream activities/scope.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** Scalar equality does not establish the correct representation/semantics of a linked-record-valued lookup, and a recurring UPDATE can overwrite later manual values or repair flag resets that the native event trigger leaves untouched. Validate schema, native exact-match behavior, and approved write precedence before implementation. Original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET 
  operator_error_or_misuse = 'No Operator Error or Misuse',
  confirmed_demotion_type = 'Unintended Vehicle Demotion',
  investigation_complete = 'Investigation Complete'
WHERE triage_process = 'Automatic Non-Perception Demotion'
  AND manual_demotion_masking IN ('Manual Mask', 'N/A');
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Triage Process | INPUT | Is exactly Automatic Non-Perception Demotion |
| Manual Demotion Masking | INPUT | Is any of Manual Mask, N/A |
| MAIN Demotion Code | INDIRECT INPUT | Schema-confirmed source link for Triage Process |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Confirmed Demotion Type | OUTPUT | Fixed Unintended Vehicle Demotion |
| Investigation Complete | OUTPUT | Fixed Investigation Complete; not a trigger predicate |

---

#### Evidence record A-37: Automatic Intended Vehicle Demotion

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three current screenshots and trigger-record-ID convention. Both predicates, Always setting, target table/record token, and three assignments are confirmed.  
**Behavior/migration status:** Specific historical successful actions, owner-confirmed classification reversals, and one A-37/A-1 investigation overwrite are documented below. Broader coverage, current-to-historical version correspondence, and migration behavior remain unverified. No production test or write performed by the agent.  
**Runs:** Current configuration and earlier history captures display 8 this month; older notes recorded 3. These are point-in-time UI counts.  
**Enabled:** ON in the current and earlier history screenshots.  
**Name/group:** A-37 Automatic Intended Vehicle Demotion / Confirmed Demotion Type in the inventory; current sidebar labels are truncated and the group displays 4 active automations.  
**Identity/version:** No immutable automation ID/stable link or exact current published revision/effective time captured. Brian Moffatt is displayed as last updater. No unpublished-change or reconnecting banner is visible. Earlier timeline evidence is preserved separately below.

###### Timeline evidence
- **Earliest visible revision:** August 17, 2026 at 6:16 PM. The supplied Revision history screenshot shows one visible entry. Brian identifies this as the likely creation date; record it as the initial observed revision rather than independently verified creation/enablement metadata.
- **Earliest observed successful run:** August 19, 2026 at 11:29 AM, from the earlier Run history screenshot. Completeness of the historical run listing is not independently established.
- Times are recorded exactly as displayed; the UI timezone is not shown.
- Exact first enablement/publication time remains unverified. Do not equate a revision with an executed run or assume pre-existing matching records were backfilled when the rule was enabled.
- For the A-39 analysis, distinguish event timestamp from automation execution time: an older event may have been processed later. These screenshots do not prove A-37's availability or behavior before the observed revision, nor establish who assigned a particular record's operator status.

###### Read-only follow-up: 17.0 / 27.2 dashboard question
Current reference reads resolve 17.0 (recB6c3goFeSG5EmW) to DR-13 Vehicle Operation Check and Triage Process recHwqiVE0JtIPAoH, Automatic Intended Vehicle Demotion. Current 27.2 (reco5Ukhd2DieS44c) resolves to DR-11 Operator Error and recoTqFZ7aulm7SQA, Automatic Non-Perception Demotion. These are different routing paths; do not assume A-37 currently covers both codes.

A Databricks diagnostic query restricted to Demotions = 1, raw halt_code in 17.0/27.2, and event Timestamp_utc >= 2026-08-18 00:00:00 UTC found six 17.0 records (four Intended Vehicle, two Unintended Vehicle) and twenty 27.2 records (all Unintended Vehicle). This broad date check does not reproduce the coworker's Fall #1 customer-package filter and does not include all possible manual demotions whose MAIN code differs from the raw code.

The two 17.0 exceptions were independently read in live Airtable and have the same Unintended Vehicle Demotion value there, so they are not just a Databricks-only lag in this check:

| Redacted case alias | Event UTC | Machine type | Current process / masking | Current confirmed type |
|---|---|---|---|---|
| CASE-17-OVERRIDE-A | 2026-08-25 16:33:28.832627 | customer | Automatic Intended Vehicle Demotion / N/A | Unintended Vehicle Demotion |
| CASE-17-OVERRIDE-B | 2026-08-25 16:35:51.841120 | customer | Automatic Intended Vehicle Demotion / N/A | Unintended Vehicle Demotion |

Both are later than the initial observed August 17 revision. Expanded A-37 run-history screenshots match BOTH record IDs above: each run is marked Ran successfully on 8/25/2026 at 11:31 AM, in the UI's unspecified timezone. Each trigger found its respective record in Demotions_DatabricksSync. Subsequent action captures confirm Update record Success for both, with input and returned record IDs matching the respective affected record. Both actions used specific fields and included Operator Error or Misuse, Confirmed Demotion Type, and Investigation Complete. This rules out A-37 never triggering, targeting a different record, or omitting Confirmed Demotion Type in these two runs.

Subsequent screenshots expand the selected Confirmed Demotion Type item for BOTH runs: selfI8xmtc22xciNt. A read-only describe_table lookup resolves that ID under field fldIVTtGqsK8mResN to Intended Vehicle Demotion. The other shown option IDs resolve to selPU699wajE1CsHt = No Operator Error or Misuse and selIN75mWRN43Y7ph = Investigation Complete. This establishes the intended selection used by the successful actions, rather than inferring it from the automation name or legacy documentation.

A fresh read of BOTH records after resolving the historical inputs still returns Confirmed Demotion Type = Unintended Vehicle Demotion. The current schema maps that label to a DIFFERENT option, selYEnZvjt4g2v3i9, while the historical selected option selfI8xmtc22xciNt still exists as Intended Vehicle Demotion. The evidence therefore supports a subsequent change of the stored classification, not A-37 skipping these records or a simple relabeling of the same selected option.

Brian then supplied five record-revision screenshots for CASE-17-OVERRIDE-A, identified by its exact A_UID at the top. One entry attributes the addition of Intended Vehicle Demotion and completion of investigation to A-37. Another explicitly says You edited this record and shows Confirmed Demotion Type removing Intended Vehicle Demotion and adding Non-Perception Demotion. This is direct evidence of a classification override attributed to the signed-in user's account for this first record, not merely an inferred competing automation. Do not infer whether it was an intentional correction, bulk cleanup, or accidental edit. Separate nearby pasted edits concern Pilot VINs Linked and Headlands Reviewer; the pictured API-token edit concerns Foxglove URL and No of Spark Engagements, not Confirmed Demotion Type.

The displayed edit times are only 2w ago; exact chronology/timestamps are not captured. Preserve the historical Non-Perception Demotion label verbatim: its mapping/rename to today's Unintended Vehicle Demotion option is not yet independently established. The history also warns that changes to externally syncing data are hidden, and Show more is visible, so these captures are not a complete write ledger. The second record CASE-17-OVERRIDE-B has not yet had its record revisions inspected; do not transfer the first record's attribution to it.

A condition-entry automation does not continuously enforce its output: changing only the output while the trigger conditions remain matched does not itself create a new false-to-true trigger transition. The investigation above was read-only; the agent performed no backfill, reclassification, or automation change.

###### Owner-confirmed resolution and reported 17.0 backfill
Brian subsequently confirmed that the automation change was applied too early, the classifications were deliberately switched back, and then the decision changed again. He recalled making the edits himself and considers the discrepancy explained. Treat this as owner-confirmed intentional reversal, consistent with the observed first-record history, not evidence of A-37 failure. Exact edit timestamps, the second record's revision trail, and the historical option-label mapping remain uncaptured but are no longer blockers to this owner-confirmed explanation.

Brian reported retroactively classifying 14 supplied 17.0 demotion identifiers, with events back to August 1, 2026, as Intended Vehicle Demotion. The owner-held source contains the exact A_UIDs, including plain and hashed VIN forms; these customer identifiers are intentionally omitted from this Git copy. The subsequent read described below matched the 14 identifiers. Its scope was raw halt code and UTC event time, not an independently reproduced dashboard filter. Redacted case aliases below preserve the distinctions between observations without publishing the original record keys.

###### Post-backfill read: classification verified; four investigations incomplete
A subsequent read of production Demotions_DatabricksSync (tblSJItXuuUd0lyHP), filtered by Halt Code - Import = 17.0 and Timestamp UTC >= 2026-08-01T00:00:00Z, returned 14 records (below the 100-record request cap) matching all 14 supplied A_UIDs. All now have Confirmed Demotion Type = Intended Vehicle Demotion, Triage Process = Automatic Intended Vehicle Demotion, MAIN code 17.0, Manual Demotion Masking = N/A, and No Operator Error or Misuse. The classification backfill is verified in Airtable for that scope; earlier Unintended values above are pre-backfill observations, not current results. Investigation Complete is Complete for ten and Not Complete for four:

| Redacted case alias | Event UTC (full precision from A_UID) | Current machine type | Investigation Complete |
|---|---|---|---|
| CASE-INCOMPLETE-A | 2026-08-14 19:18:23.529769 | test | Investigation Not Complete |
| CASE-INCOMPLETE-B | 2026-08-14 21:02:32.962418 | test | Investigation Not Complete |
| CASE-A1-RESET | 2026-09-10 15:34:58.879893 | demo | Investigation Not Complete |
| CASE-INCOMPLETE-C | 2026-09-10 16:10:40.975512 | demo | Investigation Not Complete |

All four also have Triage Activities Complete = Not Complete. One additional test record (CASE-ACTIVITIES-INCOMPLETE, August 11) has Investigation Complete but overall activities Not Complete; these are distinct statuses. Nine customer records have completed investigations, one test record has a completed investigation, and two test plus two demo records do not. This machine-type pattern is a clue, not proof of an automation filter; do not invent a customer-only restriction.

The two September 10 demo records already had Intended Vehicle Demotion plus Investigation Not Complete in reads taken BEFORE Brian's reported backfill. Thus the discrepancy in those two predates this latest classification update. August 14 event dates precede A-37's first observed revision, but event time is not proof of Airtable creation/trigger timing or absence of a later automation run.

Known mechanism and subsequent record-level confirmation:
- Eight subsequent record-history screenshots for CASE-A1-RESET confirm A-37 added Investigation Complete and Intended Vehicle Demotion, followed by an A-1-attributed revision replacing Investigation Complete with Investigation Not Complete. A-1 also assigned Headlands Not Complete and Not Yet Determined scope. This identifies the initialization overwrite for this specific record. It does not establish a repeated A-1 trigger; a creation-triggered action can finish after other automations. Relative timestamps are 3h ago, not exact trigger/run times.
- The same cause has NOT been verified for the other three incomplete records. A-37's current guards are now captured below; the other records' historical input states and execution histories remain unverified. This record's A-37 revision also demonstrates that its demo machine type did not prevent A-37 from completing its investigation in this instance.
- Changing only Confirmed Demotion Type does not by itself enter the documented A-37 conditions again. A manual classification backfill is not necessarily an investigation-status backfill.
- A-38's current capture confirms it watches/reads Investigation Complete to set ONLY Triage Activities Complete through Complete/Not Complete branches. It does not complete or reopen the investigation and cannot itself repair the A-1 investigation reset.
- The reviewed local dev sync notebook's Airtable upsert payload (sync_notebook_dev.py, send_data_to_airtable) does not include Investigation Complete; its Airtable-to-Databricks conversion reads that field. sync_triage_full.py is a dev Airtable-to-Databricks mirror. These local files do not establish deployed production behavior or exclude other writers.

The targeted history check now establishes A-1's overwrite for CASE-A1-RESET; remaining scope assessment must inspect the other incomplete records and all writers. Brian requested urgent gating to prevent recurrence. The proposed initialization barrier and controlled cutover are tracked in the existing audit plan; no field, automation, ingestion job, or production record has been changed to implement it.

The UTC/raw-code diagnostic does not establish the intended cutoff timezone, completeness of manual demotions whose MAIN code differs from the raw code, or downstream Databricks/dashboard propagation after backfill. No data, automation, or sync code was changed by the agent. Changing classification does not authorize automatically marking investigations complete or extending the policy to 27.2.

###### Current trigger
- **Type:** When a record matches conditions.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the current trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Conditions:** BOTH are required; the full trigger card confirms the labels cropped in the selector:
  1. `Triage Process` **is exactly** `Automatic Intended Vehicle Demotion`.
  2. **AND** `Manual Demotion Masking` **is any of** `Manual Mask`, `N/A`.
- Preserve exact-match on this linked-record-valued lookup, not A-35's any-match operator. Empty/distinct/duplicate process values and resolved identity need native-semantics validation.
- This is process-based, not a hardcoded 17.0 rule. There is no direct imported-code, date, machine-type, headlands-completion, Investigation Not Complete, or initialization-ready condition. No-mask is not one of the two allowed masking values.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. It does not continuously enforce the three outputs.

###### Current action
- **Visible structure:** One Update record action; no branches or additional actions shown.
- **Description:** Empty; the current Description editor shows Enter a description.
- **Action will run:** Always, confirmed in the current action panel.
- **Target table:** Demotions_DatabricksSync, confirmed in both action captures.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's convention. Earlier run histories separately corroborate the correct targets for the two August 25 records.
- **Card subtitle:** Confirmed Demotion Type, Operator Error or Misuse and Investigation Complete; the full field panel confirms exactly these three assignments.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice |
| Confirmed Demotion Type | `Intended Vehicle Demotion` | One fixed multiple-select choice shown |
| Investigation Complete | `Investigation Complete` | Fixed single-select choice |

The current action values corroborate the earlier resolved successful action inputs. That does not independently establish that every current trigger setting/version was in effect at each historical event.

###### Dependencies and gating implications
- Triage Process is the schema-confirmed lookup through MAIN Demotion Code to linked Halt Codes process data. MAIN/reference changes can change eligibility; the exact upstream reference producers and trigger propagation still require validation.
- Manual Mask is explicitly accepted. This rule can cover a qualifying manually masked event as well as N/A masking; the imported code need not itself be 17.0. The separate requested 17.0 backfill and its read-only verification above must not be confused with automatic historical replay by this rule.
- A-37 writes ONLY the three listed fields. It does not set Bug or Intended Behavior, JRM links, MAIN, masking, secondary links, reviewer, headlands state, overall triage completion, or scope. Intended Vehicle Demotion does not mean it also assigned Intended Behavior to the separate bug/behavior field.
- **Confirmed reset mechanism for the observed record:** A-37 completed investigation, then A-1 overwrote it to Investigation Not Complete. The current trigger confirms investigation status is not an input; a flag-only reset does not make unchanged process/masking newly match. Do not call this a repeat A-1 trigger, a skipped A-37 run, or proof all incomplete records share the same cause.
- Manual reopening or classification/operator edits alone also do not retrigger A-37 while process/masking remain matched. A new process/masking transition can run the Always action even on an already-completed investigation; no existing-value guard is shown.
- A-34 is disjoint on the settled masking value. A-36 has the same masking choices but a different exact process label, whereas A-35 uses any-match. Preserve these operators and validate mixed/duplicate lookup representations rather than assuming common semantics or global execution precedence.
- Other context-dependent classifiers may require Investigation Not Complete and later-arriving inputs. An earlier completion writer can block their future eligibility, or queued writes can finish after inputs change. No additional cohort/race is established by this configuration capture.
- A-38's current completion logic is captured; A-40's current scope definition is now captured. Actual downstream runs still require validation. Conditional No Operator Error or Misuse coverage here does not prove A-39 redundancy or safe removal.
- The initialization overwrite remains unmitigated while Brian's chosen full-audit-first workflow continues. Preserve both business predicates for the proposed readiness gate; adding an investigation-status guard or changing exact-match is a separate behavior change. No production gate, replay, or correction has been performed by the agent.

###### Remaining identity and validation evidence
Current core configuration capture is complete. Preserve the historical evidence and its limitations above; no more A-37 configuration/run-history screenshots are required at this stage.
1. Immutable automation ID/stable link, full name, current published revision/effective time, historical version correspondence, and process/reference identities.
2. Validate native exact-match semantics, both allowed masking values, new versus already-matching records, output-only edits/reopening, late initialization, reference changes, competing classifiers, unchanged bug/JRM fields, and downstream activities/scope. The other three incomplete records and post-backfill Databricks propagation remain separate unverified items, not implicitly repaired by documentation.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** A recurring UPDATE would reassert outputs on already-matching rows, overwrite some later manual edits, and repair flag resets that the native trigger leaves untouched. Scalar process equality also requires validation against the actual lookup representation. Establish schema, native semantics, and an approved write-precedence/override policy before implementation. Original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET 
  operator_error_or_misuse = 'No Operator Error or Misuse',
  confirmed_demotion_type = 'Intended Vehicle Demotion',
  investigation_complete = 'Investigation Complete'
WHERE triage_process = 'Automatic Intended Vehicle Demotion'
  AND manual_demotion_masking IN ('Manual Mask', 'N/A');
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Triage Process | INPUT | Is exactly Automatic Intended Vehicle Demotion |
| Manual Demotion Masking | INPUT | Is any of Manual Mask, N/A |
| MAIN Demotion Code | INDIRECT INPUT | Schema-confirmed source link for Triage Process |
| Operator Error or Misuse | OUTPUT | Fixed No Operator Error or Misuse |
| Confirmed Demotion Type | OUTPUT | Fixed Intended Vehicle Demotion |
| Investigation Complete | OUTPUT | Fixed Investigation Complete; not a trigger predicate |

---

#### Triage Activities Complete

#### Evidence record A-38: Activities Complete or NOT

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's three screenshots and owner-confirmed trigger-record-ID convention: trigger type/table/view setting, five watched fields, complete If/Otherwise criteria, both action destinations, and both output values.  
**Behavior/migration status:** Full run inputs/outputs, current version correspondence, and ordering are not verified. No test performed by the agent.  
**Identity/context:** A-38 Activities Complete or NOT / Triage Activities Complete in the inventory. Its original captures crop the full header; the later A-40 sidebar corroborates A-38 ON and its group showing 1 active automation. The old 1,976/month note is historical, not a fresh run count. No immutable automation ID/stable link or current published revision/effective time captured. Brian Moffatt is displayed as last updater.

###### Trigger
- **Type:** When a record is updated.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **View:** No view selected; the selector shows Select a view. No view restriction is configured in the displayed panel.
- **Watched fields:** Exactly FIVE selected fields, corroborated by Watching 5 fields:
  1. `Confirmed Demotion Type`
  2. `Investigation Complete`
  3. `Headlands Assessment`
  4. `MAIN Demotion Code`
  5. `Headlands Assessment Complete`
- The UI explicitly says this trigger does NOT include record creation. This is an update trigger, not starts-matching conditions and not an all-fields watcher; the generic help about automatically watching newly created fields when all fields are watched does not describe this five-field selection.
- Triage Activities Complete itself is NOT watched. Neither are Operator Error or Misuse, Bug or Intended Behavior, JRM links, scope, reviewer, the separate Headlands vs Interior/Headlands Turn fields, or a proposed initialization-ready field.

###### Conditional actions
One If group followed by Otherwise, with one Update record action in each. Both target Demotions_DatabricksSync and the trigger's Airtable record ID, confirmed in the two action panels and Brian's convention. Card subtitles identify Triage Activities Complete; Description editors are not shown.

**If ALL FOUR criteria hold:**
1. `Investigation Complete` **is** `Investigation Complete`.
2. **AND** `Headlands Assessment Complete` **is** `Headlands Complete`.
3. **AND** `Confirmed Demotion Type` **has any of**:
   - Intended Manual Demotion
   - Unintended Perception Demotion
   - Unintended Vehicle Demotion
   - Intended Perception Demotion
   - Intended Vehicle Demotion
4. **AND** `MAIN Demotion Code` **length ≠ 0**.

| Branch | Action will run | Sole assignment |
|--------|-----------------|-----------------|
| If | If all four criteria above are met | Triage Activities Complete = Complete |
| Otherwise | If no other conditions are met | Triage Activities Complete = Not Complete |

These are conditional actions, not two Always updates. No outer initialization-ready condition or other action-level guard is shown.

###### Meaning and exact predicate semantics
- This action sets ONLY Triage Activities Complete. It does not complete/reopen investigation, modify headlands status, classify a demotion, set operator/bug/JRM values, or assign scope.
- The type condition is any-match, not exactly one recognized classification or validation of every selected type. Do not replace it with scalar equality or a mere nonempty check. A multi-selection including a listed value can satisfy that criterion without establishing consistency of the whole selection.
- MAIN's condition is linked-list length not equal to zero, not a character-length test or exactly-one-code requirement. It does not exclude a linked N/A placeholder by name or validate the selected code's appropriateness.
- Headlands Assessment is watched but is not itself a branch criterion. The branch reads the Headlands Complete FLAG, not the two breakout fields, reviewer, or certainty of the assessment. Nonempty Not Sure results accepted by A-14 can therefore participate in completion; a later blank assessment or breakout edit is not independently ruled out by this branch's four criteria.
- Misuse/Potential Operator Error, absent JRM links, and scope are not branch checks. Complete here means these four configured criteria passed, not no misuse, in-scope status, all evidence present, or all possible review work finished.

###### Dependencies and gating audit
- A-1 initializes both completion flags and Triage Activities Complete. A-14 sets the headlands-completion input; MAIN writers and classification/investigation writers update the other watched inputs. Their action order can produce multiple evaluations of A-38.
- Unlike the one-way A-14 completion rule, A-38 has a configured Otherwise downgrade. A watched investigation/headlands flag changing to incomplete can cause overall activities to become Not Complete. A-38 reflects that input state; it does not repair the A-1 investigation reset or write the investigation field itself.
- Directly changing only Triage Activities Complete does not trigger A-38; its own output is not watched, avoiding a direct self-trigger from that write. This does not establish absence of indirect loops or guarantee later correction of a manual/stale output value.
- A-31's initial classification update and later investigation-completion branch touch different watched fields in separate actions. They can produce intermediate evaluations; investigate snapshot/current-value handling and ordering of overlapping A-38 runs before assuming the last output represents the latest input state. No A-38 race or stale-write incident is proven here.
- Changes to headlands breakout fields alone are not watched. A-14 also does not continuously reopen its completion flag when they are cleared, so these rules are not a general consistency validator for all headlands data.
- Record creation with prepopulated qualifying fields does not itself fire this update-only trigger. If initialization moves into a create-only ingestion payload, provide an explicit creation/handoff evaluation; merely watching a ready flag already true on insertion would not create a later update event.
- **Deferred initialization gate:** Watch the new readiness field as well as the required inputs so a post-creation ready transition can release evaluation. Gate the ENTIRE If/Otherwise action tree; before readiness means no write, not falling through to Not Complete. A condition added only to the Complete branch would still allow the Otherwise branch to run before initialization. Preserve update-only versus creation behavior and the historical-record cutover plan until changes are approved.
- Initialization gating alone does not serialize later evaluations or prevent stale decisions following concurrent updates. A-40's scope rules and five-field watcher are now captured; investigation/headlands completion flags are watched there but are not scope criteria. Overall triage completion must not be conflated with scope.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-38 screenshots are required at this stage. This is not migration approval.
1. Complete header/name and current run count, immutable automation ID/stable link, optional Descriptions, and published revision/effective time. ON status is now corroborated by the A-40 sidebar capture.
2. Validate updates to each watched field versus output-only/unwatched edits, creation with prepopulated fields, no-op updates, both branches, type-list membership/multiple selections, empty/multiple/N/A MAIN links, Not Sure or stale headlands flags, A-1 resets, A-31 staged updates, overlapping runs, readiness handoff, and preservation of the historical cohort during cutover.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** A recurring table-wide recomputation would evaluate creations/unwatched changes and reassert manually changed outputs differently from this five-field update trigger. Scalar IN and string LENGTH also do not establish equivalence to the multiple-select membership and linked-list length conditions. Validate representations and approve any intentional behavior change before implementation. Original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET triage_activities_complete = CASE
  WHEN investigation_complete = 'Investigation Complete'
    AND headlands_assessment_complete = 'Headlands Complete'
    AND confirmed_demotion_type IN (
      'Intended Manual Demotion',
      'Unintended Perception Demotion',
      'Unintended Vehicle Demotion',
      'Intended Perception Demotion',
      'Intended Vehicle Demotion'
    )
    AND main_demotion_code IS NOT NULL AND LENGTH(main_demotion_code) > 0
  THEN 'Complete'
  ELSE 'Not Complete'
END;
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Confirmed Demotion Type | WATCHED INPUT / CRITERION | Has any of five specified selections |
| Investigation Complete | WATCHED INPUT / CRITERION | Exact Investigation Complete |
| Headlands Assessment | WATCHED INPUT ONLY | Triggers evaluation; not directly tested by the branch |
| MAIN Demotion Code | WATCHED INPUT / CRITERION | Linked-list length not equal to zero |
| Headlands Assessment Complete | WATCHED INPUT / CRITERION | Exact Headlands Complete |
| Triage Activities Complete | OUTPUT ONLY | Complete or Not Complete; not watched by A-38 |

---

#### Misuse Checking

#### Evidence record A-39: Misuse Checking - Create

**Definition status:** CORE CONFIGURATION CAPTURED. Brian's two current screenshots corroborate the saved earlier A-39 UI transcription and confirm the single predicate, Always setting, production table/target token, and sole assignment.  
**Behavior/migration status:** NOT VERIFIED; current configuration does not establish cohort coverage, historical ordering/overwrites, or redundancy. No test performed by the agent.  
**Identity/context:** A-39 Misuse Checking - Create in the inventory. Earlier saved UI evidence records ON and 190 runs this month at that capture; older notes recorded 62. Its direct screenshots crop the full header, but the later A-40 sidebar corroborates A-39 ON and its group showing 1 active automation. There is no fresh A-39 run-count measurement. Brian Moffatt is displayed as last updater. Immutable automation ID/stable link and current published revision/effective time remain uncaptured.  
**Prior evidence:** A-39 section of the owner-held initial UI transcription, identified in [source inventory](../reference/source-inventory.md). The detailed A-39 transcription is retained here. The original file's A-28 section predates the later published policy and is not current A-28 evidence.

###### Trigger
- **Type:** When a record matches conditions, NOT When a record is created. The Create title does not establish a creation-only trigger.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the current trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **Sole condition:** `Misuse Check Required` **is exactly** `NOT Required - Misuse Check`.
- Preserve the full selected value and exact-match operator. This is not merely not Required: Unknown, blank, and Required are not the configured positive value. Native exact-match behavior for duplicate/mixed lookup values still needs validation.
- **Native event semantics shown:** Fires when a record starts matching; excludes already-matching records. An existing record can become newly eligible after source/reference changes; a current match alone does not prove a run or backfill.
- No Operator Error or Misuse is empty check, investigation/headlands completion, masking, MAIN process/code, machine-type, or initialization-ready condition is shown.

###### Action
- **Visible structure:** One Update record action; no branches or additional actions shown.
- **Action will run:** Always, confirmed in the current action panel.
- **Target table:** Demotions_DatabricksSync, confirmed in that panel.
- **Target record source:** Trigger → Airtable record ID, based on the visible token and Brian's global convention. This closes the earlier token-origin evidence gap without another popup.
- **Card subtitle:** Operator Error or Misuse; Description editor is outside the captures.

| Field | Assignment shown | Value source/type |
|-------|------------------|-------------------|
| Operator Error or Misuse | `No Operator Error or Misuse` | Fixed single-select choice; the sole field in the full action capture |

###### Lookup lineage: original linked code, not MAIN
The earlier production schema identifies Misuse Check Required as multipleLookupValues through recordLinkFieldId fld4qfE6tQ7c7l2mG. That ID resolves to Halt Code - Linked, a multipleRecordLinks field targeting Halt Codes (tblN8uu4Gl1eDZMLs). It reads linked field fldn9R876FeC0psJ6, whose result exposes Required - Misuse Check, NOT Required - Misuse Check, and Unknown choices.

This differs from Triage Process, which is looked up through MAIN Demotion Code. Do not substitute MAIN's process/reason for this original linked-code flag, or assume raw import text and its linked reference are always synchronized. Source-link/reference edits can change the lookup and eligibility; their actual timing/trigger propagation needs validation.

###### Default behavior, competing writers, and coverage
- The rule assigns a no-error/no-misuse default based on the lookup policy. It does not independently establish actual operator behavior, and the label Create does not constrain it to the first creation event.
- Always execution plus no empty-output guard means a qualifying action can replace an existing operator selection. It is NOT a verified fill-only-if-empty rule.
- Conversely, changing only the operator output while the lookup stays matched does not retrigger A-39. It is not continuous enforcement that overwrites every manual edit. A lookup transition away/back or an earlier queued action can cause a later assignment; no such overwrite is proven for a particular record by these captures.
- A-30 assigns Potential Operator Error; A-31 has Misuse/Potential branches; A-32 directly assigns Misuse. None of those captured predicates explicitly excludes A-39's required lookup state, and A-39 has no predicate excluding their MAIN/location/detail states. Actual shared eligibility depends on reference mappings and data; test those before declaring a production conflict. The differing output assignments and lack of preservation are confirmed, not a historical race.
- A-26 through A-29, A-33 through A-37, and A-31's Otherwise branch also assign No Operator Error or Misuse under different prerequisites. Those assignments do not automatically replace A-39 coverage: many require MAIN/masking, incomplete investigation, completed headlands, location/details, or other context that A-39 does not require.
- A-39 can be eligible before MAIN is populated or before a context-dependent investigation rule is ready, if the original linked-code lookup already equals the required value. This is a configuration-level possibility, not a measured cohort. Removing it without an explicit replacement/default policy could leave eligible records without the earlier default.
- A-1 does not assign Operator Error or Misuse. A-39 does not write investigation/classification/headlands/activities completion, MAIN/masking, bug/JRM values, reviewer, or scope. It cannot itself complete or repair an investigation.
- A-38 does not watch the operator field and does not use it in its completion criteria. A-40's current five-field watcher includes it, and scope branches distinguish Misuse from populated non-Misuse values. Preserve that confirmed dependency when assessing removal/replacement of A-39; actual cohorts and timing still require validation.
- A generic initialization barrier would not alone settle later competition between this default and final operator decisions. If future design introduces an empty-field guard, a trigger-time check alone is not proof of an atomic action-time protection; establish ordering/ownership or verified write semantics.
- **No retirement decision:** Finish A-40/current inventory verification and evaluate live eligible cohorts, competing writers, manual-review preservation, and timing before removing or replacing A-39. No automation change or deletion is authorized by configuration capture.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-39 screenshots are requested at this stage. This is not migration or retirement approval.
1. Full current header/run count, immutable automation ID/stable link, optional Description, published revision/effective time, and original-code/reference flag provenance. ON status is now corroborated by the A-40 sidebar.
2. Validate blank/Unknown/Required/NOT Required and mixed lookup values, link/reference transitions, already-matching records, populated operator values, manual corrections, queued defaults versus A-30/A-31/A-32, MAIN-not-ready and other classifier-ineligible populations, and A-40 downstream behavior. Reuse saved redundancy-audit evidence only within its recorded scope/version; no new coverage result is claimed here.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** This recurring UPDATE would overwrite manual values on already-matching records, unlike the native condition-entry trigger. The lookup representation and original linked-code lineage also require validation. Define an approved default/override policy and write ordering before implementation. Original SQL retained below.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET operator_error_or_misuse = 'No Operator Error or Misuse'
WHERE misuse_check_required = 'NOT Required - Misuse Check';
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Misuse Check Required | INPUT | Exactly NOT Required - Misuse Check |
| Halt Code - Linked | INDIRECT INPUT | Schema-confirmed source link for Misuse Check Required; not MAIN |
| Operator Error or Misuse | OUTPUT ONLY | Fixed No Operator Error or Misuse; not an empty-field prerequisite |

---

#### In Scope

#### Evidence record A-40: In Scope - Updating

**Definition status:** CORE CONFIGURATION CAPTURED from Brian's four screenshots and owner-confirmed trigger-record-ID convention: update trigger/table/view setting, five watched fields, all three ordered branches, action destinations, and exact output values.  
**Behavior/migration status:** NOT VERIFIED; full run inputs/outputs, current version correspondence, and ordering remain unverified. No test performed by the agent.  
**Displayed name:** A-40 In Scope - Updating  
**Group:** In Scope, shown with 1 active automation.  
**Enabled:** ON in the screenshots  
**Runs:** 4,827 this month displayed; older notes recorded 1,994. These are point-in-time counts, not execution-success or coverage measurements.  
**Identity/version:** No immutable automation ID/stable link or exact published revision/effective time captured. Brian Moffatt is displayed as last updater; no unpublished-change or reconnecting banner is visible.

###### Trigger
- **Type:** When a record is updated; the UI explicitly excludes record creation.
- **Base:** Triage Tool Prototype, previously verified as `app1jXoB1g13R9iOl`.
- **Table:** Demotions_DatabricksSync, confirmed in the trigger panel; previously verified table ID `tblSJItXuuUd0lyHP`.
- **View:** No view selected; the selector shows Select a view.
- **Watched fields:** Exactly FIVE selected fields, confirmed by Watching 5 fields:
  1. `Operator Error or Misuse`
  2. `Investigation Complete`
  3. `Bug or Intended Behavior`
  4. `Headlands vs Interior`
  5. `Headlands Assessment Complete`
- The old two-field watch list omitted the last three. In particular, Headlands vs Interior and Bug or Intended Behavior ARE watched in the current configuration; do not carry forward a missing-watcher diagnosis based on the old list.
- This is not an all-fields watcher. In Scope itself, MAIN, Confirmed Demotion Type, Headlands Assessment, Headlands Turn, JRM links, and a proposed readiness field are not selected here.

###### Ordered conditional actions
The workflow is If / Otherwise if / Otherwise, with one Update record action per branch. All three panels show Demotions_DatabricksSync and the trigger's Airtable record ID. Card subtitles identify In Scope. The first and final branch Description editors are empty; the middle branch's Description editor is outside its capture.

**Branch 1 — If ANY of the following:**
- `Headlands vs Interior` **is any of** `Headlands Pass`, `Not Sure`.
- **OR** `Operator Error or Misuse` **is** `Misuse`.
- **OR** `Bug or Intended Behavior` **is** `Out of Scope`.

**Sole assignment:** `In Scope` = `Outside of Scope`.

**Branch 2 — Otherwise if ALL of the following:**
- `Headlands vs Interior` **is** `Interior Pass`.
- **AND** `Operator Error or Misuse` **is not** `Misuse`.
- **AND** `Operator Error or Misuse` **is not empty**.
- **AND** `Headlands vs Interior` **is not empty**.

**Sole assignment:** `In Scope` = `In Scope`.

**Branch 3 — Otherwise / If no other conditions are met:**

**Sole assignment:** `In Scope` = `Not Yet Determined`.

Each action's Action will run setting matches its branch condition, not Always. No outer initialization-ready guard is shown. Preserve the explicit nonempty checks even where another comparison appears to imply them.

###### Exact scope semantics
- The input choice on Bug or Intended Behavior is Out of Scope, while the output on In Scope is Outside of Scope. These are different literal labels on different fields; the old output transcription Out of Scope was wrong.
- Branch order matters: the outside branch wins even if the second branch's own criteria would otherwise hold. For example, Interior Pass + a populated non-Misuse operator value + Bug or Intended Behavior = Out of Scope produces Outside of Scope, not In Scope.
- Not Sure headlands position is sufficient for Outside of Scope, as is Misuse or the explicit bug/behavior override, without requiring the other fields or completion flags to be populated.
- The in-scope criterion is NOT specifically No Operator Error or Misuse. Any nonempty operator choice other than Misuse, including Potential Operator Error, satisfies that part of the second branch. The first branch must still fail and the position must be Interior Pass.
- Investigation Complete and Headlands Assessment Complete are WATCHED but are not tested in any branch. Scope does not require either assessment/investigation completion; their updates simply cause reevaluation of the position/operator/bug criteria.
- Vehicle/Object Outside Field is not this rule's position input. Do not substitute object-location assessments from A-31/A-32/A-33 for Headlands vs Interior.
- This automation writes ONLY In Scope. It does not classify, complete/reopen an investigation, change operator/bug/headlands values, or set overall activities completion.

###### Dependencies and gating audit
- A-7 through A-13 write the watched headlands position. A-26 through A-37 and A-39 write operator status, with some also writing bug/investigation fields. A-14 writes the watched headlands-completion flag. These inputs can prompt scope reevaluation without requiring a particular classifier to finish first.
- All three actual branch-input fields are watched. The historical concern that headlands/bug-only edits might not trigger A-40 is not supported by the current five-field capture. Other queued-action/snapshot timing questions remain open.
- A-1 is another In Scope writer, assigning Not Yet Determined on creation. Its changes to watched status flags can prompt A-40 to reevaluate. But direct changes to In Scope alone are not watched, so do not assume every late/manual output reset automatically repairs itself.
- The output is not watched, avoiding a direct self-trigger from A-40's own scope assignment. Indirect loops or stale final writes across overlapping runs still require validation; there is no proven A-40 ordering failure here.
- A-30's Potential Operator Error and A-31's potential-error branch can satisfy the non-Misuse condition for Interior Pass, whereas the Misuse values assigned by A-31/A-32 satisfy the first exclusion branch regardless of headlands position. A-39's no-error default can also affect scope before investigation is complete. These are configured implications, not proof of actual runs or dashboard inclusion.
- Record creation does not fire this trigger, even with all inputs/ready flags already populated. Moving defaults into create-only ingestion needs an explicit post-creation handoff/evaluation plan, as for A-38.
- **Deferred readiness gate:** Gate evaluation BEFORE choosing any of the three branches. A not-ready record must cause no write, not the final Not Yet Determined fallback. If a ready transition is used to release an update-triggered workflow, it must be watched and occur after creation; simply adding it to the first branch or one OR alternative is insufficient. Validate the supported trigger/view/action design before rollout, including existing-record and in-flight cohorts.
- Initialization gating alone does not serialize later scope evaluations or establish current-versus-trigger-snapshot reads. Investigation/headlands completion requirements, Potential Operator Error treatment, direct scope override behavior, or branch precedence changes would be separate policy changes. No gate has been implemented.

###### Remaining identity and validation evidence
Core configuration capture is complete; no more A-40 screenshots are required at this stage. This is not migration approval or proof the entire base inventory is covered.
1. Immutable automation ID/stable link, current published revision/effective time, optional middle-branch Description, and reference/choice identity validation.
2. Validate all three branches and precedence conflicts, blank/Not Sure/Interior/Headlands position, Misuse/Potential/no-error operator values, the two distinct scope literals, watched flag-only updates, output-only edits, prepopulated creation, no-op updates, A-1 resets, overlapping runs, readiness handoff, and downstream reporting.
3. The subsequent sidebar capture identifies three additional OFF entries under Triage Protocols/Triage Investigations, recorded in Additional Disabled Automation Inventory. Their names/statuses are reconciled, but internal definitions and historical effects are not yet reviewed; do not call them deleted or proven obsolete.

###### Databricks Equivalent

**Historical sketch only — not an approved event-equivalent implementation:** The legacy SQL below writes Out of Scope, but the captured target-field choice is Outside of Scope. Its input comparison to Bug or Intended Behavior = Out of Scope is a separate correct literal. The sketch is retained unchanged, including original comments, to distinguish historical material from the current specification. A recurring UPDATE also differs from the five-field update-only trigger and can overwrite manual outputs or process creations/unwatched edits. Validate representations, branch priority, and approved trigger/override behavior before implementing a corrected replacement.
```sql
UPDATE jupiter_prod.jfa_metrics.demotion_context
SET in_scope = CASE
  -- Out of Scope: Headlands, Not Sure, Misuse, or explicitly Out of Scope
  WHEN headlands_vs_interior IN ('Headlands Pass', 'Not Sure')
    OR operator_error_or_misuse = 'Misuse'
    OR bug_or_intended_behavior = 'Out of Scope'
  THEN 'Out of Scope'
  
  -- In Scope: Interior Pass with no misuse and fields populated
  WHEN headlands_vs_interior = 'Interior Pass'
    AND operator_error_or_misuse != 'Misuse'
    AND operator_error_or_misuse IS NOT NULL AND LENGTH(operator_error_or_misuse) > 0
    AND headlands_vs_interior IS NOT NULL AND LENGTH(headlands_vs_interior) > 0
  THEN 'In Scope'
  
  -- Otherwise: Not Yet Determined
  ELSE 'Not Yet Determined'
END;
```

###### Columns Used
| Airtable Column | Direction | Evidence |
|-----------------|-----------|----------|
| Operator Error or Misuse | WATCHED INPUT / CRITERION | Misuse exclusion; non-Misuse and nonempty inclusion |
| Investigation Complete | WATCHED INPUT ONLY | Prompts reevaluation; not a branch prerequisite |
| Bug or Intended Behavior | WATCHED INPUT / CRITERION | Exact Out of Scope forces first branch |
| Headlands vs Interior | WATCHED INPUT / CRITERION | Headlands Pass/Not Sure exclusion; Interior Pass inclusion |
| Headlands Assessment Complete | WATCHED INPUT ONLY | Prompts reevaluation; not a branch prerequisite |
| In Scope | OUTPUT ONLY | Outside of Scope, In Scope, or Not Yet Determined; not watched |

---

#### Additional Disabled Automation Inventory

Brian's supplemental sidebar screenshot and explicit statement that these are all off identify the following additional entries. This reconciles the previously uninspected visible groups; it does not capture their internal definitions or historical execution.

| Group | Displayed automation name | Status | Configuration evidence |
|-------|---------------------------|--------|------------------------|
| Triage Protocols | TP-1 Headlands Assessment | OFF | Sidebar name/status and matches-conditions trigger summary; full settings not inspected |
| Triage Investigations | JRM-476 | OFF | Sidebar name/status and matches-conditions trigger summary; full settings not inspected |
| Triage Investigations | JRM-446 - Bug Assignment | OFF | Sidebar name/status and matches-conditions trigger summary; full settings not inspected |

These are retained as disabled entries, not deleted or proven obsolete. No active-rule gate changes are planned for them while they remain off. Their full definitions, historical/in-flight execution, and dependencies must be reviewed before reactivation, migration, or a retirement decision; OFF alone establishes none of those conclusions.

JRM-446 - Bug Assignment being off does not disable the JRM-446 reference or A-33's separately captured assignment of that reference. Do not conflate an automation named after an issue with the linked issue record or every rule that uses it. TP-1 is likewise not assumed identical to the differently named protocols in the old obsolete notes.

#### Summary: Captured A-1 through A-40 Field Dependencies

All forty numbered entries now have displayed core trigger/action configurations captured, with the individual evidence caveats retained. The additional visible groups are reconciled above as three owner-confirmed OFF entries: 43 identified automations in the supplied inventory, with full displayed settings captured for A-1 through A-40 and status-only evidence for the three disabled entries. This is UI/owner evidence, not an independently exhaustive automation API export. Disabled-rule definitions, runtime semantics, data-path/reference resolution, published identity/version gaps, and post-incident checks remain separate open work.

The following map covers only the captured A-1 through A-40 configurations. It does not include every manual edit, API/import writer, linked-reference update, interface, Databricks/reporting consumer, or unlisted automation. None shown is NOT permission to delete a column or remove a rule. Per-rule predicates and action details remain authoritative.

##### Fields written by captured automations
| Field | Captured writers | Captured readers/watchers or indirect dependencies |
|-------|------------------|---------------------------------------------------|
| Headlands Assessment Complete | A-1: Headlands Not Complete; A-14: Headlands Complete | A-2–A-6, A-28, A-38; A-40 watches only |
| Investigation Complete | A-1: Investigation Not Complete; A-26–A-37: Investigation Complete | A-26–A-33, A-38; A-40 watches only. NOT a prerequisite for A-34–A-37 |
| Triage Activities Complete | A-1: Not Complete; A-38: Complete/Not Complete | No direct reader shown among A-1–A-40; A-38 does not watch its own output |
| In Scope | A-1: Not Yet Determined; A-40: three-way scope result | No direct reader shown among A-1–A-40; A-40 does not watch its own output |
| Headlands Assessment | A-2–A-6 | A-7–A-13; A-38 watches only |
| Headlands Reviewer | A-2–A-6: Automatic linked reference | No direct reader shown among A-1–A-40 |
| Headlands vs Interior | A-7–A-13 | A-14; A-28 branch input; A-40 watches and tests |
| Headlands Turn | A-7–A-13 | A-14 |
| Secondary Demotion Manual | A-15: preceding-code Names; A-18: N/A name | A-15/A-16/A-19–A-25; also supplies Secondary Demotion Reason, including A-17's indirect dependency |
| MAIN Demotion Code | A-16–A-25 | A-28–A-33; A-38 watches/tests list length; indirectly supplies MAIN Demotion Reason and Triage Process for A-34–A-37 |
| Manual Demotion Masking | A-16–A-25 | A-34–A-37 |
| Confirmed Demotion Type | A-26–A-37 | A-38 watches and tests membership |
| Operator Error or Misuse | A-26–A-37, A-39 | A-40 watches and tests; NOT watched/tested by A-38 |
| Bug or Intended Behavior | A-26–A-33 | A-40 watches and tests |
| Confirmed JRM Link | A-27: JRM-613; A-29: JRM-548; A-33: JRM-446 | No direct reader shown among A-1–A-40; external/reference consumers not assessed by this table |

##### Inputs without a captured direct writer in A-1 through A-40
| Input | Captured use |
|-------|--------------|
| Implement Path Position Type Text | A-2–A-6 |
| Computed Implement Path Position Type Text | A-5/A-6 |
| Preceding Stop Code | A-15 trigger and dynamic source |
| Halt Code - Import | A-16–A-18 dynamic sources; A-26/A-27 trigger predicates |
| Halt Code - Linked | Indirect source of Demotion Reason and Misuse Check Required in reviewed schema |
| Demotion Reason | A-15–A-25 |
| Secondary Demotion Reason | A-17/A-22–A-25; lookup through Secondary Demotion Manual |
| MAIN Demotion Reason | A-34; MAIN-linked lookup |
| Triage Process | A-35–A-37; MAIN-linked lookup |
| Misuse Check Required | A-39; original Halt Code - Linked lookup, not MAIN |
| Vehicle/Object Outside Field | A-31–A-33 |
| NonNavigable Object Misuse Details | A-31 prerequisite and branches |
| MAIN_SparkURL_Manual | A-29 contains missing; stored URL field in reviewed schema |

Producer timing/reference resolution for these inputs is not established merely by configuration capture. This matters for initialization and later-readiness ordering.

##### Open gates after numbered configuration capture
- The visible additional groups are now reconciled as TP-1 Headlands Assessment, JRM-476, and JRM-446 - Bug Assignment, all OFF. Preserve their disabled state; full definitions remain unreviewed and must be accounted for before reactivation/migration/retirement. No further screenshots are requested merely to re-confirm their OFF status.
- Resolve current published identity/version and connection-related caveats, notably A-12's unrevisited settings and A-31's initial connection notice, without requesting unnecessary duplicate captures.
- Validate dynamic source-step/data representations for A-16–A-18 and A-22/A-23; distinguish editor display settings from data projections and verify linked name/ID/cardinality behavior.
- Validate exact versus any/none lookup predicates, input/branch snapshots, record-created versus record-updated handoffs, repeated/late writes, and actual populations for the documented conditional overlaps. Configuration-level possibilities are not observed incidents.
- Evaluate A-39 coverage/replacement with original linked-code lineage, other classifier prerequisites, manual decisions, and the now-captured A-40 scope dependency. No retirement decision is made.
- Keep the confirmed A-1 initialization overwrite, other unexplained incomplete records, and post-backfill Databricks propagation checks separate from documentation completeness.
- Obtain explicit rollout/cutover and correction approval before adding gates, pausing ingestion, changing triggers/branches, replaying records, or applying historical repairs. No production remediation has been performed.
