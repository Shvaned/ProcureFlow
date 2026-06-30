from fastapi import APIRouter

from app.api.ai_routes import router as ai_router
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.inventory import router as inventory_router
from app.api.procurement import router as procurement_router
from app.api.products import router as products_router
from app.api.scenarios import router as scenarios_router
from app.api.simulation import router as simulation_router
from app.api.sku import router as sku_router
from app.api.supplier_intelligence import router as supplier_intel_router
from app.api.workflows import router as workflows_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(products_router, tags=["Product Catalog"])
api_router.include_router(inventory_router, tags=["Inventory & Warehouse"])
api_router.include_router(procurement_router, tags=["Suppliers & Procurement"])
api_router.include_router(analytics_router, tags=["Analytics & KPIs"])
api_router.include_router(simulation_router, tags=["Business Simulation"])
api_router.include_router(workflows_router, tags=["Workflow Automation"])
api_router.include_router(supplier_intel_router, tags=["Supplier Intelligence"])
api_router.include_router(scenarios_router, tags=["Scenario Lab"])
api_router.include_router(sku_router, tags=["SKU Management"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Workspace"])
