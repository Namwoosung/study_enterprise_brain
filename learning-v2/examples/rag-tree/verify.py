import json
from math import isclose
from pathlib import Path

fixture = json.loads(Path(__file__).with_name("tree.json").read_text(encoding="utf-8"))
nodes = fixture["nodes"]


def ranked(candidates, question):
    return sorted(candidates, key=lambda node_id: (-nodes[node_id]["score"][question], node_id))


def traversal(question, k):
    root_layer = max(node["layer"] for node in nodes.values())
    candidates = [node_id for node_id, node in nodes.items() if node["layer"] == root_layer]
    selected = []
    while candidates:
        current = ranked(candidates, question)[:k]
        selected.extend(current)
        candidates = list(dict.fromkeys(
            child for parent in current for child in nodes[parent]["children"]
        ))
    return selected


def collapsed(question, budget):
    selected = []
    length = 0
    for node_id in ranked(nodes, question):
        node_length = nodes[node_id]["length"]
        if length + node_length > budget:
            break
        selected.append(node_id)
        length += node_length
    return selected, length


def main():
    for leaf_id, probabilities in fixture["memberships"].items():
        assert isclose(sum(probabilities), 1.0)
        expected_parents = [
            parent for parent, probability in zip(fixture["topic_parents"], probabilities)
            if probability > fixture["membership_threshold"]
        ]
        assert expected_parents == [
            parent for parent in fixture["topic_parents"] if leaf_id in nodes[parent]["children"]
        ]
    for parent in nodes.values():
        assert all(nodes[child]["layer"] == parent["layer"] - 1 for child in parent["children"])
    budget = fixture["budget"]
    narrow_path = traversal("narrow", k=1)
    assert narrow_path == ["R1", "S2", "T03"]
    assert sum(nodes[node_id]["length"] for node_id in narrow_path) == budget
    assert traversal("narrow", k=2) == ["R1", "S2", "S1", "T03", "T02"]
    broad_path = traversal("broad", k=1)
    assert broad_path == ["R1", "S1", "T01"]
    assert sum(nodes[node_id]["length"] for node_id in broad_path) == 84
    assert collapsed("narrow", budget) == (["T03", "T02"], 77)
    assert collapsed("broad", budget) == (["R1", "S1", "S2"], 96)
    assert collapsed("narrow", 65) == (["T03"], 35)
    print("Synthetic tree memberships, traversal, and collapsed budgets: OK")


if __name__ == "__main__":
    main()
