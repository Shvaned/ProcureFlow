# ProcureFlow AI — User Stories

**Version:** 1.0.0
**Date:** 2026-06-30

---

## Epic 1: Authentication & Access

### As an Admin (Rajesh)
- US-1.1: I can create users with email, name, and role so new employees can access the system.
- US-1.2: I can assign roles to users so they have appropriate access.
- US-1.3: I can create custom roles with specific permissions so I can model our organization's structure.
- US-1.4: I can view audit logs so I know who did what and when.
- US-1.5: I can lock/unlock user accounts so I can respond to security events.
- US-1.6: I can view all active sessions so I can identify suspicious activity.

### As any User
- US-1.7: I can login with email and password so I can access the system.
- US-1.8: I can change my password so I can maintain account security.
- US-1.9: My session persists across page refreshes so I don't need to re-login constantly.
- US-1.10: I am automatically logged out after inactivity so my account stays secure.
- US-1.11: I see only features I have permission to access so the interface isn't cluttered.

---

## Epic 2: Product Catalog

### As a Procurement Manager (Ankit)
- US-2.1: I can create new products with SKU, barcode, pricing, and tax information so they can be ordered and tracked.
- US-2.2: I can edit product details when specifications change.
- US-2.3: I can search products by SKU, name, brand, or category so I can find products quickly.
- US-2.4: I can filter products by status, category, brand, and price so I can narrow down large lists.
- US-2.5: I can bulk-import products from CSV so I can onboard large catalogs quickly.
- US-2.6: I can export the product list to CSV for offline analysis.

### As an Operations Manager (Priya)
- US-2.7: I can organize products into hierarchical categories so reporting is structured logically.
- US-2.8: I can see which products are active vs. inactive so I can manage the catalog lifecycle.

### As a Warehouse Manager (Vikram)
- US-2.9: I can scan/search by barcode to identify products during receiving.
- US-2.10: I can see product images and specifications so I can verify correct items.

---

## Epic 3: Warehouse & Inventory

### As a Warehouse Manager (Vikram)
- US-3.1: I can create warehouses with address, zones, and bins so I can model our physical layout.
- US-3.2: I can view real-time inventory by product, warehouse, zone, and bin.
- US-3.3: I can transfer stock between bins, zones, and warehouses.
- US-3.4: I can record inventory adjustments with a reason when physical counts differ.
- US-3.5: I can reserve stock for specific orders so it cannot be allocated elsewhere.
- US-3.6: I can track lot numbers and expiry dates so I can implement FIFO picking.
- US-3.7: I receive alerts when stock falls below reorder level so I can request replenishment.
- US-3.8: I receive alerts when products are expiring soon so I can action them.
- US-3.9: I can view complete inventory history for any product so I can trace discrepancies.

### As an Operations Manager (Priya)
- US-3.10: I can see warehouse utilization across all locations so I can balance load.
- US-3.11: I can view inventory valuation by warehouse and category.
- US-3.12: I can see low stock and out-of-stock products across all warehouses.
- US-3.13: I can run stock aging reports to identify dead or slow-moving inventory.

### As a Finance Manager (Meera)
- US-3.14: I can view inventory valuation reports (FIFO, weighted average) for financial reporting.
- US-3.15: I can see inventory carrying costs by warehouse.

### As a Viewer (Sneha)
- US-3.16: I can check stock availability for any product across all warehouses.
- US-3.17: I can see expected incoming stock from purchase orders.

---

## Epic 4: Supplier Management

### As a Procurement Manager (Ankit)
- US-4.1: I can onboard new suppliers with contact details, GST, payment terms.
- US-4.2: I can upload supplier documents (GST certificate, PAN, agreements).
- US-4.3: I can track supplier performance: lead time, delivery accuracy, quality scores.
- US-4.4: I can compare suppliers side-by-side on price, lead time, and reliability.
- US-4.5: I can search suppliers by name, code, GST, or product supplied.
- US-4.6: I can see complete purchase history per supplier.

### As an Operations Manager (Priya)
- US-4.7: I can view supplier scorecards and rankings.
- US-4.8: I can identify single-supplier dependencies for risk mitigation.

---

## Epic 5: Procurement

### As a Procurement Manager (Ankit)
- US-5.1: I can create purchase requests for products that need replenishment.
- US-5.2: I can generate purchase orders from approved requests.
- US-5.3: I can send POs for approval with all relevant context.
- US-5.4: I can track PO status from draft through to received.
- US-5.5: I receive recommendations on what to reorder and when.
- US-5.6: I can compare supplier quotations before committing to a PO.
- US-5.7: I can record goods received against a PO (full or partial).
- US-5.8: I can see what's pending delivery and which deliveries are late.

### As a Warehouse Manager (Vikram)
- US-5.9: I can record goods receipt, verifying quantity and condition.
- US-5.10: Received goods automatically update inventory and create transaction records.

### As a Finance Manager (Meera)
- US-5.11: I can see procurement spend by supplier, category, and warehouse.
- US-5.12: I can approve purchase orders above a threshold.

### As an Operations Manager (Priya)
- US-5.13: I can view open purchase orders and expected delivery dates.
- US-5.14: I can approve or reject purchase requests and purchase orders.

---

## Epic 6: Business Simulation

### As an Admin (Rajesh)
- US-6.1: I can start, pause, and stop the simulation engine.
- US-6.2: I can change simulation speed (real-time, 10x, 100x, 1000x).
- US-6.3: I can select different business scenarios (normal, peak, crisis).
- US-6.4: I can generate realistic seed data for demonstrations.

### As an Operations Manager (Priya)
- US-6.5: I can see the live event log of simulated business operations.
- US-6.6: The simulation makes the ERP feel alive — orders, shipments, transfers happen continuously.

---

## Epic 7: Analytics & Dashboards

### As an Operations Manager (Priya)
- US-7.1: I have an executive dashboard with revenue, inventory value, procurement spend, and KPIs.
- US-7.2: Every KPI shows current value, trend, and comparison to previous period.
- US-7.3: I can drill down from summary metrics to detailed breakdowns.
- US-7.4: I can filter dashboards by date range, warehouse, supplier, and category.
- US-7.5: I can export reports and charts for presentations.

### As a Warehouse Manager (Vikram)
- US-7.6: I have a warehouse-specific dashboard with utilization, movement, and alerts.

### As a Procurement Manager (Ankit)
- US-7.7: I have a procurement dashboard with open POs, spend, and supplier metrics.

### As a Finance Manager (Meera)
- US-7.8: I have financial analytics with valuation, margins, and cost breakdowns.

---

## Epic 8: Executive AI Copilot

### As an Operations Manager (Priya)
- US-8.1: Every morning I receive an AI-generated daily brief summarizing the business.
- US-8.2: The AI highlights the top 3 risks and top 3 opportunities.
- US-8.3: I can ask natural-language questions about business performance.
- US-8.4: The AI explains WHY metrics changed — not just WHAT changed.
- US-8.5: Every AI insight references specific ERP data as evidence.
- US-8.6: I can click on AI recommendations to navigate directly to the relevant ERP module.

---

## Epic 9: AI Procurement Copilot

### As a Procurement Manager (Ankit)
- US-9.1: The system tells me which products need reordering and why.
- US-9.2: When comparing suppliers, the AI explains trade-offs beyond just price.
- US-9.3: Before I approve a PO, the AI reviews it and highlights potential concerns.
- US-9.4: I can run what-if scenarios: "What if this supplier is delayed by 7 days?"
- US-9.5: The AI never places orders — I always approve.

---

## Epic 10: AI Supplier Intelligence

### As a Procurement Manager (Ankit)
- US-10.1: I can upload supplier quotations (PDF or Excel) and the system extracts structured data.
- US-10.2: I can compare multiple quotations side-by-side with AI analysis.
- US-10.3: I can see price trends over time for each supplier and product.
- US-10.4: The AI suggests negotiation points based on historical supplier data.
- US-10.5: I can see supplier risk assessments (dependency, reliability, price risk).

---

## Epic 11: Natural Language Analytics

### As an Operations Manager (Priya)
- US-11.1: I can ask "Which products sold the most this month?" and get a chart + explanation.
- US-11.2: I can ask "Compare inventory value this quarter vs. last quarter."
- US-11.3: I can see the SQL generated for my question (for transparency).
- US-11.4: I can save frequently asked questions for quick access.
- US-11.5: The system never executes unsafe SQL (no DELETE, DROP, UPDATE).

---

## Epic 12: Workflow Automation

### As an Operations Manager (Priya)
- US-12.1: I can build automated workflows using a visual drag-and-drop editor.
- US-12.2: I can describe a workflow in plain English and the AI helps me build it.
- US-12.3: I can simulate a workflow before publishing to verify behavior.
- US-12.4: I receive notifications when workflows trigger actions.

### As a Procurement Manager (Ankit)
- US-12.5: A workflow auto-generates a draft PO when inventory falls below safety stock.
- US-12.6: A workflow notifies me when a supplier delivery is delayed.

---

## Epic 13: Notifications

### As any User
- US-13.1: I receive in-app notifications for relevant events.
- US-13.2: I can see my notification history and mark items as read.
- US-13.3: I can configure which notification types I receive.

---

## Coverage Summary

| Epic | Stories | P0 Stories | Primary Persona |
|------|---------|------------|-----------------|
| Auth & Access | 11 | 7 | Rajesh (Admin) |
| Product Catalog | 10 | 7 | Ankit (Procurement) |
| Warehouse & Inventory | 17 | 10 | Vikram (Warehouse) |
| Supplier Management | 8 | 5 | Ankit (Procurement) |
| Procurement | 14 | 9 | Ankit (Procurement) |
| Business Simulation | 6 | 4 | Rajesh (Admin) |
| Analytics | 8 | 5 | Priya (Operations) |
| Executive AI Copilot | 6 | 4 | Priya (Operations) |
| AI Procurement Copilot | 5 | 3 | Ankit (Procurement) |
| AI Supplier Intelligence | 5 | 3 | Ankit (Procurement) |
| NL Analytics | 5 | 3 | Priya (Operations) |
| Workflow Automation | 6 | 3 | Priya (Operations) |
| Notifications | 3 | 2 | All Users |
| **Total** | **104** | **65** | |
