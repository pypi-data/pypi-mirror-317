import click

from mongodb_migrator.core import MongoDBMigrator, create_default_config


@click.group()
def cli():
    """MongoDB Migrator CLI."""
    pass


@cli.command()
@click.option(
    "--config-file",
    default="mongodb_migrator_config.yaml",
    help="Path to the config file.",
)
def init(config_file):
    """Initialize the migrations system."""
    create_default_config(config_file)
    migrator = MongoDBMigrator(config_file)
    migrator.init()


@cli.command()
@click.argument("name")
@click.option(
    "--config-file",
    default="mongodb_migrator_config.yaml",
    help="Path to the config file.",
)
def create(name, config_file):
    """Create a new migration file."""
    migrator = MongoDBMigrator(config_file)
    migrator.create_migration(name)


@cli.command()
@click.argument("target", required=False, default="all")
@click.option(
    "--config-file",
    default="mongodb_migrator_config.yaml",
    help="Path to the config file.",
)
def upgrade(target, config_file):
    """Apply migrations up to a specific target."""
    migrator = MongoDBMigrator(config_file)
    if target == "all":
        migrator.apply_migrations()
    else:
        migrator.apply_migrations(target)


@cli.command()
@click.argument("target", required=False, default="all")
@click.option(
    "--config-file",
    default="mongodb_migrator_config.yaml",
    help="Path to the config file.",
)
def downgrade(target, config_file):
    """Rollback migrations down to a specific target."""
    migrator = MongoDBMigrator(config_file)
    if target == "all":
        migrator.rollback_migrations()
    else:
        migrator.rollback_migrations(target)


@cli.command()
@click.option(
    "--config-file",
    default="mongodb_migrator_config.yaml",
    help="Path to the config file.",
)
def history(config_file):
    """Show the migration history."""
    migrator = MongoDBMigrator(config_file)
    migrator.show_migration_history()


if __name__ == "__main__":
    cli()
