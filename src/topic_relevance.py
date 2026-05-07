import re
from typing import Any


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "about",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "using",
    "with",
    "research",
    "paper",
    "papers",
    "published",
    "publication",
    "citations",
    "citation",
    "find",
}


PHRASE_ALIASES = {
    "rag": "retrieval augmented generation",
    "llm": "large language model",
    "llms": "large language models",
}


def normalize_text(text: str | None) -> str:
    if not text:
        return ""

    text = text.lower()

    for short, expanded in PHRASE_ALIASES.items():
        text = re.sub(rf"\b{re.escape(short)}\b", expanded, text)

    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_topic_terms(topic: str) -> list[str]:
    normalized = normalize_text(topic)

    terms = [
        term
        for term in normalized.split()
        if term not in STOP_WORDS and len(term) > 2
    ]

    return terms


def topic_relevance_score(topic: str, paper: dict[str, Any]) -> int:
    terms = extract_topic_terms(topic)

    if not terms:
        return 0

    title = normalize_text(paper.get("title"))
    abstract = normalize_text(paper.get("abstract"))

    searchable_text = f"{title} {abstract}"

    score = 0

    for term in terms:
        if term in title:
            score += 3
        elif term in searchable_text:
            score += 1

    normalized_topic = normalize_text(topic)

    if normalized_topic and normalized_topic in searchable_text:
        score += 10

    return score


def filter_by_topic_relevance(
    papers: list[dict[str, Any]],
    topic: str,
    minimum_score: int = 2,
) -> list[dict[str, Any]]:
    relevant_papers = []

    for paper in papers:
        score = topic_relevance_score(topic, paper)

        if score >= minimum_score:
            paper["topic_relevance_score"] = score
            relevant_papers.append(paper)

    return relevant_papers