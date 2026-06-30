"""SKU Management API — generation, preview, validation, prefix/brand management."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.providers import get_db
from app.middleware.auth import RequirePermission
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.services.sku_service import SKUService

router = APIRouter()


@router.get("/sku/prefixes")
async def list_prefixes(
    _: User = Depends(RequirePermission("Products.Read")),
):
    return StandardResponse.ok(data=SKUService.list_prefixes())


@router.get("/sku/brand-codes")
async def list_brand_codes(
    _: User = Depends(RequirePermission("Products.Read")),
):
    return StandardResponse.ok(data=SKUService.list_brand_codes())


@router.post("/sku/preview")
async def preview_sku(
    body: dict,
    _: User = Depends(RequirePermission("Products.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SKUService(db)
    sku = await svc.preview_sku(
        category_name=body.get("category_name", ""),
        brand_name=body.get("brand_name", ""),
        variant=body.get("variant"),
    )
    return StandardResponse.ok(data={"sku": sku})


@router.post("/sku/generate")
async def generate_sku(
    body: dict,
    _: User = Depends(RequirePermission("Products.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = SKUService(db)
    sku = await svc.generate_sku(
        category_name=body.get("category_name", ""),
        brand_name=body.get("brand_name", ""),
        variant=body.get("variant"),
    )
    return StandardResponse.ok(data={"sku": sku}, message="SKU generated")


@router.post("/sku/validate")
async def validate_sku(
    body: dict,
    _: User = Depends(RequirePermission("Products.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = SKUService(db)
    result = await svc.validate_sku(body.get("sku", ""))
    return StandardResponse.ok(data=result)


@router.post("/sku/reserve")
async def reserve_sku(
    body: dict,
    _: User = Depends(RequirePermission("Products.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = SKUService(db)
    result = await svc.reserve_sku(body.get("sku", ""))
    return StandardResponse.ok(data=result)
