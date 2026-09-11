import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


class AuditError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def load_payload(path):
    if Path(path).suffix.lower() == ".csv":
        with Path(path).open(newline="", encoding="utf-8-sig") as stream:
            return {"csv_rows": list(csv.DictReader(stream))}
    text = Path(path).read_text()
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        lines = text.splitlines()
        numbered = [re.match(r"^\s*\d+\|\s?(.*)$", line) for line in lines]
        if not lines or not all(numbered):
            raise AuditError(f"Not a complete JSON export: {path}") from None
        try:
            value = json.loads("\n".join(match.group(1) for match in numbered))
        except json.JSONDecodeError:
            raise AuditError(f"Invalid numbered JSON export: {path}") from None
    for _ in range(3):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                break
        elif isinstance(value, dict) and "content" in value and isinstance(value["content"], list):
            parts = [p.get("text", "") for p in value["content"] if p.get("type") == "text"]
            try:
                value = json.loads("\n".join(parts))
            except json.JSONDecodeError:
                break
        else:
            break
    if not isinstance(value, (dict, list)):
        raise AuditError(f"Unsupported evidence object: {path}")
    return value


def extract_records(payload):
    if not isinstance(payload, dict) or "records" not in payload:
        raise AuditError("Missing records envelope")
    if payload.get("error") or payload.get("success") is False or payload.get("offset") or payload.get("complete") is False:
        raise AuditError("Failed or incomplete records response")
    records = payload["records"]
    if not isinstance(records, list):
        raise AuditError("Records is not an array")
    ids = set()
    for record in records:
        if not isinstance(record, dict) or not record.get("id") or not isinstance(record.get("fields"), dict):
            raise AuditError("Invalid record")
        if record["id"] in ids:
            raise AuditError("Duplicate record ID in export")
        ids.add(record["id"])
    return records


def sanitize(value):
    if isinstance(value, dict):
        return {key: "[REDACTED]" if re.search(r"(^|_)(token|secret|password|authorization|api_key)($|_)", key, re.I)
                else sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"https?://[^\s\"<>]+", lambda match: urlunsplit((*urlsplit(match.group())[:3], "", "")), value)
    return value


class EvidenceStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)

    def save(self, label, payload, provenance):
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", label):
            raise AuditError("Invalid evidence label")
        data = (json.dumps(sanitize(payload), indent=2, ensure_ascii=False) + "\n").encode()
        path = self.root / f"{label}.json"
        with path.open("xb") as stream:
            path.chmod(0o600)
            stream.write(data)
        entry = {"artifact": path.name, "sha256": hashlib.sha256(data).hexdigest(),
                 "saved_at_utc": now(), "bytes": len(data), **sanitize(provenance)}
        with (self.root / "manifest.jsonl").open("a") as stream:
            (self.root / "manifest.jsonl").chmod(0o600)
            stream.write(json.dumps(entry) + "\n")
        return path


def schema_tables(payload):
    if isinstance(payload, dict) and "tables" in payload:
        return payload["tables"]
    if isinstance(payload, dict) and "table" in payload:
        return [payload["table"]]
    if isinstance(payload, dict) and "fields" in payload:
        return [payload]
    raise AuditError("Missing schema envelope")


def build_schema_graph(tables):
    graph = {"tables": {}, "fields": {}, "links": [], "derived": []}
    for table in tables:
        if table["id"] in graph["tables"]:
            raise AuditError("Duplicate schema table")
        graph["tables"][table["id"]] = table
        for field in table["fields"]:
            item = {**field, "table_id": table["id"]}
            if field["id"] in graph["fields"]:
                raise AuditError("Duplicate schema field ID")
            graph["fields"][field["id"]] = item
            if field["type"] == "multipleRecordLinks":
                graph["links"].append(item)
            elif field["type"] in ("formula", "multipleLookupValues", "rollup", "count"):
                graph["derived"].append(item)
    return graph


def normalize_records(records, table):
    fields = {field["id"]: field for field in table["fields"]}
    names = defaultdict(list)
    for field in fields.values():
        names[field["name"]].append(field["id"])
    output = []
    for record in records:
        values = {}
        for key, value in record["fields"].items():
            candidates = [key] if key in fields else names[key]
            if len(candidates) != 1:
                raise AuditError(f"Unknown/ambiguous field {key!r} in {table['id']}")
            values[candidates[0]] = value
        output.append({**record, "fields": values})
    return output


def canonical_candidates(records, code_field, tag_field):
    groups = defaultdict(list)
    for record in records:
        fields = record["fields"]
        code = fields.get(code_field)
        if isinstance(code, str) and code and not code.endswith("_Duplicate") and fields.get(tag_field) != "Duplicate":
            groups[code].append(record["id"])
    return dict(groups)


def edge_findings(before, originals, current, graph, halt_table, code_field, tag_field):
    candidates = canonical_candidates(originals, code_field, tag_field)
    current_index = {table: {r["id"]: r for r in records} for table, records in current.items()}
    output = []
    for duplicate in before:
        code = duplicate["fields"].get(code_field, "")
        base_code = code.removesuffix("_Duplicate")
        for field_id, values in duplicate["fields"].items():
            field = graph["fields"].get(field_id, {})
            if field.get("type") != "multipleRecordLinks" or field.get("name") in ("ERC", "Demotion Reason_Old"):
                continue
            options = field["options"]
            source_table = options["linkedTableId"]
            source_field = options.get("inverseLinkFieldId")
            for record_id in values or []:
                if source_table not in current_index:
                    reason, status = "source_table_not_collected", "UNKNOWN"
                elif record_id not in current_index[source_table]:
                    reason, status = "source_record_absent_requires_history", "UNKNOWN"
                elif len(candidates.get(base_code, [])) != 1:
                    reason, status = "canonical_identity_ambiguous", "UNKNOWN"
                elif not source_field:
                    reason, status = "inverse_field_not_available", "UNKNOWN"
                else:
                    observed = current_index[source_table][record_id]["fields"].get(source_field, [])
                    restored = candidates[base_code][0] in observed
                    reason = "replacement_present_identity_needs_baseline" if restored else "replacement_missing"
                    status = "PASS" if restored else "FAIL"
                expected = candidates.get(base_code, [])
                output.append({"check": "historical_edge", "status": status, "reason": reason,
                               "code": base_code, "duplicate_id": duplicate["id"], "table_id": source_table,
                               "record_id": record_id, "field_id": source_field,
                               "expected_id": expected[0] if len(expected) == 1 else None,
                               "reference_only": source_table not in {f["table_id"] for f in graph["links"]
                                                                     if f.get("options", {}).get("linkedTableId") == halt_table
                                                                     and f["table_id"] in current}})
    return output


def compare_fields(before, after, requested):
    missing = {"state": "omitted"}
    return [{"field_id": key, "before": before.get(key, missing), "after": after.get(key, missing)}
            for key in requested if before.get(key, missing) != after.get(key, missing)]


def parse_timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise AuditError("Naive timestamp has no verified timezone")
    return parsed.astimezone(timezone.utc)


def validate_sql(sql):
    if not re.match(r"^\s*(SELECT|SHOW|DESCRIBE|EXPLAIN)\b", sql, re.I):
        raise AuditError("Only reviewed read-only SQL forms supported")
    if any(marker in sql for marker in [";", "--", "/*", "*/"]):
        raise AuditError("Multiple statements/comments not allowed")
    if re.search(r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|RESTORE|VACUUM|CALL|INTO|REFLECT|JAVA_METHOD|HTTP_REQUEST|AI_QUERY)\b", sql, re.I):
        raise AuditError("Potential side-effect statement/function rejected")
    return sql


def summarize(findings):
    counts = Counter(item["status"] for item in findings)
    verdict = "FAIL" if counts["FAIL"] else "UNKNOWN" if counts["UNKNOWN"] or not findings else "PASS"
    return {"verdict": verdict, "counts": dict(counts), "exit_code": {"PASS": 0, "FAIL": 1, "UNKNOWN": 2}[verdict]}


def field_id(table, name):
    matches = [f["id"] for f in table["fields"] if f["name"] == name]
    if len(matches) != 1:
        raise AuditError(f"Unknown/ambiguous field name: {name}")
    return matches[0]


def analyze(graph, before, current, halt_table, complete_tables):
    halt_schema = graph["tables"][halt_table]
    code_field, tag_field = (field_id(halt_schema, name) for name in ("Halt Code", "Duplicate"))
    originals = current.get(halt_table, [])
    candidates = canonical_candidates(originals, code_field, tag_field)
    deleted_ids = {r["id"] for r in before}
    surviving_ids = {r["id"] for r in originals}
    findings = []
    for duplicate in before:
        code = duplicate["fields"][code_field].removesuffix("_Duplicate")
        findings.append({"check": "deleted_id_absent", "record_id": duplicate["id"],
                         "status": "FAIL" if duplicate["id"] in surviving_ids else "PASS" if halt_table in complete_tables else "UNKNOWN"})
    for code in sorted({r["fields"][code_field].removesuffix("_Duplicate") for r in before}):
        matches = candidates.get(code, [])
        findings.append({"check": "canonical_display_unique", "code": code, "candidate_ids": matches,
                         "status": "PASS" if len(matches) == 1 else "FAIL" if halt_table in complete_tables else "UNKNOWN"})
    for field in graph["links"]:
        if field["options"].get("linkedTableId") != halt_table:
            continue
        table = field["table_id"]
        if table not in current or table not in complete_tables:
            findings.append({"check": "forward_link_coverage", "table_id": table, "field_id": field["id"], "status": "UNKNOWN"})
            continue
        for record in current[table]:
            links = record["fields"].get(field["id"], [])
            if not isinstance(links, list):
                raise AuditError("Linked-record field is not an array")
            invalid = set(links) - surviving_ids
            duplicate_links = set(links) & deleted_ids
            if invalid or duplicate_links:
                findings.append({"check": "invalid_forward_link", "table_id": table, "record_id": record["id"],
                                 "field_id": field["id"], "invalid_ids": sorted(invalid), "status": "FAIL"})
    findings.extend(edge_findings(before, originals, current, graph, halt_table, code_field, tag_field))
    findings.extend({"check": name, "status": "UNKNOWN"} for name in [
        "preincident_canonical_identity", "earlier_links_and_unrelated_members_preserved",
        "automation_execution_history", "databricks_complete_reconciliation", "downstream_reconciliation", "stable_capture"])
    return {"as_of_utc": now(), "counts": {table: len(records) for table, records in current.items()},
            "known_deleted_count": len(deleted_ids), "known_code_count": len({r["fields"][code_field] for r in before}),
            "findings": findings, "summary": summarize(findings)}


def extract_rows(payload, expected_count=None):
    if payload.get("success") is not True or not isinstance(payload.get("columns"), list) or not isinstance(payload.get("rows"), list):
        raise AuditError("Invalid Databricks export")
    if payload.get("row_count") != len(payload["rows"]) or (expected_count is not None and len(payload["rows"]) != expected_count):
        raise AuditError("Databricks export does not match independent row count")
    if any(len(row) != len(payload["columns"]) for row in payload["rows"]):
        raise AuditError("Databricks row width mismatch")
    return [dict(zip(payload["columns"], row)) for row in payload["rows"]]


def reconcile_dbx(graph, current, parts, expected_rows, expected_ids):
    rows = []
    seen = set()
    for payload, expected in parts:
        batch = extract_rows(payload, expected)
        ids = {row["Airtable_ID"] for row in batch}
        if ids & seen:
            raise AuditError("Overlapping Databricks partitions")
        seen.update(ids)
        rows.extend(batch)
    if len(rows) != expected_rows or len(seen) != expected_ids:
        raise AuditError("Combined Databricks census is incomplete")
    index = defaultdict(list)
    for row in rows:
        index[row["Airtable_ID"]].append(row)
    ht, pt, rt = "tblN8uu4Gl1eDZMLs", "tblSJItXuuUd0lyHP", "tblINqDuMCUehLzgj"
    hf = {f["name"]: f["id"] for f in graph["tables"][ht]["fields"]}
    pf = {f["name"]: f["id"] for f in graph["tables"][pt]["fields"]}
    code_map = {r["id"]: r["fields"].get(hf["Halt Code"]) for r in current[ht]}
    rf = field_id(graph["tables"][rt], "Airtable_Demotion_Reason")
    reason_map = {r["id"]: r["fields"].get(rf) for r in current[rt]}
    scalar = {"Halt Code - Import": "halt_code", "Manual Demotion Masking": "manual_demotion_masking",
              "Operator Error or Misuse": "operator_error_or_misuse", "Investigation Complete": "investigation_complete",
              "Triage Activities Complete": "triage_activities_complete", "In Scope": "in_scope",
              "Bug or Intended Behavior": "bug_or_intended_behavior", "VIN": "VIN", "Timestamp UTC": "Timestamp_utc"}
    linked = {"MAIN Demotion Code": ("main_demotion_code", code_map), "Secondary Demotion Manual": ("secondary_demotion", code_map),
              "Preceding Stop Code": ("prev_stop_halt_code", code_map), "Demotion Reason": ("demotion_reason", reason_map),
              "MAIN Demotion Reason": ("main_demotion_reason", reason_map), "Secondary Demotion Reason": ("secondary_demotion_reason", reason_map)}
    differences, missing, ambiguous, multivalued = [], [], [], []
    for record in current[pt]:
        matches = index.get(record["id"], [])
        if not matches:
            missing.append(record["id"])
            continue
        if len(matches) != 1:
            ambiguous.append(record["id"])
            continue
        f, row = record["fields"], matches[0]
        expected = {column: f.get(pf[name]) for name, column in scalar.items()}
        for name, (column, mapping) in linked.items():
            values = f.get(pf[name], [])
            if len(values) > 1:
                multivalued.append({"record_id": record["id"], "field": name, "links": values})
                continue
            expected[column] = mapping.get(values[0]) if values else None
        expected["confirmed_demotion_type"] = f.get(pf["Confirmed Demotion Type"])
        observed = {column: row.get(column) for column in expected}
        if isinstance(observed.get("confirmed_demotion_type"), str):
            observed["confirmed_demotion_type"] = json.loads(observed["confirmed_demotion_type"])
        diff = compare_fields(expected, observed, list(expected))
        if diff:
            differences.append({"record_id": record["id"], "timestamp_utc": f.get(pf["Timestamp UTC"]),
                                "differences_airtable_to_dbx": diff, "attribution": "UNKNOWN"})
    return {"dbx_rows": len(rows), "dbx_distinct_ids": len(seen), "airtable_rows": len(current[pt]),
            "missing_dbx_ids": missing, "ambiguous_dbx_ids": ambiguous, "multivalued_fields": multivalued,
            "mismatched_record_count": len(differences), "mismatches": differences,
            "field_mismatch_counts": dict(Counter(d["field_id"] for r in differences for d in r["differences_airtable_to_dbx"])),
            "mismatches_since_march10": sum(r["timestamp_utc"] >= "2026-03-10" for r in differences if r["timestamp_utc"]),
            "status": "UNKNOWN", "reason": "non_atomic_capture_and_history_needed_for_attribution"}


def current_facts(graph, before, current, baseline_csv=None):
    halt_table, prod_table = "tblN8uu4Gl1eDZMLs", "tblSJItXuuUd0lyHP"
    hs, ps = graph["tables"][halt_table], graph["tables"][prod_table]
    hf = {f["name"]: f["id"] for f in hs["fields"]}
    pf = {f["name"]: f["id"] for f in ps["fields"]}
    halts = current[halt_table]
    by_id = {r["id"]: r["fields"] for r in halts}
    groups = canonical_candidates(halts, hf["Halt Code"], hf["Duplicate"])
    affected_codes = {r["fields"][hf["Halt Code"]].removesuffix("_Duplicate") for r in before}
    role_ids = [f["id"] for f in graph["links"] if f["table_id"] == prod_table and f["options"]["linkedTableId"] == halt_table]
    missing, mismatches, cohort, lookup_mismatches = [], [], [], []
    sentinel = []
    for record in current[prod_table]:
        f = record["fields"]
        linked = f.get(pf["Halt Code - Linked"], [])
        imported = f.get(pf["Halt Code - Import"])
        linked_codes = [by_id.get(link, {}).get(hf["Halt Code"]) for link in linked]
        identity = {"record_id": record["id"], "a_uid": f.get(pf["A_UID"]), "imported": imported,
                    "linked_codes": linked_codes}
        if imported and not linked:
            missing.append(identity)
        elif imported and linked_codes != [imported]:
            mismatches.append(identity)
        if imported in affected_codes or any(by_id.get(link, {}).get(hf["Halt Code"]) in affected_codes
                                            for role in role_ids for link in f.get(role, [])):
            cohort.append(record["id"])
        for role_name, lookup_name in [("Halt Code - Linked", "Demotion Reason"), ("MAIN Demotion Code", "MAIN Demotion Reason"),
                                       ("Secondary Demotion Manual", "Secondary Demotion Reason"), ("Preceding Stop Code", "Preceding Stop Code Reason")]:
            links = f.get(pf[role_name], [])
            expected = {reason for link in links for reason in by_id.get(link, {}).get(hf["Demotion Reason_Old"], [])}
            observed = set(f.get(pf[lookup_name], []))
            if expected != observed:
                lookup_mismatches.append({**identity, "role": role_name, "expected": sorted(expected), "observed": sorted(observed)})
        if f.get(pf["A_UID"]) == "1RW9640DPNJ820391 | 2025-02-14 00:47:40.554801":
            sentinel.append({"id": record["id"], "fields": {graph["fields"][key]["name"]: value for key, value in f.items()}})
    reasons_table = "tblINqDuMCUehLzgj"
    reasons = {}
    if reasons_table in current:
        label = field_id(graph["tables"][reasons_table], "Airtable_Demotion_Reason")
        reasons = {r["id"]: r["fields"].get(label) for r in current[reasons_table]}
    reference_diffs, ambiguous_csv, compared_codes = [], {}, []
    if baseline_csv:
        with Path(baseline_csv).open(newline="", encoding="utf-8-sig") as stream:
            baseline = list(csv.DictReader(stream))
        baseline_counts = Counter(row["Halt Code"] for row in baseline)
        ambiguous_csv = {code: count for code, count in baseline_counts.items() if code in affected_codes and count != 1}
        for row in baseline:
            code = row["Halt Code"]
            if code not in affected_codes or code in ambiguous_csv:
                continue
            compared_codes.append(code)
            candidates = groups.get(code, [])
            if len(candidates) != 1:
                continue
            actual = by_id[candidates[0]]
            for name in ("Description", "Human vs System", "Default MTBI", "If Bug MTBI", "Misuse Check Required", "Demotion Reason_Old"):
                expected = row.get(name, "")
                value = actual.get(hf[name], "")
                if name == "Demotion Reason_Old":
                    value = ", ".join(reasons.get(item, item) for item in value or [])
                if expected != value:
                    reference_diffs.append({"code": code, "record_id": candidates[0], "field": name,
                                            "csv_value": expected, "current_value": value, "attribution": "UNKNOWN"})
    inverse = [f for f in graph["links"] if f["table_id"] == halt_table and f["options"]["linkedTableId"] == prod_table]
    historical_edges = [(r["id"], field["id"], event) for r in before for field in inverse for event in r["fields"].get(field["id"], [])]
    return {"production_count": len(current[prod_table]), "halt_count": len(halts), "affected_code_count": len(affected_codes),
            "historical_link_occurrences": len(historical_edges), "historical_distinct_demotions": len({edge[2] for edge in historical_edges}),
            "historical_demotions": sorted({edge[2] for edge in historical_edges}),
            "cohort_count": len(cohort), "cohort_ids": cohort,
            "missing_primary_count": len(missing), "missing_primary": missing,
            "primary_code_mismatch_count": len(mismatches), "primary_code_mismatches": mismatches,
            "lookup_mismatch_count": len(lookup_mismatches), "lookup_mismatches": lookup_mismatches,
            "duplicate_display_groups": {code: ids for code, ids in groups.items() if len(ids) > 1},
            "created_today": [{"record_id": r["id"], "code": r["fields"].get(hf["Halt Code"]),
                               "created": r["fields"].get(hf["Created Time"])} for r in halts
                              if r["fields"].get(hf["Created Time"], "") >= "2026-09-09T07:00:00"],
            "reference_csv_diffs": reference_diffs, "reference_csv_ambiguous_codes": ambiguous_csv,
            "reference_csv_compared_codes": compared_codes, "sentinel": sentinel}


def verify_recovery(baselines, live_records, halt_records, dbx_rows):
    live = {r["id"]: r["fields"] for r in live_records}
    codes = {r["id"]: r["fields"].get("Halt Code") for r in halt_records}
    dbx = defaultdict(list)
    for row in dbx_rows:
        dbx[row["Airtable_ID"]].append(row)
    scalar = {"manual_demotion_masking": "Manual Demotion Masking", "operator_error_or_misuse": "Operator Error or Misuse",
              "confirmed_demotion_type": "Confirmed Demotion Type", "investigation_complete": "Investigation Complete",
              "triage_activities_complete": "Triage Activities Complete", "in_scope": "In Scope",
              "bug_or_intended_behavior": "Bug or Intended Behavior"}
    linked = {"main_demotion_code": "MAIN Demotion Code", "secondary_demotion": "Secondary Demotion Manual",
              "prev_stop_halt_code": "Preceding Stop Code"}
    fields = list(scalar) + list(linked)
    results = []
    for baseline in baselines:
        record_id = baseline["record_id"]
        if record_id not in live:
            results.append({"record_id": record_id, "status": "UNKNOWN", "reason": "record_not_returned"})
            continue
        current = live[record_id]
        actual = {column: current.get(name) for column, name in scalar.items()}
        for column, name in linked.items():
            values = current.get(name, [])
            resolved = [codes.get(value, f"UNRESOLVED:{value}") for value in values]
            actual[column] = resolved[0] if len(resolved) == 1 else resolved if resolved else None
        expected = {column: baseline["before_day_utc"].get(column) for column in fields}
        differences = compare_fields(expected, actual, fields)
        protected = ["Halt Code - Linked", "Preceding Stop Code", "Confirmed JRM Link", "Reviewer"]
        protected_changes = compare_fields(baseline.get("current_airtable_snapshot", {}), current, protected)
        dbx_diff = None
        projected_diff = None
        if len(dbx[record_id]) == 1:
            observed = {column: dbx[record_id][0].get(column) for column in fields}
            if isinstance(observed["confirmed_demotion_type"], str):
                observed["confirmed_demotion_type"] = json.loads(observed["confirmed_demotion_type"])
            dbx_diff = compare_fields(actual, observed, fields)
            projected = dict(actual)
            if isinstance(projected["secondary_demotion"], list):
                projected["secondary_demotion"] = projected["secondary_demotion"][0] if projected["secondary_demotion"] else None
            projected_diff = compare_fields(projected, observed, fields)
        results.append({"record_id": record_id, "a_uid": current.get("A_UID"),
                        "status": "MATCH" if not differences and not protected_changes else "REVIEW",
                        "expected": expected, "actual": actual, "baseline_differences": differences,
                        "protected_changes_since_audit": protected_changes, "databricks_vs_airtable": dbx_diff,
                        "databricks_vs_sync_projection": projected_diff})
    known = [r for r in results if "actual" in r]
    field_counts = Counter(d["field_id"] for r in known for d in r["baseline_differences"])
    summary = {"checked_at_utc": now(), "cohort_size": len(baselines), "records_returned": len(known),
               "fields_compared": fields, "status_counts": dict(Counter(r["status"] for r in results)),
               "manual_mask_count": sum(r["actual"]["manual_demotion_masking"] == "Manual Mask" for r in known),
               "secondary_matches_baseline": sum(r["actual"]["secondary_demotion"] == r["expected"]["secondary_demotion"] for r in known),
               "still_intended_manual_type": sum("Intended Manual Demotion" in (r["actual"]["confirmed_demotion_type"] or []) for r in known),
               "baseline_difference_counts": dict(field_counts),
               "databricks_matches_airtable": sum(r["databricks_vs_airtable"] == [] for r in known),
               "databricks_matches_sync_projection": sum(r["databricks_vs_sync_projection"] == [] for r in known),
               "sync_projection_note": "Existing sync stores only the first Secondary Demotion Manual code; raw arrays are retained above, not claimed fully replicated.",
               "sync_exceptions": [{"record_id": r["record_id"], "a_uid": r["a_uid"], "differences": r["databricks_vs_sync_projection"]} for r in known if r["databricks_vs_sync_projection"] != []],
               "databricks_observed_times": sorted({r.get("observed_at_utc") for r in dbx_rows if r.get("observed_at_utc")}),
               "notes": "Exact comparison of selected fields; differences require review, not automatic rollback. No production writes."}
    return {"summary": summary, "records": results}


def incident_report(root, output):
    root = Path(root)
    store = EvidenceStore(output)
    diffs = extract_rows(load_payload(root / "dbx_triage_diffs.json"), 61)
    during = extract_rows(load_payload(root / "dbx_transient_diffs.json"), 241)
    live = {r["id"]: r["fields"] for r in extract_records(load_payload(root / "current_production.json"))}
    resets, all_changes, live_states, transitions = [], [], Counter(), defaultdict(Counter)
    for row in diffs:
        before, after = (json.loads(row[key]) for key in ("before_payload", "after_payload"))
        changes = compare_fields(before, after, sorted(set(before) | set(after)))
        entry = {"record_id": row["Airtable_ID"], "timestamp_utc": row["Timestamp_utc"],
                 "before_day_utc": before, "version_65920": after, "field_differences": changes,
                 "attribution": "requires_automation_and_revision_history"}
        all_changes.append(entry)
        for change in changes:
            transitions[change["field_id"]][json.dumps([change["before"], change["after"]])] += 1
        if before.get("manual_demotion_masking") == "Manual Mask" and after.get("manual_demotion_masking") == "Intended Manual Demotion - No Mask":
            entry["current_airtable_snapshot"] = live.get(row["Airtable_ID"])
            resets.append(entry)
            live_states[live.get(row["Airtable_ID"], {}).get("Manual Demotion Masking", "NOT_PRESENT")] += 1
    historical = load_payload(root / "reconciliation-3" / "current_facts.json")
    dbx = load_payload(root / "reconciliation-3" / "dbx_reconciliation.json")
    affected_ids = {row["Airtable_ID"] for row in diffs + during}
    summary = {"verdict": "FAIL", "audit_writes_to_production": 0, "recorded_at_utc": now(),
               "scope": {"base": "app1jXoB1g13R9iOl", "production_airtable_records": len(live),
                         "context_version": 65920, "baseline_utc": "2026-09-09T07:00:00Z",
                         "transient_snapshots_utc": ["18:00", "19:00", "21:00"], "snapshots_atomic": False},
               "manual_mask_resets": len(resets), "reset_live_airtable_states": dict(live_states),
               "end_to_end_changed_rows": len(diffs), "sampled_transient_distinct_ids": len({r["Airtable_ID"] for r in during}),
               "observed_change_union_ids": len(affected_ids),
               "missing_primary_links": historical["missing_primary"],
               "historical_edges": historical["historical_link_occurrences"],
               "historical_distinct_demotions": historical["historical_distinct_demotions"],
               "current_cross_system_mismatches": dbx["mismatched_record_count"],
               "cross_system_mismatches_since_march10": dbx["mismatches_since_march10"],
               "csv_baseline_ambiguous_codes": historical["reference_csv_ambiguous_codes"],
               "field_transitions": {k: dict(v) for k, v in transitions.items()},
               "unknown_checks": ["exact_creation_cause_and_run_logs", "full_Airtable_revision_and_automation_history",
                                  "preincident_values_for_old_unsynced_Airtable_records", "all_intermediate_versions",
                                  "exact_historical_MTBI_and_cached_dashboard_impact", "concurrent_writer_drift"],
               "repair_action": "None executed. Obtain owner evidence and separate approval before repairs."}
    store.save("incident_summary", summary, {"source": "preserved_evidence", "read_only": True})
    store.save("manual_mask_resets", {"records": resets}, {"source": "version_pinned_context_comparison"})
    store.save("all_triage_differences", {"records": all_changes}, {"source": "version_pinned_context_comparison"})
    store.save("observed_change_cohort", {"record_ids": sorted(affected_ids)}, {"source": "union_of_sampled_differences"})
    csv_path = store.root / "manual_mask_resets.csv"
    with csv_path.open("x", newline="") as stream:
        csv_path.chmod(0o600)
        writer = csv.writer(stream)
        writer.writerow(["record_id", "event_timestamp_utc", "before_main", "after_main", "before_secondary", "after_secondary", "before_operator_error", "after_operator_error", "review_only"])
        for row in resets:
            b, a = row["before_day_utc"], row["version_65920"]
            writer.writerow([row["record_id"], row["timestamp_utc"], b.get("main_demotion_code"), a.get("main_demotion_code"),
                             b.get("secondary_demotion"), a.get("secondary_demotion"), b.get("operator_error_or_misuse"), a.get("operator_error_or_misuse"), True])
    print(json.dumps({k: v for k, v in summary.items() if k != "field_transitions"}, indent=2))
    return 1


def pairs(values):
    output = {}
    for value in values:
        if "=" not in value:
            raise AuditError("Expected label=path")
        label, path = value.split("=", 1)
        if label in output:
            raise AuditError("Duplicate input label")
        output[label] = Path(path)
    return output


def main():
    parser = argparse.ArgumentParser(description="Offline incident auditor. No database/Airtable writes or notebook execution.")
    sub = parser.add_subparsers(dest="command", required=True)
    preserve = sub.add_parser("preserve")
    preserve.add_argument("--output", type=Path, required=True)
    preserve.add_argument("--source", action="append", required=True)
    inventory = sub.add_parser("inventory")
    inventory.add_argument("--schema", type=Path, action="append", required=True)
    inventory.add_argument("--output", type=Path, required=True)
    inventory.add_argument("--relationships-only", action="store_true")
    compare = sub.add_parser("compare")
    compare.add_argument("--schema", type=Path, action="append", required=True)
    compare.add_argument("--before", type=Path, required=True)
    compare.add_argument("--current", action="append", required=True)
    compare.add_argument("--complete-table", action="append", default=[])
    compare.add_argument("--halt-table", default="tblN8uu4Gl1eDZMLs")
    compare.add_argument("--output", type=Path, required=True)
    compare.add_argument("--baseline-csv", type=Path)
    compare.add_argument("--dbx-part", action="append", default=[])
    compare.add_argument("--dbx-count", type=int)
    compare.add_argument("--dbx-distinct", type=int)
    compare.add_argument("--dbx-version", type=int)
    recovery = sub.add_parser("verify-recovery")
    recovery.add_argument("--baseline", type=Path, required=True)
    recovery.add_argument("--live", type=Path, required=True)
    recovery.add_argument("--halts", type=Path, required=True)
    recovery.add_argument("--dbx", type=Path, required=True)
    recovery.add_argument("--output", type=Path, required=True)
    finalize = sub.add_parser("finalize")
    finalize.add_argument("--root", type=Path, required=True)
    finalize.add_argument("--output", type=Path, required=True)
    report = sub.add_parser("report")
    report.add_argument("input", type=Path)
    report.add_argument("--since")
    report.add_argument("--until")
    report.add_argument("--aggregate", action="store_true")
    report.add_argument("--user")
    args = parser.parse_args()
    if args.command == "verify-recovery":
        result = verify_recovery(load_payload(args.baseline)["records"], extract_records(load_payload(args.live)),
                                 extract_records(load_payload(args.halts)), extract_rows(load_payload(args.dbx)))
        store = EvidenceStore(args.output)
        store.save("recovery_verification", result, {"baseline": str(args.baseline), "live": str(args.live), "dbx": str(args.dbx)})
        print(json.dumps(result["summary"], indent=2))
        csv_path = store.root / "remaining_review.csv"
        with csv_path.open("x", newline="") as stream:
            csv_path.chmod(0o600)
            writer = csv.writer(stream)
            writer.writerow(["record_id", "a_uid", "field", "before_incident", "current"])
            for record in result["records"]:
                for difference in record.get("baseline_differences", []):
                    writer.writerow([record["record_id"], record["a_uid"], difference["field_id"],
                                     json.dumps(difference["before"]), json.dumps(difference["after"])])
        return 0 if all(r["status"] == "MATCH" for r in result["records"]) else 2
    if args.command == "finalize":
        return incident_report(args.root, args.output)
    if args.command == "report":
        data = load_payload(args.input)
        if "columns" in data and "rows" in data:
            if data.get("success") is False or data.get("row_count") != len(data["rows"]):
                raise AuditError("Incomplete Databricks result")
            rows = [dict(zip(data["columns"], row)) for row in data["rows"]]
            if data["columns"] == ["createtab_stmt"]:
                print(data["rows"][0][0])
                return 0
            if "version" in data["columns"] and "operationMetrics" in data["columns"]:
                rows = [{key: row.get(key) for key in ("version", "timestamp", "userName", "operation", "job", "operationMetrics")} for row in rows]
                for row in rows:
                    metrics = json.loads(row["operationMetrics"] or "{}")
                    row["operationMetrics"] = {key: value for key, value in metrics.items() if key in ("numTargetRowsUpdated", "numTargetRowsDeleted", "numDeletedRows", "numOutputRows", "numTargetRowsInserted")}
                    row["job"] = {key: value for key, value in json.loads(row["job"] or "{}").items() if key in ("jobId", "jobRunId", "jobName")}
            if "before_payload" in data["columns"] and "after_payload" in data["columns"]:
                transitions = defaultdict(Counter)
                reset_ids = []
                differences = []
                for row in rows:
                    before = json.loads(row["before_payload"] or "{}")
                    after = json.loads(row["after_payload"] or "{}")
                    changed = compare_fields(before, after, sorted(set(before) | set(after)))
                    for change in changed:
                        transitions[change["field_id"]][json.dumps([change["before"], change["after"]], sort_keys=True)] += 1
                    differences.append({"record_id": row["Airtable_ID"], "changes": changed})
                    if before.get("manual_demotion_masking") == "Manual Mask" and after.get("manual_demotion_masking") == "Intended Manual Demotion - No Mask":
                        reset_ids.append(row["Airtable_ID"])
                print(json.dumps({"changed_records": len(rows), "manual_mask_reset_count": len(reset_ids), "manual_mask_reset_ids": reset_ids,
                                  "field_transitions": {key: dict(value) for key, value in transitions.items()}}, indent=2))
                return 0
            if args.since:
                rows = [row for row in rows if row.get("timestamp", "") >= args.since]
            if args.until:
                rows = [row for row in rows if row.get("timestamp", "") < args.until]
            if args.user:
                rows = [row for row in rows if row.get("userName") == args.user]
            if args.aggregate:
                result = {"rows": len(rows), "columns": data["columns"]}
                if "timestamp" in data["columns"]:
                    result["time_bounds"] = [min((r["timestamp"] for r in rows), default=None), max((r["timestamp"] for r in rows), default=None)]
                for key in ("userName", "operation", "snapshot"):
                    if key in data["columns"]:
                        result[key] = dict(Counter(r[key] for r in rows))
                if "Airtable_ID" in data["columns"]:
                    result["distinct_airtable_ids"] = len({r["Airtable_ID"] for r in rows})
                print(json.dumps(result, indent=2))
            else:
                print(json.dumps(rows, indent=2))
        else:
            print(json.dumps(data.get("summary", data), indent=2))
        return data.get("summary", {}).get("exit_code", 0)
    store = EvidenceStore(args.output)
    if args.command == "preserve":
        for label, path in pairs(args.source).items():
            raw = path.read_bytes()
            payload = load_payload(path)
            provenance = {"source_path": str(path), "source_sha256": hashlib.sha256(raw).hexdigest(),
                          "source_mtime_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                          "capture_time_verified": False}
            store.save(label, payload, provenance)
            if isinstance(payload, dict) and "records" in payload:
                print(f"{label}: {len(extract_records(payload))} records preserved")
            else:
                print(f"{label}: preserved")
        return 0
    tables = [table for path in args.schema for table in schema_tables(load_payload(path))]
    graph = build_schema_graph(tables)
    if args.command == "inventory":
        store.save("schema_graph", graph, {"source": "supplied_schema_exports"})
        if args.relationships_only:
            for table in tables:
                targets = defaultdict(list)
                for field in graph["links"]:
                    if field["table_id"] == table["id"]:
                        target = field["options"]["linkedTableId"]
                        targets[graph["tables"].get(target, {}).get("name", target)].append(field["name"])
                print(json.dumps({"table": table["name"], "id": table["id"], "field_count": len(table["fields"]), "linked_fields_by_target": dict(targets)}))
            return 0
        print(json.dumps({"tables": len(tables), "fields": len(graph["fields"]), "direct_links": len(graph["links"]),
                          "halt_incoming": [f for f in graph["links"] if f.get("options", {}).get("linkedTableId") == "tblN8uu4Gl1eDZMLs"]}, indent=2))
        return 0
    before = normalize_records(extract_records(load_payload(args.before)), graph["tables"][args.halt_table])
    current = {table: normalize_records(extract_records(load_payload(path)), graph["tables"][table])
               for table, path in pairs(args.current).items()}
    result = analyze(graph, before, current, args.halt_table, set(args.complete_table))
    if args.dbx_part:
        if None in (args.dbx_count, args.dbx_distinct, args.dbx_version):
            raise AuditError("Independent row/ID counts and source version are required")
        parts = []
        for value in args.dbx_part:
            count, path = value.split("=", 1)
            parts.append((load_payload(path), int(count)))
        dbx = reconcile_dbx(graph, current, parts, args.dbx_count, args.dbx_distinct)
        store.save("dbx_reconciliation", dbx, {"version": args.dbx_version, "source": "independently_counted_partitions"})
        print(json.dumps({k: v for k, v in dbx.items() if k != "mismatches" and k != "multivalued_fields"}, indent=2))
    store.save("findings", result, {"source": "offline_reconciliation", "collection_completeness_assertions": args.complete_table})
    if "tblSJItXuuUd0lyHP" in current:
        facts = current_facts(graph, before, current, args.baseline_csv)
        store.save("current_facts", facts, {"source": "current_exports_and_preserved_edges"})
        print(json.dumps({key: value for key, value in facts.items() if key.endswith("_count") or key in (
            "historical_link_occurrences", "historical_distinct_demotions", "duplicate_display_groups", "created_today", "reference_csv_diffs", "sentinel")}, indent=2))
    print(json.dumps({"counts": result["counts"], "known_deleted_count": result["known_deleted_count"],
                      "summary": result["summary"], "exceptions": [f for f in result["findings"] if f["status"] == "FAIL"]}, indent=2))
    return result["summary"]["exit_code"]


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (AuditError, OSError) as error:
        print(f"Audit incomplete: {error}", file=sys.stderr)
        sys.exit(2)
