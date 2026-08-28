QUESTION_STARTERS = {
    "who",
    "whom",
    "whose",
    "what",
    "when",
    "where",
    "which",
    "why",
    "how",
    "is",
    "are",
    "was",
    "were",
    "do",
    "does",
    "did",
    "can",
    "could",
    "should",
    "would",
}


def looks_like_question(user_input):
    normalized_input = user_input.strip().lower()

    if not normalized_input:
        return False

    first_word = normalized_input.split()[0].strip(".,!?;:")

    return normalized_input.endswith("?") or first_word in QUESTION_STARTERS


def validate_fact_check_input(user_input):
    if not user_input or not user_input.strip():
        return {
            "is_valid": False,
            "reason": "Please enter a factual claim.",
        }

    if looks_like_question(user_input):
        return {
            "is_valid": False,
            "reason": (
                "This system verifies factual claims, but your input looks like a "
                "question. Please rewrite it as a claim. Example: "
                '"Spain won the FIFA 2026 World Cup."'
            ),
        }

    return {
        "is_valid": True,
        "reason": "",
    }
