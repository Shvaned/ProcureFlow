import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.middleware.auth import get_current_user, RequirePermission
from app.services.product_service import ProductService, CategoryService, BrandService, UnitService
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.repositories.base import FilterCondition, FilterOperator, SortParam, PaginationParams

router = APIRouter()


def parse_filters(filters_str: str | None = None) -> list[FilterCondition] | None:
    if not filters_str:
        return None
    import json
    try:
        raw = json.loads(filters_str)
        return [FilterCondition(**f) for f in raw]
    except Exception:
        return None


def parse_sorting(sort_str: str | None = None) -> list[SortParam] | None:
    if not sort_str:
        return None
    import json
    try:
        raw = json.loads(sort_str)
        return [SortParam(**s) for s in raw]
    except Exception:
        return None


# Products
@router.get("/products")
async def list_products(
    filters: str | None = Query(None),
    sort: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    _: User = Depends(RequirePermission("Products.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    result = await service.list_products(
        filters=parse_filters(filters),
        sorting=parse_sorting(sort),
        pagination=PaginationParams(page=page, page_size=page_size),
    )
    return StandardResponse.paginated(
        data=[{
            "id": str(p.id), "sku": p.sku, "barcode": p.barcode, "name": p.name,
            "brand": {"id": str(p.brand.id), "name": p.brand.name} if p.brand else None,
            "category": {"id": str(p.category.id), "name": p.category.name} if p.category else None,
            "cost_price": float(p.cost_price), "selling_price": float(p.selling_price),
            "mrp": float(p.mrp) if p.mrp else None,
            "gst_rate": float(p.gst_rate), "is_active": p.is_active,
            "hsn_code": p.hsn_code, "country_of_origin": p.country_of_origin,
            "created_at": p.created_at.isoformat(),
        } for p in result.items],
        pagination=result,
        message="Products retrieved",
    )


@router.get("/products/{product_id}")
async def get_product(
    product_id: uuid.UUID,
    _: User = Depends(RequirePermission("Products.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.get_product(product_id)
    return StandardResponse.ok(data={
        "id": str(product.id), "sku": product.sku, "barcode": product.barcode,
        "name": product.name, "short_description": product.short_description,
        "long_description": product.long_description,
        "brand": {"id": str(product.brand.id), "name": product.brand.name} if product.brand else None,
        "category": {"id": str(product.category.id), "name": product.category.name} if product.category else None,
        "unit": {"id": str(product.unit.id), "name": product.unit.name} if product.unit else None,
        "cost_price": float(product.cost_price), "selling_price": float(product.selling_price),
        "mrp": float(product.mrp) if product.mrp else None,
        "gst_rate": float(product.gst_rate), "hsn_code": product.hsn_code,
        "country_of_origin": product.country_of_origin,
        "manufacturer": product.manufacturer,
        "is_active": product.is_active, "is_hazardous": product.is_hazardous,
        "is_cold_storage": product.is_cold_storage,
        "min_order_qty": product.min_order_qty,
        "reorder_level": product.reorder_level, "safety_stock": product.safety_stock,
        "images": [{"id": str(i.id), "url": i.url, "is_primary": i.is_primary} for i in product.images],
        "documents": [{"id": str(d.id), "name": d.name, "document_type": d.document_type, "url": d.url} for d in product.documents],
        "attributes": [{"key": a.key, "value": a.value} for a in product.attributes],
        "created_at": product.created_at.isoformat(), "updated_at": product.updated_at.isoformat(),
    })


@router.post("/products")
async def create_product(
    body: dict,
    _: User = Depends(RequirePermission("Products.Create")),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.create_product(body)
    return StandardResponse.ok(
        data={"id": str(product.id)}, message="Product created"
    )


@router.put("/products/{product_id}")
async def update_product(
    product_id: uuid.UUID,
    body: dict,
    _: User = Depends(RequirePermission("Products.Update")),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    product = await service.update_product(product_id, body)
    return StandardResponse.ok(
        data={"id": str(product.id)}, message="Product updated"
    )


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: uuid.UUID,
    _: User = Depends(RequirePermission("Products.Delete")),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    await service.delete_product(product_id)
    return StandardResponse.ok(message="Product deleted")


# Categories
@router.get("/categories")
async def list_categories(
    _: User = Depends(RequirePermission("Categories.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)
    cats = await service.list_categories()

    def build_tree(categories, parent_id=None):
        result = []
        for c in categories:
            if (parent_id is None and c.parent_id is None) or (parent_id and c.parent_id == parent_id):
                result.append({
                    "id": str(c.id), "name": c.name, "slug": c.slug,
                    "description": c.description, "display_order": c.display_order,
                    "children": build_tree(categories, c.id),
                })
        return result

    return StandardResponse.ok(data=build_tree(cats))


@router.post("/categories")
async def create_category(
    body: dict,
    _: User = Depends(RequirePermission("Categories.Write")),
    db: AsyncSession = Depends(get_db),
):
    service = CategoryService(db)
    cat = await service.create_category(body)
    return StandardResponse.ok(data={"id": str(cat.id)}, message="Category created")


# Brands
@router.get("/brands")
async def list_brands(
    _: User = Depends(RequirePermission("Brands.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = BrandService(db)
    result = await service.list_brands()
    return StandardResponse.ok(data=[
        {"id": str(b.id), "name": b.name, "country": b.country,
         "is_active": b.is_active, "website": b.website}
        for b in result.items
    ])


@router.post("/brands")
async def create_brand(
    body: dict,
    _: User = Depends(RequirePermission("Brands.Write")),
    db: AsyncSession = Depends(get_db),
):
    service = BrandService(db)
    brand = await service.create_brand(body)
    return StandardResponse.ok(data={"id": str(brand.id)}, message="Brand created")


# Units
@router.get("/units")
async def list_units(
    _: User = Depends(RequirePermission("Products.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = UnitService(db)
    units = await service.list_units()
    return StandardResponse.ok(data=[
        {"id": str(u.id), "name": u.name, "symbol": u.symbol,
         "conversion_factor": float(u.conversion_factor)}
        for u in units
    ])
