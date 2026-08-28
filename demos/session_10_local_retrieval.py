import re

from session_08_cited_fact_checker import check_claim_with_citations
from session_09_validate_citations import validate_citation_ids


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "known",
    "of",
    "on",
    "or",
    "the",
    "to",
    "was",
}

LOCAL_EVIDENCE_STORE = [
    {
        "id": "evidence_1",
        "title": "Eiffel Tower Location Note",
        "source_type": "local_demo_fact",
        "source_quality": "demo_verified",
        "source_score": 0.8,
        "url": "local://eiffel-tower-location",
        "text": "The Eiffel Tower is a landmark in Paris, France.",
    },
    {
        "id": "evidence_2",
        "title": "Berlin Capital Note",
        "source_type": "local_demo_fact",
        "source_quality": "demo_verified",
        "source_score": 0.8,
        "url": "local://berlin-capital",
        "text": "Berlin is the capital city of Germany.",
    },
    {
        "id": "evidence_3",
        "title": "Mars Nickname Note",
        "source_type": "local_demo_fact",
        "source_quality": "demo_verified",
        "source_score": 0.8,
        "url": "local://mars-red-planet",
        "text": "Mars is often called the Red Planet because of its reddish appearance.",
    },
    {
        "id": "evidence_4",
        "title": "Brazil Coffee Note",
        "source_type": "local_demo_fact",
        "source_quality": "demo_partial",
        "source_score": 0.5,
        "url": "local://brazil-coffee",
        "text": "Coffee is widely grown in Brazil today.",
    },
    {
        "id": "evidence_5",
        "title": "FIFA World Cup 2022 Winner Note",
        "source_type": "local_demo_fact",
        "source_quality": "demo_verified",
        "source_score": 0.8,
        "url": "local://fifa-world-cup-2022-winner",
        "text": "Argentina won the 2022 FIFA World Cup.",
    },
]


def get_meaningful_words(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


def score_evidence_item(claim, evidence_item):
    claim_words = get_meaningful_words(claim)
    evidence_words = get_meaningful_words(evidence_item["text"])
    shared_words = claim_words & evidence_words
    relevance_score = len(shared_words)
    source_score = evidence_item.get("source_score", 0.0)
    combined_score = relevance_score + (source_score * 0.1)

    return combined_score, relevance_score, shared_words


def retrieve_evidence(claim, evidence_store, top_k=2):
    scored_items = []

    for evidence_item in evidence_store:
        combined_score, relevance_score, shared_words = score_evidence_item(
            claim,
            evidence_item,
        )
        scored_items.append(
            {
                "combined_score": combined_score,
                "relevance_score": relevance_score,
                "shared_words": shared_words,
                "item": evidence_item,
            }
        )

    scored_items.sort(
        key=lambda scored_item: scored_item["combined_score"],
        reverse=True,
    )
    relevant_items = [
        scored["item"]
        for scored in scored_items
        if scored["relevance_score"] > 0
    ]

    return relevant_items[:top_k]


def main():
    claim = "The Eiffel Tower is in Berlin."

    print("SESSION 10 DEMO: Local retrieval")
    print("=" * 48)

    retrieved_evidence = retrieve_evidence(claim, LOCAL_EVIDENCE_STORE)

    print("Claim:")
    print(claim)

    print("\nRetrieved evidence:")
    for evidence_item in retrieved_evidence:
        print(
            f"- {evidence_item['id']} ({evidence_item['title']}): "
            f"{evidence_item['text']} "
            f"[quality={evidence_item['source_quality']}, "
            f"score={evidence_item['source_score']}]"
        )

    result = check_claim_with_citations(claim, retrieved_evidence)
    citation_errors = validate_citation_ids(result, retrieved_evidence)

    print("\nModel result:")
    print(f"Verdict: {result.get('verdict')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Citation IDs: {result.get('citation_ids')}")
    print(f"Explanation: {result.get('explanation')}")
    print(f"Citation validation: {'PASS' if not citation_errors else 'FAIL'}")

    if citation_errors:
        print("Citation errors:")
        for error in citation_errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
