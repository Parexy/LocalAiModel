import warnings

warnings.filterwarnings(
    "ignore",
    message="flaml.automl is not available.*",
    category=UserWarning,
)

import json
from pathlib import Path

from src.agent import run_research_agent


def main():
    prompts_path = Path("evaluation/eval_prompts.json")
    output_path = Path("evaluation/evaluation_results.md")

    if not prompts_path.exists():
        print(f"Could not find evaluation prompt file: {prompts_path}")
        return

    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))

    lines = []

    lines.append("# Evaluation Results")
    lines.append("")
    lines.append("This evaluation runs the agent on 10 prompts and stores the outputs.")
    lines.append("The scoring is filled in manually using the rubric below.")
    lines.append("")
    lines.append("## Rubric")
    lines.append("")
    lines.append("| Criterion | Question | Score |")
    lines.append("|---|---|---:|")
    lines.append("| Relevance | Is the selected paper actually about the requested topic? | 0 or 1 |")
    lines.append("| Year OK | Does the publication year satisfy the request? | 0 or 1 |")
    lines.append("| Citation OK | Does the citation count satisfy the request? | 0 or 1 |")
    lines.append("| Source OK | Is the citation count source provided? | 0 or 1 |")
    lines.append("| No hallucination | Does the answer avoid invented citation counts or unsupported facts? | 0 or 1 |")
    lines.append("| Explanation OK | Is the explanation useful and based on the retrieved metadata? | 0 or 1 |")
    lines.append("")
    lines.append("Maximum score per prompt: 6 points.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for item in prompts:
        prompt_id = item["id"]
        prompt = item["prompt"]
        purpose = item.get("purpose", "")

        print(f"Running prompt {prompt_id}: {prompt}")

        try:
            result = run_research_agent(prompt)
        except Exception as error:
            result = f"ERROR: {error}"

        lines.append(f"## Prompt {prompt_id}")
        lines.append("")
        lines.append(f"**Purpose:** {purpose}")
        lines.append("")
        lines.append(f"**Prompt:** {prompt}")
        lines.append("")
        lines.append("**Agent output:**")
        lines.append("")
        lines.append("```text")
        lines.append(result)
        lines.append("```")
        lines.append("")
        lines.append("**Manual score:**")
        lines.append("")
        lines.append("| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|")
        lines.append("| TODO | TODO | TODO | TODO | TODO | TODO | TODO/6 |")
        lines.append("")
        lines.append("**Notes:**")
        lines.append("")
        lines.append("TODO")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")

    print()
    print(f"Evaluation written to: {output_path}")


if __name__ == "__main__":
    main()