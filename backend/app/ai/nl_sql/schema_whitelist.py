"""Whitelist of allowed tables, columns, and functions for NL→SQL queries."""

ALLOWED_TABLES = {
    "products": {
        "columns": ["id", "sku", "name", "cost_price", "selling_price", "mrp", "gst_rate", "is_active", "brand_id", "category_id", "created_at", "updated_at", "country_of_origin", "manufacturer"],
        "description": "Product master data",
    },
    "categories": {
        "columns": ["id", "name", "slug", "parent_id", "display_order", "created_at"],
        "description": "Product categories hierarchy",
    },
    "brands": {
        "columns": ["id", "name", "country", "is_active", "created_at"],
        "description": "Product brands",
    },
    "inventory": {
        "columns": ["id", "product_id", "warehouse_id", "available_quantity", "reserved_quantity", "damaged_quantity", "on_order_quantity", "lot_number", "batch_number", "expiry_date", "cost_price", "selling_price", "reorder_level", "safety_stock", "last_movement_at", "created_at"],
        "description": "Current inventory levels per warehouse",
    },
    "inventory_transactions": {
        "columns": ["id", "inventory_id", "product_id", "warehouse_id", "transaction_type", "before_quantity", "after_quantity", "quantity_change", "reason", "unit_cost", "total_cost", "created_at", "created_by"],
        "description": "Immutable inventory transaction log",
    },
    "warehouses": {
        "columns": ["id", "code", "name", "city", "state", "country", "warehouse_type", "is_active", "created_at"],
        "description": "Warehouse locations",
    },
    "suppliers": {
        "columns": ["id", "code", "legal_name", "display_name", "gst_number", "email", "phone", "country", "state", "city", "currency", "payment_terms", "rating", "is_preferred", "is_active", "created_at"],
        "description": "Supplier master data",
    },
    "supplier_performance": {
        "columns": ["id", "supplier_id", "avg_lead_time_days", "late_deliveries_count", "rejected_goods_count", "quality_rating", "delivery_rating", "price_competitiveness", "overall_score", "total_purchase_orders", "on_time_delivery_pct", "created_at"],
        "description": "Supplier performance metrics",
    },
    "purchase_orders": {
        "columns": ["id", "po_number", "supplier_id", "warehouse_id", "expected_delivery_date", "currency", "subtotal", "tax_amount", "discount_amount", "shipping_amount", "total_amount", "status", "approved_by", "approved_at", "created_at"],
        "description": "Purchase orders with amounts and status",
    },
    "purchase_order_items": {
        "columns": ["id", "purchase_order_id", "product_id", "quantity", "received_quantity", "unit_cost", "discount_pct", "tax_pct", "line_total", "expected_date"],
        "description": "Line items on purchase orders",
    },
}

ALLOWED_FUNCTIONS = {"COUNT", "SUM", "AVG", "MIN", "MAX", "COALESCE", "ROUND"}
ALLOWED_AGGREGATIONS = {"COUNT", "SUM", "AVG", "MIN", "MAX"}
UNSAFE_KEYWORDS = {"INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "EXEC", "EXECUTE", "MERGE", "UNION", "GRANT", "REVOKE"}


def get_schema_context() -> str:
    """Generate schema description for the AI context."""
    lines = []
    for table, info in ALLOWED_TABLES.items():
        cols = ", ".join(info["columns"])
        lines.append(f"  {table} ({cols}): {info['description']}")
    return "\n".join(lines)


def validate_table(table: str) -> bool:
    return table.lower() in ALLOWED_TABLES


def validate_column(table: str, column: str) -> bool:
    t = ALLOWED_TABLES.get(table.lower(), {})
    return column.lower() in t.get("columns", [])


def get_allowed_columns(table: str) -> list[str]:
    return ALLOWED_TABLES.get(table.lower(), {}).get("columns", [])
