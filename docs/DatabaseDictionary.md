# ProcureFlow AI — Database Dictionary

**Version:** 1.0.0
**Date:** 2026-06-30

---

## Identity Context

### users
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User email address |
| name | VARCHAR(255) | NOT NULL | Display name |
| hashed_password | VARCHAR(255) | NOT NULL | Argon2 hashed password |
| is_active | BOOLEAN | DEFAULT true | Account active status |
| is_locked | BOOLEAN | DEFAULT false | Account locked after failed attempts |
| failed_login_attempts | INTEGER | DEFAULT 0 | Consecutive failed login count |
| last_login_at | TIMESTAMPTZ | NULLABLE | Last successful login timestamp |
| last_login_ip | VARCHAR(45) | NULLABLE | Last login IP address |
| email_verified_at | TIMESTAMPTZ | NULLABLE | Email verification timestamp |
| profile_picture_url | VARCHAR(500) | NULLABLE | Avatar URL |
| created_at | TIMESTAMPTZ | NOT NULL | Record creation time |
| updated_at | TIMESTAMPTZ | NOT NULL | Record update time |
| deleted_at | TIMESTAMPTZ | NULLABLE | Soft delete timestamp |
| is_deleted | BOOLEAN | DEFAULT false | Soft delete flag |
| created_by | UUID | NULLABLE, FK→users | Creator user ID |
| updated_by | UUID | NULLABLE, FK→users | Updater user ID |

### roles
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Role name |
| description | VARCHAR(500) | NULLABLE | Role description |
| is_system | BOOLEAN | DEFAULT false | System roles cannot be deleted |
| created_at | TIMESTAMPTZ | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL | Update timestamp |

### permissions
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Permission name (e.g., "Products.Read") |
| description | VARCHAR(500) | NULLABLE | What the permission grants |
| group | VARCHAR(100) | NOT NULL | Permission group (e.g., "Products") |

### user_roles
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| user_id | UUID | PK, FK→users | User |
| role_id | UUID | PK, FK→roles | Role |

### role_permissions
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| role_id | UUID | PK, FK→roles | Role |
| permission_id | UUID | PK, FK→permissions | Permission |

### user_sessions
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK→users, NOT NULL, INDEX | Owning user |
| refresh_token | VARCHAR(500) | NOT NULL | JWT refresh token |
| ip_address | VARCHAR(45) | NULLABLE | Client IP |
| device | VARCHAR(255) | NULLABLE | Device name |
| browser | VARCHAR(255) | NULLABLE | Browser name |
| os | VARCHAR(100) | NULLABLE | Operating system |
| is_revoked | BOOLEAN | DEFAULT false | Token revocation flag |
| last_activity | TIMESTAMPTZ | NOT NULL | Last activity timestamp |

---

## Product Catalog Context

### products
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| sku | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Stock keeping unit |
| barcode | VARCHAR(100) | UNIQUE, NULLABLE, INDEX | EAN/UPC barcode |
| internal_sku | VARCHAR(50) | NULLABLE | Internal reference |
| name | VARCHAR(500) | NOT NULL | Product name |
| short_description | TEXT | NULLABLE | Brief description |
| long_description | TEXT | NULLABLE | Detailed description |
| brand_id | UUID | FK→brands, INDEX | Brand reference |
| category_id | UUID | FK→categories, INDEX | Category reference |
| unit_id | UUID | FK→units | Unit of measure |
| cost_price | NUMERIC(18,2) | NOT NULL | Purchase cost |
| selling_price | NUMERIC(18,2) | NOT NULL | Sale price |
| mrp | NUMERIC(18,2) | NULLABLE | Maximum retail price |
| gst_rate | NUMERIC(5,2) | DEFAULT 18.00 | GST percentage |
| hsn_code | VARCHAR(20) | NULLABLE | HSN/SAC code |
| country_of_origin | VARCHAR(100) | NULLABLE | Manufacturing country |
| manufacturer | VARCHAR(255) | NULLABLE | Manufacturer name |
| is_active | BOOLEAN | DEFAULT true, INDEX | Active status |
| is_hazardous | BOOLEAN | DEFAULT false | Hazardous material flag |
| is_cold_storage | BOOLEAN | DEFAULT false | Cold chain required |
| min_order_qty | INTEGER | DEFAULT 1 | Minimum order quantity |
| reorder_level | INTEGER | NULLABLE | Reorder trigger point |
| safety_stock | INTEGER | NULLABLE | Safety stock level |

### categories
Self-referencing hierarchy via `parent_id`. Supports unlimited nesting.

### brands
| Column | Type | Constraints |
|--------|------|------------|
| id | UUID | PK |
| name | VARCHAR(255) | NOT NULL |
| country | VARCHAR(100) | NULLABLE |
| is_active | BOOLEAN | DEFAULT true |

---

## Inventory Context

### inventory
Each row represents a unique product-location-lot combination.

| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| product_id | UUID | FK→products, INDEX | Product |
| warehouse_id | UUID | FK→warehouses, INDEX | Storage location |
| zone_id | UUID | FK→warehouse_zones, NULLABLE | Zone within warehouse |
| bin_id | UUID | FK→warehouse_bins, NULLABLE | Specific bin |
| lot_number | VARCHAR(100) | NULLABLE, INDEX | Manufacturing lot |
| batch_number | VARCHAR(100) | NULLABLE, INDEX | Production batch |
| serial_number | VARCHAR(100) | NULLABLE | Individual serial |
| expiry_date | DATE | NULLABLE, INDEX | Expiration date |
| manufacturing_date | DATE | NULLABLE | Production date |
| available_quantity | INTEGER | DEFAULT 0 | Available for use |
| reserved_quantity | INTEGER | DEFAULT 0 | Reserved/allocated |
| damaged_quantity | INTEGER | DEFAULT 0 | Damaged/unusable |
| on_order_quantity | INTEGER | DEFAULT 0 | Incoming from POs |
| safety_stock | INTEGER | NULLABLE | Safety stock threshold |
| reorder_level | INTEGER | NULLABLE | Reorder trigger point |
| last_movement_at | TIMESTAMPTZ | NULLABLE | Last movement timestamp |
| cost_price | NUMERIC(18,2) | DEFAULT 0 | Unit cost for valuation |

### inventory_transactions
Immutable. Every inventory change creates exactly one transaction. Never updated after creation.

### stock_transfers
Inter-warehouse movement with approval workflow. Status: draft → pending_approval → approved → in_transit → received / cancelled.

---

## Procurement Context

### purchase_orders
| Column | Type | Constraints | Description |
|--------|------|------------|-------------|
| id | UUID | PK | Unique identifier |
| po_number | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Auto-generated PO number |
| supplier_id | UUID | FK→suppliers, INDEX | Supplier |
| warehouse_id | UUID | FK→warehouses, INDEX | Delivery warehouse |
| status | ENUM | NOT NULL, INDEX | DRAFT/APPROVED/SENT/PARTIALLY_RECEIVED/RECEIVED/CANCELLED/CLOSED |
| subtotal | NUMERIC(18,2) | DEFAULT 0 | Pre-tax total |
| tax_amount | NUMERIC(18,2) | DEFAULT 0 | Tax total |
| total_amount | NUMERIC(18,2) | DEFAULT 0 | Grand total |
| expected_delivery_date | DATE | NULLABLE | Expected delivery |
| approved_by | UUID | FK→users, NULLABLE | Approver |
| approved_at | TIMESTAMPTZ | NULLABLE | Approval timestamp |

### goods_received_notes
Created on goods receipt. Links to purchase_order. Triggers inventory transactions via service layer.

---

## Enums

| Enum | Values |
|------|--------|
| transaction_type | goods_received, sale, manual_adjustment, transfer_out, transfer_in, damage, expiry, return, reservation, allocation, release, cycle_count |
| transfer_status | draft, pending_approval, approved, in_transit, received, cancelled |
| adjustment_reason | damage, shrinkage, manual_correction, expiry, cycle_count, audit_adjustment |
| pr_status | draft, pending_approval, approved, rejected, cancelled |
| po_status | draft, approved, sent, partially_received, received, cancelled, closed |
| quotation_status | draft, active, expired, accepted, rejected |
| invoice_status | draft, sent, paid, partially_paid, overdue, cancelled |
| payment_method | bank_transfer, cheque, cash, upi, credit_card |
| workflow_status | draft, published, archived |
| execution_status | pending, running, completed, failed, cancelled |

---

## Key Indexes

| Table | Index | Type | Purpose |
|-------|-------|------|---------|
| users | ix_users_email | UNIQUE | Login lookup |
| products | ix_products_sku | UNIQUE | SKU search |
| products | ix_products_barcode | UNIQUE | Barcode scan |
| products | ix_products_is_active | BTREE | Active product filter |
| inventory | ix_inventory_product_id | BTREE | Product lookup |
| inventory | ix_inventory_warehouse_id | BTREE | Warehouse filter |
| inventory | ix_inventory_expiry_date | BTREE | Expiry alerts |
| inventory_transactions | ix_inv_transactions_inventory_id | BTREE | Transaction history |
| purchase_orders | ix_po_status | BTREE | Status filter |
| purchase_orders | ix_po_supplier_id | BTREE | Supplier filter |
| purchase_receipts | ix_receipts_po_id | BTREE | PO receipt lookup |
| stock_adjustments | ix_adjustments_inventory_id | BTREE | Adjustment history |
| stock_reservations | ix_reservations_inventory_id | BTREE | Active reservations |
| ai_conversations | ix_conv_user_id | BTREE | User conversations |
| audit_logs | ix_audit_user_id | BTREE | User audit trail |
| audit_logs | ix_audit_action | BTREE | Action filter |
