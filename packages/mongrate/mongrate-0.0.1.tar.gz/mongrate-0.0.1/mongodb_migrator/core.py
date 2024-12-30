# flake8: noqa
import importlib
import os
from datetime import datetime

import pymongo
import yaml  # type: ignore

DEFAULT_CONFIG_FILE = "mongodb_migrator_config.yaml"


def create_default_config(config_file=DEFAULT_CONFIG_FILE):
    """Create a default configuration file."""
    if not os.path.exists(config_file):
        config = {
            "db_url": "mongodb://mongoadmin:secret@localhost:27017",
            "db_name": "my_database",
            "migrations_dir": "migrations",
        }
        with open(config_file, "w") as f:
            yaml.dump(config, f)
        print(f"Created default config file: {config_file}")
    else:
        print(f"Config file already exists: {config_file}")


def load_config(config_file=DEFAULT_CONFIG_FILE):
    """Load the configuration from the file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


class MongoDBMigrator:
    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        config = load_config(config_file)
        self.db_url = config["db_url"]
        self.db_name = config["db_name"]
        self.migrations_dir = config.get("migrations_dir", "migrations")

        self.client = pymongo.MongoClient(self.db_url)
        self.db = self.client[self.db_name]
        self.migrations_collection = self.db["_migrations"]

    def init(self):
        """Initialize the migrations directory and system."""
        if not os.path.exists(self.migrations_dir):
            os.makedirs(self.migrations_dir)
            print(f"Created migrations directory: {self.migrations_dir}")
        else:
            print(f"Migrations directory already exists: {self.migrations_dir}")

        if "_migrations" not in self.db.list_collection_names():
            self.db.create_collection("_migrations")
            print("Initialized migrations tracking collection in the database.")

    def create_migration(self, name):
        """Create a new migration file."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{name}.py"
        filepath = os.path.join(self.migrations_dir, filename)

        migration_template = f"""# Migration: {name}
# Generated on: {datetime.now().isoformat()}

def upgrade(db):
    # Write upgrade logic here
    pass

def downgrade(db):
    # Write downgrade logic here
    pass
"""
        with open(filepath, "w") as f:
            f.write(migration_template)
        print(f"Created migration file: {filepath}")

    def apply_migrations(self, target=None):
        """Apply migrations up to a specific target."""
        applied_migrations = {
            doc["migration"] for doc in self.migrations_collection.find()
        }
        migration_files = sorted(os.listdir(self.migrations_dir))
        applied = False

        for filename in migration_files:
            if filename.endswith(".py") and filename not in applied_migrations:
                if target and filename > target:
                    break

                module_name = f"{self.migrations_dir}.{filename[:-3]}"
                # import pdb; pdb.set_trace()
                migration = importlib.import_module(module_name)

                print(f"Applying migration: {filename}")
                migration.upgrade(self.db)
                self.migrations_collection.insert_one({"migration": filename})
                print(f"Applied: {filename}")
                applied = True

                if target and filename == target:
                    break

        if not applied:
            print("No pending migrations to apply.")

    def rollback_migrations(self, target=None):
        """Rollback migrations down to a specific target."""
        applied_migrations = list(
            doc["migration"] for doc in self.migrations_collection.find()
        )
        applied_migrations.sort(reverse=True)
        reverted = False

        for filename in applied_migrations:
            if target and filename <= target:
                break

            module_name = f"{self.migrations_dir}.{filename[:-3]}"
            migration = importlib.import_module(module_name)

            print(f"Rolling back migration: {filename}")
            migration.downgrade(self.db)
            self.migrations_collection.delete_one({"migration": filename})
            print(f"Rolled back: {filename}")
            reverted = True

            if target and filename == target:
                break

        if not reverted:
            print("No migrations to rollback.")

    def get_migration_history(self):
        """Get the history of applied and pending migrations."""
        applied_migrations = list(
            doc["migration"] for doc in self.migrations_collection.find()
        )
        migration_files = sorted(os.listdir(self.migrations_dir))

        applied = []
        pending = []

        for migration in migration_files:
            if migration.endswith(".py"):
                if migration in applied_migrations:
                    applied.append(migration)
                else:
                    pending.append(migration)

        return {"applied": applied, "pending": pending}

    def show_migration_history(self):
        """Print migration history to the console."""
        history = self.get_migration_history()

        print("\nApplied Migrations:")
        for migration in history["applied"]:
            print(f"  - {migration}")

        print("\nPending Migrations:")
        for migration in history["pending"]:
            print(f"  - {migration}")

        if not history["applied"]:
            print("No migrations have been applied yet.")

        if not history["pending"]:
            print("No pending migrations.")
