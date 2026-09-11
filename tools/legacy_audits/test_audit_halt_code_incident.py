import json
import tempfile
import unittest
from pathlib import Path

from audit_halt_code_incident import (
    AuditError, EvidenceStore, build_schema_graph, canonical_candidates,
    compare_fields, edge_findings, extract_records, extract_rows, load_payload,
    normalize_records, parse_timestamp, summarize, validate_sql, reconcile_dbx, verify_recovery,
)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.halt = {"id": "halt", "fields": [
            {"id": "code", "name": "Halt Code", "type": "formula"},
            {"id": "tag", "name": "Duplicate", "type": "singleSelect"},
            {"id": "reverse", "name": "Production", "type": "multipleRecordLinks",
             "options": {"linkedTableId": "prod", "inverseLinkFieldId": "primary"}},
        ]}
        self.prod = {"id": "prod", "fields": [
            {"id": "primary", "name": "Primary", "type": "multipleRecordLinks",
             "options": {"linkedTableId": "halt", "inverseLinkFieldId": "reverse"}},
        ]}
        self.before = [{"id": "old", "fields": {"code": "3.1_Duplicate", "reverse": ["event"]}}]
        self.originals = [{"id": "original", "fields": {"code": "3.1", "tag": "Original"}}]

    def test_schema_preserves_duplicate_names(self):
        self.prod["fields"].append({"id": "other", "name": "Primary", "type": "multipleRecordLinks",
                                   "options": {"linkedTableId": "halt"}})
        graph = build_schema_graph([self.halt, self.prod])
        self.assertEqual(len(graph["links"]), 3)
        self.assertIn("other", graph["fields"])
        with self.assertRaises(AuditError):
            normalize_records([{"id": "event", "fields": {"Primary": []}}], self.prod)

    def test_lookup_is_not_direct_link(self):
        self.prod["fields"].append({"id": "lookup", "type": "multipleLookupValues", "name": "Reason",
                                   "options": {"result": {"type": "multipleRecordLinks"}}})
        graph = build_schema_graph([self.prod])
        self.assertEqual(len(graph["links"]), 1)

    def test_ids_and_omissions_preserved(self):
        result = normalize_records([{"id": "event", "fields": {"primary": []}}], self.prod)
        self.assertEqual(result[0]["fields"], {"primary": []})
        with self.assertRaises(AuditError):
            normalize_records([{"id": "event", "fields": {"Unrecognized": "value"}}], self.prod)

    def test_canonical_is_one_to_many(self):
        records = self.originals + [{"id": "another", "fields": {"code": "3.1"}}]
        self.assertEqual(len(canonical_candidates(records, "code", "tag")["3.1"]), 2)

    def test_code_is_not_float(self):
        records = [{"id": x, "fields": {"code": x}} for x in ["12.20", "12.2", "N/A", "12.X1"]]
        self.assertEqual(len(canonical_candidates(records, "code", "tag")), 4)

    def check_edges(self, fields, originals=None):
        return edge_findings(self.before, self.originals if originals is None else originals,
                             {"prod": [{"id": "event", "fields": fields}]},
                             build_schema_graph([self.halt, self.prod]), "halt", "code", "tag")

    def test_restored_historical_edge(self):
        result = self.check_edges({"primary": ["original", "unrelated"]})
        self.assertEqual(result[0]["status"], "PASS")
        self.assertEqual(result[0]["expected_id"], "original")

    def test_cleared_and_wrong_original_fail(self):
        for fields in [{}, {"primary": []}, {"primary": ["wrong"]}]:
            with self.subTest(fields=fields):
                self.assertEqual(self.check_edges(fields)[0]["status"], "FAIL")

    def test_deleted_source_record_is_unknown(self):
        result = edge_findings(self.before, self.originals, {"prod": []},
                              build_schema_graph([self.halt, self.prod]), "halt", "code", "tag")
        self.assertEqual(result[0]["status"], "UNKNOWN")

    def test_uncollected_table_not_empty(self):
        result = edge_findings(self.before, self.originals, {},
                              build_schema_graph([self.halt, self.prod]), "halt", "code", "tag")
        self.assertEqual(result[0]["reason"], "source_table_not_collected")

    def test_ambiguous_canonical_unknown(self):
        originals = self.originals + [{"id": "second", "fields": {"code": "3.1"}}]
        self.assertEqual(self.check_edges({"primary": ["original"]}, originals)[0]["status"], "UNKNOWN")

    def test_empty_suffix_result_not_coverage(self):
        self.assertEqual(summarize([])["verdict"], "UNKNOWN")

    def test_omitted_vs_unrequested(self):
        self.assertEqual(compare_fields({}, {}, ["x"]), [])
        diff = compare_fields({"x": "Misuse"}, {}, ["x"])
        self.assertEqual(diff[0]["after"], {"state": "omitted"})
        self.assertEqual(compare_fields({"x": "Misuse"}, {}, []), [])

    def test_null_empty_na_and_order_differ(self):
        for value in ["", [], "N/A"]:
            self.assertTrue(compare_fields({"x": None}, {"x": value}, ["x"]))
        self.assertTrue(compare_fields({"x": ["a", "b"]}, {"x": ["b", "a"]}, ["x"]))

    def test_extract_refuses_partial_and_duplicate_ids(self):
        for payload in [{"records": [], "offset": "next"}, {"records": [], "error": "bad"},
                        {"records": [], "complete": False},
                        {"records": [{"id": "x", "fields": {}}, {"id": "x", "fields": {}}]}]:
            with self.subTest(payload=payload), self.assertRaises(AuditError):
                extract_records(payload)
        self.assertEqual(extract_records({"records": []}), [])

    def test_large_export_not_capped(self):
        records = [{"id": str(i), "fields": {}} for i in range(1101)]
        self.assertEqual(len(extract_records({"records": records})), 1101)

    def test_timestamp_precision_and_utc(self):
        a = parse_timestamp("2025-02-14T00:47:40.554801Z")
        b = parse_timestamp("2025-02-13T16:47:40.554801-08:00")
        self.assertEqual(a, b)
        self.assertNotEqual(a, parse_timestamp("2025-02-14T00:47:40.554Z"))
        with self.assertRaises(AuditError):
            parse_timestamp("2025-02-14 00:47:40")

    def test_sql_read_boundary(self):
        for sql in ["SELECT count(*) FROM catalog.schema.table", "DESCRIBE HISTORY catalog.schema.table", "SHOW TABLES IN catalog.schema"]:
            validate_sql(sql)
        for sql in ["DELETE FROM x", "SELECT 1; DELETE FROM x", "WITH x AS (SELECT 1) INSERT INTO y SELECT * FROM x", "SELECT * INTO new FROM old", "CALL anything()", "SELECT reflect('x')", "SELECT 1 /* comment */"]:
            with self.subTest(sql=sql), self.assertRaises(AuditError):
                validate_sql(sql)

    def test_evidence_is_immutable_and_redacted(self):
        with tempfile.TemporaryDirectory() as root:
            store = EvidenceStore(Path(root) / "run")
            store.save("first", {"token": "secret", "url": "https://example.com/a?signature=secret"}, {"source": "test"})
            result = json.loads((store.root / "first.json").read_text())
            self.assertEqual(result["token"], "[REDACTED]")
            self.assertNotIn("signature", result["url"])
            with self.assertRaises(FileExistsError):
                store.save("first", {}, {})
            with self.assertRaises(AuditError):
                store.save("../escape", {}, {})

    def test_failure_keeps_unknowns(self):
        result = summarize([{"status": "FAIL"}, {"status": "UNKNOWN"}])
        self.assertEqual(result["exit_code"], 1)
        self.assertEqual(result["counts"]["UNKNOWN"], 1)

    def test_independent_row_count_catches_silent_chunking(self):
        payload = {"success": True, "columns": ["Airtable_ID"], "rows": [["a"]], "row_count": 1}
        self.assertEqual(extract_rows(payload, 1), [{"Airtable_ID": "a"}])
        with self.assertRaises(AuditError):
            extract_rows(payload, 2)
        payload["rows"].append(["b", "unexpected"])
        payload["row_count"] = 2
        with self.assertRaises(AuditError):
            extract_rows(payload, 2)

    def test_partition_overlap_rejected(self):
        payload = {"success": True, "columns": ["Airtable_ID"], "rows": [["a"]], "row_count": 1}
        with self.assertRaises(AuditError):
            reconcile_dbx({}, {}, [(payload, 1), (payload, 1)], 2, 1)

    def test_partition_totals_rejected(self):
        payload = {"success": True, "columns": ["Airtable_ID"], "rows": [["a"]], "row_count": 1}
        with self.assertRaises(AuditError):
            reconcile_dbx({}, {}, [(payload, 1)], 2, 2)

    def test_reference_links_not_replacement_targets(self):
        self.halt["fields"].append({"id": "reason", "name": "Demotion Reason_Old", "type": "multipleRecordLinks",
                                   "options": {"linkedTableId": "reasons", "inverseLinkFieldId": "back"}})
        self.before[0]["fields"]["reason"] = ["DR10"]
        self.assertEqual(len(self.check_edges({"primary": ["original"]})), 1)

    def test_csv_duplicate_rows_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "input.csv"
            path.write_text('Halt Code,Reason\n3.1,DR1\n3.1,DR10\n')
            self.assertEqual(len(load_payload(path)["csv_rows"]), 2)

    def test_schema_discovers_new_links(self):
        for i in range(19):
            self.prod["fields"].append({"id": f"new{i}", "name": "copy", "type": "multipleRecordLinks",
                                       "options": {"linkedTableId": "halt"}})
        graph = build_schema_graph([self.halt, self.prod])
        self.assertEqual(len(graph["links"]), 21)

    def test_55_deleted_id_candidates_not_current_suffix(self):
        before = [{"id": f"deleted{i}", "fields": {"code": "3.1_Duplicate", "reverse": ["event"]}} for i in range(55)]
        result = edge_findings(before, self.originals, {"prod": [{"id": "event", "fields": {"primary": ["original"]}}]},
                              build_schema_graph([self.halt, self.prod]), "halt", "code", "tag")
        self.assertEqual(len(result), 55)
        self.assertTrue(all(r["status"] == "PASS" for r in result))

    def test_sql_side_effect_functions_rejected(self):
        for sql in ["SELECT http_request('https://example.com')", "SELECT java_method('x')", "SELECT ai_query('x','y')"]:
            with self.assertRaises(AuditError):
                validate_sql(sql)

    def test_recovery_requires_classification_not_only_masking(self):
        baseline = {"record_id": "a", "before_day_utc": {"manual_demotion_masking": "Manual Mask",
                    "confirmed_demotion_type": ["Unintended Vehicle Demotion"]}}
        live = {"id": "a", "fields": {"Manual Demotion Masking": "Manual Mask",
                "Confirmed Demotion Type": ["Intended Manual Demotion"]}}
        result = verify_recovery([baseline], [live], [], [])
        self.assertEqual(result["summary"]["manual_mask_count"], 1)
        self.assertEqual(result["summary"]["status_counts"], {"REVIEW": 1})
        live["fields"]["Confirmed Demotion Type"] = ["Unintended Vehicle Demotion"]
        result = verify_recovery([baseline], [live], [], [])
        self.assertEqual(result["summary"]["status_counts"], {"MATCH": 1})
        self.assertEqual(result["summary"]["databricks_matches_airtable"], 0)

    def test_recovery_missing_record_is_not_success(self):
        result = verify_recovery([{"record_id": "missing", "before_day_utc": {}}], [], [], [])
        self.assertEqual(result["summary"]["status_counts"], {"UNKNOWN": 1})

    def test_recovery_keeps_manual_override_and_null_assessment(self):
        baseline = {"record_id": "a", "before_day_utc": {"main_demotion_code": "12.X2"}}
        live = {"id": "a", "fields": {"MAIN Demotion Code": ["halt"], "Operator Error or Misuse": "No Operator Error or Misuse"}}
        result = verify_recovery([baseline], [live], [{"id": "halt", "fields": {"Halt Code": "12.111"}}], [])
        differences = result["summary"]["baseline_difference_counts"]
        self.assertEqual(differences["main_demotion_code"], 1)
        self.assertEqual(differences["operator_error_or_misuse"], 1)

    def test_sync_projection_keeps_raw_arrays_and_detects_stale_masking(self):
        baseline = {"record_id": "a", "before_day_utc": {"secondary_demotion": "12.111"}}
        live = {"id": "a", "fields": {"Secondary Demotion Manual": ["raw", "classified"]}}
        halts = [{"id": "raw", "fields": {"Halt Code": "12.111"}}, {"id": "classified", "fields": {"Halt Code": "12.X2"}}]
        dbx = {"Airtable_ID": "a", "secondary_demotion": "12.111"}
        result = verify_recovery([baseline], [live], halts, [dbx])
        self.assertEqual(result["summary"]["databricks_matches_airtable"], 0)
        self.assertEqual(result["summary"]["databricks_matches_sync_projection"], 1)
        self.assertEqual(result["records"][0]["actual"]["secondary_demotion"], ["12.111", "12.X2"])
        dbx["manual_demotion_masking"] = "Intended Manual Demotion - No Mask"
        result = verify_recovery([baseline], [live], halts, [dbx])
        self.assertEqual(result["summary"]["databricks_matches_sync_projection"], 0)
        self.assertEqual(result["summary"]["sync_exceptions"][0]["differences"][0]["field_id"], "manual_demotion_masking")

    def test_load_json_and_numbered_transcript(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "input"
            path.write_text('1|{\n2|  "records": []\n3|}')
            self.assertEqual(load_payload(path), {"records": []})
            path.write_text('output truncated')
            with self.assertRaises(AuditError):
                load_payload(path)


if __name__ == "__main__":
    unittest.main()
