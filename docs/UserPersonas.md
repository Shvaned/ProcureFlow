# ProcureFlow AI — User Personas

**Version:** 1.0.0
**Date:** 2026-06-30

---

## Persona 1: Rajesh — Admin / System Administrator

**Role:** System Administrator
**Organization:** Mid-size B2B Distributor (500+ employees, 7 warehouses)
**Technical Level:** High

### Bio
Rajesh has 10 years in IT operations. He manages user accounts, security policies, and system configuration. He needs full visibility into who accessed what and when. He values audit trails and permission clarity above all.

### Goals
- Onboard new employees quickly with correct roles
- Ensure no unauthorized access to sensitive modules
- Maintain system health and configuration
- Respond to audit requests within minutes

### Pain Points
- Manual permission assignment across growing teams
- Lack of visibility into user activity
- Inconsistent access control across modules

### Usage Patterns
- Daily: User management, monitoring system health
- Weekly: Permission audits, configuration reviews
- Monthly: Full security review, access recertification

---

## Persona 2: Priya — Operations Manager

**Role:** Head of Operations
**Organization:** National B2B Distributor
**Technical Level:** Medium

### Bio
Priya oversees end-to-end operations across multiple warehouses. She reports to the CEO weekly. She needs a consolidated view of inventory health, warehouse utilization, and operational KPIs. Every morning she needs to know: where are the problems?

### Goals
- See inventory status across all warehouses in one view
- Identify problems before they escalate (stockouts, delays, dead stock)
- Track operational KPIs daily: fill rate, turnover, accuracy
- Reduce inventory holding costs while maintaining availability

### Pain Points
- Switching between warehouse-specific spreadsheets
- Discovering stockouts after they happen
- Explaining inventory valuation to finance without real-time data
- No single source of truth for operations KPIs

### Usage Patterns
- Morning: Executive dashboard, AI daily brief, review risks
- Throughout day: Spot-check inventory across warehouses
- Weekly: Review trend reports, compare with targets
- Monthly: Operations review presentation, capacity planning

---

## Persona 3: Vikram — Warehouse Manager

**Role:** Warehouse Manager (Delhi Warehouse)
**Organization:** Enterprise Distributor
**Technical Level:** Medium-Low

### Bio
Vikram manages a 50,000 sq ft warehouse with 15 staff. He handles receiving, storage, picking, packing, and dispatch. He needs to know exactly what is where, what's expiring, and what needs to move. He processes 200+ inventory movements daily.

### Goals
- Know exact inventory location (warehouse → zone → bin)
- Process transfers and adjustments quickly with proper documentation
- Track lot numbers and expiry dates
- Never run out of fast-moving products
- Identify and action expiring stock before it's too late

### Pain Points
- Physical count mismatches requiring investigation
- Items stored in wrong locations
- Expiring stock discovered too late
- Paper-based adjustment approvals taking days
- No real-time view of bin capacity

### Usage Patterns
- Hourly: Check inbound/outbound schedule, process movements
- Throughout day: Receiving, transfers, adjustments, cycle counts
- End of day: Review warehouse dashboard, verify movements
- Weekly: Inventory health check, expiry review

---

## Persona 4: Ankit — Procurement Manager

**Role:** Procurement Manager
**Organization:** Multi-warehouse B2B Distributor
**Technical Level:** Medium

### Bio
Ankit manages procurement for 20,000+ SKUs across 500 suppliers. He processes 30-50 purchase orders weekly. He needs to know what to buy, from whom, at what price, and when it will arrive. Supplier reliability matters more than unit price.

### Goals
- Never stock out of critical products
- Select the best supplier based on data (price, lead time, reliability)
- Reduce procurement cycle time from request to receipt
- Maintain procurement budget while ensuring availability
- Build strong supplier relationships based on performance data

### Pain Points
- Manual reorder calculations based on gut feel
- Difficulty comparing suppliers objectively
- Late deliveries discovered after the fact
- Approvals delayed because approvers lack context
- No centralized supplier performance tracking

### Usage Patterns
- Morning: Review reorder recommendations, approve POs
- Throughout day: Compare suppliers, generate POs, track deliveries
- Weekly: Supplier performance review, spend analysis
- Monthly: Procurement budget review, supplier negotiations

---

## Persona 5: Meera — Finance Manager

**Role:** Finance Manager
**Organization:** Mid-size Distributor
**Technical Level:** Medium-High

### Bio
Meera oversees financial reporting, inventory valuation, and procurement spend. She needs accurate, real-time data to close monthly books and inform leadership. Inventory is typically the largest asset on the balance sheet — she needs precise valuation.

### Goals
- Accurate real-time inventory valuation (FIFO, weighted average)
- Track procurement spend vs. budget
- Monitor margins by product, category, supplier
- Reduce inventory carrying costs
- Close monthly books faster with reliable data

### Pain Points
- Inventory valuation based on outdated reports
- Spend data fragmented across systems
- Manual reconciliation between purchasing and finance
- No visibility into landed costs

### Usage Patterns
- Daily: Spend dashboards, margin checks
- Weekly: Cost analysis, budget vs. actual
- Monthly: Inventory valuation reconciliation, financial close
- Quarterly: Audit preparation, cost optimization analysis

---

## Persona 6: Sneha — Viewer (Regional Sales Manager)

**Role:** Regional Sales Manager
**Organization:** Multi-region Distributor
**Technical Level:** Low-Medium

### Bio
Sneha manages sales across North India. She needs inventory visibility to promise stock to customers. She doesn't need to modify anything — she needs reliable read access to know what's available and when incoming stock arrives.

### Goals
- Check real-time stock availability before promising to customers
- Know when incoming purchase orders will arrive
- Identify alternative warehouses when local stock is unavailable
- Understand product trends in her region

### Pain Points
- Promising stock only to find it was reserved
- No visibility into incoming shipments
- Can't see stock in other warehouses for transfer opportunities
- Waiting for warehouse managers to respond to stock queries

### Usage Patterns
- Throughout day: Stock checks, order status, incoming shipment tracking
- Weekly: Regional demand trends, stock availability planning
- Monthly: Regional performance review

---

## Persona Summary Matrix

| Persona | Role | Primary Tools | Frequency |
|---------|------|--------------|-----------|
| Rajesh | Admin | User Mgmt, Permissions, Audit Logs | Daily |
| Priya | Operations Manager | Executive Dashboard, AI Copilot | Daily |
| Vikram | Warehouse Manager | Warehouse, Inventory, Transfers | Hourly |
| Ankit | Procurement Manager | Suppliers, POs, AI Procurement Copilot | Daily |
| Meera | Finance Manager | Finance Analytics, Valuation, Spend | Daily |
| Sneha | Viewer | Inventory Lookup, Dashboards | Daily |
