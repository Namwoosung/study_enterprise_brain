"""Check the supplementary fixture with the existing U13 filter and corpus."""

import json

from verify import directory, eligible, fixture

supplement = json.loads((directory / "query-design.json").read_text(encoding="utf-8"))


def score(text, terms):
    return sum(weight for term, weight in terms.items() if term in text)


def main():
    documents = fixture["documents"] + supplement["additional_documents"]
    assert len(documents) == 8
    chunks = {
        chunk["id"]: chunk["text"]
        for doc in documents
        if eligible(doc, fixture["asOf"]) and doc.get("observedOn", "") <= fixture["asOf"]
        for chunk in doc["chunks"]
    }
    first = supplement["queries"]["A"]["terms"]
    second = supplement["queries"]["B"]["terms"]
    scores = {
        chunk_id: (score(text, first), score(text, second))
        for chunk_id, text in chunks.items()
    }
    assert scores == {
        "D02a": (8, 1), "D02b": (1, 1), "D04a": (1, 8), "D05a": (1, 1),
        "D06a": (0, 0), "D07a": (1, 1), "D08a": (1, 4)
    }
    selected = [
        min(scores, key=lambda chunk_id: (-scores[chunk_id][column], chunk_id))
        for column in range(2)
    ]
    assert selected == ["D02a", "D04a"]
    assert sum(len(chunks[chunk_id]) for chunk_id in selected) == 88
    shortened = {term: weight for term, weight in second.items() if term != "기록"}
    assert score(chunks["D04a"], shortened) == score(chunks["D08a"], shortened) == 4
    prior_manuals = [
        doc["id"] for doc in documents
        if doc["kind"] == "manual" and eligible(doc, "2026-02-15")
    ]
    assert prior_manuals == ["D01"]
    print("Two rewritten searches, exact evidence length, and historical date filter: OK")


if __name__ == "__main__":
    main()
