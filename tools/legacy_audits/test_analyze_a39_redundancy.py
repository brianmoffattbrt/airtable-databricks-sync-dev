import unittest

from analyze_a39_redundancy import (
    UNKNOWN_VALUE, Rule, evaluate_condition, evaluate_state, trigger_eligibility,
    documented_rules, build_coverage_matrix, render_decision, dependency_closure,
    normalize_state, explore_finite_model, compare_observation_sets, check_source_snapshot,
)


class A39Tests(unittest.TestCase):
    def leaf(self, op, value=None):
        return {"field": "x", "op": op, "value": value}

    def test_exact_singleton_does_not_flatten_mixed_values(self):
        c = self.leaf("singleton_exact", "NOT Required - Misuse Check")
        self.assertTrue(evaluate_condition(c, {"x": ["NOT Required - Misuse Check"]}))
        self.assertFalse(evaluate_condition(c, {"x": []}))
        self.assertIsNone(evaluate_condition(c, {"x": ["NOT Required - Misuse Check"] * 2}))
        self.assertIsNone(evaluate_condition(c, {"x": ["Required - Misuse Check", "NOT Required - Misuse Check"]}))
        self.assertIsNone(evaluate_condition(c, {}))

    def test_unknown_operator_is_unknown(self):
        self.assertIsNone(evaluate_condition(self.leaf("unsupported"), {"x": 1}))

    def test_three_valued_groups(self):
        false = self.leaf("eq", "yes")
        unknown = {"field": "missing", "op": "eq", "value": 1}
        self.assertFalse(evaluate_condition({"all": [false, unknown]}, {"x": "no"}))
        self.assertIsNone(evaluate_condition({"any": [false, unknown]}, {"x": "no"}))
        self.assertTrue(evaluate_condition({"any": [false, unknown]}, {"x": "yes"}))
        self.assertIsNone(evaluate_condition({"all": []}, {}))

    def test_different_types_not_coerced(self):
        self.assertIsNone(evaluate_condition(self.leaf("eq", "N/A"), {"x": ["N/A"]}))
        self.assertIsNone(evaluate_condition(self.leaf("any_of", ["N/A"]), {"x": "N/A"}))
        self.assertFalse(evaluate_condition(self.leaf("eq", "12.2"), {"x": "12.20"}))

    def test_requested_empty_vs_missing(self):
        self.assertTrue(evaluate_condition(self.leaf("empty"), {"x": None}))
        self.assertIsNone(evaluate_condition(self.leaf("empty"), {}))

    def test_true_predicate_is_not_a_trigger(self):
        rule = Rule("r", self.leaf("eq", "yes"), "value", enabled=True, verified=True)
        state = {"x": "yes"}
        self.assertFalse(trigger_eligibility(rule, state, state, calibrated=True))
        self.assertTrue(trigger_eligibility(rule, {"x": "no"}, state, calibrated=True))
        self.assertIsNone(trigger_eligibility(rule, None, state, calibrated=True))
        self.assertIsNone(trigger_eligibility(rule, {"x": "no"}, state, calibrated=False))

    def test_disabled_writer_not_eligible(self):
        rule = Rule("r", self.leaf("eq", "yes"), "value", enabled=False, verified=True)
        self.assertFalse(trigger_eligibility(rule, {}, {"x": "yes"}, calibrated=True))

    def test_unverified_rule_never_execution_proof(self):
        rule = Rule("r", self.leaf("eq", "yes"), "value", enabled=True)
        self.assertIsNone(trigger_eligibility(rule, {"x": "no"}, {"x": "yes"}, calibrated=True))

    def test_primary_flag_not_replaced_by_main_flag(self):
        state = {"misuse_required": ["NOT Required - Misuse Check"], "main_code": ["3.1"], "masking": None,
                 "main_reason": [], "triage_process": [], "import_code": "17.0", "headlands": None,
                 "spark_url": None, "outside_field": None, "nonnavigable_details": None}
        result = evaluate_state(state, documented_rules())
        self.assertTrue(result["A-39"]["predicate"])
        self.assertFalse(result["A-34"]["predicate"])
        self.assertFalse(result["A-36"]["predicate"])
        self.assertIsNone(result["A-39"]["execution_eligibility"])

    def test_same_label_with_existing_value_not_attributed(self):
        state = {"misuse_required": ["NOT Required - Misuse Check"], "operator": "No Operator Error or Misuse"}
        matrix = build_coverage_matrix([{"record_id": "a", "state": state}], documented_rules())
        self.assertEqual(matrix[0]["writer_attribution"], "UNKNOWN")

    def test_no_gaps_never_implies_redundant(self):
        self.assertEqual(render_decision([], []) ["automation_verdict"], "UNKNOWN / KEEP")

    def test_unknown_reference_not_empty_lookup(self):
        raw = {"id": "a", "fields": {"MAIN Demotion Code": ["missing"]}}
        state = normalize_state(raw, {}, {}, {}, {"MAIN Demotion Code"})
        self.assertIs(state["main_code"], UNKNOWN_VALUE)
        self.assertIs(state["misuse_required"], UNKNOWN_VALUE)

    def test_producer_and_consumers_distinguished(self):
        tables = [{"id": "t", "fields": [
            {"id": "source", "name": "Source", "type": "singleSelect"},
            {"id": "lookup", "name": "Lookup", "type": "multipleLookupValues", "options": {"fieldIdInLinkedTable": "source"}},
            {"id": "consumer", "name": "Consumer", "type": "formula", "options": {"referencedFieldIds": ["lookup"]}},
        ]}]
        closure = dependency_closure(tables, "lookup")
        self.assertEqual(closure["consumers"], ["consumer"])
        self.assertEqual(closure["producers"], ["source"])

    def test_finite_exploration_reports_limit(self):
        model = explore_finite_model([0], lambda n: [n + 1], max_states=5)
        self.assertFalse(model["complete"])
        self.assertEqual(model["verdict"], "UNKNOWN")

    def test_cycle_exploration_terminates_without_hiding_state(self):
        model = explore_finite_model([0], lambda n: [(n + 1) % 3], max_states=5)
        self.assertTrue(model["complete"])
        self.assertEqual(len(model["states"]), 3)

    def test_equal_final_values_do_not_hide_trace_difference(self):
        result = compare_observation_sets([[None, "No Error"]], [["No Error", "No Error"]], complete=True)
        self.assertEqual(result["result"], "MODEL_DIFFERENCE")
        self.assertEqual(compare_observation_sets([[1]], [[1]], complete=False)["result"], "UNKNOWN")

    def test_a28_requires_investigation_not_complete(self):
        rule = next(r for r in documented_rules() if r.name == "A-28-headlands")
        state = {"main_code": ["12.35"], "headlands": "Headlands Pass", "headlands_complete": "Headlands Complete", "investigation": "Investigation Complete"}
        self.assertFalse(evaluate_condition(rule.condition, state))
        state["investigation"] = "Investigation Not Complete"
        self.assertTrue(evaluate_condition(rule.condition, state))
        state["investigation"] = None
        self.assertFalse(evaluate_condition(rule.condition, state))

    def test_a28_waits_for_headlands_completion(self):
        rules = [r for r in documented_rules() if r.name.startswith("A-28-")]
        for completion in [None, "Headlands Unknown", "Headlands Not Complete"]:
            for headlands in ["Headlands Pass", "Interior Pass", "Not Sure", None]:
                state = {"main_code": ["12.35"], "headlands": headlands, "headlands_complete": completion,
                         "investigation": "Investigation Not Complete"}
                self.assertTrue(all(evaluate_condition(r.condition, state) is False for r in rules))

    def test_a28_completed_not_sure_blank_or_new_value_uses_fallback(self):
        fallback = next(r for r in documented_rules() if r.name == "A-28-otherwise")
        headlands_rule = next(r for r in documented_rules() if r.name == "A-28-headlands")
        for headlands in ["Interior Pass", "Not Sure", None, "Future Position"]:
            state = {"main_code": ["12.35"], "headlands": headlands, "headlands_complete": "Headlands Complete",
                     "investigation": "Investigation Not Complete"}
            self.assertIs(evaluate_condition(fallback.condition, state), True)
            self.assertIs(evaluate_condition(headlands_rule.condition, state), False)
        state["headlands"] = "Headlands Pass"
        self.assertIs(evaluate_condition(fallback.condition, state), False)
        self.assertIs(evaluate_condition(headlands_rule.condition, state), True)

    def test_a28_completion_transition_enters_trigger(self):
        rule = next(r for r in documented_rules() if r.name == "A-28-otherwise")
        previous = {"main_code": ["12.35"], "headlands": "Not Sure", "headlands_complete": "Headlands Unknown",
                    "investigation": "Investigation Not Complete"}
        current = {**previous, "headlands_complete": "Headlands Complete"}
        self.assertIs(trigger_eligibility(rule, previous, current, calibrated=True), True)

    def test_a28_branch_change_is_not_trigger_transition(self):
        rule = next(r for r in documented_rules() if r.name == "A-28-otherwise")
        previous = {"main_code": ["12.35"], "headlands": "Not Sure", "headlands_complete": "Headlands Complete",
                    "investigation": "Investigation Not Complete"}
        current = {**previous, "headlands": "Interior Pass"}
        self.assertTrue(evaluate_condition(rule.condition, current))
        self.assertIs(trigger_eligibility(rule, previous, current, calibrated=True), False)

    def test_a39_ui_definition_has_no_existing_assessment_guard(self):
        rule = next(r for r in documented_rules() if r.name == "A-39")
        state = {"misuse_required": ["NOT Required - Misuse Check"], "operator": "Misuse"}
        self.assertTrue(evaluate_condition(rule.condition, state))
        self.assertTrue(rule.enabled)
        self.assertTrue(rule.verified)

    def test_source_flag_and_identity_drift(self):
        record = {"id": "a", "fields": {"A_UID": "uid", "Halt Code - Linked": ["halt"], "Misuse Check Required": ["NOT Required - Misuse Check"]}}
        halts = [{"id": "halt", "fields": {"Misuse Check Required": "NOT Required - Misuse Check"}}]
        result = check_source_snapshot([record], halts, [{"id": "a", "fields": {"A_UID": "uid"}}])
        self.assertEqual(result["source_lookup_issues"], [])
        self.assertEqual(result["repeat_identity_status"], "MATCH")
        halts[0]["fields"]["Misuse Check Required"] = "Required - Misuse Check"
        result = check_source_snapshot([record], halts, [{"id": "a", "fields": {"A_UID": "changed"}}])
        self.assertEqual(len(result["source_lookup_issues"]), 1)
        self.assertEqual(result["changed_uid_ids"], ["a"])
        self.assertEqual(result["repeat_identity_status"], "DRIFT")

    def test_conflict_not_counted_as_same_value(self):
        rules = [Rule("A-39", {"field": "flag", "op": "eq", "value": True}, "No Operator Error or Misuse"),
                 Rule("conflict", {"field": "flag", "op": "eq", "value": True}, "Misuse")]
        row = build_coverage_matrix([{"record_id": "a", "state": {"flag": True}}], rules)[0]
        self.assertEqual(row["same_value_candidates"], [])
        self.assertEqual(row["conflicting_candidates"], ["conflict"])


if __name__ == "__main__":
    unittest.main()
