"""Seed default roles and permissions."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.identity.user import Role, Permission, User
from app.core.security import hash_password

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

DEFAULT_ROLES = {
    "Admin": [
        "Users.Read", "Users.Write",
        "Inventory.Read", "Inventory.Write", "Inventory.Delete",
        "Inventory.Transfer", "Inventory.Adjust", "Inventory.ViewHistory",
        "Products.Read", "Products.Create", "Products.Update", "Products.Delete",
        "Categories.Read", "Categories.Write",
        "Brands.Read", "Brands.Write",
        "Warehouses.Read", "Warehouses.Write",
        "Suppliers.Read", "Suppliers.Create", "Suppliers.Update", "Suppliers.Delete",
        "PurchaseOrders.Read", "PurchaseOrders.Create", "PurchaseOrders.Update",
        "PurchaseOrders.Approve", "PurchaseOrders.Receive",
        "Procurement.Manage", "Finance.Read", "Finance.Write",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Analytics.Advanced",
        "Reports.Read", "Reports.Export", "Reports.Manage",
        "AI.Use", "Automation.Read", "Automation.Create", "Automation.Update",
        "Automation.Execute", "Automation.Approve", "Workflow.Publish", "Workflow.Delete",
        "Audit.Read", "Settings.Manage", "Simulation.Read", "Simulation.Manage",
    ],
    "Operations Manager": [
        "Users.Read", "Inventory.Read", "Inventory.ViewHistory",
        "Products.Read", "Categories.Read", "Brands.Read",
        "Warehouses.Read", "Suppliers.Read",
        "PurchaseOrders.Read", "PurchaseOrders.Approve",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Reports.Read", "Reports.Export",
        "AI.Use", "Automation.Read", "Audit.Read", "Simulation.Read",
    ],
    "Warehouse Manager": [
        "Inventory.Read", "Inventory.Write", "Inventory.Transfer",
        "Inventory.Adjust", "Inventory.ViewHistory",
        "Products.Read", "Categories.Read", "Brands.Read",
        "Warehouses.Read", "Warehouses.Write",
        "PurchaseOrders.Read", "PurchaseOrders.Receive",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Reports.Read",
        "Simulation.Read",
    ],
    "Procurement Manager": [
        "Inventory.Read", "Inventory.ViewHistory",
        "Products.Read", "Categories.Read", "Brands.Read",
        "Warehouses.Read", "Suppliers.Read", "Suppliers.Create", "Suppliers.Update",
        "PurchaseOrders.Read", "PurchaseOrders.Create", "PurchaseOrders.Update",
        "PurchaseOrders.Approve", "PurchaseOrders.Receive", "Procurement.Manage",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Reports.Read", "Reports.Export",
        "AI.Use", "Audit.Read",
    ],
    "Finance Manager": [
        "Inventory.Read", "Inventory.ViewHistory",
        "Products.Read", "Categories.Read", "Brands.Read",
        "Warehouses.Read", "Suppliers.Read",
        "PurchaseOrders.Read", "Finance.Read", "Finance.Write",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Reports.Read", "Reports.Export",
        "Audit.Read",
    ],
    "Viewer": [
        "Inventory.Read", "Products.Read", "Categories.Read", "Brands.Read",
        "Warehouses.Read", "Suppliers.Read", "PurchaseOrders.Read",
        "Dashboard.Read", "Dashboard.View", "Analytics.Read", "Reports.Read",
    ],
}


async def seed_permissions(db: AsyncSession):
    for name, desc, group in DEFAULT_PERMISSIONS:
        result = await db.execute(select(Permission).where(Permission.name == name))
        if not result.scalar_one_or_none():
            db.add(Permission(name=name, description=desc, group=group))
    await db.flush()


async def seed_roles(db: AsyncSession):
    await seed_permissions(db)
    for role_name, perm_names in DEFAULT_ROLES.items():
        from sqlalchemy.orm import selectinload
        result = await db.execute(
            select(Role).where(Role.name == role_name).options(selectinload(Role.permissions))
        )
        role = result.scalars().first()
        if not role:
            role = Role(name=role_name, description=f"Default {role_name} role", is_system=True)
            db.add(role)
            await db.flush()
        perm_result = await db.execute(
            select(Permission).where(Permission.name.in_(perm_names))
        )
        role.permissions = list(perm_result.scalars().all())
    await db.flush()


async def seed_admin(db: AsyncSession):
    result = await db.execute(select(User).where(User.email == "admin@procureflow.ai"))
    if not result.scalar_one_or_none():
        admin_role_result = await db.execute(select(Role).where(Role.name == "Admin"))
        admin_role = admin_role_result.scalar_one_or_none()
        user = User(
            email="admin@procureflow.ai",
            name="System Admin",
            hashed_password=hash_password("Admin@123"),
            is_active=True,
        )
        if admin_role:
            user.roles = [admin_role]
        db.add(user)
        await db.flush()
