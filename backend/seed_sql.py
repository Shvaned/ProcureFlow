"""Seed using raw SQL via asyncpg — bypasses ORM lazy-load issues entirely."""
import asyncio
import uuid
from datetime import datetime, timezone
from app.core.database import async_session_factory
from app.core.security import hash_password
from sqlalchemy import text

PERMS = [
    ("Users.Read","View users","Users"),("Users.Write","Create and edit users","Users"),
    ("Inventory.Read","View inventory","Inventory"),("Inventory.Write","Modify inventory","Inventory"),
    ("Inventory.Delete","Delete inventory records","Inventory"),("Inventory.Transfer","Create transfers","Inventory"),
    ("Inventory.Adjust","Create adjustments","Inventory"),("Inventory.ViewHistory","View inventory history","Inventory"),
    ("Products.Read","View products","Products"),("Products.Create","Create products","Products"),
    ("Products.Update","Update products","Products"),("Products.Delete","Delete products","Products"),
    ("Categories.Read","View categories","Categories"),("Categories.Write","Manage categories","Categories"),
    ("Brands.Read","View brands","Brands"),("Brands.Write","Manage brands","Brands"),
    ("Warehouses.Read","View warehouses","Warehouses"),("Warehouses.Write","Manage warehouses","Warehouses"),
    ("Suppliers.Read","View suppliers","Suppliers"),("Suppliers.Create","Create suppliers","Suppliers"),
    ("Suppliers.Update","Update suppliers","Suppliers"),("Suppliers.Delete","Delete suppliers","Suppliers"),
    ("PurchaseOrders.Read","View purchase orders","Procurement"),("PurchaseOrders.Create","Create purchase orders","Procurement"),
    ("PurchaseOrders.Update","Update purchase orders","Procurement"),("PurchaseOrders.Approve","Approve purchase orders","Procurement"),
    ("PurchaseOrders.Receive","Receive purchase orders","Procurement"),("Procurement.Manage","Manage procurement","Procurement"),
    ("Finance.Read","View financial data","Finance"),("Finance.Write","Manage financial data","Finance"),
    ("Dashboard.Read","View dashboard","Dashboard"),("Dashboard.View","Access dashboard","Dashboard"),
    ("Analytics.Read","View analytics","Analytics"),("Analytics.Advanced","Advanced analytics","Analytics"),
    ("Reports.Read","View reports","Reports"),("Reports.Export","Export reports","Reports"),
    ("Reports.Manage","Manage reports","Reports"),("AI.Use","Use AI features","AI"),
    ("Automation.Read","View automation","Automation"),("Automation.Create","Create workflows","Automation"),
    ("Automation.Update","Update workflows","Automation"),("Automation.Execute","Execute workflows","Automation"),
    ("Automation.Approve","Approve workflows","Automation"),("Workflow.Publish","Publish workflows","Automation"),
    ("Workflow.Delete","Delete workflows","Automation"),("Audit.Read","View audit logs","Audit"),
    ("Settings.Manage","Manage system settings","Settings"),("Simulation.Read","View simulation","Simulation"),
    ("Simulation.Manage","Manage simulation","Simulation"),
]

async def seed():
    now = datetime.now(timezone.utc)
    admin_role_id = uuid.uuid4()
    admin_user_id = uuid.uuid4()
    pwd = hash_password("Admin@123")

    async with async_session_factory() as db:
        # Delete existing data for clean start
        await db.execute(text("DELETE FROM user_roles"))
        await db.execute(text("DELETE FROM role_permissions"))
        await db.execute(text("DELETE FROM users"))
        await db.execute(text("DELETE FROM roles"))
        await db.execute(text("DELETE FROM permissions"))
        await db.flush()

        # Insert permissions
        for name, desc, grp in PERMS:
            await db.execute(text(
                "INSERT INTO permissions (id, name, description, \"group\", created_at, updated_at) "
                "VALUES (:id, :name, :desc, :grp, :now, :now)"
            ), {"id": uuid.uuid4(), "name": name, "desc": desc, "grp": grp, "now": now})
        print(f"Inserted {len(PERMS)} permissions")

        # Create Admin role
        await db.execute(text(
            "INSERT INTO roles (id, name, description, is_system, created_at, updated_at) "
            "VALUES (:id, 'Admin', 'Default Admin role', true, :now, :now)"
        ), {"id": admin_role_id, "now": now})

        # Assign all permissions to Admin role
        result = await db.execute(text("SELECT id, name FROM permissions"))
        for row in result:
            await db.execute(text(
                "INSERT INTO role_permissions (role_id, permission_id) VALUES (:rid, :pid)"
            ), {"rid": admin_role_id, "pid": row[0]})
        print(f"Admin role created with all permissions")

        # Create admin user
        await db.execute(text(
            "INSERT INTO users (id, email, name, hashed_password, is_active, is_locked, "
            "failed_login_attempts, is_deleted, created_at, updated_at) "
            "VALUES (:id, :email, :name, :pwd, true, false, 0, false, :now, :now)"
        ), {"id": admin_user_id, "email": "admin@procureflow.ai", "name": "System Admin", "pwd": pwd, "now": now})

        # Assign Admin role
        await db.execute(text(
            "INSERT INTO user_roles (user_id, role_id) VALUES (:uid, :rid)"
        ), {"uid": admin_user_id, "rid": admin_role_id})

        await db.commit()
        print(f"Admin user created: admin@procureflow.ai / Admin@123")
        print("Seed complete.")

asyncio.run(seed())
