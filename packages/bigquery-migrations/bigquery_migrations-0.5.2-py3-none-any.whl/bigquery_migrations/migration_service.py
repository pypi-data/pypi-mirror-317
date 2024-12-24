import os
from .bq_client import BqClient
from .migration_manager import MigrationManager


class MigrationService:

    def __init__(self, sa_dir: str, sa_fname: str, gcp_id: str, migrations_dir: str):
        self.bq_client = self._auth(sa_dir, sa_fname, gcp_id)
        self.migrations_dir = migrations_dir

    def create(self):
        return MigrationManager(self.bq_client, self.migrations_dir)

    def _auth(self, sa_dir: str, sa_fname: str, gcp_id: str):
        return BqClient.authWithSa(os.path.join(sa_dir, sa_fname), gcp_id)
