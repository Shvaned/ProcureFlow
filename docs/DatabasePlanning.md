# ProcureFlow AI — Database Planning

**Version:** 1.0.0
**Date:** 2026-06-30

> **Phase 0 Note:** This document defines high-level entities and bounded contexts. Actual table definitions, columns, indexes, and relationships are implemented in Phase 2.

---

## 1. Bounded Contexts

| Context | Purpose | Why It Exists |
|---------|---------|--------------|
| **Identity** | Users, roles, permissions, sessions | Centralized authentication and authorization independent of business domains |
| **Product Catalog** | Products, categories, brands, units | Product master data shared across inventory, procurement, and analytics |
| **Warehouse** | Warehouses, zones, bins, locations | Physical storage modeling independent of what's stored |
| **Inventory** | Stock levels, transactions, reservations, snapshots | The core of the ERP — inventory state and history |
| **Supplier** | Suppliers, contacts, documents, performance | Supplier master data and relationship tracking |
| **Procurement** | Purchase requests, purchase orders, approvals, GRNs | The purchasing lifecycle from request to receipt |
| **Finance** | Invoices, payments, tax config, valuation | Financial record-keeping separate from operational procurement |
| **Analytics** | KPIs, metrics, snapshots, reports | Pre-aggregated data for dashboards — separate from operational tables |
| **AI** | Conversations, messages, prompts, model config | AI interaction data — independent from business domains |
| **Automation** | Workflows, executions, triggers, actions | Workflow engine state — separate from the processes it orchestrates |
| **Audit** | Audit logs, change history | Immutable audit trail spanning all domains |
| **Notifications** | Notifications, templates, history | Cross-cutting notification delivery |
| **File Storage** | Uploaded files, document references | File management shared across all domains |

---

## 2. High-Level Entity Map

### Identity Context
```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Users   │────►│  UserRoles   │◄────│  Roles   │
└────┬─────┘     └──────────────┘     └────┬─────┘
     │                                     │
     │                              ┌──────▼──────────┐
     │                              │ RolePermissions │
     │                              └──────┬──────────┘
     │                                     │
     │                              ┌──────▼──────────┐
     │                              │  Permissions    │
     │                              └─────────────────┘
     ▼
┌──────────┐
│ Sessions │
└──────────┘
```

### Product Catalog Context
```
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Brands  │◄────│   Products   │────►│Categories│
└──────────┘     └──────┬───────┘     └────┬─────┘
                        │                  │
                        ▼                  ▼
                  ┌──────────┐     ┌──────────────┐
                  │  Units   │     │Subcategories  │
                  └──────────┘     │(self-ref)     │
                                   └──────────────┘
                  ┌──────────────┐  ┌──────────────┐
                  │ProductImages │  │ProductDocs   │
                  └──────────────┘  └──────────────┘
                  ┌──────────────┐
                  │  Attributes  │
                  └──────────────┘
```

### Warehouse Context
```
┌────────────┐
│ Warehouses │
└─────┬──────┘
      │
      ▼
┌──────────────┐
│    Zones     │
└─────┬────────┘
      │
      ▼
┌──────────────┐     ┌──────────────────┐
│    Bins      │────►│InventoryLocation │
└──────────────┘     └──────────────────┘
```

### Inventory Context
```
┌──────────┐     ┌────────────────────┐     ┌──────────────────┐
│ Products │────►│     Inventory      │◄────│   Warehouses     │
└──────────┘     └────────┬───────────┘     └──────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐
│InventoryMovement│ │Reservations  │ │InventorySnapshot │
└─────────────────┘ └──────────────┘ └──────────────────┘
         │
         ▼
┌─────────────────┐
│ InvTransactions │ (Goods Received, Sale, Transfer, Adjustment…)
└─────────────────┘
```

### Supplier Context
```
┌───────────┐
│ Suppliers │
└─────┬─────┘
      │
      ├────► SupplierContacts
      ├────► SupplierAddresses
      ├────► SupplierDocuments
      ├────► SupplierRatings
      └────► SupplierPerformance
```

### Procurement Context
```
┌──────────────────┐
│ PurchaseRequests │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌─────────────────────┐
│ PurchaseOrders   │────►│ PurchaseOrderItems  │
└────────┬─────────┘     └─────────────────────┘
         │
         ├────► PurchaseOrderApproval (history)
         │
         ▼
┌──────────────────┐     ┌─────────────────────┐
│ GoodsReceivedNote│────►│  PurchaseReceipts   │
└────────┬─────────┘     └─────────────────────┘
         │
         ▼
    (Creates Inventory Transactions)
```

### Finance Context
```
┌──────────┐     ┌───────────────┐     ┌──────────┐
│ Invoices │────►│ InvoiceItems  │     │ Payments │
└──────────┘     └───────────────┘     └──────────┘
┌──────────────┐     ┌─────────────────┐
│ PaymentTerms │     │ TaxConfiguration│
└──────────────┘     └─────────────────┘
```

### AI Context
```
┌─────────────────┐     ┌───────────────┐
│ AIConversation  │────►│  AIMessages   │
└─────────────────┘     └───────────────┘
┌─────────────────┐     ┌──────────────────┐
│ PromptTemplate  │────►│ PromptExecution  │
└─────────────────┘     └──────────────────┘
┌──────────────────┐
│ModelConfiguration│
└──────────────────┘
```

### Automation Context
```
┌──────────┐     ┌───────────────────┐
│ Workflow │────►│ WorkflowExecution │
└────┬─────┘     └───────────────────┘
     │
     ├────► WorkflowTrigger
     ├────► WorkflowAction
     └────► WorkflowHistory
```

### Audit & Notifications
```
┌───────────┐     ┌───────────────┐
│ AuditLogs │     │ ChangeHistory │
└───────────┘     └───────────────┘

┌──────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│Notifications │     │NotificationTemplates │     │NotificationHistory   │
└──────────────┘     └──────────────────────┘     └──────────────────────┘
```

---

## 3. Key Design Decisions

| Decision | Rationale |
|----------|----------|
| UUID primary keys | No sequential ID leakage, distributed-friendly, future multi-tenancy |
| Soft deletes | Preserve referential integrity, support undo, audit compliance |
| Timestamp mixin on all tables | Every record has created_at, updated_at |
| Separate inventory from products | Product is master data; inventory is state that changes via transactions |
| Transaction-driven inventory | Every quantity change is an immutable record, not a column update |
| Approval history as separate table | Immutable approval trail, never update an approval record |
| AI tables isolated from ERP | AI doesn't touch ERP tables directly — only through services |
| Pre-aggregated analytics tables | Dashboards query snapshots, not live operational tables |

---

## 4. Domain Independence Rules

- No module references another module's repository directly — use services
- Inventory only changes through transactions — no direct quantity updates
- Procurement creates inventory transactions via Goods Receipt — tight coupling via service layer, not database
- AI models don't reference ERP models — context builders map between them
- Audit logs are append-only — never updated or deleted

---

## 5. Scalability Considerations

- All list queries support pagination (no unbounded SELECT *)
- Indexes designed for common query patterns (Phase 2 details)
- Materialized views planned for analytics aggregation
- Partitioning ready for high-volume tables (inventory transactions)
- Connection pooling configured for serverless database
