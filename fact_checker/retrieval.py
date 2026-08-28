import re


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


def get_meaningful_words(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {word for word in words if len(word) > 2 and word not in STOPWORDS}


def get_numbers(text):
    return set(re.findall(r"\d+", text))


def score_evidence_item(claim, evidence_item):
    claim_words = get_meaningful_words(claim)
    evidence_words = get_meaningful_words(evidence_item["text"])
    shared_words = claim_words & evidence_words
    relevance_score = len(shared_words)
    claim_numbers = get_numbers(claim)
    evidence_numbers = get_numbers(evidence_item["text"])
    shared_numbers = claim_numbers & evidence_numbers
    conflicting_numbers = claim_numbers - evidence_numbers
    number_conflict = bool(claim_numbers and evidence_numbers and conflicting_numbers)
    source_score = evidence_item.get("source_score", 0.0)
    combined_score = relevance_score + (len(shared_numbers) * 2) + (source_score * 0.1)

    return {
        "combined_score": combined_score,
        "relevance_score": relevance_score,
        "shared_words": shared_words,
        "claim_numbers": claim_numbers,
        "evidence_numbers": evidence_numbers,
        "shared_numbers": shared_numbers,
        "conflicting_numbers": conflicting_numbers,
        "number_conflict": number_conflict,
    }


def retrieve_evidence(claim, evidence_store, top_k=2, min_relevance_score=1):
    scored_items = []

    for evidence_item in evidence_store:
        score = score_evidence_item(claim, evidence_item)
        scored_items.append(
            {
                **score,
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
        if (
            scored["relevance_score"] >= min_relevance_score
            or scored["number_conflict"]
        )
    ]

    return relevant_items[:top_k]


def retrieve_evidence_with_diagnostics(claim, evidence_store, top_k=2, min_relevance_score=1):
    scored_items = []

    for evidence_item in evidence_store:
        score = score_evidence_item(claim, evidence_item)
        scored_items.append(
            {
                **score,
                "item": evidence_item,
            }
        )

    scored_items.sort(
        key=lambda scored_item: scored_item["combined_score"],
        reverse=True,
    )

    selected_items = [
        scored
        for scored in scored_items
        if (
            scored["relevance_score"] >= min_relevance_score
            or scored["number_conflict"]
        )
    ][:top_k]

    evidence_items = [scored["item"] for scored in selected_items]
    diagnostics = [
        {
            "evidence_id": scored["item"]["id"],
            "combined_score": scored["combined_score"],
            "relevance_score": scored["relevance_score"],
            "shared_words": sorted(scored["shared_words"]),
            "claim_numbers": sorted(scored["claim_numbers"]),
            "evidence_numbers": sorted(scored["evidence_numbers"]),
            "shared_numbers": sorted(scored["shared_numbers"]),
            "conflicting_numbers": sorted(scored["conflicting_numbers"]),
            "number_conflict": scored["number_conflict"],
        }
        for scored in selected_items
    ]

    return evidence_items, diagnostics
