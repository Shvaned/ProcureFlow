import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import async_session_factory
from app.models.identity.user import User, Role

async def main():
    async with async_session_factory() as db:
        result = await db.execute(
            select(User).where(User.email == "admin@procureflow.ai").options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            print("Admin user not found")
            return

        role_result = await db.execute(
            select(Role).where(Role.name == "Admin").options(selectinload(Role.permissions))
        )
        admin_role = role_result.scalar_one_or_none()
        if not admin_role:
            print("Admin role not found")
            return

        user.roles = [admin_role]
        await db.commit()
        print(f"Done. User: {user.email}, Roles: {[r.name for r in user.roles]}, Permissions: {len(admin_role.permissions)}")

asyncio.run(main())
