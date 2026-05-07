from typing import Any

import requests

from src.tools.openalex_tool import search_papers_openalex
from src.tools.semantic_scholar_tool import search_papers_semantic_scholar


use_openalex_only = False


def search_papers_with_fallback(
    topic: str,
    limit: int = 20,
) -> tuple[list[dict[str, Any]], str]:
    """
    Search papers using Semantic Scholar first.

    If Semantic Scholar fails once, the program switches to OpenAlex for the
    rest of the current run. This avoids repeatedly hitting Semantic Scholar
    during evaluation after a rate-limit error.
    """

    global use_openalex_only

    if use_openalex_only:
        openalex_results = search_papers_openalex(
            topic=topic,
            limit=limit,
        )

        return openalex_results, "OpenAlex"

    try:
        semantic_results = search_papers_semantic_scholar(
            topic=topic,
            limit=limit,
        )

        if semantic_results:
            return semantic_results, "Semantic Scholar"

        print("Semantic Scholar returned no results. Switching to OpenAlex for the rest of this run.")
        use_openalex_only = True

    except requests.exceptions.HTTPError as error:
        status_code = None

        if error.response is not None:
            status_code = error.response.status_code

        if status_code == 429:
            print("Semantic Scholar rate limit hit. Switching to OpenAlex for the rest of this run.")
        else:
            print(f"Semantic Scholar failed with HTTP {status_code}. Switching to OpenAlex for the rest of this run.")

        use_openalex_only = True

    except Exception as error:
        print(f"Semantic Scholar failed: {error}. Switching to OpenAlex for the rest of this run.")
        use_openalex_only = True

    openalex_results = search_papers_openalex(
        topic=topic,
        limit=limit,
    )

    return openalex_results, "OpenAlex"