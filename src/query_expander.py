def expand_topic_queries(topic: str) -> list[str]:
    """
    Expands short or modern topic phrases into alternative search queries.

    This helps because some older papers may not use modern terms such as "LLM".
    """

    normalized_topic = topic.lower().strip()

    expansions = {
        "llm": [
            "large language models",
            "pretrained language models",
            "language model pretraining",
            "transformer language models",
            "BERT language model",
            "GPT language model",
        ],
        "llms": [
            "large language models",
            "pretrained language models",
            "language model pretraining",
            "transformer language models",
            "BERT language model",
            "GPT language model",
        ],
        "rag": [
            "retrieval augmented generation",
            "retrieval-augmented generation",
            "retrieval based question answering",
            "open domain question answering retrieval generation",
        ],
    }

    if normalized_topic in expansions:
        return expansions[normalized_topic]

    return [topic]