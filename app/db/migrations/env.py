import argparse
import sys
import os
from typing import Optional

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

VERSION_TABLE_SCHEMA = 'alembic'

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from app.db.base import Base

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


from app.core.config import settings


def get_db_name_from_args() -> Optional[str]:
    if context.get_x_argument(as_dictionary=True).get('dbname'):
        return context.get_x_argument(as_dictionary=True)['dbname']
    else:
        return None


def get_url():
    db_name = get_db_name_from_args()
    if db_name == 'test':
        db_url = settings.TEST_DATABASE_URL
    else:
        user = settings.POSTGRES_USER
        password = settings.POSTGRES_PASSWORD
        server = settings.POSTGRES_SERVER
        db = settings.POSTGRES_DB
        db_url = f"postgresql://{user}:{password}@{server}/{db}"
    return db_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            include_schema=True,
            version_table_schema=VERSION_TABLE_SCHEMA
        )

        connection.execute(f'CREATE SCHEMA IF NOT EXISTS {VERSION_TABLE_SCHEMA}')

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
