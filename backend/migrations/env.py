import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.models.base import Base
import app.models.identity.user  # noqa: F401
import app.models.product.product  # noqa: F401
import app.models.inventory.inventory  # noqa: F401
import app.models.warehouse.warehouse  # noqa: F401
import app.models.supplier.supplier  # noqa: F401
import app.models.procurement.procurement  # noqa: F401
import app.models.finance.finance  # noqa: F401
import app.models.ai.ai_models  # noqa: F401
import app.models.automation.automation  # noqa: F401
import app.models.notification.notification  # noqa: F401
import app.models.audit.audit_log  # noqa: F401
import app.models.file_storage.file_storage  # noqa: F401
import app.models.dashboard.dashboard  # noqa: F401
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
