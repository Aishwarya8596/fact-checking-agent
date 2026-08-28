def validate_citation_ids(result, evidence_items):
    errors = []

    citation_ids = result.get("citation_ids")
    if not isinstance(citation_ids, list):
        return ["citation_ids must be a list."]

    allowed_ids = {item["id"] for item in evidence_items}

    for citation_id in citation_ids:
        if not isinstance(citation_id, str):
            errors.append("Every citation ID must be a string.")
        elif citation_id not in allowed_ids:
            errors.append(f"Unknown citation ID: {citation_id}")

    return errors
