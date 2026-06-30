"""Seed 50+ dental products with proper SKUs, categories, brands, and suppliers."""
import asyncio, uuid, random
from app.core.database import async_session_factory
from app.models.product.product import Product, Category, Brand, Unit
from app.models.supplier.supplier import Supplier
from app.services.sku_service import SKUService
from sqlalchemy import select

DENTAL_PRODUCTS = [
    # (name, category, brand, cost, sell, shade)
    ("Filtek Z350 XT Flowable", "Composite", "3M", 850, 1400, "A2"),
    ("Filtek Z250 Universal", "Composite", "3M", 650, 1100, "A3"),
    ("Filtek Supreme Ultra", "Composite", "3M", 1200, 2000, "A1"),
    ("GC Fuji IX GP Extra", "Cement", "GC", 750, 1200, None),
    ("GC Fuji II LC", "Cement", "GC", 580, 950, None),
    ("GC FujiCEM 2", "Cement", "GC", 3200, 4800, None),
    ("Pana Max Air Rotor", "Handpiece", "NSK", 8500, 12500, None),
    ("EX-203 M4 Slow Speed", "Handpiece", "NSK", 12000, 18000, None),
    ("Ti-Max Z High Speed", "Handpiece", "NSK", 25000, 35000, None),
    ("LED Curing Light", "General", "Woodpecker", 4500, 7200, None),
    ("LED.B Curing Light", "General", "Woodpecker", 3800, 6000, None),
    ("Woodpecker Scaler", "Scaler", "Woodpecker", 12000, 18000, None),
    ("Mani K-File #15", "Endodontics", "Mani", 45, 85, "21mm"),
    ("Mani K-File #20", "Endodontics", "Mani", 45, 85, "21mm"),
    ("Mani K-File #25", "Endodontics", "Mani", 45, 85, "25mm"),
    ("Mani H-File #20", "Endodontics", "Mani", 55, 95, "25mm"),
    ("Mani H-File #25", "Endodontics", "Mani", 55, 95, "25mm"),
    ("Mani NiTi Rotary File", "Endodontics", "Mani", 350, 650, "25mm"),
    ("AH Plus Sealer", "Endodontics", "Dentsply Sirona", 1800, 2800, None),
    ("ProTaper Gold F2", "Endodontics", "Dentsply Sirona", 450, 750, "25mm"),
    ("ProTaper Gold F1", "Endodontics", "Dentsply Sirona", 450, 750, "21mm"),
    ("Zhermack Elite HD+ Putty", "Impression Material", "Zhermack", 2200, 3500, None),
    ("Zhermack Hydrorise Light", "Impression Material", "Zhermack", 1800, 2900, None),
    ("Zhermack Elite HD+ Light", "Impression Material", "Zhermack", 1900, 3000, None),
    ("Elite Glass Ionomer", "Restorative", "Zhermack", 950, 1500, "A3"),
    ("Nitrile Exam Gloves S", "Gloves", "General", 280, 450, "S"),
    ("Nitrile Exam Gloves M", "Gloves", "General", 280, 450, "M"),
    ("Nitrile Exam Gloves L", "Gloves", "General", 280, 450, "L"),
    ("Latex Surgical Gloves S", "Gloves", "General", 350, 580, "S"),
    ("Latex Surgical Gloves M", "Gloves", "General", 350, 580, "M"),
    ("DPI Alginate Fast Set", "Impression Material", "DPI", 350, 600, None),
    ("DPI Alginate Normal Set", "Impression Material", "DPI", 320, 550, None),
    ("DPI Dental Plaster", "General", "DPI", 120, 200, None),
    ("Kerr Temp-Bond NE", "Cement", "Kerr", 850, 1400, None),
    ("Kerr Maxcem Elite", "Cement", "Kerr", 4200, 6500, None),
    ("Ivoclar Tetric N-Ceram", "Composite", "Ivoclar", 780, 1300, "A2"),
    ("Ivoclar Tetric N-Flow", "Composite", "Ivoclar", 650, 1100, "A3"),
    ("Ivoclar IPS e.max Press", "Restorative", "Ivoclar", 2200, 3800, "A2"),
    ("Septodont Septocaine 4%", "General", "Septodont", 180, 320, None),
    ("Coltene Affinis Putty", "Impression Material", "Coltene", 1600, 2600, None),
    ("Bisco All-Bond Universal", "Bonding Agent", "Bisco", 2800, 4500, None),
    ("Kuraray Clearfil SE Bond", "Bonding Agent", "Kuraray", 3200, 5000, None),
    ("3M RelyX U200", "Cement", "3M", 3800, 5800, None),
    ("3M Scotchbond Universal", "Bonding Agent", "3M", 2800, 4400, None),
    ("Shofu Beautifil II", "Restorative", "Shofu", 680, 1100, "A2"),
    ("Parkell Brush&Bond", "Bonding Agent", "Parkell", 1200, 2000, None),
    ("Ultradent Ultra-Etch", "Etchant", "Ultradent", 850, 1400, None),
    ("DMG Luxatemp Automix", "Restorative", "DMG", 1800, 2900, "A2"),
    ("Voco Grandio SO", "Composite", "Voco", 720, 1200, "A3"),
    ("Dental Mirror No.5", "Mirror", "General", 80, 150, None),
    ("Dental Explorer No.23", "Instrument", "General", 120, 200, None),
    ("Composite Placement Instrument", "Instrument", "General", 350, 600, None),
    ("Alginate Mixing Spatula", "Instrument", "General", 200, 350, None),
]


async def seed():
    async with async_session_factory() as db:
        # Create categories
        for cat_name in ["Composite", "Gloves", "Handpiece", "Impression Material", "Endodontics", "Restorative", "Cement", "Bonding Agent", "Etchant", "Bur", "Implant", "Orthodontics", "Instrument", "Mirror", "Scaler", "PPE", "General"]:
            existing = await db.execute(select(Category).where(Category.name == cat_name))
            if not existing.scalar_one_or_none():
                db.add(Category(name=cat_name, slug=cat_name.lower().replace(" ", "-")))

        # Create brands
        for brand_name in ["3M", "GC", "NSK", "Woodpecker", "Mani", "Dentsply Sirona", "Zhermack", "DPI", "Kerr", "Ivoclar", "Septodont", "Coltene", "Bisco", "Kuraray", "Shofu", "Parkell", "Ultradent", "DMG", "Voco", "Dentsply"]:
            existing = await db.execute(select(Brand).where(Brand.name == brand_name))
            if not existing.scalar_one_or_none():
                db.add(Brand(name=brand_name, is_active=True))

        await db.flush()

        sku_svc = SKUService(db)
        count = 0
        for name, cat, brand_name, cost, sell, shade in DENTAL_PRODUCTS:
            cat_result = await db.execute(select(Category).where(Category.name == cat))
            category_row = cat_result.scalar_one_or_none()
            brand_result = await db.execute(select(Brand).where(Brand.name == brand_name))
            brand_row = brand_result.scalar_one_or_none()

            sku = await sku_svc.generate_sku(cat, brand_name, shade)

            existing = await db.execute(select(Product).where(Product.sku == sku))
            if existing.scalar_one_or_none():
                continue

            p = Product(
                sku=sku, name=name, cost_price=cost, selling_price=sell,
                gst_rate=18, is_active=True,
                category_id=category_row.id if category_row else None,
                brand_id=brand_row.id if brand_row else None,
                reorder_level=random.randint(10, 50),
                safety_stock=random.randint(5, 20),
            )
            db.add(p)
            count += 1

        await db.commit()
        print(f"Seeded {count} dental products with auto-generated SKUs")

asyncio.run(seed())
