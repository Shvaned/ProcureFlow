import asyncio, uuid
from datetime import datetime, timezone
from app.core.database import async_session_factory
from app.core.security import hash_password
from sqlalchemy import text

async def main():
    now = datetime.now(timezone.utc)
    uid = uuid.uuid4()
    pwd = hash_password("Admin@123")
    async with async_session_factory() as db:
        result = await db.execute(text("SELECT id FROM roles WHERE name = 'Admin'"))
        row = result.fetchone()
        if not row:
            print("Admin role not found")
            return
        rid = row[0]
        await db.execute(text(
            "INSERT INTO users (id, email, name, hashed_password, is_active, is_locked, "
            "failed_login_attempts, is_deleted, created_at, updated_at) "
            "VALUES (:id, :email, :name, :pwd, true, false, 0, false, :now, :now)"
        ), {"id": uid, "email": "admin@procureflow.ai", "name": "System Admin", "pwd": pwd, "now": now})
        await db.execute(text(
            "INSERT INTO user_roles (user_id, role_id) VALUES (:uid, :rid)"
        ), {"uid": uid, "rid": rid})
        await db.commit()
        print("Admin created: admin@procureflow.ai / Admin@123")

asyncio.run(main())
