"""One-time setup: create all tables using existing engine."""
import asyncio
from app.core.database import engine
from app.models.base import Base

# Import ALL models to register tables with Base.metadata
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


async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("All tables created successfully.")
    print("Done. Run 'python seed_sql.py' for identity data if needed.")


if __name__ == "__main__":
    asyncio.run(setup())
