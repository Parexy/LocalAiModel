import warnings

warnings.filterwarnings(
    "ignore",
    message="flaml.automl is not available.*",
    category=UserWarning,
)

from src.agent import run_research_agent


def main():
    print("AI research assistant")
    print("Type a research paper request.")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_request = input("Request: ").strip()

        if user_request.lower() in {"exit", "quit"}:
            break

        if not user_request:
            continue

        print()
        print("Searching...")
        print()

        try:
            result = run_research_agent(user_request)
            print(result)
        except Exception as error:
            print("The agent failed to complete the request.")
            print(f"Error: {error}")

        print()
        print("-" * 80)
        print()


if __name__ == "__main__":
    main()