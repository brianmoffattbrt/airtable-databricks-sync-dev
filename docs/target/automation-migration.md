# Automation Migration Map

**Status: implementation/design roadmap, not deployed code.** The [captured as-is specification](../as-is/automations.md) remains authoritative for source settings. Root sync notebooks are legacy integrations, and the offline audit utilities are not a complete/native-calibrated forty-rule engine.

All forty rules have an explicit place in the replacement scope. Grouping below is a proposed code responsibility, not forty scheduled jobs, scheduler priority, or an approved behavioral change.

| Rule | Captured definition | Proposed responsibility | Implementation status |
|---|---|---|---|
| A-1 | [Baseline](../as-is/automations.md#a-1) | Initialization/default ownership | Design pending; late overwrite must be addressed explicitly |
| A-2 | [Baseline](../as-is/automations.md#a-2) | Headlands primary assessment | Not implemented |
| A-3 | [Baseline](../as-is/automations.md#a-3) | Headlands primary assessment | Not implemented |
| A-4 | [Baseline](../as-is/automations.md#a-4) | Headlands primary assessment | Not implemented |
| A-5 | [Baseline](../as-is/automations.md#a-5) | Computed headlands fallback | Not implemented |
| A-6 | [Baseline](../as-is/automations.md#a-6) | Computed unknown-turn fallback | Not implemented |
| A-7 | [Baseline](../as-is/automations.md#a-7) | Headlands breakout | Not implemented |
| A-8 | [Baseline](../as-is/automations.md#a-8) | Headlands breakout | Not implemented |
| A-9 | [Baseline](../as-is/automations.md#a-9) | Headlands breakout | Not implemented |
| A-10 | [Baseline](../as-is/automations.md#a-10) | Headlands breakout | Not implemented |
| A-11 | [Baseline](../as-is/automations.md#a-11) | Headlands breakout | Not implemented |
| A-12 | [Baseline](../as-is/automations.md#a-12) | Explicit uncertain assessment breakout | Not implemented |
| A-13 | [Baseline](../as-is/automations.md#a-13) | Unknown-turn breakout | Not implemented |
| A-14 | [Baseline](../as-is/automations.md#a-14) | Headlands completion | Not implemented |
| A-15 | [Baseline](../as-is/automations.md#a-15) | Secondary-code initialization | Not implemented |
| A-16 | [Baseline](../as-is/automations.md#a-16) | MAIN/masking resolution | Not implemented |
| A-17 | [Baseline](../as-is/automations.md#a-17) | MAIN/masking resolution | Not implemented |
| A-18 | [Baseline](../as-is/automations.md#a-18) | MAIN/masking resolution | Not implemented |
| A-19 | [Baseline](../as-is/automations.md#a-19) | MAIN/masking resolution | Not implemented |
| A-20 | [Baseline](../as-is/automations.md#a-20) | MAIN/masking resolution | Not implemented |
| A-21 | [Baseline](../as-is/automations.md#a-21) | MAIN/masking resolution | Not implemented |
| A-22 | [Baseline](../as-is/automations.md#a-22) | MAIN/masking resolution | Not implemented |
| A-23 | [Baseline](../as-is/automations.md#a-23) | MAIN/masking resolution | Not implemented |
| A-24 | [Baseline](../as-is/automations.md#a-24) | Literal X1 resolution | Not implemented |
| A-25 | [Baseline](../as-is/automations.md#a-25) | Literal X2 resolution | Not implemented |
| A-26 | [Baseline](../as-is/automations.md#a-26) | Imported-code classification | Not implemented |
| A-27 | [Baseline](../as-is/automations.md#a-27) | Imported-code classification/JRM | Not implemented |
| A-28 | [Baseline](../as-is/automations.md#a-28) | Headlands-conditioned classification | Not implemented |
| A-29 | [Baseline](../as-is/automations.md#a-29) | Missing-Spark classification/JRM | Not implemented |
| A-30 | [Baseline](../as-is/automations.md#a-30) | X1/X2 classification | Not implemented |
| A-31 | [Baseline](../as-is/automations.md#a-31) | Non-navigable classification/misuse | Not implemented |
| A-32 | [Baseline](../as-is/automations.md#a-32) | Inside-field classification | Not implemented |
| A-33 | [Baseline](../as-is/automations.md#a-33) | Outside/potential/interior-obstacle classification/JRM | Not implemented |
| A-34 | [Baseline](../as-is/automations.md#a-34) | MAIN-reason classification | Not implemented |
| A-35 | [Baseline](../as-is/automations.md#a-35) | Process-driven classification | Not implemented |
| A-36 | [Baseline](../as-is/automations.md#a-36) | Process-driven classification | Not implemented |
| A-37 | [Baseline](../as-is/automations.md#a-37) | Process-driven classification | Not implemented |
| A-38 | [Baseline](../as-is/automations.md#a-38) | Overall completion | Not implemented |
| A-39 | [Baseline](../as-is/automations.md#a-39) | Original-code misuse default | Retain in scope; retirement undecided |
| A-40 | [Baseline](../as-is/automations.md#a-40) | Scope classification | Not implemented |

## Required target decisions

- Event identity and create/update/condition-entry detection, including already-matching rows and watched-field changes.
- Native collection/null/missing/N/A/Not Sure behavior and name/link conversion. Keep raw imported code, MAIN, and secondary codes distinct and preserve string codes such as 12.110 and 12.X1.
- DBX-owned reference catalogs and actor/issue identities. Airtable IDs may remain baseline provenance, not a permanent runtime dependency.
- Initialization, input readiness, manual override protection, and precedence for competing writers. Do not silently implement a guessed numeric A-order.
- How A-31's two configured updates map to target atomicity and downstream observations.
- Manual-result revisions and corrections through the [app contract](platform-app-contract.md), including the response to edits after investigation completion.
- A-39 retention/replacement, explicitly separate from documentation completeness.
- Reference/bootstrap/data migration and downstream reporting compatibility, with separate approvals for writes/cutover.

The platform contract's explicit Spark-selection status is a proposed target representation. It is not an already approved substitution for A-29's native contains-missing test. Likewise, a new enum spelling or generic periodic recomputation is an intentional difference requiring a decision, not a transcription correction.

## Implementation growth

Use `src/triage_workflows/` for pure rules and orchestration, `sql/` for approved data definitions/migrations, `resources/` for the agreed deployment format, and `tests/` for synthetic rule/contract/integration checks. These locations are not scaffolded with fake code now. Do not import the Mesa deployment pipeline or run legacy sync as the new engine.

A future implemented row must link its actual code, relevant tests, approved differences, and deployment status. Shadow/parity testing is appropriate when code exists; it is not a prerequisite to preserving the captured documentation in Git. See [decisions](../decisions.md) and the [project roadmap](../../README.md#growth-path).
