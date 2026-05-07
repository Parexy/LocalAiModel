# How to Run the Project

## 1. Install required software

Install Python 3.11 if it is not already installed:

~~~powershell
winget install -e --id Python.Python.3.11
~~~

Install Ollama if it is not already installed:

~~~powershell
winget install -e --id Ollama.Ollama
~~~

## 2. Clone the repository

~~~powershell
git clone <repository-url>
cd <repository-folder>
~~~

## 3. Install Python dependencies

~~~powershell
pip install -r requirements.txt
~~~

## 4. Install the Ollama model

The project uses Ollama with `llama3.1:8b`.

~~~powershell
ollama pull llama3.1:8b
~~~

## 5. Configuration

The project includes a `.env` file with the default Ollama configuration:

~~~env
OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=127.0.0.1:11434
~~~

Semantic Scholar is used as the primary paper search source. OpenAlex is used as fallback if Semantic Scholar is rate-limited.

## 6. Run the agent

~~~powershell
python -m src.main
~~~

Example prompt:

~~~text
Find a research paper about AI agents using tools after 2022 with at least 100 citations.
~~~

To stop the agent, type:

~~~text
exit
~~~

## 7. Run the evaluation

~~~powershell
python -m evaluation.run_evaluation
~~~

The evaluation output is written to:

~~~text
evaluation/evaluation_results.md
~~~