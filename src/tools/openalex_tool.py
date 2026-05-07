from typing import Any

import requests


OPENALEX_WORKS_URL = "https://api.openalex.org/works"


def search_papers_openalex(topic: str, limit: int = 20) -> list[dict[str, Any]]:
    """
    Search OpenAlex for research papers.

    Citation counts come from OpenAlex's cited_by_count field.
    """

    params = {
        "search": topic,
        "per-page": limit,
    }

    response = requests.get(
        OPENALEX_WORKS_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    return _map_openalex_results(data)


def _map_openalex_results(data: dict[str, Any]) -> list[dict[str, Any]]:
    papers = []

    for work in data.get("results", []):
        authors = []

        for authorship in work.get("authorships", []):
            author = authorship.get("author") or {}
            display_name = author.get("display_name")

            if display_name:
                authors.append(display_name)

        doi = work.get("doi")

        papers.append(
            {
                "title": work.get("display_name"),
                "authors": authors,
                "year": work.get("publication_year"),
                "citation_count": work.get("cited_by_count"),
                "citation_source": "OpenAlex",
                "url": work.get("id"),
                "doi": doi,
                "abstract": _reconstruct_abstract(
                    work.get("abstract_inverted_index")
                ),
            }
        )

    return papers


def _reconstruct_abstract(
    inverted_index: dict[str, list[int]] | None,
) -> str | None:
    """
    OpenAlex stores abstracts as an inverted index.
    This converts it back into normal text.
    """

    if not inverted_index:
        return None

    words_by_position = {}

    for word, positions in inverted_index.items():
        for position in positions:
            words_by_position[position] = word

    return " ".join(
        words_by_position[position]
        for position in sorted(words_by_position)
    )