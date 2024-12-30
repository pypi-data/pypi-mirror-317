import os
import unittest
from unittest.mock import MagicMock

from mongodb_migrator.core import MongoDBMigrator, create_default_config
from tests.conftest import TEST_DEFAULT_CONFIG_FILE


class TestMongoDBMigrator(unittest.TestCase):
    def setUp(self):
        create_default_config(config_file=TEST_DEFAULT_CONFIG_FILE)
        self.migrator = MongoDBMigrator(config_file=TEST_DEFAULT_CONFIG_FILE)

        # Check if MOCK_DB environment variable is set
        self.mock_db = os.getenv("MOCK_DB", "false").lower() == "true"
        if self.mock_db:
            # Mock database methods
            self.migrator.db = MagicMock()

    def test_initialization(self):
        self.migrator.init()
        self.assertTrue(os.path.exists("tests_migrations"))

    def test_create_migration(self):
        self.migrator.init()
        self.migrator.create_migration("test_migration")
        migrations = os.listdir("tests_migrations")
        self.assertTrue(any("test_migration" in migration for migration in migrations))

    def test_migration_history(self):
        self.migrator.init()
        self.migrator.create_migration("test_migration1")
        self.migrator.create_migration("test_migration2")

        if not self.mock_db:
            # Simulate applying one migration in real DB mode
            self.migrator.apply_migrations(target="test_migration1")
        else:
            # Mock the behavior for applied migrations
            self.migrator.get_migration_history = MagicMock(
                return_value={
                    "applied": ["test_migration1.py"],
                    "pending": ["test_migration2.py"],
                }
            )

        history = self.migrator.get_migration_history()

        self.assertTrue(
            any("test_migration1.py" in history for history in history["applied"])
        )
        # Uncomment for pending migration check if needed
        # self.assertTrue(
        #     any("test_migration2.py" in history for history in history["pending"])
        # )

    def test_zzzz_delete_migration(self):
        import shutil

        if not self.mock_db:
            self.migrator.rollback_migrations()
            history = self.migrator.get_migration_history()
            self.assertFalse(
                any("test_migration1.py" in history for history in history["applied"])
            )
        else:
            # Mock the rollback behavior
            self.migrator.rollback_migrations = MagicMock()
            self.migrator.get_migration_history = MagicMock(
                return_value={"applied": [], "pending": []}
            )

        migrations = os.listdir("tests_migrations")
        self.assertTrue(any("test_migration" in migration for migration in migrations))
        shutil.rmtree("tests_migrations")


if __name__ == "__main__":
    unittest.main()
