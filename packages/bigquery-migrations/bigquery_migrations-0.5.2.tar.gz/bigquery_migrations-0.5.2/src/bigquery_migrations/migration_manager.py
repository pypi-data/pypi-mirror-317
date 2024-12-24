from google.cloud import bigquery
from .migration_dir_handler import MigrationDirHandler
from .migration_log_handler import MigrationLogHandler
from .migration_factory import MigrationFactory
from .migration import Migration
from colorama import init, Fore
from typing import Optional, Tuple


class MigrationManager:
    """
    Provides methods to interact with the BigQuery database migration files

    Attributes:
        migration_dir_handler (MigrationDirHandler): Migration directory handler class instance
        migration_log_handler (MigrationLogHandler): Migration log file handler class instance
        migration_factory (MigrationFactory): Migration factory class instance
    """

    def __init__(self, client: bigquery.Client, migrations_dir: str):
        """
        Load class dependecies as attributes

        Args:
            client (bigquery.Client): Google Cloud BigQuery Client
            migrations_dir (str): Migrations directory path
        """
        self.migration_dir_handler = MigrationDirHandler(migrations_dir)
        self.migration_log_handler = MigrationLogHandler(migrations_dir)
        self.migration_factory = MigrationFactory(client, migrations_dir)
        init(autoreset=True)  # For colorama (CLI colored print)

    def list_migrations(self) -> list[str]:
        return self.migration_dir_handler.filename_list()

    def load_migration(self, migration_name: str) -> Migration:
        return self.migration_factory.create(migration_name)

    def get_last_migration(self) -> Tuple[Optional[str], Optional[str]]:
        return self.migration_log_handler.get_last()

    def save_last_migration(self, migration_name: str) -> Optional[bool]:
        return self.migration_log_handler.save_last(migration_name)

    def run(self) -> list[Optional[str]]:
        """
        Run all migrations starting from the last successful one

        Returns:
            list[Optional[str]]: List of applied migration names
        """
        applied_migrations = []
        last_migration, last_timestamp = self.get_last_migration()
        migrations = self.list_migrations()

        # Determine migrations to run
        if last_migration:
            try:
                start_index = migrations.index(last_migration) + 1
                migrations = migrations[start_index:]
            except ValueError:
                print(Fore.RED + f"Error: Last migration '{last_migration}' not found in directory.")
                return applied_migrations
        else:
            print(Fore.CYAN + "No previous migration found. Running all migrations...")

        if not migrations:
            print(Fore.GREEN + "We are up-to-date. Nothing to do now!")

        # Run each migration in sequence
        for migration_name in migrations:
            print(Fore.YELLOW + f"Migrating: {migration_name}")
            migration = self.load_migration(migration_name)
            try:
                migration.up()
                self.save_last_migration(migration_name)
                applied_migrations.append(migration_name)
                print(Fore.GREEN + f"Migrated: {migration_name}")
            except Exception as e:
                print(Fore.RED + f"Error applying migration {migration_name}: {e}")
                break
        return applied_migrations

    def rollback(self, migration_name: str) -> Tuple[str, Optional[str]]:
        """
        Rollback a specific migration

        Args:
            migration_name (str): Migration to rollback

        Returns:
            Tuple(str, Optional[str]): Migrated migration name, Previous migration name
        """
        print(Fore.YELLOW + f"Rolling back migration: {migration_name}")
        migrations = self.list_migrations()
        prev_index = migrations.index(migration_name) - 1
        prev_migration = migrations[prev_index] if prev_index >= 0 else None
        try:
            migration = self.load_migration(migration_name)
            migration.down()
            self.save_last_migration(prev_migration)
            print(Fore.GREEN + f"Successfully rolled back migration: {migration_name}")
        except (FileNotFoundError, Exception, IOError) as e:
            print(Fore.RED + f"Error rolling back migration {migration_name}: {e}")
            migration_name = None
        finally:
            return migration_name, prev_migration
    
    def rollback_last(self):
        """Rollback the last applied migration"""
        last_migration, last_timestamp = self.get_last_migration()
        if not last_migration:
            print(Fore.CYAN + "No migrations have been applied yet.")
            return
        return self.rollback(last_migration)


    def reset(self) -> list[Optional[str]]:
        """
        Rollback all migrations in reverse (time desc) order

        Returns:
            list[Optional[str]]: List of rolledback migration names
        """
        reversed_migrations = []
        migrations = self.list_migrations()

        # Get the last applied migration to start the rollback
        last_migration, last_timestamp = self.get_last_migration()

        if not last_migration:
            print(Fore.CYAN + "No migrations have been applied yet.")
            return reversed_migrations

        print(Fore.CYAN + "Rolling back migrations in reverse order...")

        # If last migration exists, start from it
        if last_migration:
            try:
                start_index = migrations.index(last_migration) + 1
                migrations = migrations[:start_index]
            except ValueError:
                print(Fore.RED + f"Error: Last migration '{last_migration}' not found in directory.")
                return reversed_migrations

        # Rollback each migration in reverse order
        for migration_name in reversed(migrations):
            rolled_back_migration, prev_migration = self.rollback(migration_name)
            if rolled_back_migration:
                reversed_migrations.append(rolled_back_migration)
            else:
                break

        return reversed_migrations
