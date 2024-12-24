import os
import json
from datetime import datetime, timezone
from typing import Optional, Tuple


class MigrationLogHandler():

    LOG_FILE_NAME = "migration_log.json"

    def __init__(self, migrations_dir: str):
        """
        Load class dependecies as attributes

        Args:
            migrations_dir (str): Migrations directory path
        """
        self.log_file = os.path.join(migrations_dir, self.LOG_FILE_NAME)

    def get_last(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieve the last successfully run migration from the log file

        Raises:
            ValueError: If migration log file is an invalid JSON file

        Returns:
            Tuple[Optional[str], Optional[str]]: last migartion name & timestamp
        """
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as file:
                    log = json.load(file)
                    return log.get("last_migration"), log.get("timestamp")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {self.log_file}: {e}")
        return None, None

    def save_last(self, migration_name: str) -> Optional[bool]:
        """
        Save the last successfully run migration and its timestamp to the log file.

        Args:
            migration_name (str): Migration name

        Raises:
            IOError: If last migration info can not save as json file

        Returns:
            Optional[bool]:
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            with open(self.log_file, "w") as file:
                json.dump({"last_migration": migration_name, "timestamp": timestamp}, file)
            return True
        except IOError as e:
            raise IOError(f"Can not save last migration: {e}")
