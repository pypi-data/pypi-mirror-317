import os
import re
from typing import Optional


class MigrationDirHandler():

    def __init__(self, migrations_dir: str):
        """
        Load class dependecies as attributes

        Args:
            migrations_dir (str): Migrations directory path
        """
        self.check(migrations_dir)
        self.migrations_dir = migrations_dir

    @staticmethod
    def check(migrations_dir: str) -> Optional[bool]:
        """
        Check if the migrations directory exists

        Args:
            migrations_dir (str): Migrations dir path

        Raises:
            FileNotFoundError: If the migration directory does not exist
        """
        if not os.path.isdir(migrations_dir):
            raise FileNotFoundError(f"Migration directory not found: {migrations_dir}")
        return True

    def filename_list(self) -> list[str]:
        """
        List migration files in the migrations directory
        File naming convention: yyyy_mm_dd_hhmmss_method_entityname_entitytype.py
        Example: 2024_12_10_120000_create_users_table.py

        Returns:
            list[str]: Ordered list of migration names without the .py extension
        """
        file_name_regex = r"^\d{4}_(0[1-9]|1[0-2])_(0[1-9]|[12][0-9]|3[01])_([01][0-9]|2[0-3])[0-5][0-9][0-5][0-9]_.+\.py$"
        return sorted(
            f.replace(".py", "")  # remove .py extension from the result
            for f in os.listdir(self.migrations_dir)
            if re.match(file_name_regex, f)  # filter filenames in the directory using regex
        )
