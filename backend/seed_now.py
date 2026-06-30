import asyncio
from app.core.database import async_session_factory
from app.models.identity.user import User, Role, Permission
from app.core.security import hash_password
from sqlalchemy import select
from sqlalchemy.orm import selectinload

DEFAULT_PERMISSIONS = [
    ("Users.Read", "View users", "Users"),
    ("Users.Write", "Create and edit users", "Users"),
    ("Inventory.Read", "View inventory", "Inventory"),
    ("Inventory.Write", "Modify inventory", "Inventory"),
    ("Inventory.Delete", "Delete inventory records", "Inventory"),
    ("Inventory.Transfer", "Create transfers", "Inventory"),
    ("Inventory.Adjust", "Create adjustments", "Inventory"),
    ("Inventory.ViewHistory", "View inventory history", "Inventory"),
    ("Products.Read", "View products", "Products"),
    ("Products.Create", "Create products", "Products"),
    ("Products.Update", "Update products", "Products"),
    ("Products.Delete", "Delete products", "Products"),
    ("Categories.Read", "View categories", "Categories"),
    ("Categories.Write", "Manage categories", "Categories"),
    ("Brands.Read", "View brands", "Brands"),
    ("Brands.Write", "Manage brands", "Brands"),
    ("Warehouses.Read", "View warehouses", "Warehouses"),
    ("Warehouses.Write", "Manage warehouses", "Warehouses"),
    ("Suppliers.Read", "View suppliers", "Suppliers"),
    ("Suppliers.Create", "Create suppliers", "Suppliers"),
    ("Suppliers.Update", "Update suppliers", "Suppliers"),
    ("Suppliers.Delete", "Delete suppliers", "Suppliers"),
    ("PurchaseOrders.Read", "View purchase orders", "Procurement"),
    ("PurchaseOrders.Create", "Create purchase orders", "Procurement"),
    ("PurchaseOrders.Update", "Update purchase orders", "Procurement"),
    ("PurchaseOrders.Approve", "Approve purchase orders", "Procurement"),
    ("PurchaseOrders.Receive", "Receive purchase orders", "Procurement"),
    ("Procurement.Manage", "Manage procurement", "Procurement"),
    ("Finance.Read", "View financial data", "Finance"),
    ("Finance.Write", "Manage financial data", "Finance"),
    ("Dashboard.Read", "View dashboard", "Dashboard"),
    ("Dashboard.View", "Access dashboard", "Dashboard"),
    ("Analytics.Read", "View analytics", "Analytics"),
    ("Analytics.Advanced", "Advanced analytics", "Analytics"),
    ("Reports.Read", "View reports", "Reports"),
    ("Reports.Export", "Export reports", "Reports"),
    ("Reports.Manage", "Manage reports", "Reports"),
    ("AI.Use", "Use AI features", "AI"),
    ("Automation.Read", "View automation", "Automation"),
    ("Automation.Create", "Create workflows", "Automation"),
    ("Automation.Update", "Update workflows", "Automation"),
    ("Automation.Execute", "Execute workflows", "Automation"),
    ("Automation.Approve", "Approve workflows", "Automation"),
    ("Workflow.Publish", "Publish workflows", "Automation"),
    ("Workflow.Delete", "Delete workflows", "Automation"),
    ("Audit.Read", "View audit logs", "Audit"),
    ("Settings.Manage", "Manage system settings", "Settings"),
    ("Simulation.Read", "View simulation", "Simulation"),
    ("Simulation.Manage", "Manage simulation", "Simulation"),
]

ADMIN_PERMS = [p[0] for p in DEFAULT_PERMISSIONS]

async def seed():
    async with async_session_factory() as db:
        # Create all permissions
        perm_objects = {}
        for name, desc, group in DEFAULT_PERMISSIONS:
            result = await db.execute(select(Permission).where(Permission.name == name))
            p = result.scalar_one_or_none()
            if not p:
                p = Permission(name=name, description=desc, group=group)
                db.add(p)
                await db.flush()
            perm_objects[name] = p
        print(f"Created/verified {len(perm_objects)} permissions")

        # Create Admin role
        result = await db.execute(
            select(Role).where(Role.name == "Admin").options(selectinload(Role.permissions))
        )
        admin_role = result.scalars().first()
        if not admin_role:
            admin_role = Role(name="Admin", description="Default Admin role", is_system=True)
            db.add(admin_role)
            await db.flush()
            admin_role.permissions = list(perm_objects.values())
            await db.flush()
            print("Admin role created with all permissions")
        else:
            current = {p.name for p in admin_role.permissions}
            new = set(ADMIN_PERMS)
            if current != new:
                admin_role.permissions = list(perm_objects.values())
                await db.flush()
                print("Admin role permissions updated")
            else:
                print("Admin role already configured")

        # Create admin user
        result = await db.execute(
            select(User).where(User.email == "admin@procureflow.ai").options(selectinload(User.roles))
        )
        user = result.scalars().first()
        if not user:
            user = User(
                email="admin@procureflow.ai",
                name="System Admin",
                hashed_password=hash_password("Admin@123"),
                is_active=True,
            )
            db.add(user)
            await db.flush()
        user.roles = [admin_role]
        await db.commit()
        print(f"Admin user ready: {user.email}")
        print(f"Roles: {[r.name for r in user.roles]}")
        print(f"Permissions: {len([p for r in user.roles for p in r.permissions])}")

asyncio.run(seed())
