from __future__ import with_statement
import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# make project root importable so `from farm_cli...` works
sys.path.insert(0, os.path.abspath('.'))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# import your SQLAlchemy Base and DATABASE_URL
from farm_cli.db.models import Base
from farm_cli.config import DATABASE_URL

target_metadata = Base.metadata

# set sqlalchemy.url from your environment-based config
section = config.get_section(config.config_ini_section)
section['sqlalchemy.url'] = DATABASE_URL


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = section.get('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
