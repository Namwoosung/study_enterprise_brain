"""Verify the U12 teaching fixture without model or ontology engine dependencies."""

import json
from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parent


def ancestors(class_id, inclusion_edges):
    """Return types entailed by only the fixture's named-class inclusions."""
    found = {class_id}
    pending = [class_id]
    while pending:
        current = pending.pop()
        for narrower, broader in inclusion_edges:
            if narrower == current and broader not in found:
                found.add(broader)
                pending.append(broader)
    return found


def summarize(fixture, model_version):
    baseline, change = fixture["baseline"], fixture["change"]
    edges = baseline["subclass_of"]
    if model_version == change["version"]:
        edges = edges + change["subclass_of_added"]
        registered_types = change["source_mapping_types"]
    else:
        registered_types = {}

    process_equipment = [
        unit["id"]
        for unit in fixture["units"]
        if "ProcessEquipment" in ancestors(unit["type"], edges)
    ]
    equipment_entries = [
        (entry, registered_types.get(entry["source_kind"], "InspectionEntry"))
        for entry in fixture["entries"]
        if entry["equipment"] == "E-17" and entry["date"].startswith("2026-10-")
    ]
    assert all("InspectionEntry" in ancestors(kind, edges) for _, kind in equipment_entries)
    if not registered_types:
        return {"Q1": None, "Q2": process_equipment, "Q3": None}

    records = [
        entry for entry, kind in equipment_entries
        if kind == "InspectionRecord" and entry["status"] == "final"
    ]
    requests = [
        entry for entry, kind in equipment_entries
        if kind == "InspectionRequest" and entry["status"] == "received"
    ]
    latest = max(records, key=lambda entry: entry["date"])
    return {
        "Q1": {"id": latest["id"], "outcome": latest["outcomes"][0]},
        "Q2": process_equipment,
        "Q3": {"final_records": len(records), "received_requests": len(requests)},
    }


def outcome_check(entry, policy):
    if (
        entry["source_kind"] != "inspection_record"
        or entry["status"] != "final"
        or entry["issue_origin"] != "new"
        or entry["date"] < policy["new_issue_effective_from"]
    ):
        return "out_of_scope"

    count = len(entry["outcomes"])
    if policy["final_outcome_min"] <= count <= policy["final_outcome_max"]:
        return "pass"
    return "violation"


def compare_join_grain():
    with sqlite3.connect(":memory:") as connection:
        connection.executescript("""
            CREATE TABLE lines (order_id TEXT, line_id TEXT, amount INTEGER);
            CREATE TABLE channel_events (order_id TEXT, event_id TEXT);
            INSERT INTO lines VALUES ('O-8', 'A', 80), ('O-8', 'B', 20);
            INSERT INTO channel_events VALUES ('O-8', 'shipment'), ('O-8', 'collection');
        """)
        raw = connection.execute("SELECT COUNT(*), SUM(amount) FROM lines").fetchone()
        joined = connection.execute("""
            SELECT COUNT(*), SUM(lines.amount)
            FROM lines JOIN channel_events USING (order_id)
        """).fetchone()
    return {"line_count_and_sum": raw, "joined_row_count_and_sum": joined}


def main():
    fixture = json.loads((ROOT / "inspection.json").read_text(encoding="utf-8"))
    lesson = (ROOT.parent.parent / "units" / "U12" / "02-documents-to-ontology.md").read_text(
        encoding="utf-8"
    )
    for document_id, line in fixture["documents"].items():
        assert f"| {document_id} |" in lesson and line in lesson
    for decision_id, decision in fixture["candidate_decisions"].items():
        assert f"| {decision_id} |" in lesson
        assert all(location in fixture["documents"] for location in decision["evidence"])

    old = summarize(fixture, "1.0")
    new = summarize(fixture, "1.1")
    assert old == {"Q1": None, "Q2": [], "Q3": None}
    assert new == {
        "Q1": {"id": "I-51", "outcome": "적합"},
        "Q2": ["E-17", "E-18"],
        "Q3": {"final_records": 2, "received_requests": 1},
    }

    edges = fixture["baseline"]["subclass_of"] + fixture["change"]["subclass_of_added"]
    assert "EtchEquipment" not in ancestors("ProcessEquipment", edges)
    rejected_edges = edges + [["ProcessEquipment", "EtchEquipment"]]
    assert "EtchEquipment" in ancestors("ProcessEquipment", rejected_edges)
    assert "ProcessEquipment" in ancestors("EtchEquipment", rejected_edges)

    confirmed, legacy, request = fixture["entries"]
    missing_outcome = {**confirmed, "id": "I-99", "outcomes": []}
    multiple_outcomes = {**confirmed, "id": "I-98", "outcomes": ["적합", "부적합"]}
    policy = fixture["change"]["validation"]
    checks = {
        entry["id"]: outcome_check(entry, policy)
        for entry in (confirmed, legacy, request, missing_outcome, multiple_outcomes)
    }
    assert checks == {
        "I-51": "pass",
        "I-43": "out_of_scope",
        "R-52": "out_of_scope",
        "I-99": "violation",
        "I-98": "violation",
    }

    grain = compare_join_grain()
    assert grain == {"line_count_and_sum": (2, 100), "joined_row_count_and_sum": (4, 200)}
    print(json.dumps({"v1.0": old, "v1.1": new, "outcome_checks": checks, "join_grain": grain},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
