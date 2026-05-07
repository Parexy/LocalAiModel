## Setup

### Requirements

- Python 3.11
- Ollama

### Install required software

~~~powershell
winget install -e --id Python.Python.3.11
winget install -e --id Ollama.Ollama
~~~

### Install the Ollama model

~~~powershell
ollama pull llama3.1:8b
~~~

### Install Python dependencies

~~~powershell
pip install -r requirements.txt
~~~

## Run the Agent

~~~powershell
python -m src.main
~~~

## Run the Evaluation

~~~powershell
python -m evaluation.run_evaluation
~~~

The evaluation output is written to:

~~~text
evaluation/evaluation_results.md
~~~

No API key is required. The project includes a `.env` file with the default Ollama configuration, and i ran this using my local machine.

# Evaluation Results

This evaluation runs the agent on 10 prompts and stores the outputs.
The scoring is filled in manually using the rubric below.

## Rubric

| Criterion | Question | Score |
|---|---|---:|
| Relevance | Is the selected paper actually about the requested topic? | 0 or 1 |
| Year OK | Does the publication year satisfy the request? | 0 or 1 |
| Citation OK | Does the citation count satisfy the request? | 0 or 1 |
| Source OK | Is the citation count source provided? | 0 or 1 |
| No hallucination | Does the answer avoid invented citation counts or unsupported facts? | 0 or 1 |
| Explanation OK | Is the explanation useful and based on the retrieved metadata? | 0 or 1 |

Maximum score per prompt: 6 points.

---

## Prompt 1

**Purpose:** Tests before-year and minimum citation constraint

**Prompt:** Find a research paper about retrieval-augmented generation published before 2021 with more than 500 citations.

**Agent output:**

```text
No matching paper was found.

Search topic:
retrieval-augmented generation

Applied constraints:
- Year operator: before
- Year: 2021
- Citation operator: min
- Citation count: 500

The agent searched external paper data, but no candidate satisfied the requested constraints.
No citation count was invented.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 | 1 | 2/6 |

**Notes:**

It did not find a paper matching this likely due to keywords used not matching anything. This could be due to terms being too new or something else.

---

## Prompt 2

**Purpose:** Tests recent AI agents topic and minimum citation constraint

**Prompt:** Find a research paper about AI agents using tools after 2022 with at least 100 citations.

**Agent output:**

```text
Title:
Empowering biomedical discovery with AI agents

Authors:
Shanghua Gao, Ada Fang, Yepeng Huang, Valentina Giunchiglia, Ayush Noori, et al.

Publication year:
2024

Citation count:
222

Citation count source:
OpenAlex

Link:
https://openalex.org/W4403925918

Why this matches:
The selected paper "Empowering biomedical discovery with AI agents" matches the user's request because it deals with AI agents. The paper was published in 2024, which is after the specified year of 2022. It has a citation count of 222, exceeding the minimum requirement of 100 citations. The OpenAlex citation source provides evidence for this high citation count. The abstract suggests that the paper explores the use of tools by AI agents, aligning with the topic constraint. Overall, the paper's metadata and abstract indicate that it meets all the specified constraints.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 | 6/6 |

**Notes:**

Successfully found a matching paper and included correct metadata and provided a explanation on if it thinks the paper matches the given constraints.

---

## Prompt 3

**Purpose:** Tests broad recent topic with weak constraints

**Prompt:** Find a recent paper about AI agents using tools and explain whether it would be useful for autonomous software agents.

**Agent output:**

```text
Title:
Modelling social action for AI agents

Authors:
Cristiano Castelfranchi

Publication year:
1998

Citation count:
535

Citation count source:
OpenAlex

Link:
https://openalex.org/W2145467192

Why this matches:
The selected paper, "Modelling social action for AI agents" by Cristiano Castelfranchi, partially matches the user's request. The paper is about AI agents, which aligns with the topic specified in the constraints. However, I must note that the abstract is missing, making it difficult to assess its relevance and usefulness. Nevertheless, the paper's title suggests that it explores how AI agents can model social actions, which could be relevant for autonomous software agents. The year of publication (1998) is relatively recent compared to other papers in the field. Despite this, the paper's citation count of 535 indicates a significant impact on the research community.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 1 | 1 | 1 | 5/6 |

---

## Prompt 4

**Purpose:** Tests exact year and high citation count

**Prompt:** Find a paper about chain-of-thought prompting published in 2022 with at least 1000 citations.

**Agent output:**

```text
No matching paper was found.

Search topic:
chain-of-thought prompting

Applied constraints:
- Year operator: in
- Year: 2022
- Citation operator: min
- Citation count: 1000

The agent searched external paper data, but no candidate satisfied the requested constraints.
No citation count was invented.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 | 1 | 2/6 |

---

## Prompt 5

**Purpose:** Tests software engineering related LLM topic

**Prompt:** Find a paper about code generation with large language models after 2021 with at least 300 citations.

**Agent output:**

```text
Title:
Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models

Authors:
Priyan Vaithilingam, Tianyi Zhang, Elena L. Glassman

Publication year:
2022

Citation count:
536

Citation count source:
OpenAlex

Link:
https://openalex.org/W4225108562

Why this matches:
This paper matches the user's request because it deals with code generation using large language models, specifically evaluating the usability of a tool called Copilot. The study was conducted in 2022, which meets the "after 2021" constraint. Additionally, the paper has a high citation count of 536 from OpenAlex, exceeding the minimum requirement of 300 citations. Although the abstract is brief and does not provide extensive details about code generation, it suggests that the research explores the usability of LLM-based tools in programming tasks. The authors' focus on evaluating Copilot's effectiveness and identifying areas for improvement aligns with the topic of code generation. Overall, this paper appears to be a relevant study on large language models and code generation after 2021 with a substantial citation count.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 | 6/6 |

---

## Prompt 6

**Purpose:** Tests recent topic and moderate citation constraint

**Prompt:** Find a paper about hallucination detection in LLMs after 2023 with at least 50 citations.

**Agent output:**

```text
Title:
A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

Authors:
Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, et al.

Publication year:
2024

Citation count:
1310

Citation count source:
OpenAlex

Link:
https://openalex.org/W4404534210

Why this matches:
The selected paper "A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions" matches the user's request because it deals with the topic of hallucination detection in LLMs. The paper was published in 2024, which is after the specified year of 2023. It has a high citation count of 1310, exceeding the minimum requirement of 50 citations. Although the abstract does not explicitly mention "detection" as part of its title, it discusses various methods and benchmarks for mitigating hallucinations, implying that detection is an underlying aspect of the research. The paper's focus on LLMs aligns with the specified topic, and its publication year meets the constraint. Overall, this paper appears to be a relevant match for the user's request.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 | 6/6 |

---

## Prompt 7

**Purpose:** Tests older high-impact research topic

**Prompt:** Find a paper about federated learning before 2018 with more than 1000 citations.

**Agent output:**

```text
Title:
Federated Learning: Strategies for Improving Communication Efficiency

Authors:
Jakub Konečný, H. Brendan McMahan, Felix X. Yu, Peter Richtárik, Ananda Theertha Suresh, et al.

Publication year:
2016

Citation count:
3050

Citation count source:
OpenAlex

Link:
https://openalex.org/W2535838896

Why this matches:
The selected paper "Federated Learning: Strategies for Improving Communication Efficiency" (2016) matches the user's request because it is about federated learning, a topic specified in the constraints. The paper was published before 2018, meeting another constraint. Additionally, its citation count of 3050 exceeds the minimum requirement of 1000 citations. However, I must note that the abstract provides a clear and detailed explanation of the paper's content, which is not always the case with research papers. Therefore, I am confident in my assessment based on the provided metadata.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 | 6/6 |

---

## Prompt 8

**Purpose:** Tests no-result case

**Prompt:** Find a paper about quantum blockchain agents after 2024 with at least 10000 citations.

**Agent output:**

```text
No matching paper was found.

Search topic:
quantum blockchain agents

Applied constraints:
- Year operator: after
- Year: 2024
- Citation operator: min
- Citation count: 10000

The agent searched external paper data, but no candidate satisfied the requested constraints.
No citation count was invented.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 | 1 | 2/6 |

---

## Prompt 9

**Purpose:** Tests ambiguous abbreviation

**Prompt:** Find a paper about RAG.

**Agent output:**

```text
Title:
Improving the Domain Adaptation of Retrieval Augmented Generation (RAG) Models for Open Domain Question Answering

Authors:
Shamane Siriwardhana, Rivindu Weerasekera, Elliott Wen, Tharindu Kaluarachchi, Rajib Rana, et al.

Publication year:
2023

Citation count:
264

Citation count source:
OpenAlex

Link:
https://openalex.org/W4317898419

Why this matches:
This paper matches the user's request for a paper about RAG because its title explicitly mentions "Retrieval Augmented Generation (RAG) Models". The abstract also discusses RAG, highlighting its limitations in adapting to specialized domains and proposing an extension called RAG-end2end. The authors evaluate their approach on datasets from various domains, including COVID-19, News, and Conversations, which demonstrates the application of RAG in different areas. Although the paper's focus is on improving RAG for domain adaptation, it still centers around the core concept of RAG. Unfortunately, the abstract does not provide a detailed explanation of RAG itself, but based on the title and content, it appears to be relevant to the user's request. Overall, this paper seems to match the request as it deals with RAG in some capacity.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 6 | 6/6 |

---

## Prompt 10

**Purpose:** Tests maximum citation constraint

**Prompt:** Find a paper about autonomous agents with fewer than 20 citations after 2023.

**Agent output:**

```text
No matching paper was found.

Search topic:
autonomous agents

Applied constraints:
- Year operator: after
- Year: 2023
- Citation operator: max
- Citation count: 20

The agent searched external paper data, but no candidate satisfied the requested constraints.
No citation count was invented.
```

**Manual score:**

| Relevant | Year OK | Citation OK | Source OK | No hallucination | Explanation OK | Score |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 1 | 1 | 2/6 |

**Notes:**

This could have failed due to there not being a paper after 2023 with fewer than 20 citations, when using this source.

---
