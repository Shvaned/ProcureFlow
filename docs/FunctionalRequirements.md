# ProcureFlow AI — Functional Requirements

**Version:** 1.0.0
**Date:** 2026-06-30

---

## FR-1: Authentication & Authorization

| ID | Requirement | Priority |
|----|------------|----------|
| FR-1.1 | Users can register with email and password | P0 |
| FR-1.2 | Users can login and receive JWT access + refresh tokens | P0 |
| FR-1.3 | Users can logout (token revocation) | P0 |
| FR-1.4 | System supports token refresh without re-login | P0 |
| FR-1.5 | Users can change their password | P1 |
| FR-1.6 | System supports password reset flow (forgot/reset) | P2 |
| FR-1.7 | System locks accounts after N failed attempts | P1 |
| FR-1.8 | System tracks active sessions with device info | P2 |

## FR-2: Role-Based Access Control

| ID | Requirement | Priority |
|----|------------|----------|
| FR-2.1 | Admin can create, update, and delete roles | P0 |
| FR-2.2 | Admin can assign permissions to roles | P0 |
| FR-2.3 | Admin can assign roles to users | P0 |
| FR-2.4 | System validates permissions on every API request | P0 |
| FR-2.5 | Frontend conditionally renders based on permissions | P0 |
| FR-2.6 | Default roles: Admin, Operations Manager, Warehouse Manager, Procurement Manager, Finance Manager, Viewer | P0 |

## FR-3: Product Catalog

| ID | Requirement | Priority |
|----|------------|----------|
| FR-3.1 | Users can create, read, update, delete products | P0 |
| FR-3.2 | Products have SKU, barcode, name, description, pricing, tax info | P0 |
| FR-3.3 | System prevents duplicate SKU and barcode | P0 |
| FR-3.4 | Categories support unlimited nesting (parent/child) | P0 |
| FR-3.5 | Users can manage brands with logo, country, status | P1 |
| FR-3.6 | Users can define units of measure with conversion | P1 |
| FR-3.7 | Products support multiple images with sort order | P1 |
| FR-3.8 | Products support document attachments (datasheets, certificates) | P2 |
| FR-3.9 | Products support dynamic attributes (color, size, material) | P2 |
| FR-3.10 | Enterprise search across SKU, barcode, name, brand, category, manufacturer, HSN | P0 |
| FR-3.11 | Table supports pagination, sorting, filtering, column selection, bulk actions, CSV export | P0 |

## FR-4: Warehouse Management

| ID | Requirement | Priority |
|----|------------|----------|
| FR-4.1 | Users can create and manage multiple warehouses | P0 |
| FR-4.2 | Each warehouse has configurable zones (receiving, storage, cold storage, etc.) | P1 |
| FR-4.3 | Each zone has configurable bins with capacity tracking | P2 |
| FR-4.4 | Warehouse dashboard shows utilization, inventory summary, alerts | P0 |

## FR-5: Inventory Management

| ID | Requirement | Priority |
|----|------------|----------|
| FR-5.1 | Inventory quantity is NEVER directly editable | P0 |
| FR-5.2 | Every inventory change creates an immutable transaction record | P0 |
| FR-5.3 | Transaction types: Goods Received, Sale, Adjustment, Transfer, Damage, Expiry, Return, Reservation, Allocation, Release | P0 |
| FR-5.4 | Each transaction records before/after quantity, reason, user, timestamp | P0 |
| FR-5.5 | Inventory supports lot number, batch number, expiry date, manufacturing date | P1 |
| FR-5.6 | Inventory supports FIFO lot selection | P1 |
| FR-5.7 | System supports stock reservations (prevent double-selling) | P1 |
| FR-5.8 | System supports inter-warehouse transfers with approval | P1 |
| FR-5.9 | Stock adjustments require reason and approval for large variances | P1 |
| FR-5.10 | System auto-detects: low stock, out of stock, overstock, expiring soon, expired, negative inventory | P1 |
| FR-5.11 | Inventory search by SKU, barcode, lot, batch, warehouse, zone, bin, expiry | P0 |
| FR-5.12 | Inventory timeline shows full movement history per product | P1 |
| FR-5.13 | Inventory snapshots support daily/weekly/monthly aggregation | P2 |

## FR-6: Supplier Management

| ID | Requirement | Priority |
|----|------------|----------|
| FR-6.1 | Users can create, read, update, delete suppliers | P0 |
| FR-6.2 | Suppliers have code, legal name, GST, PAN, contacts, addresses, payment terms | P0 |
| FR-6.3 | Supplier documents support GST certificate, PAN, bank details, agreements | P1 |
| FR-6.4 | System tracks supplier performance: lead time, late deliveries, rejected goods, quality score | P1 |
| FR-6.5 | Supplier dashboard with ratings, lead time trends, open orders | P0 |
| FR-6.6 | Supplier search by code, name, GST, country, email, phone | P0 |

## FR-7: Procurement Management

| ID | Requirement | Priority |
|----|------------|----------|
| FR-7.1 | Users can create purchase requests (warehouse → request → approval → PO) | P0 |
| FR-7.2 | Users can create, read, update, delete purchase orders | P0 |
| FR-7.3 | PO status: Draft, Approved, Sent, Partially Received, Received, Cancelled, Closed | P0 |
| FR-7.4 | POs support supplier, warehouse, expected delivery, currency, taxes, discount, shipping | P0 |
| FR-7.5 | PO items track product, quantity, unit cost, received qty, remaining qty | P0 |
| FR-7.6 | System supports approval workflow: single and multi-level | P1 |
| FR-7.7 | System prevents PO modification after approval | P0 |
| FR-7.8 | Goods Received Notes (GRN) create inventory transactions automatically | P0 |
| FR-7.9 | System supports partial receiving and multiple GRNs per PO | P1 |
| FR-7.10 | Purchase receipts track received by, date, condition, rejected/damaged items | P1 |
| FR-7.11 | Supplier quotations support upload, comparison, acceptance | P1 |
| FR-7.12 | Procurement dashboard: open POs, pending approval, delayed deliveries, spend | P0 |

## FR-8: Business Simulation

| ID | Requirement | Priority |
|----|------------|----------|
| FR-8.1 | Simulation engine generates realistic business events continuously | P0 |
| FR-8.2 | Events: orders, shipments, transfers, adjustments, delays, returns, expiry | P0 |
| FR-8.3 | Simulation supports configurable speed (paused, real-time, 10x, 100x, 1000x) | P1 |
| FR-8.4 | Simulation supports scenarios: normal, peak, crisis, demand spike, etc. | P1 |
| FR-8.5 | All simulation events use existing business services (never bypass them) | P0 |
| FR-8.6 | Simulation generates realistic historical data (products, suppliers, orders) | P0 |

## FR-9: Analytics

| ID | Requirement | Priority |
|----|------------|----------|
| FR-9.1 | Executive dashboard with revenue, profit, inventory value, KPIs | P0 |
| FR-9.2 | Every KPI shows current value, previous value, trend, percentage change | P0 |
| FR-9.3 | Inventory analytics: health, ABC analysis, aging, dead inventory, overstock | P1 |
| FR-9.4 | Warehouse analytics: capacity, utilization, inbound/outbound, transfers | P1 |
| FR-9.5 | Supplier analytics: ranking, lead time, delivery accuracy, spend | P1 |
| FR-9.6 | Procurement analytics: PO trends, approval time, spend breakdown | P1 |
| FR-9.7 | Financial analytics: valuation, margins, carrying cost | P1 |
| FR-9.8 | Product analytics: best/worst sellers, category performance, velocity | P1 |
| FR-9.9 | Custom report builder with metric/dimension selection, filters, export | P2 |
| FR-9.10 | Charts: line, bar, area, pie, treemap, heatmap, scatter, waterfall, gauge, KPI cards | P0 |
| FR-9.11 | Global date range, warehouse, supplier, category filters | P0 |
| FR-9.12 | Drill-down from summary → warehouse → category → product → transactions | P1 |

## FR-10: AI Platform

| ID | Requirement | Priority |
|----|------------|----------|
| FR-10.1 | AI provider abstraction (OpenRouter primary, extensible to others) | P0 |
| FR-10.2 | Prompts stored as external markdown files, never in source code | P0 |
| FR-10.3 | Every AI response validates against Pydantic schemas (structured output) | P0 |
| FR-10.4 | AI never accesses repositories, ORM, or SQL directly — only through tools | P0 |
| FR-10.5 | AI never makes business decisions — only explains, summarizes, recommends | P0 |
| FR-10.6 | Conversation memory stored in PostgreSQL | P1 |
| FR-10.7 | Token usage, cost tracking, and latency observability | P1 |

## FR-11: Executive AI Copilot

| ID | Requirement | Priority |
|----|------------|----------|
| FR-11.1 | AI generates daily executive brief summarizing KPIs, risks, opportunities | P0 |
| FR-11.2 | Business health score (0-100) with explanation | P1 |
| FR-11.3 | Risk detection with severity, probability, business impact, recommended action | P1 |
| FR-11.4 | Opportunity detection (restock, promote, balance, negotiate) | P1 |
| FR-11.5 | Conversational business chat — ask questions about business state | P0 |
| FR-11.6 | Every AI insight cites specific ERP metrics as evidence | P0 |
| FR-11.7 | AI suggests follow-up questions for deeper analysis | P2 |

## FR-12: AI Procurement Copilot

| ID | Requirement | Priority |
|----|------------|----------|
| FR-12.1 | Reorder engine identifies products needing replenishment (deterministic) | P0 |
| FR-12.2 | AI explains WHY reorder is recommended (trend, consumption, lead time) | P0 |
| FR-12.3 | Supplier comparison with AI explanation of trade-offs | P1 |
| FR-12.4 | AI reviews draft POs before approval, highlighting concerns | P2 |
| FR-12.5 | Procurement risk detection (delay, price increase, single dependency) | P1 |
| FR-12.6 | What-if simulation ("What if supplier delayed 7 days?") | P2 |
| FR-12.7 | Procurement chat for natural-language questions | P1 |

## FR-13: AI Supplier Intelligence

| ID | Requirement | Priority |
|----|------------|----------|
| FR-13.1 | Upload and parse supplier quotations (PDF, Excel) | P1 |
| FR-13.2 | Deterministic extraction of supplier, products, prices, terms, dates | P1 |
| FR-13.3 | Side-by-side supplier comparison with AI explanation | P1 |
| FR-13.4 | Price trend analysis across historical quotations | P2 |
| FR-13.5 | Negotiation suggestions based on historical data | P2 |
| FR-13.6 | Supplier risk detection (single dependency, price increase, low reliability) | P2 |

## FR-14: Natural Language Analytics

| ID | Requirement | Priority |
|----|------------|----------|
| FR-14.1 | Users can ask business questions in plain English | P1 |
| FR-14.2 | System generates safe SQL (SELECT only, no DROP/DELETE/UPDATE) | P1 |
| FR-14.3 | SQL validation: syntax, permissions, table access, complexity, cost | P1 |
| FR-14.4 | Results auto-visualized with appropriate chart type | P1 |
| FR-14.5 | AI explains results in business language | P1 |
| FR-14.6 | Query history and saved questions | P2 |
| FR-14.7 | Users can view and copy generated SQL | P2 |

## FR-15: AI Agent Runtime

| ID | Requirement | Priority |
|----|------------|----------|
| FR-15.1 | Tool registry with automatic discovery and versioning | P1 |
| FR-15.2 | Every tool defines name, description, input/output schema, permissions | P1 |
| FR-15.3 | Tools never access database directly — call business services | P1 |
| FR-15.4 | Tool execution pipeline: intent → permission check → validation → execute → format | P1 |
| FR-15.5 | Multi-tool orchestration (call multiple tools, combine results) | P2 |
| FR-15.6 | Tools for: inventory, supplier, procurement, warehouse, executive, analytics, simulation | P1 |

## FR-16: Workflow Automation

| ID | Requirement | Priority |
|----|------------|----------|
| FR-16.1 | Visual workflow designer with drag-and-drop nodes (React Flow) | P1 |
| FR-16.2 | Node types: trigger, condition, decision, action, delay, approval, notification | P1 |
| FR-16.3 | AI-powered workflow builder (natural language → workflow) | P2 |
| FR-16.4 | Workflow simulation before publishing | P2 |
| FR-16.5 | Workflow execution engine with retry, timeout, idempotency | P1 |
| FR-16.6 | Approval center for pending workflow approvals | P1 |
| FR-16.7 | Pre-built workflow templates (low stock reorder, supplier delay, etc.) | P2 |

## FR-17: Audit & Logging

| ID | Requirement | Priority |
|----|------------|----------|
| FR-17.1 | Every authentication event is logged | P0 |
| FR-17.2 | Every inventory change is audited | P0 |
| FR-17.3 | Every procurement action (PO, approval, GRN) is audited | P0 |
| FR-17.4 | Every permission change is audited | P1 |
| FR-17.5 | Audit logs include user, timestamp, IP, request ID, action, before/after | P1 |
| FR-17.6 | Structured JSON logging with request IDs | P0 |

## FR-18: Notifications

| ID | Requirement | Priority |
|----|------------|----------|
| FR-18.1 | In-app notification center | P1 |
| FR-18.2 | Notification types: low stock, PO approved, transfer received, supplier delay | P1 |
| FR-18.3 | Email notification infrastructure (placeholder, not real sending) | P2 |
| FR-18.4 | Notification preferences per user | P2 |

---

## Priority Definitions

- **P0**: Must have — core ERP functionality
- **P1**: Should have — significant value, implemented in primary phases
- **P2**: Nice to have — implemented if bandwidth permits
