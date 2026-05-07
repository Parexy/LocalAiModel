import os
from typing import Any

import requests


SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_papers_semantic_scholar(topic: str, limit: int = 20) -> list[dict[str, Any]]:
    """
    Search Semantic Scholar for research papers.

    The citation count comes from Semantic Scholar.
    """

    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    headers = {}

    if api_key:
        headers["x-api-key"] = api_key

    params = {
        "query": topic,
        "limit": limit,
        "fields": "title,authors,year,citationCount,url,abstract,externalIds",
    }

    response = requests.get(
        SEMANTIC_SCHOLAR_SEARCH_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    return _map_semantic_scholar_results(data)


def _map_semantic_scholar_results(data: dict[str, Any]) -> list[dict[str, Any]]:
    papers = []

    for paper in data.get("data", []):
        external_ids = paper.get("externalIds") or {}

        papers.append(
            {
                "title": paper.get("title"),
                "authors": [
                    author.get("name")
                    for author in paper.get("authors", [])
                    if author.get("name")
                ],
                "year": paper.get("year"),
                "citation_count": paper.get("citationCount"),
                "citation_source": "Semantic Scholar",
                "url": paper.get("url"),
                "doi": external_ids.get("DOI"),
                "abstract": paper.get("abstract"),
            }
        )

    return papers