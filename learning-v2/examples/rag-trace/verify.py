"""Recompute the educational U13 trace using only Python's standard library."""

import json
from math import hypot
from pathlib import Path


directory = Path(__file__).resolve().parent
fixture = json.loads((directory / "trace.json").read_text(encoding="utf-8"))
lesson = (
    directory.parent.parent / "units" / "U13" / "01-retrieval-trace.md"
).read_text(encoding="utf-8")


def eligible(document, date):
    return (
        document["equipment"] in (fixture["equipment"], "ALL")
        and (document["effectiveFrom"] is None or document["effectiveFrom"] <= date)
        and (
            document["effectiveUntilExclusive"] is None
            or date < document["effectiveUntilExclusive"]
        )
    )


def cosine_score(chunk):
    query = fixture["queryVector"]
    vector = chunk["vector"]
    dot_product = sum(left * right for left, right in zip(query, vector, strict=True))
    return dot_product / (hypot(*query) * hypot(*vector))


def lexical_score(chunk):
    return sum(
        weight for term, weight in fixture["lexicalTerms"].items() if term in chunk["text"]
    )


def top_ids(chunks, score):
    ranking = sorted(chunks, key=lambda chunk: (-score(chunk), chunk["id"]))
    return [chunk["id"] for chunk in ranking[:fixture["topK"]]]


def trace(chunks):
    vector = top_ids(chunks, cosine_score)
    lexical = top_ids(chunks, lexical_score)
    fusion_scores = {}
    for ranking in (vector, lexical):
        for position, chunk_id in enumerate(ranking, start=1):
            fusion_scores[chunk_id] = fusion_scores.get(chunk_id, 0.0) + 1 / (
                fixture["rrfConstant"] + position
            )
    fused = sorted(fusion_scores, key=lambda chunk_id: (-fusion_scores[chunk_id], chunk_id))
    by_id = {chunk["id"]: chunk for chunk in chunks}
    # In this fixture, ID order also places the criterion before the record instructions.
    reranked = sorted(fused, key=lambda chunk_id: (-by_id[chunk_id]["rerank"], chunk_id))
    remaining = fixture["evidenceCharacterBudget"]
    context = []
    for chunk_id in reranked:
        length = len(by_id[chunk_id]["text"])
        if length <= remaining:
            remaining -= length
            context.append(chunk_id)
    return {
        "vector": vector,
        "lexical": lexical,
        "fused": [(chunk_id, f"{fusion_scores[chunk_id]:.5f}") for chunk_id in fused],
        "reranked": reranked,
        "context": context,
        "remaining": remaining,
    }


def main():
    documents = fixture["documents"]
    all_chunks = [chunk for document in documents for chunk in document["chunks"]]
    assert len(documents) == 6 and len(all_chunks) == 7
    unfiltered = sorted(all_chunks, key=lambda chunk: (-cosine_score(chunk), chunk["id"]))
    cosines = [(chunk["id"], f"{cosine_score(chunk):.4f}") for chunk in unfiltered]
    assert cosines == [
        ("D01a", "0.9950"), ("D03a", "0.9864"), ("D05a", "0.9701"),
        ("D02b", "0.9487"), ("D02a", "0.8944"), ("D06a", "0.7071"),
        ("D04a", "0.5547"),
    ]
    current = [
        chunk for document in documents if eligible(document, fixture["asOf"])
        for chunk in document["chunks"]
    ]
    current_ids = {chunk["id"] for chunk in current}
    prior_ids = {document["id"] for document in documents if eligible(document, "2026-02-15")}
    assert prior_ids & {"D01", "D02", "D04"} == {"D01"}
    postfiltered = [chunk_id for chunk_id in top_ids(all_chunks, cosine_score) if chunk_id in current_ids]
    assert postfiltered == ["D05a"]
    assert {chunk["id"]: lexical_score(chunk) for chunk in current} == {
        "D02a": 5, "D02b": 1, "D04a": 6, "D05a": 3, "D06a": 2,
    }

    standard = trace(current)
    assert standard == {
        "vector": ["D05a", "D02b", "D02a"],
        "lexical": ["D04a", "D02a", "D05a"],
        "fused": [
            ("D05a", "0.03227"), ("D02a", "0.03200"),
            ("D04a", "0.01639"), ("D02b", "0.01613"),
        ],
        "reranked": ["D02a", "D04a", "D05a", "D02b"],
        "context": ["D02a", "D04a"],
        "remaining": 12,
    }
    for chunk in current:
        if chunk["id"] in standard["context"]:
            assert chunk["text"] in lesson

    variant = fixture["boundaryVariant"]
    first, second = variant["chunks"]
    assert (f"{cosine_score(first):.4f}", lexical_score(first), len(first["text"])) == ("0.7071", 5, 36)
    assert (f"{cosine_score(second):.4f}", lexical_score(second)) == ("0.2425", 0)
    split = trace([chunk for chunk in current if chunk["id"] != variant["replaces"]] + variant["chunks"])
    assert split == {
        "vector": ["D05a", "D02b", "D02-s1"],
        "lexical": ["D04a", "D02-s1", "D05a"],
        "fused": [
            ("D05a", "0.03227"), ("D02-s1", "0.03200"),
            ("D04a", "0.01639"), ("D02b", "0.01613"),
        ],
        "reranked": ["D04a", "D02-s1", "D05a", "D02b"],
        "context": ["D04a", "D02-s1"],
        "remaining": 23,
    }
    print(json.dumps({
        "unfilteredCosines": cosines,
        "postfilteredTopK": postfiltered,
        "standard": standard,
        "boundarySplit": split,
    }, indent=2))


if __name__ == "__main__":
    main()
