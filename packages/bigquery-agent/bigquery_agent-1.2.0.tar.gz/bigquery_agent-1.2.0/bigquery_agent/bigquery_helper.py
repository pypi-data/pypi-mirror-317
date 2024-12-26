from google.cloud import bigquery

import re


class BigQueryHelper:

    def __init__(self, project_id: str, dataset_id: str, table_id: str, credentials=None, max_byte_limit_per_query=0):
        """
        Initialize the BigQueryHelper with the provided project, dataset, and table IDs.
        This constructor also initializes the BigQuery client and table reference.

        :param project_id: GCP project ID
        :param dataset_id: BigQuery dataset ID
        :param table_id:   BigQuery table ID
        :param credentials: credentials used to access BigQuery
        :param max_byte_limit_per_query: the query will NOT be executed if this value is set and estimates is exceeds it
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.max_byte_limit_per_query = max_byte_limit_per_query

        # Initialize the BigQuery client
        self.client = bigquery.Client(project=self.project_id, credentials=credentials)

        # Fully-qualified table ID in standard SQL format
        self.table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

    def get_schema(self) -> str:
        """
        Retrieves the schema of the configured BigQuery table.

        :return: A list of SchemaField objects describing the table schema.
        """
        table = self.client.get_table(self.table_ref)
        return table.schema

    def run_query(self, sql_query: str) -> str:
        """
        Runs a SQL query against the BigQuery database. 
        SQL query should be valid BigQuery SQL query with single quotes around strings, 
        do not escape them. Example of correct usage: SELECT * FROM `my_table` WHERE id = 'abc-123'"

        :param sql_query: The SQL query to execute.
        :return: A newline-separated string representation of the query results.
        """        
        updated_sql_query = self._clean_sql(sql_query)
        if self.max_byte_limit_per_query > 0:
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
            query_job = self.client.query(updated_sql_query, job_config=job_config)
            if query_job.total_bytes_processed >= self.max_byte_limit_per_query:
                return (f"Executing query {updated_sql_query} will exceed byte" +
                         f"limit: {self.max_byte_limit_per_query}" +
                         f"and will take: {query_job.total_bytes_processed} bytes." +
                         "Please stop/do not do query any more and tell user about the error."+
                         "Show user the query and byte limits you have and size of request that query would do")


        query_job = self.client.query(self._clean_sql(sql_query))
        results = query_job.result()

        result_str_list = []
        for row in results:
            # Convert the row to a dictionary for readability
            row_dict = dict(row)
            result_str_list.append(str(row_dict))

        return "\n".join(result_str_list)

    def get_table_ref(self) -> str:
        """
        Returns the fully-qualified table reference string.

        :return: The table reference in the format project_id.dataset_id.table_id
        """
        return self.table_ref

    def _clean_sql(self, sql_query):
        """Cleans up a SQL query string, specifically removing excessive backslashes."""
        # Replace multiple backslashes followed by a single quote with just a single quote
        cleaned_sql = re.sub(r"\\+'", "'", sql_query)
        
        #This regex will target backslashes that are immediately followed by a word character (\w) or a hyphen (-)
        #It will match only the single backslashes, but only if they are followed by the specified characters.
        cleaned_sql = re.sub(r"\\(?=[\w-])", "", cleaned_sql)

        return cleaned_sql