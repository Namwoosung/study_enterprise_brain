import json
from fractions import Fraction
from pathlib import Path
from statistics import mean

directory = Path(__file__).resolve().parent


def read_fixture(path):
    return json.loads(path.read_text(encoding="utf-8"))


fixture = read_fixture(directory / "evaluation.json")


def retrieval_scores(ranked, gold, k):
    top = ranked[:k]
    retained = set(top) & gold
    first = next((index for index, item in enumerate(top, start=1) if item in gold), None)
    return (
        Fraction(len(retained), k),
        Fraction(len(retained), len(gold)) if gold else None,
        Fraction(1, first) if first else Fraction(0)
    )


def citation_scores(claims, context):
    required = [claim for claim in claims if claim["requires_citation"]]
    faithful = sum(bool(set(claim["support"]) & context) for claim in claims)
    cited = sum(bool(set(claim["citations"]) & set(claim["support"])) for claim in required)
    links = [item in claim["support"] for claim in claims for item in claim["citations"]]
    return Fraction(faithful, len(claims)), Fraction(cited, len(required)), Fraction(sum(links), len(links))


def main():
    trace = read_fixture(directory.parent / "rag-trace" / "trace.json")
    graph = read_fixture(directory.parent / "rag-graph" / "graph.json")
    tree = read_fixture(directory.parent / "rag-tree" / "tree.json")
    known = ({chunk["id"] for doc in trace["documents"] for chunk in doc["chunks"]}
             | set(graph["sources"])
             | {node_id for node_id, node in tree["nodes"].items() if node["layer"] == 0})
    question_map = {question["id"]: question for question in fixture["questions"]}
    for question in fixture["questions"]:
        assert question["answerable"] == bool(question["gold"])
        assert set(question["gold"]) <= known
        for ranking in question["rankings"].values():
            assert set(ranking) <= known and len(set(ranking)) == len(ranking)

    expected = {"Vector": (Fraction(3, 4), 1), "Graph": (Fraction(19, 20), Fraction(9, 10)),
                "Tree": (Fraction(9, 10), 1)}
    for method, expected_averages in expected.items():
        metrics = [
            retrieval_scores(question["rankings"][method], set(question["gold"]), k=4)
            for question in fixture["questions"] if question["answerable"]
        ]
        _, recall, reciprocal_rank = zip(*metrics)
        assert (mean(recall), mean(reciprocal_rank)) == expected_averages
        print(method, "recall@4", float(mean(recall)), "MRR@4", float(mean(reciprocal_rank)))

    q2 = question_map["Q2"]
    assert retrieval_scores(q2["rankings"]["Tree"], set(q2["gold"]), k=2) == (
        Fraction(1, 2), Fraction(1, 4), 1
    )
    q3 = question_map["Q3"]
    assert retrieval_scores(q3["rankings"]["Vector"], set(q3["gold"]), k=2)[1] == Fraction(1, 2)
    assert retrieval_scores(q3["rankings"]["Vector"], set(q3["gold"]), k=4)[1] == 1
    assert retrieval_scores(question_map["Q6"]["rankings"]["Vector"], set(), k=4)[1] is None

    example = fixture["generated_example"]
    claims = example["claims"]
    context = set(example["context"])
    assert context <= known
    assert citation_scores(claims, context) == (Fraction(3, 4), Fraction(1, 2), Fraction(1, 2))
    corrected = [
        {**claim, "citations": ["D04a"]} if claim["id"] == "A3" else claim
        for claim in claims
    ]
    assert citation_scores(corrected, context) == (Fraction(3, 4),) * 3
    assert citation_scores(corrected[:3], context) == (1, 1, 1)
    print("Retrieval and answer citation arithmetic: OK")


if __name__ == "__main__":
    main()
