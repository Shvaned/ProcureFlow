"""SKU Generation Service — enterprise-grade auto-SKU with manual override."""
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException
from app.core.logging import get_logger
from app.models.product.product import Product
from app.models.product.sku_sequence import SKUSequence

logger = get_logger(__name__)

# Configurable category → prefix mapping
CATEGORY_PREFIXES = {
    "Composite": "CMP", "Gloves": "GLV", "Handpiece": "HP", "Impression Material": "IMP",
    "Endodontics": "ENDO", "Restorative": "RES", "Cement": "CEM", "Bonding Agent": "BND",
    "Etchant": "ETG", "Bur": "BUR", "Implant": "IMPNT", "Orthodontics": "ORT",
    "Instrument": "INS", "Mirror": "MIR", "Scaler": "SCL", "PPE": "PPE",
    "Needle": "NDL", "Syringe": "SYR", "Suture": "SUT", "General": "GEN",
}

# Configurable brand → code mapping
BRAND_CODES = {
    "3M": "3M", "GC": "GC", "Dentsply Sirona": "DSP", "NSK": "NSK",
    "Woodpecker": "WOOD", "Mani": "MANI", "Ivoclar": "IVO", "Kerr": "KERR",
    "Septodont": "SEPT", "Zhermack": "ZHER", "DPI": "DPI", "Coltene": "COL",
    "Ultradent": "ULT", "Bisco": "BIS", "Kuraray": "KUR", "Shofu": "SHO",
    "Parkell": "PARK", "Pentron": "PEN", "DMG": "DMG", "Voco": "VOCO",
}

SKU_PATTERN = re.compile(r'^[A-Z0-9]+-[A-Z0-9]+-\d{4}(?:-[A-Z0-9]+)?$')


class SKUService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def get_prefix(self, category_name: str) -> str:
        prefix = CATEGORY_PREFIXES.get(category_name)
        if not prefix:
            # Try partial match
            for key, val in CATEGORY_PREFIXES.items():
                if key.lower() in category_name.lower():
                    return val
            return category_name[:3].upper()
        return prefix

    def get_brand_code(self, brand_name: str) -> str:
        code = BRAND_CODES.get(brand_name)
        if not code:
            for key, val in BRAND_CODES.items():
                if key.lower() in brand_name.lower():
                    return val
            words = brand_name.upper().replace("-", " ").replace(".", " ").split()
            return "".join(w[0] for w in words[:4])
        return code

    async def preview_sku(self, category_name: str, brand_name: str, variant: str | None = None) -> str:
        prefix = self.get_prefix(category_name)
        brand = self.get_brand_code(brand_name)
        seq = await self._get_next_sequence(prefix, brand, dry_run=True)
        sku = f"{prefix}-{brand}-{seq:04d}"
        if variant:
            sku += f"-{variant.upper().replace(' ', '')}"
        return self._normalize(sku)

    async def generate_sku(self, category_name: str, brand_name: str, variant: str | None = None) -> str:
        prefix = self.get_prefix(category_name)
        brand = self.get_brand_code(brand_name)
        seq = await self._get_next_sequence(prefix, brand, dry_run=False)
        sku = f"{prefix}-{brand}-{seq:04d}"
        if variant:
            sku += f"-{variant.upper().replace(' ', '')}"
        sku = self._normalize(sku)

        # Verify uniqueness
        existing = await self.db.execute(select(Product).where(Product.sku == sku))
        if existing.scalar_one_or_none():
            raise ConflictException(f"SKU '{sku}' already exists")
        return sku

    async def validate_sku(self, sku: str) -> dict:
        errors = []
        sku = self._normalize(sku)
        if len(sku) < 6:
            errors.append("SKU too short (min 6 characters)")
        if len(sku) > 30:
            errors.append("SKU too long (max 30 characters)")
        if not SKU_PATTERN.match(sku):
            errors.append("Invalid SKU format. Expected: PREFIX-BRAND-0000[-VARIANT]")
        if not re.match(r'^[A-Z0-9\-]+$', sku):
            errors.append("SKU can only contain uppercase letters, numbers, and hyphens")

        # Check uniqueness
        existing = await self.db.execute(select(Product).where(Product.sku == sku))
        if existing.scalar_one_or_none():
            errors.append("SKU already exists")

        return {"valid": len(errors) == 0, "errors": errors, "normalized": sku}

    async def reserve_sku(self, sku: str) -> dict:
        validation = await self.validate_sku(sku)
        if not validation["valid"]:
            return validation
        return {"reserved": True, "sku": validation["normalized"], "message": "SKU reserved"}

    async def _get_next_sequence(self, prefix: str, brand: str, dry_run: bool = False) -> int:
        result = await self.db.execute(
            select(SKUSequence).where(
                SKUSequence.category_prefix == prefix,
                SKUSequence.brand_code == brand,
            )
        )
        seq = result.scalar_one_or_none()

        if not seq:
            seq = SKUSequence(category_prefix=prefix, brand_code=brand, current_sequence=1)
            self.db.add(seq)
            await self.db.flush()
            return 1

        seq.current_sequence += 1
        if not dry_run:
            await self.db.flush()
        return seq.current_sequence

    def _normalize(self, sku: str) -> str:
        return sku.upper().strip()

    @classmethod
    def list_prefixes(cls) -> dict:
        return dict(CATEGORY_PREFIXES)

    @classmethod
    def list_brand_codes(cls) -> dict:
        return dict(BRAND_CODES)

    @classmethod
    def update_prefix(cls, category: str, prefix: str) -> None:
        CATEGORY_PREFIXES[category] = prefix.upper()

    @classmethod
    def update_brand_code(cls, brand: str, code: str) -> None:
        BRAND_CODES[brand] = code.upper()
