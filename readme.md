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

No API key is required. The project includes a `.env` file with the default Ollama configuration.