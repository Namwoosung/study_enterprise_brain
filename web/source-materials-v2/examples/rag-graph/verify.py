import json
from datetime import date
from pathlib import Path

fixture = json.loads(Path(__file__).with_name("graph.json").read_text(encoding="utf-8"))
sources = fixture["sources"]
relationships = fixture["relationships"]


def follow(edges, start, relation):
    return [(end, source) for origin, kind, end, source in edges
            if origin == start and kind == relation]


def valid_on(change, as_of):
    start, end = fixture["change_validity"][change]
    return date.fromisoformat(start) <= as_of and (end is None or as_of < date.fromisoformat(end))


def resolve_path(edges, work, alias, as_of):
    rows = []
    candidates = fixture["part_alias"][alias]
    for part, replacement_source in follow(edges, work, "REPLACED"):
        if part not in candidates:
            continue
        for change, change_source in follow(edges, part, "HAS_CHANGE"):
            if not valid_on(change, date.fromisoformat(as_of)):
                continue
            for supplier, supplier_source in follow(edges, change, "NEW_SUPPLIER"):
                for approver, approval_source in follow(edges, change, "APPROVED_BY"):
                    evidence = dict.fromkeys(
                        [replacement_source, candidates[part], change_source,
                         supplier_source, approval_source]
                    )
                    rows.append((part, change, supplier, approver, list(evidence)))
    return rows


def main():
    assert all(source in sources for _, _, _, source in relationships)
    current = resolve_path(relationships, "W-207", "현장 밸브", "2026-04-10")
    historical = resolve_path(relationships, "W-207", "현장 밸브", "2026-03-20")
    assert current == [("VL-042", "CR-119", "한빛정밀", "김하늘", ["G01", "G02", "G03", "G04"])]
    assert historical == [("VL-042", "CR-106", "세림밸브", "박정우", ["G01", "G02", "G05", "G06"])]
    assert resolve_path(relationships, "W-207", "현장 밸브", "2026-04-01") == current
    assert not resolve_path(relationships, "W-305", "현장 밸브", "2026-04-10")
    bad_edges = [edge for edge in relationships if edge[:2] != ["CR-119", "APPROVED_BY"]]
    bad_edges.append(["CR-119", "APPROVED_BY", "이별", "G09"])
    corrupted = resolve_path(bad_edges, "W-207", "현장 밸브", "2026-04-10")
    assert corrupted[0][3:] == ("이별", ["G01", "G02", "G03", "G09"])
    assert "CR-121" in sources["G09"][0] and "CR-119" not in sources["G09"][0]
    reports = fixture["reports"]
    assert all(ref in sources or ref in reports for report in reports.values() for ref in report["sources"])
    assert all(ref in sources for ref in fixture["local_context"]["text_units"])
    assert "한빛정밀" in reports["R-A2"]["text"]
    points = sorted(fixture["global_map_points"], key=lambda point: point[1], reverse=True)[:3]
    assert [(report, score) for report, score, _ in points] == [("R-A1", 90), ("R-B1", 88), ("R-A2", 84)]
    print("Graph path, dates, conflicting source, and simulated points: OK")


if __name__ == "__main__":
    main()
