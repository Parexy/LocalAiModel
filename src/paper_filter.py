from typing import Any


def year_matches(
    paper_year: int | None,
    operator: str,
    target_year: int | None,
) -> bool:
    if operator == "none" or target_year is None:
        return True

    if paper_year is None:
        return False

    if operator == "before":
        return paper_year < target_year

    if operator == "after":
        return paper_year > target_year

    if operator == "in":
        return paper_year == target_year

    return False


def citation_matches(
    citation_count: int | None,
    operator: str,
    target_count: int | None,
) -> bool:
    if operator == "none" or target_count is None:
        return True

    if citation_count is None:
        return False

    if operator == "min":
        return citation_count >= target_count

    if operator == "max":
        return citation_count <= target_count

    if operator == "approx":
        tolerance = max(25, int(target_count * 0.2))
        return abs(citation_count - target_count) <= tolerance

    return False


def filter_papers(
    papers: list[dict[str, Any]],
    constraints: dict[str, Any],
) -> list[dict[str, Any]]:
    valid_papers = []

    for paper in papers:
        if not year_matches(
            paper.get("year"),
            constraints.get("year_operator", "none"),
            constraints.get("year"),
        ):
            continue

        if not citation_matches(
            paper.get("citation_count"),
            constraints.get("citation_operator", "none"),
            constraints.get("citation_count"),
        ):
            continue

        valid_papers.append(paper)

    return valid_papers


def select_best_paper(
    papers: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not papers:
        return None

    return sorted(
        papers,
        key=lambda paper: (
            paper.get("topic_relevance_score") or 0,
            paper.get("citation_count") or 0,
        ),
        reverse=True,
    )[0]