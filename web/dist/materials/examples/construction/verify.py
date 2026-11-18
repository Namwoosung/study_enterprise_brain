"""Check the U09–U11 synthetic examples with the Python standard library."""

import json
import sqlite3
import sys
from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def source_checks():
    fixture = load("sources.json")
    registry = fixture["registry"]
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            "CREATE TABLE zones (facility_id TEXT, zone_code TEXT, label TEXT)"
        )
        connection.execute(
            "CREATE TABLE assets (facility_id TEXT, serial_no TEXT, "
            "local_label TEXT, zone_code TEXT, status_code TEXT)"
        )
        connection.executemany("INSERT INTO zones VALUES (?, ?, ?)", registry["locations"])
        connection.executemany("INSERT INTO assets VALUES (?, ?, ?, ?, ?)", registry["assets"])
        mapped = connection.execute("""
            SELECT a.facility_id, a.serial_no, z.label
            FROM assets AS a LEFT JOIN zones AS z
                 ON a.facility_id = z.facility_id AND a.zone_code = z.zone_code
            ORDER BY a.facility_id, a.serial_no
            """).fetchall()
        wrong = connection.execute("""
            SELECT z.label FROM assets AS a JOIN zones AS z ON a.zone_code = z.zone_code
            WHERE a.facility_id = 'N' AND a.serial_no = 'A017'
            ORDER BY z.facility_id
            """).fetchall()
    assert mapped == [("N", "A017", "북동 N03"), ("N", "A018", None), ("S", "A055", "남동 N03")]
    assert wrong == [("북동 N03",), ("남동 N03",)]

    observation, missing = registry["observations"]
    assert observation[5] == missing[5] == "mW"
    watts = Decimal(observation[4]) / 1000
    assert watts == Decimal("1.3")
    assert missing[4] is None and missing[6] == "M"

    document = fixture["maintenance"]
    for span in [*document["spans"].values(), *document["event_triggers"]]:
        sentence = document["sentences"][span["sentence"] - 1]
        assert sentence[span["start"]:span["end"]] == span["text"], span
    assert len(document["spans"]) == 13
    manual = fixture["manual"]
    assert manual["rows"][0] == ["A-17", "신호 탭¹", "모듈 M7"]
    assert "Q 시리즈" in manual["caption"] and "표시 소프트웨어 3.2" in manual["footnote"]

    predicted = set(fixture["evaluation"]["predicted"])
    reference = set(fixture["evaluation"]["reference"])
    hits = predicted & reference
    precision = Fraction(len(hits), len(predicted))
    recall = Fraction(len(hits), len(reference))
    assert precision == recall == Fraction(3, 5)
    assert len(predicted - reference) == len(reference - predicted) == 2
    return {
        "registry_rows": len(mapped),
        "bad_join_zones": [row[0] for row in wrong],
        "watts": str(watts),
        "source_spans": len(document["spans"]),
        "event_trigger_spans": len(document["event_triggers"]),
        "claim_precision": str(precision),
        "claim_recall": str(recall),
    }


def same_group_pairs(groups):
    return {pair for group in groups for pair in combinations(sorted(group), 2)}


def connected_components(ids, edges):
    neighbors = {record_id: set() for record_id in ids}
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    groups = set()
    unseen = set(ids)
    while unseen:
        pending = [unseen.pop()]
        group = set()
        while pending:
            record = pending.pop()
            group.add(record)
            new = neighbors[record] & unseen
            pending.extend(new)
            unseen.difference_update(new)
        groups.add(frozenset(group))
    return groups


def resolution_checks():
    fixture = load("resolution.json")
    records = [dict(zip(fixture["header"], row, strict=True)) for row in fixture["records"]]
    ids = [record["id"] for record in records]
    blocks = defaultdict(set)
    for record in records:
        record_id = record["id"]
        if record["kind"] == "asset":
            if record["facility"] and record["serial"]:
                blocks["serial", record["facility"], record["serial"]].add(record_id)
            normalized = record["label"].replace("-", "").replace(" ", "").upper()
            blocks["asset_label", normalized].add(record_id)
        elif record["slot"]:
            blocks["part_slot", record["slot"]].add(record_id)
    candidates = same_group_pairs(blocks.values())
    assert candidates == {tuple(sorted(pair)) for pair in fixture["blocking_expected"]}
    assert len(ids) == 10 and len(set(ids)) == 10
    full_pairs = len(same_group_pairs([ids]))
    assert full_pairs == 45 and len(candidates) == 9

    decisions = {
        state: {tuple(sorted(edge)) for edge in edges}
        for state, edges in fixture["initial_decisions"].items()
    }
    assert decisions["match"] | decisions["review"] | decisions["reject"] == candidates
    assert sum(map(len, decisions.values())) == len(candidates)
    reference_pairs = same_group_pairs(fixture["reference_groups"])
    missing = reference_pairs - candidates
    assert missing == {("R5", "R6")}
    assert len(candidates & reference_pairs) == 4 and len(reference_pairs) == 5
    assert len(candidates | missing) == 10

    approved = {tuple(sorted(edge)) for edge in fixture["reviewed_edges"]}
    false_bridge = tuple(sorted(fixture["false_bridge"]))
    mixed = connected_components(ids, approved | {false_bridge})
    errors = same_group_pairs(mixed) - reference_pairs
    assert len(errors) == 6
    corrected = connected_components(ids, approved)
    assert corrected == {frozenset(group) for group in fixture["reference_groups"]}
    assert any({"R3", "R4"} == group for group in corrected)
    assert any({"R1", "R2", "R10"} == group for group in corrected)
    return {
        "all_pairs": full_pairs,
        "blocked_candidates": len(candidates),
        "found_reference_pairs": len(candidates & reference_pairs),
        "total_reference_pairs": len(reference_pairs),
        "candidates_with_crosswalk": len(candidates | missing),
        "bad_equivalences_after_bridge": len(errors),
        "groups_after_correction": sorted(sorted(group) for group in corrected),
    }


def quality_checks():
    fixture = load("quality.json")
    daily = fixture["daily"]
    high = daily["high"]
    medium = daily["medium"]
    low = daily["low"]
    surviving = high["count"] + medium["count"] + low["count"]
    assert daily["intake"] - daily["quarantined"] == surviving == 216
    capacity = daily["reviewers"] * daily["minutes_per_reviewer"]
    mandatory = high["count"] * high["minutes"] + medium["count"] * medium["minutes"]
    full = mandatory + low["count"] * low["minutes"]
    minimum_deferred = surviving - capacity // min(high["minutes"], medium["minutes"], low["minutes"])
    audited = mandatory + daily["audits"] * low["minutes"]
    assert (capacity, full, full - capacity, minimum_deferred, audited, capacity - audited) == (
        360, 936, 576, 126, 344, 16,
    )
    spiked_mandatory = mandatory + daily["high_spike"] * high["minutes"]
    spiked = spiked_mandatory + daily["audits"] * low["minutes"]
    assert spiked == 404 and spiked_mandatory - capacity == 12
    assert audited + daily["double_reviews"] * high["minutes"] == 368

    assert sum(stratum["population"] for stratum in fixture["audit"]) == low["count"]
    assert sum(stratum["sample"] for stratum in fixture["audit"]) == daily["audits"]
    weighted_errors = sum(
        Fraction(stratum["population"], low["count"]) * Fraction(stratum["errors"], stratum["sample"])
        for stratum in fixture["audit"]
    )
    assert weighted_errors == Fraction(1, 13)
    for timestamps in fixture["time_checks"]:
        local = datetime.fromisoformat(timestamps["local"])
        assert local.astimezone(UTC).isoformat() == timestamps["utc"]
    return {
        "capacity_minutes": capacity,
        "all_reviews_minutes": full,
        "mandatory_and_audit_minutes": audited,
        "spike_minutes": spiked,
        "weighted_sample_error_estimate": str(weighted_errors),
        "timezone_checks": len(fixture["time_checks"]),
    }


if __name__ == "__main__":
    report = {
        "python": sys.version.split()[0],
        "sqlite": sqlite3.sqlite_version,
        "source_checks": source_checks(),
        "resolution_checks": resolution_checks(),
        "quality_checks": quality_checks(),
    }
    print(json.dumps(report, ensure_ascii=True, indent=2))
