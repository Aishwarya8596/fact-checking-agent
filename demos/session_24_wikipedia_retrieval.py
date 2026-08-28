import html
import json
import re
import urllib.parse

import requests


WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/w/rest.php/v1/search/page"
WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"
USER_AGENT = "fact-checking-agent-demo/0.1 (beginner AI project)"


def strip_html(text):
    without_tags = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(without_tags).strip()


def build_wikipedia_url(page_key):
    return "https://en.wikipedia.org/wiki/" + urllib.parse.quote(page_key)


def search_wikipedia(claim, limit=3):
    response = requests.get(
        WIKIPEDIA_SEARCH_URL,
        params={"q": claim, "limit": limit},
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()

    return response.json()


def fetch_wikipedia_summary(page_key):
    url = f"{WIKIPEDIA_SUMMARY_URL}/{urllib.parse.quote(page_key)}"
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=10,
    )
    response.raise_for_status()

    return response.json().get("extract", "")


def wikipedia_results_to_evidence(search_results):
    evidence_items = []

    for index, page in enumerate(search_results.get("pages", []), start=1):
        title = page.get("title", "Untitled page")
        page_key = page.get("key", title.replace(" ", "_"))
        excerpt = strip_html(page.get("excerpt", ""))
        description = strip_html(page.get("description", ""))
        summary = strip_html(fetch_wikipedia_summary(page_key))
        text_parts = [part for part in [description, summary, excerpt] if part]
        evidence_text = " ".join(text_parts) or title

        evidence_items.append(
            {
                "id": f"web_evidence_{index}",
                "title": title,
                "source_type": "encyclopedia",
                "source_quality": "medium",
                "source_score": 0.8,
                "url": build_wikipedia_url(page_key),
                "text": evidence_text,
            }
        )

    return evidence_items


def retrieve_wikipedia_evidence(claim, limit=3):
    search_results = search_wikipedia(claim, limit=limit)
    return wikipedia_results_to_evidence(search_results)


def main():
    claim = "Argentina won the FIFA 2022 World Cup."

    print("SESSION 24 DEMO: Wikipedia retrieval")
    print("=" * 48)
    print(f"Claim: {claim}")

    evidence_items = retrieve_wikipedia_evidence(claim)

    print("\nRetrieved web evidence:")
    for item in evidence_items:
        print(f"\n- {item['id']}: {item['title']}")
        print(f"  URL: {item['url']}")
        print(f"  Quality: {item['source_quality']} ({item['source_score']})")
        print(f"  Text: {item['text']}")


if __name__ == "__main__":
    main()
