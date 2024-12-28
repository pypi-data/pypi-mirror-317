
from .bigquery_helper import BigQueryHelper
from gemini_agents_toolkit import agent


SYSTEM_INSTRUCTION_INJECTION = """
You are a helpful assistant that helps to query data from a BigQuery database.
You have access to the tools required for this.

When using the tool to query:

- **SQL Syntax:**  You MUST generate valid BigQuery SQL.
- **String Literals:** String literals in SQL queries MUST be enclosed in single quotes (').  Do NOT use backslashes (\) to escape characters within SQL string literals unless specifically needed for a special character inside the string (e.g., a single quote within the string itself should be escaped as '').
- **Table and Column Names:** If table or column names contain special characters or are reserved keywords, enclose them in backticks (`).
- **Example**
    -  To query for a run_id of "abc-123", the SQL should be: `SELECT * FROM my_table WHERE run_id = 'abc-123'`
    - **Do not use** double backslashes: `SELECT * FROM my_table WHERE run_id = \\'abc-123\\'`
- **Do not** use excessive backslashes. Only use them when necessary to escape special characters within a string literal according to BigQuery SQL rules.
- **BEFORE** doing any query make sure that you have checked table name by calling get_table_ref and schema from get_schema to make sure that you have constracted the correct SQL
- **UNLESSS** user is asking about SQL query to show, your main goal is to answer the question and not to show the SQL query, do not respond with the query you want to execute - try to get to the answer (unless you got the error and do not know how to proceed)

When generating SQL queries, be concise and avoid unnecessary clauses or joins unless explicitly requested by the user.

Always return results in a clear and human-readable format. If the result is a table, format it nicely.
"""


def create_bigquery_agent(
    bigquery_project_id: str,
    dataset_id: str,
    table_id: str,
    model_name:str = "gemini-2.0-flash-exp",
    debug: bool = False,
    add_scheduling_functions: bool = False,
    gcs_bucket: str = None,
    gcs_blob: str = None,
    delegation_function_prompt: str = None,
    delegates: list = None,
    function_call_limit_per_chat: int = None,
    on_message = None,
    generation_config: dict = None,
    system_instruction: str = "",
    bq_credentials = None,
    max_byte_limit_per_query = 0
):
    """
    Creates and returns an agent initialized with functions from BigQueryHelper 
    that can interact with a specific BigQuery table.

    :param bigquery_project_id: GCP project ID for BigQuery.
    :param dataset_id: BigQuery dataset ID.
    :param table_id: BigQuery table ID.
    :param model_name: The Vertex AI model name to be used by the agent.
    :param debug: Optional debug mode for the agent.
    :param add_scheduling_functions: Whether to add scheduling functions to the agent.
    :param gcs_bucket: GCS bucket name for agent storage (if any).
    :param gcs_blob: GCS blob name for agent storage (if any).
    :param delegation_function_prompt: Prompt for delegation functions.
    :param delegates: List of delegate configurations.
    :param function_call_limit_per_chat: limits every chat instance to a number of backend function calls. Throws TooManyFunctionCallsException when limit is exceeded
    :param on_message: A callback that fires on each message from the agent.
    :param generation_config: Additional generation configuration parameters.
    :param system_instruction: Instruction message.
    :param bq_credentials: credentials that will be used with BigQuery
    :param max_byte_limit_per_query: the query will NOT be executed if this value is set and estimates is exceeds it
    :return: An agent instance configured to query the specified BigQuery table.
    """



    # Initialize the BigQuery helper with the bigquery_project_id
    helper = BigQueryHelper(
        project_id=bigquery_project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        credentials=bq_credentials,
        max_byte_limit_per_query=max_byte_limit_per_query
    )

    # Define the agent with helper's functions
    all_functions = [helper.get_schema, helper.run_query, helper.get_table_ref]

    # Prepend prompt to the system_instruction
    updated_system_instruction = f"""{SYSTEM_INSTRUCTION_INJECTION}. {system_instruction}""".strip()

    # Create and return the agent instance
    todo_agent = agent.create_agent_from_functions_list(
        functions=all_functions,
        model_name=model_name,
        debug=debug,
        add_scheduling_functions=add_scheduling_functions,
        gcs_bucket=gcs_bucket,
        gcs_blob=gcs_blob,
        delegation_function_prompt=delegation_function_prompt,
        delegates=delegates,
        function_call_limit_per_chat=function_call_limit_per_chat,
        on_message=on_message,
        generation_config=generation_config,
        system_instruction=updated_system_instruction
    )

    return todo_agent
