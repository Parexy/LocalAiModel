import json
import re
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """
    Extract the first JSON object from an LLM response.
    This protects us if the model adds extra text.
    """

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in model response.")

    return json.loads(match.group(0))


def validate_constraints(data: dict[str, Any]) -> dict[str, Any]:
    allowed_year_operators = {"before", "after", "in", "none"}
    allowed_citation_operators = {"min", "max", "approx", "none"}

    topic = data.get("topic")

    if not topic or not isinstance(topic, str):
        raise ValueError("Missing or invalid topic.")

    year_operator = data.get("year_operator", "none")
    citation_operator = data.get("citation_operator", "none")

    if year_operator not in allowed_year_operators:
        year_operator = "none"

    if citation_operator not in allowed_citation_operators:
        citation_operator = "none"

    year = data.get("year")
    citation_count = data.get("citation_count")

    if year_operator == "none":
        year = None

    if citation_operator == "none":
        citation_count = None

    if year is not None:
        year = int(year)

    if citation_count is not None:
        citation_count = int(citation_count)

    return {
        "topic": topic.strip(),
        "year_operator": year_operator,
        "year": year,
        "citation_operator": citation_operator,
        "citation_count": citation_count,
    }


def correct_constraints_from_request(
    user_request: str,
    constraints: dict[str, Any],
) -> dict[str, Any]:
    """
    Deterministically correct common constraint extraction mistakes.

    This is important because the LLM may misread:
    - "more than 500 citations" as max instead of min
    - "less than 500 citations" as min instead of max
    """

    request = user_request.lower()

    citation_number_match = re.search(
        r"(?:citations?|cited)\D{0,20}(\d+)|(\d+)\D{0,20}(?:citations?|cited)",
        request,
    )

    citation_number = None

    if citation_number_match:
        citation_number = citation_number_match.group(1) or citation_number_match.group(2)

    if citation_number is not None:
        citation_number = int(citation_number)

        min_patterns = [
            r"at least\s+\d+",
            r"minimum\s+\d+",
            r"more than\s+\d+",
            r"over\s+\d+",
            r"greater than\s+\d+",
            r"above\s+\d+",
            r"\d+\s+or more",
        ]

        max_patterns = [
            r"less than\s+\d+",
            r"fewer than\s+\d+",
            r"under\s+\d+",
            r"below\s+\d+",
            r"maximum\s+\d+",
            r"at most\s+\d+",
            r"no more than\s+\d+",
        ]

        approx_patterns = [
            r"around\s+\d+",
            r"approximately\s+\d+",
            r"about\s+\d+",
            r"roughly\s+\d+",
        ]

        if any(re.search(pattern, request) for pattern in min_patterns):
            constraints["citation_operator"] = "min"
            constraints["citation_count"] = citation_number

        elif any(re.search(pattern, request) for pattern in max_patterns):
            constraints["citation_operator"] = "max"
            constraints["citation_count"] = citation_number

        elif any(re.search(pattern, request) for pattern in approx_patterns):
            constraints["citation_operator"] = "approx"
            constraints["citation_count"] = citation_number

    year_match = re.search(r"(before|after|in)\s+(20\d{2}|19\d{2})", request)

    if year_match:
        operator = year_match.group(1)
        year = int(year_match.group(2))

        constraints["year_operator"] = operator
        constraints["year"] = year

    return constraints