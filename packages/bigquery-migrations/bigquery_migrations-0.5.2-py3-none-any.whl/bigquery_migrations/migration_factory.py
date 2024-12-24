import os
import importlib.util
from google.cloud import bigquery
from .migration import Migration


class MigrationFactory:

    def __init__(self, client: bigquery.Client, migrations_dir: str):
        """
        Load class dependecies as attributes

        Args:
            client (bigquery.Client): Google Cloud BigQuery Client
            migrations_dir (str): Migrations directory path
        """
        self.client = client
        self.migrations_dir = migrations_dir

    def create(self, migration_name: str) -> Migration:
        """
        Dynamically load a migration module

        Args:
            migration_name (str): Migration name

        Raises:
            FileNotFoundError: If migration file does not found

        Returns:
            Migration: Migration subclass instance
        """
        migration_path = os.path.join(self.migrations_dir, f"{migration_name}.py")
        if not os.path.exists(migration_path):
            raise FileNotFoundError(f"Migration file {migration_path} not found.")
        spec = importlib.util.spec_from_file_location(migration_name, migration_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_name = self.generate_class_name_from_filename(migration_name)
        return getattr(module, class_name)(self.client)

    @staticmethod
    def generate_class_name_from_filename(migration_name: str) -> str:
        """
        Generate the class name from the migration file name
        e.g. 2024_12_10_120000_create_users_table.py -> CreateUsersTable

        Args:
            migration_name (str): Migration name

        Returns:
            str: Migration Class Name
        """
        base_name = migration_name.split('.')[0]
        parts = base_name.split('_')
        class_name = ''.join(part.capitalize() for part in parts[4:])
        return class_name
