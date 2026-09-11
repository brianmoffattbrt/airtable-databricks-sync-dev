import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path

from audit_halt_code_incident import AuditError, EvidenceStore, extract_records, load_payload, now, schema_tables


UNKNOWN_VALUE = object()
NO_ERROR = "No Operator Error or Misuse"
NOT_REQUIRED = "NOT Required - Misuse Check"
PRODUCTION_TABLE = "tblSJItXuuUd0lyHP"
LOOKUP_FIELD = "fldOHbYtRj47uED0u"
SOURCE_FIELD = "fldn9R876FeC0psJ6"
REQUESTED_FIELDS = [
    "A_UID", "Timestamp UTC", "VIN", "VIN_machine_type", "Halt Code - Import", "Halt Code - Linked",
    "MAIN Demotion Code", "Demotion Reason", "MAIN Demotion Reason", "Secondary Demotion Manual",
    "Secondary Demotion Reason", "Preceding Stop Code", "Manual Demotion Masking", "Misuse Check Required",
    "Triage Process", "Operator Error or Misuse", "Confirmed Demotion Type", "Investigation Complete",
    "Triage Activities Complete", "In Scope", "Headlands vs Interior", "Vehicle/Object Outside Field",
    "NonNavigable Object Misuse Details", "MAIN_SparkURL_Manual", "Bug or Intended Behavior", "Headlands Assessment Complete",
]


@dataclass(frozen=True)
class Rule:
    name: str
    condition: dict
    value: str
    enabled: bool | None = None
    verified: bool = False
    trigger: str = "matches_conditions"
    source: str = "DOCUMENTATION_ONLY"
    trigger_condition: dict | None = None


def evaluate_condition(condition, state):
    for group in ("all", "any"):
        if group in condition:
            children = condition[group]
            if not isinstance(children, list) or not children:
                return None
            values = [evaluate_condition(child, state) for child in children]
            if group == "all":
                return False if False in values else None if None in values else True
            return True if True in values else None if None in values else False
    if "not" in condition:
        value = evaluate_condition(condition["not"], state)
        return None if value is None else not value
    actual = state.get(condition.get("field"), UNKNOWN_VALUE)
    if actual is UNKNOWN_VALUE:
        return None
    op, expected = condition.get("op"), condition.get("value")
    if op == "empty":
        return actual is None or actual == "" or actual == []
    if op == "not_empty":
        return not (actual is None or actual == "" or actual == [])
    if op in ("eq", "in", "not_in"):
        if isinstance(actual, (list, dict)):
            return None
        if op == "eq":
            return actual == expected
        if not isinstance(expected, list):
            return None
        return (actual in expected) if op == "in" else (actual not in expected)
    if op in ("any_of", "none_of"):
        if actual is None:
            actual = []
        if not isinstance(actual, list) or not isinstance(expected, list):
            return None
        matched = any(value in expected for value in actual)
        return matched if op == "any_of" else not matched
    if op == "singleton_exact":
        if actual is None or actual == []:
            return False
        if not isinstance(actual, list) or len(actual) != 1:
            return None
        return actual[0] == expected
    if op == "contains_ci":
        return False if actual is None else expected.lower() in actual.lower() if isinstance(actual, str) else None
    return None


def trigger_eligibility(rule, previous, current, calibrated=False):
    if rule.verified and rule.enabled is False:
        return False
    if not rule.verified or rule.enabled is not True or not calibrated or previous is None or rule.trigger != "matches_conditions":
        return None
    condition = rule.trigger_condition if rule.trigger_condition is not None else rule.condition
    before, after = evaluate_condition(condition, previous), evaluate_condition(condition, current)
    if after is False or before is True:
        return False
    if after is True and before is False:
        return True
    return None


def documented_rules():
    def leaf(field, op, value=None):
        return {"field": field, "op": op, "value": value}
    def both(*conditions):
        return {"all": list(conditions)}
    def rule(name, condition, value=NO_ERROR):
        return Rule(name, condition, value)
    mask = leaf("masking", "in", ["Manual Mask", "N/A"])
    dr3 = leaf("main_code", "any_of", ["12.29"])
    inside = leaf("outside_field", "eq", "Inside Field (OBVIOUS)")
    details = leaf("nonnavigable_details", "not_empty")
    a28_trigger = both(leaf("main_code", "any_of", ["12.35"]), leaf("investigation", "eq", "Investigation Not Complete"),
                       leaf("headlands_complete", "eq", "Headlands Complete"))
    return [
        Rule("A-39", leaf("misuse_required", "singleton_exact", NOT_REQUIRED), NO_ERROR,
             enabled=True, verified=True, source="USER_UI_SCREENSHOTS_A39_TRIGGER_ACTION"),
        rule("A-34", both(leaf("masking", "eq", "Intended Manual Demotion - No Mask"),
                          leaf("main_reason", "any_of", ["DR-1 In-Cab Controls Override", "DR-2 Human-Triggered Demotion"]))),
        rule("A-35", both(leaf("triage_process", "any_of", ["Automatic Unintended Perception Demotion"]), mask)),
        rule("A-36", both(leaf("triage_process", "singleton_exact", "Automatic Non-Perception Demotion"), mask)),
        rule("A-37", both(leaf("triage_process", "singleton_exact", "Automatic Intended Vehicle Demotion"), mask)),
        rule("A-26", leaf("import_code", "in", ["12.15", "12.110", "12.111", "12.112", "12.113", "12.101"])),
        rule("A-27", leaf("import_code", "in", ["12.20", "12.21"])),
        Rule("A-28-headlands", both(a28_trigger, leaf("headlands", "eq", "Headlands Pass")), NO_ERROR,
             enabled=True, verified=True, source="USER_SCREENSHOTS_AND_PUBLISH_CONFIRMATION_A28_V2", trigger_condition=a28_trigger),
        Rule("A-28-otherwise", both(a28_trigger, {"not": leaf("headlands", "eq", "Headlands Pass")}), NO_ERROR,
             enabled=True, verified=True, source="USER_SCREENSHOTS_AND_PUBLISH_CONFIRMATION_A28_V2", trigger_condition=a28_trigger),
        rule("A-29", both(leaf("main_code", "any_of", ["12.15", "12.101", "12.110", "12.111", "12.112", "12.113"]),
                          leaf("spark_url", "contains_ci", "missing"))),
        rule("A-30", leaf("main_code", "any_of", ["12.X1", "12.X2"]), "Potential Operator Error"),
        rule("A-31-default", both(dr3, inside, details, leaf("nonnavigable_details", "not_in", [
            "Movable UNMAPPED Object - Misuse", "Stationary Object/Equipment - Potential Error"]))),
        rule("A-31-misuse", both(dr3, inside, leaf("nonnavigable_details", "eq", "Movable UNMAPPED Object - Misuse")), "Misuse"),
        rule("A-31-potential", both(dr3, inside, leaf("nonnavigable_details", "eq", "Stationary Object/Equipment - Potential Error")), "Potential Operator Error"),
        rule("A-32", both(leaf("main_code", "any_of", ["12.24", "12.27"]), inside), "Misuse"),
    ]


def normalize_state(record, halt_labels, reason_labels, process_labels, requested):
    fields = record["fields"]
    def raw(name, array=False):
        if name not in requested:
            return UNKNOWN_VALUE
        return fields.get(name, [] if array else None)
    def linked(name, labels):
        values = raw(name, True)
        if values is UNKNOWN_VALUE or not isinstance(values, list) or any(value not in labels for value in values):
            return UNKNOWN_VALUE
        return [labels[value] for value in values]
    return {
        "misuse_required": raw("Misuse Check Required", True), "import_code": raw("Halt Code - Import"),
        "main_code": linked("MAIN Demotion Code", halt_labels), "primary_code": linked("Halt Code - Linked", halt_labels),
        "main_reason": linked("MAIN Demotion Reason", reason_labels), "triage_process": linked("Triage Process", process_labels),
        "masking": raw("Manual Demotion Masking"), "operator": raw("Operator Error or Misuse"),
        "headlands": raw("Headlands vs Interior"), "headlands_complete": raw("Headlands Assessment Complete"),
        "outside_field": raw("Vehicle/Object Outside Field"),
        "nonnavigable_details": raw("NonNavigable Object Misuse Details"), "spark_url": raw("MAIN_SparkURL_Manual"),
        "machine_type": raw("VIN_machine_type", True), "investigation": raw("Investigation Complete"),
        "activities": raw("Triage Activities Complete"), "scope": raw("In Scope"),
    }


def evaluate_state(state, rules):
    return {rule.name: {"predicate": evaluate_condition(rule.condition, state),
                        "trigger_predicate": evaluate_condition(rule.trigger_condition if rule.trigger_condition is not None else rule.condition, state),
                        "execution_eligibility": trigger_eligibility(rule, None, state),
                        "enabled": rule.enabled, "verified": rule.verified, "value": rule.value}
            for rule in rules}


def safe_value(value):
    if value is UNKNOWN_VALUE:
        return {"state": "UNAVAILABLE"}
    if isinstance(value, dict):
        return {key: safe_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [safe_value(item) for item in value]
    return value


def build_coverage_matrix(records, rules):
    output = []
    for item in records:
        evaluated = evaluate_state(item["state"], rules)
        a39 = evaluated["A-39"]["predicate"]
        same = [name for name, value in evaluated.items() if name != "A-39" and value["value"] == NO_ERROR and value["predicate"] is True and value["enabled"] is not False]
        unknown = [name for name, value in evaluated.items() if name != "A-39" and value["value"] == NO_ERROR and value["predicate"] is None and value["enabled"] is not False]
        conflicts = [name for name, value in evaluated.items() if name != "A-39" and value["value"] != NO_ERROR and value["predicate"] is True and value["enabled"] is not False]
        classification = "not_A39_singleton_candidate" if a39 is False else "unknown_A39_predicate" if a39 is None else "documented_overlap" if same else "candidate_gap_unknown_predicates" if unknown else "candidate_gap_no_documented_match"
        output.append({"record_id": item["record_id"], "a_uid": item.get("a_uid"), "timestamp_utc": item.get("timestamp_utc"),
                       "class": classification, "a39_singleton_candidate": a39, "same_value_candidates": same,
                       "unknown_candidates": unknown, "conflicting_candidates": conflicts,
                       "writer_attribution": "UNKNOWN", "state": safe_value(item["state"]), "rules": evaluated})
    return output


def dependency_closure(tables, root):
    references, fields = defaultdict(set), {}
    for table in tables:
        for field in table["fields"]:
            fields[field["id"]] = {"table": table.get("name", table["id"]), "field": field["name"], "type": field["type"]}
            options = field.get("options", {})
            references[field["id"]].update(options.get("referencedFieldIds") or [])
            for key in ("recordLinkFieldId", "fieldIdInLinkedTable"):
                if options.get(key):
                    references[field["id"]].add(options[key])
    def walk(edges):
        reached, queue = set(), deque([root])
        while queue:
            for neighbor in edges.get(queue.popleft(), []):
                if neighbor != root and neighbor not in reached:
                    reached.add(neighbor)
                    queue.append(neighbor)
        return sorted(reached)
    reverse = defaultdict(set)
    for consumer, producers in references.items():
        for producer in producers:
            reverse[producer].add(consumer)
    producers, consumers = walk(references), walk(reverse)
    return {"root": root, "root_present": root in fields, "producers": producers, "consumers": consumers,
            "field_details": {key: fields.get(key, {"unresolved": True}) for key in {root, *producers, *consumers}},
            "scope": "Structured field metadata only; excludes native automation/UI/external/manual consumers"}


def explore_finite_model(initial, transitions, max_states=10000):
    encode = lambda value: json.dumps(value, sort_keys=True)
    seen = {encode(value): value for value in initial}
    queue = deque(initial)
    edges = []
    if len(seen) > max_states:
        return {"complete": False, "states": [], "edges": [], "verdict": "UNKNOWN"}
    while queue:
        source = queue.popleft()
        for target in transitions(source):
            edges.append([source, target])
            key = encode(target)
            if key not in seen:
                if len(seen) >= max_states:
                    return {"complete": False, "states": list(seen.values()), "edges": edges, "verdict": "UNKNOWN"}
                seen[key] = target
                queue.append(target)
    return {"complete": True, "states": list(seen.values()), "edges": edges, "verdict": "MODEL_EXPLORATION_ONLY"}


def compare_observation_sets(control, treatment, complete=False):
    if not complete:
        return {"result": "UNKNOWN", "reason": "incomplete_model"}
    serialize = lambda trace: json.dumps(trace, sort_keys=True)
    before, after = {serialize(t) for t in control}, {serialize(t) for t in treatment}
    return {"result": "MODEL_EQUIVALENT" if before == after else "MODEL_DIFFERENCE",
            "control_only": sorted(before - after), "treatment_only": sorted(after - before),
            "production_proof": False}


def render_decision(matrix, dependencies):
    return {"automation_verdict": "UNKNOWN / KEEP", "lookup_verdict": "HOLD / KEEP",
            "diagnostic_counts": dict(Counter(row["class"] for row in matrix)),
            "blockers": ["Other live writer definitions remain incomplete; A-39 and A-28 visible predicates are UI-confirmed, but immutable IDs/history and cropped A-28 action destinations remain unverified",
                         "Native trigger/lookup semantics not calibrated in approved dev fixtures",
                         "No complete reachable-workflow model or paired platform traces",
                         "Native view/interface/manual and external consumers not fully inventoried",
                         "Mirror compatibility and historical/timing evidence not completed"],
            "known_code_dependency": "sync_triage_full.py maps Misuse Check Required and UPDATE SET * can null mirrored data if it disappears",
            "source_field_deletion_authorized": False, "dependencies": dependencies,
            "evidence_limit": "Static predicates from mixed UI/documentation evidence; verified flags refer to shown predicates and output assignments, not platform calibration or complete execution attribution. No current-state count proves behavioral redundancy"}


def write_csv(store, name, rows):
    path = store.root / name
    with path.open("x", newline="") as stream:
        path.chmod(0o600)
        writer = csv.writer(stream)
        writer.writerow(["record_id", "a_uid", "timestamp_utc", "class", "machine_type", "primary_code", "main_code", "masking", "triage_process", "operator", "same_value_candidates", "unknown_candidates", "conflicting_candidates", "failed_predicates"])
        for row in rows:
            state = row["state"]
            values = [row["record_id"], row["a_uid"], row["timestamp_utc"], row["class"]]
            values += [json.dumps(state.get(key), ensure_ascii=False) for key in ("machine_type", "primary_code", "main_code", "masking", "triage_process", "operator")]
            values += [json.dumps(row[key]) for key in ("same_value_candidates", "unknown_candidates", "conflicting_candidates")]
            values += [json.dumps([name for name, result in row["rules"].items() if result["predicate"] is False])]
            writer.writerow(["'" + value if isinstance(value, str) and value.startswith(("=", "+", "-", "@")) else value for value in values])
    store.save(name.replace(".csv", "_receipt"), {"file": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "rows": len(rows)}, {})


def check_source_snapshot(records, halts, repeated_ids=None):
    halt_fields = {row["id"]: row["fields"] for row in halts}
    issues = []
    for row in records:
        fields = row["fields"]
        linked = fields.get("Halt Code - Linked", [])
        if not isinstance(linked, list) or any(key not in halt_fields for key in linked):
            issues.append({"record_id": row["id"], "reason": "unresolved_primary_reference"})
            continue
        expected = [halt_fields[key]["Misuse Check Required"] for key in linked if halt_fields[key].get("Misuse Check Required") is not None]
        actual = fields.get("Misuse Check Required", [])
        if actual != expected:
            issues.append({"record_id": row["id"], "reason": "lookup_differs_from_captured_source", "expected": expected, "actual": actual})
    first = {row["id"]: row["fields"].get("A_UID") for row in records}
    result = {"source_lookup_issues": issues, "repeat_identity_status": "NOT_COLLECTED"}
    if repeated_ids is not None:
        second = {row["id"]: row["fields"].get("A_UID") for row in repeated_ids}
        result.update({"repeat_identity_status": "MATCH" if first == second else "DRIFT",
                       "repeat_record_count": len(second), "added_ids": sorted(second.keys() - first.keys()),
                       "removed_ids": sorted(first.keys() - second.keys()),
                       "changed_uid_ids": sorted(key for key in first.keys() & second.keys() if first[key] != second[key])})
    return result


def analyze(args):
    tables = schema_tables(load_payload(args.schema))
    table = next((t for t in tables if t["id"] == PRODUCTION_TABLE), None)
    if table is None:
        raise AuditError("Production schema missing")
    names = Counter(f["name"] for f in table["fields"])
    unknown_fields = [name for name in REQUESTED_FIELDS if names[name] != 1]
    requested = set(REQUESTED_FIELDS) - set(unknown_fields)
    records = extract_records(load_payload(args.records))
    if len(records) >= args.request_cap:
        raise AuditError("Record count reached acquisition cap; completeness not established")
    halts = extract_records(load_payload(args.halts))
    halt_labels = {r["id"]: r["fields"]["Halt Code"] for r in halts}
    snapshot_checks = check_source_snapshot(records, halts, extract_records(load_payload(args.repeat_ids)) if args.repeat_ids else None)
    labels = load_payload(args.labels)
    normalized = [{"record_id": r["id"], "a_uid": r["fields"].get("A_UID"), "timestamp_utc": r["fields"].get("Timestamp UTC"),
                   "state": normalize_state(r, halt_labels, labels["reasons"], labels["processes"], requested)} for r in records]
    inconsistent = {item["record_id"] for item in snapshot_checks["source_lookup_issues"]}
    for row in normalized:
        if row["record_id"] in inconsistent:
            row["state"]["misuse_required"] = UNKNOWN_VALUE
    rules = documented_rules()
    matrix = build_coverage_matrix(normalized, rules)
    deps = [dependency_closure(tables, field) for field in (LOOKUP_FIELD, SOURCE_FIELD)]
    decision = render_decision(matrix, deps)
    candidates = [row for row in matrix if row["a39_singleton_candidate"] is True]
    gaps = [row for row in candidates if not row["same_value_candidates"]]
    overlaps = [row for row in candidates if row["same_value_candidates"]]
    a28_rows = [row for row in matrix if isinstance(row["state"].get("main_code"), list) and "12.35" in row["state"]["main_code"]]
    a28_incomplete = [row for row in a28_rows if row["state"]["investigation"] == "Investigation Not Complete"]
    a28_ready = [row for row in a28_incomplete if row["rules"]["A-28-headlands"]["trigger_predicate"] is True]
    a28_waiting = [row for row in a28_incomplete if row["rules"]["A-28-headlands"]["trigger_predicate"] is False]
    def machine(row):
        value = row["state"].get("machine_type")
        return value[0] if isinstance(value, list) and len(value) == 1 else "UNMAPPED_OR_MULTIPLE"
    decision.update({"observed_at_utc": now(), "record_count": len(records), "halt_count": len(halts),
                     "candidate_count": len(candidates), "candidate_gap_count": len(gaps), "candidate_overlap_count": len(overlaps),
                     "a28_policy": "USER_CONFIRMED_PUBLISHED_V2_HEADLANDS_COMPLETE_WITH_OTHERWISE",
                     "a28_main_12_35_records": len(a28_rows), "a28_investigation_not_complete": len(a28_incomplete),
                     "a28_ready_condition_records": len(a28_ready), "a28_waiting_headlands_records": len(a28_waiting),
                     "a28_ready_ids": [row["record_id"] for row in a28_ready],
                     "a28_waiting_headlands_ids": [row["record_id"] for row in a28_waiting],
                     "gap_operator_values": dict(Counter(str(row["state"]["operator"]) for row in gaps)),
                     "gap_machine_types": dict(Counter(machine(row) for row in gaps)),
                     "gap_event_years": dict(Counter((row["timestamp_utc"] or "UNKNOWN")[:4] for row in gaps)),
                     "gap_primary_codes": dict(Counter(json.dumps(row["state"]["primary_code"]) for row in gaps)),
                     "rule_predicate_matches_within_candidates": {r.name: sum(row["rules"][r.name]["predicate"] is True for row in candidates) for r in rules},
                     "unknown_or_ambiguous_requested_fields": unknown_fields,
                     "snapshot_checks": snapshot_checks,
                     "collection_completeness": "Explicit cap not reached. Compare repeated IDs and captured reference flags below; this is not an atomic snapshot or native predicate calibration. Native page receipts are not exposed by the tool.",
                     "examples": [{key: row[key] for key in ("record_id", "a_uid", "state", "class")} for row in gaps[:10]]})
    store = EvidenceStore(args.output)
    inputs = [args.schema, args.records, args.halts, args.labels] + ([args.repeat_ids] if args.repeat_ids else [])
    provenance = {"inputs": {str(path): hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in inputs},
                  "rule_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  "production_writes": 0}
    store.save("decision", decision, provenance)
    store.save("documented_rule_model", {"authoritative": False, "rules": [asdict(r) for r in rules]}, provenance)
    store.save("dependencies", {"closures": deps}, provenance)
    store.save("coverage", {"rows": matrix}, provenance)
    write_csv(store, "record_coverage.csv", matrix)
    write_csv(store, "candidate_gaps.csv", gaps)
    print(json.dumps({key: value for key, value in decision.items() if key != "dependencies"}, indent=2))
    return 2


def main():
    parser = argparse.ArgumentParser(description="Offline A-39 diagnostic coverage analyzer. No network calls; no live redundancy verdict from documentation.")
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--records", type=Path, required=True)
    parser.add_argument("--halts", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeat-ids", type=Path)
    parser.add_argument("--request-cap", type=int, default=100000)
    return analyze(parser.parse_args())


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AuditError, OSError) as error:
        print(f"Analysis incomplete: {error}", file=sys.stderr)
        sys.exit(2)
