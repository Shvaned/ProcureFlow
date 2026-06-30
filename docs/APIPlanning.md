# ProcureFlow AI — API Planning

**Version:** 1.0.0
**Date:** 2026-06-30

> **Phase 0 Note:** This is a complete API endpoint inventory. Implementation happens across phases 1-7. Every endpoint follows the standard response format, requires authentication, and enforces RBAC permissions.

---

## Standard Response Format

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {},
  "metadata": {
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 150,
      "totalPages": 8,
      "hasNext": true,
      "hasPrevious": false
    }
  },
  "errors": null,
  "requestId": "uuid",
  "timestamp": "2026-06-30T00:00:00Z"
}
```

---

## Health & System

| Method | Path | Description | Auth | Phase |
|--------|------|-------------|------|-------|
| GET | `/api/v1/health` | Health check | No | 1 |
| GET | `/api/v1/health/ready` | Readiness check | No | 1 |
| GET | `/api/v1/health/live` | Liveness check | No | 1 |
| GET | `/api/v1/version` | API version info | No | 1 |

---

## Authentication

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| POST | `/api/v1/auth/login` | Login, returns tokens | Public | 3 |
| POST | `/api/v1/auth/logout` | Logout, revoke tokens | Authenticated | 3 |
| POST | `/api/v1/auth/refresh` | Refresh access token | Public (with refresh token) | 3 |
| GET | `/api/v1/auth/me` | Get current user profile | Authenticated | 3 |
| POST | `/api/v1/auth/change-password` | Change password | Authenticated | 3 |
| POST | `/api/v1/auth/forgot-password` | Request password reset | Public | 3 |
| POST | `/api/v1/auth/reset-password` | Reset password with token | Public (with reset token) | 3 |

---

## Users

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/users` | List users | Users.Read | 3 |
| GET | `/api/v1/users/{id}` | Get user | Users.Read | 3 |
| POST | `/api/v1/users` | Create user | Users.Write | 3 |
| PUT | `/api/v1/users/{id}` | Update user | Users.Write | 3 |
| DELETE | `/api/v1/users/{id}` | Soft-delete user | Users.Write | 3 |
| PUT | `/api/v1/users/{id}/profile` | Update own profile | Authenticated | 3 |

---

## Roles

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/roles` | List roles | Users.Read | 3 |
| GET | `/api/v1/roles/{id}` | Get role with permissions | Users.Read | 3 |
| POST | `/api/v1/roles` | Create role | Users.Write | 3 |
| PUT | `/api/v1/roles/{id}` | Update role | Users.Write | 3 |
| DELETE | `/api/v1/roles/{id}` | Delete role | Users.Write | 3 |
| PUT | `/api/v1/roles/{id}/permissions` | Assign permissions to role | Users.Write | 3 |

---

## Permissions

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/permissions` | List all permissions | Users.Read | 3 |
| GET | `/api/v1/permissions/groups` | List permission groups | Users.Read | 3 |

---

## Products

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/products` | List/search/filter products | Products.Read | 4A |
| GET | `/api/v1/products/{id}` | Get product detail | Products.Read | 4A |
| POST | `/api/v1/products` | Create product | Products.Create | 4A |
| PUT | `/api/v1/products/{id}` | Update product | Products.Update | 4A |
| DELETE | `/api/v1/products/{id}` | Soft-delete product | Products.Delete | 4A |
| POST | `/api/v1/products/bulk` | Bulk import products | Products.Create | 4A |
| PUT | `/api/v1/products/bulk` | Bulk update products | Products.Update | 4A |
| DELETE | `/api/v1/products/bulk` | Bulk delete products | Products.Delete | 4A |
| GET | `/api/v1/products/export` | Export products CSV | Products.Read | 4A |

## Product Images

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/products/{id}/images` | List product images | Products.Read | 4A |
| POST | `/api/v1/products/{id}/images` | Upload image | Products.Update | 4A |
| PUT | `/api/v1/products/{id}/images/{imageId}` | Update image metadata | Products.Update | 4A |
| DELETE | `/api/v1/products/{id}/images/{imageId}` | Delete image | Products.Update | 4A |
| PUT | `/api/v1/products/{id}/images/reorder` | Reorder images | Products.Update | 4A |

## Product Documents

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/products/{id}/documents` | List product documents | Products.Read | 4A |
| POST | `/api/v1/products/{id}/documents` | Upload document | Products.Update | 4A |
| DELETE | `/api/v1/products/{id}/documents/{docId}` | Delete document | Products.Update | 4A |

## Product Attributes

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/products/{id}/attributes` | Get product attributes | Products.Read | 4A |
| PUT | `/api/v1/products/{id}/attributes` | Update attributes | Products.Update | 4A |

---

## Categories

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/categories` | List categories (tree) | Categories.Read | 4A |
| GET | `/api/v1/categories/{id}` | Get category | Categories.Read | 4A |
| POST | `/api/v1/categories` | Create category | Categories.Write | 4A |
| PUT | `/api/v1/categories/{id}` | Update category | Categories.Write | 4A |
| DELETE | `/api/v1/categories/{id}` | Delete category | Categories.Write | 4A |
| GET | `/api/v1/categories/tree` | Get full category tree | Categories.Read | 4A |

---

## Brands

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/brands` | List/search/filter brands | Brands.Read | 4A |
| GET | `/api/v1/brands/{id}` | Get brand | Brands.Read | 4A |
| POST | `/api/v1/brands` | Create brand | Brands.Write | 4A |
| PUT | `/api/v1/brands/{id}` | Update brand | Brands.Write | 4A |
| DELETE | `/api/v1/brands/{id}` | Delete brand | Brands.Write | 4A |

---

## Units of Measure

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/units` | List units | Products.Read | 4A |
| GET | `/api/v1/units/{id}` | Get unit | Products.Read | 4A |
| POST | `/api/v1/units` | Create unit | Products.Create | 4A |
| PUT | `/api/v1/units/{id}` | Update unit | Products.Update | 4A |
| DELETE | `/api/v1/units/{id}` | Delete unit | Products.Delete | 4A |

---

## Warehouses

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/warehouses` | List warehouses | Warehouses.Read | 4B |
| GET | `/api/v1/warehouses/{id}` | Get warehouse detail | Warehouses.Read | 4B |
| POST | `/api/v1/warehouses` | Create warehouse | Warehouses.Write | 4B |
| PUT | `/api/v1/warehouses/{id}` | Update warehouse | Warehouses.Write | 4B |
| DELETE | `/api/v1/warehouses/{id}` | Soft-delete warehouse | Warehouses.Write | 4B |

## Warehouse Zones

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/warehouses/{id}/zones` | List zones | Warehouses.Read | 4B |
| POST | `/api/v1/warehouses/{id}/zones` | Create zone | Warehouses.Write | 4B |
| PUT | `/api/v1/warehouses/{id}/zones/{zoneId}` | Update zone | Warehouses.Write | 4B |
| DELETE | `/api/v1/warehouses/{id}/zones/{zoneId}` | Delete zone | Warehouses.Write | 4B |

## Warehouse Bins

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/warehouses/{id}/zones/{zoneId}/bins` | List bins | Warehouses.Read | 4B |
| POST | `/api/v1/warehouses/{id}/zones/{zoneId}/bins` | Create bin | Warehouses.Write | 4B |
| PUT | `/api/v1/warehouses/{id}/zones/{zoneId}/bins/{binId}` | Update bin | Warehouses.Write | 4B |
| DELETE | `/api/v1/warehouses/{id}/zones/{zoneId}/bins/{binId}` | Delete bin | Warehouses.Write | 4B |

---

## Inventory

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/inventory` | List/search/filter inventory | Inventory.Read | 4B |
| GET | `/api/v1/inventory/{id}` | Get inventory record detail | Inventory.Read | 4B |
| GET | `/api/v1/inventory/{id}/history` | Get inventory movement history | Inventory.ViewHistory | 4B |
| GET | `/api/v1/inventory/{id}/timeline` | Full timeline (all events) | Inventory.ViewHistory | 4B |
| GET | `/api/v1/inventory/{id}/valuation` | Inventory valuation | Inventory.Read | 4B |

## Inventory Transactions

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/inventory-transactions` | List/filter transactions | Inventory.Read | 4B |
| GET | `/api/v1/inventory-transactions/{id}` | Get transaction detail | Inventory.Read | 4B |

## Inventory Adjustments

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/adjustments` | List adjustments | Inventory.Read | 4B |
| POST | `/api/v1/adjustments` | Create adjustment | Inventory.Adjust | 4B |
| GET | `/api/v1/adjustments/{id}` | Get adjustment | Inventory.Read | 4B |
| PUT | `/api/v1/adjustments/{id}/approve` | Approve adjustment | Inventory.Adjust | 4B |

## Stock Reservations

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/reservations` | List reservations | Inventory.Read | 4B |
| POST | `/api/v1/reservations` | Create reservation | Inventory.Write | 4B |
| DELETE | `/api/v1/reservations/{id}` | Release reservation | Inventory.Write | 4B |

## Stock Transfers

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/transfers` | List transfers | Inventory.Read | 4B |
| POST | `/api/v1/transfers` | Create transfer | Inventory.Transfer | 4B |
| GET | `/api/v1/transfers/{id}` | Get transfer detail | Inventory.Read | 4B |
| PUT | `/api/v1/transfers/{id}/approve` | Approve transfer | Inventory.Transfer | 4B |
| PUT | `/api/v1/transfers/{id}/receive` | Mark transfer received | Inventory.Transfer | 4B |
| PUT | `/api/v1/transfers/{id}/cancel` | Cancel transfer | Inventory.Transfer | 4B |

## Stock Alerts

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/inventory/alerts` | Get active alerts | Inventory.Read | 4B |
| GET | `/api/v1/inventory/alerts/low-stock` | Low stock products | Inventory.Read | 4B |
| GET | `/api/v1/inventory/alerts/expiring` | Expiring products | Inventory.Read | 4B |
| GET | `/api/v1/inventory/alerts/out-of-stock` | Out of stock products | Inventory.Read | 4B |

---

## Suppliers

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/suppliers` | List/search/filter suppliers | Suppliers.Read | 4C |
| GET | `/api/v1/suppliers/{id}` | Get supplier detail | Suppliers.Read | 4C |
| POST | `/api/v1/suppliers` | Create supplier | Suppliers.Create | 4C |
| PUT | `/api/v1/suppliers/{id}` | Update supplier | Suppliers.Update | 4C |
| DELETE | `/api/v1/suppliers/{id}` | Soft-delete supplier | Suppliers.Delete | 4C |

## Supplier Contacts

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/suppliers/{id}/contacts` | List contacts | Suppliers.Read | 4C |
| POST | `/api/v1/suppliers/{id}/contacts` | Add contact | Suppliers.Update | 4C |
| PUT | `/api/v1/suppliers/{id}/contacts/{contactId}` | Update contact | Suppliers.Update | 4C |
| DELETE | `/api/v1/suppliers/{id}/contacts/{contactId}` | Remove contact | Suppliers.Update | 4C |

## Supplier Documents

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/suppliers/{id}/documents` | List documents | Suppliers.Read | 4C |
| POST | `/api/v1/suppliers/{id}/documents` | Upload document | Suppliers.Update | 4C |
| DELETE | `/api/v1/suppliers/{id}/documents/{docId}` | Delete document | Suppliers.Update | 4C |

## Supplier Performance

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/suppliers/{id}/performance` | Get performance metrics | Suppliers.Read | 4C |
| GET | `/api/v1/suppliers/{id}/scorecard` | Get scorecard | Suppliers.Read | 4C |

---

## Purchase Requests

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/purchase-requests` | List purchase requests | PurchaseOrders.Read | 4C |
| POST | `/api/v1/purchase-requests` | Create purchase request | PurchaseOrders.Create | 4C |
| GET | `/api/v1/purchase-requests/{id}` | Get PR detail | PurchaseOrders.Read | 4C |
| PUT | `/api/v1/purchase-requests/{id}` | Update PR (draft only) | PurchaseOrders.Update | 4C |
| PUT | `/api/v1/purchase-requests/{id}/approve` | Approve PR | PurchaseOrders.Approve | 4C |
| PUT | `/api/v1/purchase-requests/{id}/reject` | Reject PR | PurchaseOrders.Approve | 4C |

## Purchase Orders

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/purchase-orders` | List/search/filter POs | PurchaseOrders.Read | 4C |
| GET | `/api/v1/purchase-orders/{id}` | Get PO detail | PurchaseOrders.Read | 4C |
| POST | `/api/v1/purchase-orders` | Create PO | PurchaseOrders.Create | 4C |
| PUT | `/api/v1/purchase-orders/{id}` | Update PO (draft only) | PurchaseOrders.Update | 4C |
| PUT | `/api/v1/purchase-orders/{id}/submit` | Submit for approval | PurchaseOrders.Update | 4C |
| PUT | `/api/v1/purchase-orders/{id}/approve` | Approve PO | PurchaseOrders.Approve | 4C |
| PUT | `/api/v1/purchase-orders/{id}/reject` | Reject PO | PurchaseOrders.Approve | 4C |
| PUT | `/api/v1/purchase-orders/{id}/cancel` | Cancel PO | PurchaseOrders.Update | 4C |
| PUT | `/api/v1/purchase-orders/{id}/close` | Close PO | PurchaseOrders.Update | 4C |
| DELETE | `/api/v1/purchase-orders/{id}` | Delete draft PO | PurchaseOrders.Delete | 4C |

## Purchase Order Items

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/purchase-orders/{id}/items` | List PO items | PurchaseOrders.Read | 4C |
| POST | `/api/v1/purchase-orders/{id}/items` | Add PO item | PurchaseOrders.Update | 4C |
| PUT | `/api/v1/purchase-orders/{id}/items/{itemId}` | Update PO item | PurchaseOrders.Update | 4C |
| DELETE | `/api/v1/purchase-orders/{id}/items/{itemId}` | Remove PO item | PurchaseOrders.Update | 4C |

## Approval History

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/purchase-orders/{id}/approvals` | Get approval history | PurchaseOrders.Read | 4C |

## Goods Received Notes

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/grn` | List GRNs | PurchaseOrders.Read | 4C |
| POST | `/api/v1/grn` | Create GRN (from PO) | PurchaseOrders.Receive | 4C |
| GET | `/api/v1/grn/{id}` | Get GRN detail | PurchaseOrders.Read | 4C |

## Purchase Receipts

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/receipts` | List receipts | PurchaseOrders.Read | 4C |
| GET | `/api/v1/receipts/{id}` | Get receipt detail | PurchaseOrders.Read | 4C |

---

## Supplier Quotations

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/quotations` | List quotations | Suppliers.Read | 4C |
| POST | `/api/v1/quotations` | Upload/create quotation | Suppliers.Update | 4C |
| GET | `/api/v1/quotations/{id}` | Get quotation detail | Suppliers.Read | 4C |
| PUT | `/api/v1/quotations/{id}` | Update quotation | Suppliers.Update | 4C |
| DELETE | `/api/v1/quotations/{id}` | Delete quotation | Suppliers.Delete | 4C |
| POST | `/api/v1/quotations/parse` | Parse document (PDF/Excel) | Suppliers.Update | 7C |

---

## Invoices

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/invoices` | List invoices | Finance.Read | 4C |
| GET | `/api/v1/invoices/{id}` | Get invoice detail | Finance.Read | 4C |
| POST | `/api/v1/invoices` | Create invoice | Finance.Write | 4C |
| PUT | `/api/v1/invoices/{id}` | Update invoice | Finance.Write | 4C |

## Payments

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/payments` | List payments | Finance.Read | 4C |
| POST | `/api/v1/payments` | Record payment | Finance.Write | 4C |

---

## Analytics

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/analytics/executive` | Executive summary data | Analytics.Read | 6 |
| GET | `/api/v1/analytics/inventory` | Inventory analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/warehouse` | Warehouse analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/supplier` | Supplier analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/procurement` | Procurement analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/financial` | Financial analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/product` | Product analytics | Analytics.Read | 6 |
| GET | `/api/v1/analytics/operational` | Operational analytics | Analytics.Read | 6 |

## KPIs

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/kpis` | All KPIs | Analytics.Read | 6 |
| GET | `/api/v1/kpis/{key}` | Specific KPI with trend | Analytics.Read | 6 |
| GET | `/api/v1/kpis/{key}/history` | KPI time series | Analytics.Read | 6 |

## Reports

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/reports` | List saved reports | Reports.Read | 6 |
| POST | `/api/v1/reports` | Create custom report | Reports.Manage | 6 |
| GET | `/api/v1/reports/{id}` | Get report | Reports.Read | 6 |
| GET | `/api/v1/reports/{id}/execute` | Execute report | Reports.Read | 6 |
| DELETE | `/api/v1/reports/{id}` | Delete report | Reports.Manage | 6 |
| GET | `/api/v1/reports/{id}/export` | Export report | Reports.Export | 6 |

---

## Business Simulation

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/simulation/status` | Simulation status | Simulation.Read | 5 |
| POST | `/api/v1/simulation/start` | Start simulation | Simulation.Manage | 5 |
| POST | `/api/v1/simulation/stop` | Stop simulation | Simulation.Manage | 5 |
| POST | `/api/v1/simulation/pause` | Pause simulation | Simulation.Manage | 5 |
| POST | `/api/v1/simulation/resume` | Resume simulation | Simulation.Manage | 5 |
| POST | `/api/v1/simulation/reset` | Reset simulation data | Simulation.Manage | 5 |
| PUT | `/api/v1/simulation/speed` | Change simulation speed | Simulation.Manage | 5 |
| PUT | `/api/v1/simulation/scenario` | Change scenario | Simulation.Manage | 5 |
| GET | `/api/v1/simulation/events` | Get event log | Simulation.Read | 5 |
| GET | `/api/v1/simulation/dashboard` | Simulation dashboard data | Simulation.Read | 5 |
| POST | `/api/v1/simulation/seed` | Generate seed data | Simulation.Manage | 5 |

---

## AI Executive Copilot

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/ai/executive/daily-brief` | Get daily executive brief | AI.Use | 7A |
| GET | `/api/v1/ai/executive/health-score` | Business health score | AI.Use | 7A |
| GET | `/api/v1/ai/executive/risks` | Top risks | AI.Use | 7A |
| GET | `/api/v1/ai/executive/opportunities` | Top opportunities | AI.Use | 7A |
| POST | `/api/v1/ai/executive/chat` | Executive chat (streaming) | AI.Use | 7A |
| GET | `/api/v1/ai/executive/timeline` | Business event timeline | AI.Use | 7A |
| GET | `/api/v1/ai/executive/conversations` | Conversation history | AI.Use | 7A |

---

## AI Procurement Copilot

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/ai/procurement/dashboard` | Procurement AI dashboard | AI.Use, Procurement.Read | 7B |
| GET | `/api/v1/ai/procurement/reorder-recommendations` | Reorder recommendations with AI explanation | AI.Use, Procurement.Read | 7B |
| POST | `/api/v1/ai/procurement/review-po` | AI review of draft PO | AI.Use, Procurement.Read | 7B |
| POST | `/api/v1/ai/procurement/compare-suppliers` | AI supplier comparison | AI.Use, Procurement.Read | 7B |
| POST | `/api/v1/ai/procurement/what-if` | What-if simulation | AI.Use, Procurement.Read | 7B |
| POST | `/api/v1/ai/procurement/chat` | Procurement chat (streaming) | AI.Use | 7B |

---

## AI Supplier Intelligence

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| POST | `/api/v1/ai/suppliers/parse-quotation` | Upload & parse quotation | AI.Use, Suppliers.Read | 7C |
| POST | `/api/v1/ai/suppliers/compare` | Compare suppliers with AI analysis | AI.Use, Suppliers.Read | 7C |
| GET | `/api/v1/ai/suppliers/{id}/analysis` | AI supplier analysis | AI.Use, Suppliers.Read | 7C |
| GET | `/api/v1/ai/suppliers/{id}/price-history` | Price trend + AI explanation | AI.Use, Suppliers.Read | 7C |
| GET | `/api/v1/ai/suppliers/{id}/risk` | AI risk assessment | AI.Use, Suppliers.Read | 7C |
| GET | `/api/v1/ai/suppliers/{id}/negotiation` | Negotiation suggestions | AI.Use, Suppliers.Read | 7C |
| GET | `/api/v1/ai/suppliers/documents` | Document library | AI.Use, Suppliers.Read | 7C |

---

## AI Natural Language Analytics

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| POST | `/api/v1/ai/analytics/query` | Natural language → SQL → results | AI.Use, Analytics.Read | 7D |
| GET | `/api/v1/ai/analytics/history` | Query history | AI.Use, Analytics.Read | 7D |
| GET | `/api/v1/ai/analytics/saved` | Saved questions | AI.Use, Analytics.Read | 7D |
| POST | `/api/v1/ai/analytics/save` | Save a question | AI.Use | 7D |

---

## AI Agent Runtime

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/ai/tools` | List available tools | AI.Use | 7E |
| GET | `/api/v1/ai/tools/{name}` | Get tool metadata | AI.Use | 7E |
| POST | `/api/v1/ai/tools/execute` | Execute a tool | AI.Use | 7E |
| POST | `/api/v1/ai/agent/run` | Run multi-tool agent | AI.Use | 7E |

---

## Workflow Automation

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/workflows` | List workflows | Automation.Read | 7F |
| POST | `/api/v1/workflows` | Create workflow | Automation.Create | 7F |
| GET | `/api/v1/workflows/{id}` | Get workflow detail | Automation.Read | 7F |
| PUT | `/api/v1/workflows/{id}` | Update workflow | Automation.Update | 7F |
| DELETE | `/api/v1/workflows/{id}` | Delete workflow | Automation.Delete | 7F |
| POST | `/api/v1/workflows/{id}/publish` | Publish workflow | Workflow.Publish | 7F |
| POST | `/api/v1/workflows/{id}/simulate` | Simulate workflow | Automation.Execute | 7F |
| GET | `/api/v1/workflows/{id}/executions` | Execution history | Automation.Read | 7F |
| GET | `/api/v1/workflows/{id}/executions/{execId}` | Execution detail | Automation.Read | 7F |

## Workflow Templates

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/workflows/templates` | List templates | Automation.Read | 7F |
| POST | `/api/v1/workflows/templates/{id}/use` | Create workflow from template | Automation.Create | 7F |

## AI Workflow Builder

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| POST | `/api/v1/ai/workflows/generate` | Natural language → workflow | AI.Use, Automation.Create | 7F |

## Approval Center

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/approvals/pending` | Pending approvals | Authenticated | 7F |
| POST | `/api/v1/approvals/{id}/approve` | Approve | Automation.Approve | 7F |
| POST | `/api/v1/approvals/{id}/reject` | Reject | Automation.Approve | 7F |

---

## Notifications

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/notifications` | List notifications | Authenticated | 7F |
| PUT | `/api/v1/notifications/{id}/read` | Mark as read | Authenticated | 7F |
| PUT | `/api/v1/notifications/read-all` | Mark all read | Authenticated | 7F |
| GET | `/api/v1/notifications/preferences` | Notification preferences | Authenticated | 7F |
| PUT | `/api/v1/notifications/preferences` | Update preferences | Authenticated | 7F |

---

## Audit Logs

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| GET | `/api/v1/audit-logs` | List/filter audit logs | Audit.Read | 3 |
| GET | `/api/v1/audit-logs/{id}` | Get audit log detail | Audit.Read | 3 |
| GET | `/api/v1/audit-logs/export` | Export audit logs | Audit.Read | 3 |

---

## Files

| Method | Path | Description | Permissions | Phase |
|--------|------|-------------|-------------|-------|
| POST | `/api/v1/files/upload` | Upload file | Authenticated | 4A |
| GET | `/api/v1/files/{id}` | Get file metadata | Authenticated | 4A |
| GET | `/api/v1/files/{id}/download` | Download file | Authenticated | 4A |
| DELETE | `/api/v1/files/{id}` | Delete file | Authenticated | 4A |

---

## Summary

| Domain | Endpoint Count | Phase |
|--------|---------------|-------|
| Health & System | 4 | 1 |
| Authentication | 7 | 3 |
| Users & Roles | 12 | 3 |
| Products & Catalog | 25 | 4A |
| Warehouses | 17 | 4B |
| Inventory | 20 | 4B |
| Suppliers | 18 | 4C |
| Procurement | 30 | 4C |
| Finance | 6 | 4C |
| Analytics & Reports | 19 | 6 |
| Simulation | 10 | 5 |
| AI Executive | 7 | 7A |
| AI Procurement | 6 | 7B |
| AI Supplier Intelligence | 7 | 7C |
| AI NL Analytics | 4 | 7D |
| AI Agent Runtime | 4 | 7E |
| Workflows & Automation | 16 | 7F |
| Notifications | 5 | 7F |
| Audit | 3 | 3 |
| Files | 4 | 4A |
| **Total** | **~224** | |
