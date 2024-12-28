Below is a concise `README.md`:

---

# bigquery_agent

`bigquery_agent` creates a Gemini Agents Toolkit-based agent with built-in functions to query a specified BigQuery table.

## Requirements

- Python 3.8+
- [Gemini Agents Toolkit](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md)
- Google Cloud credentials with BigQuery access
- Vertex AI enabled for your GCP project

## Installation

```bash
pip install bigquery_agent
```

## Usage

```python
import vertexai
from bigquery_agent import create_bigquery_agent

vertexai.init(project="YOUR_GCP_PROJECT", location="us-west1")

agent = create_bigquery_agent(
    bigquery_project_id="YOUR_BQ_PROJECT",
    dataset_id="YOUR_DATASET",
    table_id="YOUR_TABLE",
    model_name="gemini-2.0-flash-exp",
    system_instruction="Query the todos table as needed."
)

response = agent.send_message("Show me all todos from the database")[0]
print(response)
```

This agent can inspect the schema (`get_schema`), run queries (`run_query`), and get table references (`get_table_ref`) using the provided BigQuery credentials and Vertex AI model.

For more details on creating and using agents, refer to the [Gemini Agents Toolkit README](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md).
