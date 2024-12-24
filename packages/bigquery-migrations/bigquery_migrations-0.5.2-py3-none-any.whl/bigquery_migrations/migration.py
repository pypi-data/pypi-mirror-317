import os
from abc import ABC, abstractmethod
from google.cloud import bigquery


class Migration(ABC):
    """
    Abstract Base class for BigQuery Migrations

    Args:
        ABC (abc.ABC):

    Attributes:
        client (bigquery.Client): Google Cloud BigQuery Client
    """

    def __init__(self, client: bigquery.Client):
        """
        Load class dependecies as attributes

        Args:
            client (bigquery.Client): Google BigQuery Client
        """
        self.client = client

    @abstractmethod
    def up(self):
        """Run the migration."""
        pass

    @abstractmethod
    def down(self):
        """Reverse the migration."""
        pass

    def get_parent_dir(self, file: str) -> str:
        """
        Get the abs. path for file parent directory

        Args:
            file (str): path of the file

        Returns:
            str: parent directory abs. path
        """
        return os.path.dirname(os.path.abspath(file))
