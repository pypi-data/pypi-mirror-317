from google.cloud import bigquery
from google.oauth2 import service_account


class BqClient():
    """Class for creating Google BigQuery API Client"""
    @staticmethod
    def authWithSa(sa_json_file_path: str, pid: str) -> bigquery.Client:
        """
        Authenticate with service account

        See:
            https://developers.google.com/identity/protocols/oauth2/service-account#python
            https://googleapis.dev/python/bigquery/latest/reference.html#module-google.cloud.bigquery.client


        Args:
            sa_json_file_path (str): The service account JSON file path.
            pid (str): Google Cloud Project ID.

        Returns:
            bigquery.Client: Google BigQuery Client instance
        """
        credentials = service_account.Credentials.from_service_account_file(sa_json_file_path)
        return bigquery.Client(credentials=credentials, project=pid)
