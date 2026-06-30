import uuid
from decimal import Decimal
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.repositories.base import BaseRepository, FilterCondition, FilterOperator, SortParam, PaginationParams
from app.models.product.product import Product, Category, Brand, Unit, ProductImage, ProductDocument
from app.core.exceptions import NotFoundException, ConflictException, ValidationException


class ProductRepository(BaseRepository[Product]):
    model = Product

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def get_by_barcode(self, barcode: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.barcode == barcode))
        return result.scalar_one_or_none()

    async def list_with_relations(self, filters=None, sorting=None, pagination=None):
        stmt = select(Product).options(
            selectinload(Product.brand),
            selectinload(Product.category),
        )
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_sorting(stmt, sorting)

        total = await self.count(filters)
        if pagination:
            offset = (pagination.page - 1) * pagination.page_size
            stmt = stmt.offset(offset).limit(pagination.page_size)
            total_pages = max(1, (total + pagination.page_size - 1) // pagination.page_size)
            from app.repositories.base import PaginatedResult
            return PaginatedResult(
                items=(await self.db.execute(stmt)).scalars().unique().all(),
                total=total, page=pagination.page, page_size=pagination.page_size,
                total_pages=total_pages,
                has_next=pagination.page < total_pages,
                has_previous=pagination.page > 1,
            )
        from app.repositories.base import PaginatedResult
        return PaginatedResult(
            items=(await self.db.execute(stmt)).scalars().unique().all(),
            total=total, page=1, page_size=total, total_pages=1,
            has_next=False, has_previous=False,
        )


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProductRepository(db)

    async def list_products(self, filters=None, sorting=None, pagination=None):
        return await self.repo.list_with_relations(filters, sorting, pagination)

    async def get_product(self, product_id: uuid.UUID) -> Product:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id).options(
                selectinload(Product.brand),
                selectinload(Product.category),
                selectinload(Product.images),
                selectinload(Product.documents),
                selectinload(Product.attributes),
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise NotFoundException("Product not found")
        return product

    async def _resolve_category_id(self, name: str) -> uuid.UUID | None:
        if not name:
            return None
        result = await self.db.execute(select(Category).where(Category.name == name))
        cat = result.scalar_one_or_none()
        return cat.id if cat else None

    async def _resolve_brand_id(self, name: str) -> uuid.UUID | None:
        if not name:
            return None
        result = await self.db.execute(select(Brand).where(Brand.name == name))
        brand = result.scalar_one_or_none()
        return brand.id if brand else None

    async def create_product(self, data: dict) -> Product:
        sku = data.get("sku", "").strip()
        if not sku:
            from app.services.sku_service import SKUService
            sku_svc = SKUService(self.db)
            sku = await sku_svc.generate_sku(
                category_name=data.get("category_name", data.get("category", "General")),
                brand_name=data.get("brand_name", data.get("brand", "Generic")),
                variant=data.get("variant"),
            )

        existing = await self.repo.get_by_sku(sku)
        if existing:
            raise ConflictException(f"Product with SKU '{sku}' already exists")
        if data.get("barcode"):
            existing = await self.repo.get_by_barcode(data["barcode"])
            if existing:
                raise ConflictException(f"Product with barcode '{data['barcode']}' already exists")
        if float(data.get("cost_price", 0)) < 0:
            raise ValidationException("Cost price cannot be negative")
        if float(data.get("selling_price", 0)) < 0:
            raise ValidationException("Selling price cannot be negative")

        # Resolve category/brand names to IDs
        cat_id = data.get("category_id")
        if not cat_id and (data.get("category_name") or data.get("category")):
            cat_id = await self._resolve_category_id(data.get("category_name") or data.get("category"))
        brand_id = data.get("brand_id")
        if not brand_id and (data.get("brand_name") or data.get("brand")):
            brand_id = await self._resolve_brand_id(data.get("brand_name") or data.get("brand"))

        product = Product(
            sku=sku,
            barcode=data.get("barcode"),
            internal_sku=data.get("internal_sku"),
            name=data.get("name", ""),
            short_description=data.get("short_description"),
            long_description=data.get("long_description"),
            brand_id=brand_id,
            category_id=cat_id,
            unit_id=data.get("unit_id"),
            cost_price=Decimal(str(data.get("cost_price", 0))),
            selling_price=Decimal(str(data.get("selling_price", 0))),
            mrp=Decimal(str(data["mrp"])) if data.get("mrp") else None,
            gst_rate=Decimal(str(data.get("gst_rate", 18))),
            hsn_code=data.get("hsn_code"),
            country_of_origin=data.get("country_of_origin"),
            manufacturer=data.get("manufacturer"),
            is_active=data.get("is_active", True),
            is_hazardous=data.get("is_hazardous", False),
            is_cold_storage=data.get("is_cold_storage", False),
            min_order_qty=data.get("min_order_qty", 1),
            reorder_level=data.get("reorder_level"),
            safety_stock=data.get("safety_stock"),
        )
        return await self.repo.create(product)

    async def update_product(self, product_id: uuid.UUID, data: dict) -> Product:
        product = await self.get_product(product_id)
        if data.get("sku") and data["sku"] != product.sku:
            existing = await self.repo.get_by_sku(data["sku"])
            if existing:
                raise ConflictException(f"Product with SKU '{data['sku']}' already exists")

        for field in ["name", "short_description", "long_description", "barcode",
                       "internal_sku", "hsn_code", "country_of_origin", "manufacturer",
                       "is_active", "is_hazardous", "is_cold_storage",
                       "min_order_qty", "reorder_level", "safety_stock", "sku"]:
            if field in data:
                setattr(product, field, data[field])

        for decimal_field in ["cost_price", "selling_price", "mrp", "gst_rate"]:
            if decimal_field in data and data[decimal_field] is not None:
                setattr(product, decimal_field, Decimal(str(data[decimal_field])))

        if "brand_id" in data:
            product.brand_id = data["brand_id"]
        if "category_id" in data:
            product.category_id = data["category_id"]
        if "unit_id" in data:
            product.unit_id = data["unit_id"]

        return await self.repo.update(product)

    async def delete_product(self, product_id: uuid.UUID) -> None:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundException("Product not found")
        await self.repo.delete(product)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = BaseRepository[Category](db)
        self.repo.model = Category

    async def list_categories(self):
        result = await self.db.execute(
            select(Category).options(selectinload(Category.children))
        )
        return result.scalars().unique().all()

    async def get_category(self, category_id: uuid.UUID) -> Category:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id).options(
                selectinload(Category.children),
                selectinload(Category.parent),
            )
        )
        cat = result.scalar_one_or_none()
        if not cat:
            raise NotFoundException("Category not found")
        return cat

    async def create_category(self, data: dict) -> Category:
        cat = Category(
            name=data["name"],
            slug=data.get("slug", data["name"].lower().replace(" ", "-")),
            description=data.get("description"),
            parent_id=data.get("parent_id"),
            display_order=data.get("display_order", 0),
        )
        return await self.repo.create(cat)

    async def update_category(self, category_id: uuid.UUID, data: dict) -> Category:
        cat = await self.get_category(category_id)
        for field in ["name", "slug", "description", "display_order"]:
            if field in data:
                setattr(cat, field, data[field])
        if "parent_id" in data:
            cat.parent_id = data["parent_id"]
        return await self.repo.update(cat)


class BrandService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_brands(self, filters=None, sorting=None, pagination=None):
        repo = BaseRepository[Brand](self.db)
        repo.model = Brand
        return await repo.find_all(filters, sorting, pagination)

    async def get_brand(self, brand_id: uuid.UUID) -> Brand:
        result = await self.db.execute(select(Brand).where(Brand.id == brand_id))
        brand = result.scalar_one_or_none()
        if not brand:
            raise NotFoundException("Brand not found")
        return brand

    async def create_brand(self, data: dict) -> Brand:
        repo = BaseRepository[Brand](self.db)
        repo.model = Brand
        brand = Brand(
            name=data["name"], logo_url=data.get("logo_url"),
            country=data.get("country"), website=data.get("website"),
            description=data.get("description"),
            is_active=data.get("is_active", True),
        )
        return await repo.create(brand)

    async def update_brand(self, brand_id: uuid.UUID, data: dict) -> Brand:
        brand = await self.get_brand(brand_id)
        for field in ["name", "logo_url", "country", "website", "description", "is_active"]:
            if field in data:
                setattr(brand, field, data[field])
        repo = BaseRepository[Brand](self.db)
        repo.model = Brand
        return await repo.update(brand)


class UnitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_units(self):
        result = await self.db.execute(select(Unit))
        return result.scalars().all()

    async def create_unit(self, data: dict) -> Unit:
        repo = BaseRepository[Unit](self.db)
        repo.model = Unit
        unit = Unit(
            name=data["name"], symbol=data["symbol"],
            conversion_factor=data.get("conversion_factor", 1.0),
        )
        return await repo.create(unit)
