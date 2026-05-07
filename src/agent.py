import os

from autogen import AssistantAgent
from dotenv import load_dotenv

from src.constraint_parser import (
    extract_json_object,
    validate_constraints,
    correct_constraints_from_request,
)
from src.paper_filter import filter_papers, select_best_paper
from src.tools.paper_search_tool import search_papers_with_fallback
from src.topic_relevance import filter_by_topic_relevance
from src.query_expander import expand_topic_queries

load_dotenv()


LLM_CONFIG = {
    "config_list": [
        {
            "model": os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            "client_host": os.getenv("OLLAMA_HOST", "127.0.0.1:11434"),
            "api_type": "ollama",
            "num_predict": -1,
            "repeat_penalty": 1.1,
            "stream": False,
            "seed": 42,
            "temperature": 0.0,
            "top_k": 50,
            "top_p": 0.8,
            "native_tool_calls": False,
            "cache_seed": None,
        }
    ]
}


constraint_agent = AssistantAgent(
    name="constraint_extractor",
    llm_config=LLM_CONFIG,
    system_message="""
You extract research paper search constraints from user requests.

Return only valid JSON with this exact schema:

{
  "topic": string,
  "year_operator": "before" | "after" | "in" | "none",
  "year": number | null,
  "citation_operator": "min" | "max" | "approx" | "none",
  "citation_count": number | null
}

Rules:
- "after 2022" means year_operator = "after", year = 2022.
- "before 2021" means year_operator = "before", year = 2021.
- "published in 2020" means year_operator = "in", year = 2020.
- "at least", "minimum", "more than", "over" mean citation_operator = "min".
- "less than", "fewer than", "under" mean citation_operator = "max".
- "around", "approximately", "about 500 citations" mean citation_operator = "approx".
- If a constraint is missing, use "none" and null.
- Do not include markdown.
- Do not include explanations.
""",
)


explanation_agent = AssistantAgent(
    name="relevance_explainer",
    llm_config=LLM_CONFIG,
    system_message="""
You explain why a selected research paper matches a user's request.

Rules:
- Do not invent facts.
- Use only the supplied paper metadata.
- Do not invent citation counts.
- Mention uncertainty if the abstract is missing or weak.
- Keep the explanation short and evidence-based.
""",
)


def ask_llm(agent: AssistantAgent, prompt: str) -> str:
    reply = agent.generate_reply(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    if isinstance(reply, dict):
        return reply.get("content", "")

    return str(reply)


def extract_constraints(user_request: str) -> dict:
    response = ask_llm(
        constraint_agent,
        f"Extract constraints from this request:\n\n{user_request}",
    )

    raw_constraints = extract_json_object(response)
    constraints = validate_constraints(raw_constraints)

    constraints = correct_constraints_from_request(
        user_request=user_request,
        constraints=constraints,
    )

    return constraints


def build_explanation(
    user_request: str,
    constraints: dict,
    paper: dict,
) -> str:
    prompt = f"""
User request:
{user_request}

Extracted constraints:
{constraints}

Selected paper:
Title: {paper.get("title")}
Authors: {paper.get("authors")}
Year: {paper.get("year")}
Citation count: {paper.get("citation_count")}
Citation source: {paper.get("citation_source")}
URL: {paper.get("url")}
DOI: {paper.get("doi")}
Abstract: {paper.get("abstract")}

Write 5-7 sentences explaining why this paper matches the request.
"""

    return ask_llm(explanation_agent, prompt).strip()


def format_structured_answer(
    paper: dict | None,
    constraints: dict,
    explanation: str | None = None,
) -> str:
    if paper is None:
        return f"""
No matching paper was found.

Search topic:
{constraints["topic"]}

Applied constraints:
- Year operator: {constraints["year_operator"]}
- Year: {constraints["year"]}
- Citation operator: {constraints["citation_operator"]}
- Citation count: {constraints["citation_count"]}

The agent searched external paper data, but no candidate satisfied the requested constraints.
No citation count was invented.
""".strip()

    authors = paper.get("authors") or []
    author_text = ", ".join(authors[:5])

    if len(authors) > 5:
        author_text += ", et al."

    link = paper.get("url") or paper.get("doi") or "No link available"

    return f"""
Title:
{paper.get("title")}

Authors:
{author_text}

Publication year:
{paper.get("year")}

Citation count:
{paper.get("citation_count")}

Citation count source:
{paper.get("citation_source")}

Link:
{link}

Why this matches:
{explanation}
""".strip()


def run_research_agent(user_request: str) -> str:
    constraints = extract_constraints(user_request)

    papers = []

    expanded_queries = expand_topic_queries(constraints["topic"])

    for query in expanded_queries:
        query_results, source_used = search_papers_with_fallback(
            topic=query,
            limit=25,
        )

        papers.extend(query_results)

        if len(papers) >= 25:
            break

    topic_relevant_papers = []

    for query in expanded_queries:
        relevant_for_query = filter_by_topic_relevance(
            papers=papers,
            topic=query,
        )

        topic_relevant_papers.extend(relevant_for_query)

    seen_titles = set()
    deduplicated_papers = []

    for paper in topic_relevant_papers:
        title = paper.get("title")

        if not title:
            continue

        normalized_title = title.lower().strip()

        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)
        deduplicated_papers.append(paper)

    topic_relevant_papers = deduplicated_papers

    valid_papers = filter_papers(
        papers=topic_relevant_papers,
        constraints=constraints,
    )

    best_paper = select_best_paper(valid_papers)

    if best_paper is None:
        return format_structured_answer(
            paper=None,
            constraints=constraints,
        )

    explanation = build_explanation(
        user_request=user_request,
        constraints=constraints,
        paper=best_paper,
    )

    return format_structured_answer(
        paper=best_paper,
        constraints=constraints,
        explanation=explanation,
    )