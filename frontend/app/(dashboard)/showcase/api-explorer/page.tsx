"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Code2,
  Key,
  Shield,
  Database,
  Brain,
  Zap,
  BarChart3,
  Package,
  Truck,
  Warehouse,
  ShoppingCart,
  Users,
} from "lucide-react";

const API_MODULES = [
  {
    name: "Health & System",
    icon: Zap,
    endpoints: [
      { method: "GET", path: "/api/v1/health", auth: "Public", desc: "Service health check" },
      { method: "GET", path: "/api/v1/health/ready", auth: "Public", desc: "Readiness probe" },
      { method: "GET", path: "/api/v1/health/live", auth: "Public", desc: "Liveness probe" },
    ],
  },
  {
    name: "Authentication",
    icon: Key,
    endpoints: [
      {
        method: "POST",
        path: "/api/v1/auth/login",
        auth: "Public",
        desc: "JWT login with refresh token",
      },
      { method: "POST", path: "/api/v1/auth/logout", auth: "Bearer", desc: "Session revocation" },
      {
        method: "POST",
        path: "/api/v1/auth/refresh",
        auth: "Public",
        desc: "Token refresh rotation",
      },
      { method: "GET", path: "/api/v1/auth/me", auth: "Bearer", desc: "Current user profile" },
      {
        method: "POST",
        path: "/api/v1/auth/change-password",
        auth: "Bearer",
        desc: "Password change",
      },
    ],
  },
  {
    name: "Users & RBAC",
    icon: Users,
    endpoints: [
      { method: "GET", path: "/api/v1/users", auth: "Users.Read", desc: "List users" },
      { method: "GET", path: "/api/v1/users/{id}", auth: "Users.Read", desc: "User detail" },
      { method: "POST", path: "/api/v1/users", auth: "Users.Write", desc: "Create user" },
      { method: "PUT", path: "/api/v1/users/{id}", auth: "Users.Write", desc: "Update user" },
      {
        method: "GET",
        path: "/api/v1/roles",
        auth: "Users.Read",
        desc: "List roles with permissions",
      },
      { method: "POST", path: "/api/v1/roles", auth: "Users.Write", desc: "Create role" },
      { method: "PUT", path: "/api/v1/roles/{id}", auth: "Users.Write", desc: "Update role" },
      {
        method: "GET",
        path: "/api/v1/permissions",
        auth: "Users.Read",
        desc: "List all permissions",
      },
    ],
  },
  {
    name: "Product Catalog",
    icon: Package,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/products",
        auth: "Products.Read",
        desc: "Paginated product list",
      },
      {
        method: "GET",
        path: "/api/v1/products/{id}",
        auth: "Products.Read",
        desc: "Product detail with images",
      },
      { method: "POST", path: "/api/v1/products", auth: "Products.Create", desc: "Create product" },
      {
        method: "PUT",
        path: "/api/v1/products/{id}",
        auth: "Products.Update",
        desc: "Update product",
      },
      {
        method: "DELETE",
        path: "/api/v1/products/{id}",
        auth: "Products.Delete",
        desc: "Soft-delete product",
      },
      { method: "GET", path: "/api/v1/categories", auth: "Categories.Read", desc: "Category tree" },
      { method: "GET", path: "/api/v1/brands", auth: "Brands.Read", desc: "Brands list" },
      { method: "GET", path: "/api/v1/units", auth: "Products.Read", desc: "Units of measure" },
    ],
  },
  {
    name: "Warehouse & Inventory",
    icon: Warehouse,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/warehouses",
        auth: "Warehouses.Read",
        desc: "List warehouses",
      },
      {
        method: "POST",
        path: "/api/v1/warehouses",
        auth: "Warehouses.Write",
        desc: "Create warehouse",
      },
      {
        method: "GET",
        path: "/api/v1/warehouses/{id}/zones",
        auth: "Warehouses.Read",
        desc: "Warehouse zones",
      },
      {
        method: "GET",
        path: "/api/v1/inventory",
        auth: "Inventory.Read",
        desc: "Paginated inventory",
      },
      {
        method: "GET",
        path: "/api/v1/inventory/alerts/low-stock",
        auth: "Inventory.Read",
        desc: "Low stock alerts",
      },
      {
        method: "GET",
        path: "/api/v1/inventory/alerts/expiring",
        auth: "Inventory.Read",
        desc: "Expiring stock",
      },
      {
        method: "GET",
        path: "/api/v1/inventory/{id}/transactions",
        auth: "Inventory.ViewHistory",
        desc: "Transaction history",
      },
      {
        method: "POST",
        path: "/api/v1/transfers",
        auth: "Inventory.Transfer",
        desc: "Create transfer",
      },
      {
        method: "POST",
        path: "/api/v1/adjustments",
        auth: "Inventory.Adjust",
        desc: "Create adjustment",
      },
    ],
  },
  {
    name: "Suppliers & Procurement",
    icon: Truck,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/suppliers",
        auth: "Suppliers.Read",
        desc: "Paginated supplier list",
      },
      {
        method: "GET",
        path: "/api/v1/suppliers/{id}",
        auth: "Suppliers.Read",
        desc: "Supplier with contacts",
      },
      {
        method: "POST",
        path: "/api/v1/suppliers",
        auth: "Suppliers.Create",
        desc: "Create supplier",
      },
      {
        method: "PUT",
        path: "/api/v1/suppliers/{id}",
        auth: "Suppliers.Update",
        desc: "Update supplier",
      },
      {
        method: "GET",
        path: "/api/v1/purchase-orders",
        auth: "PurchaseOrders.Read",
        desc: "PO list",
      },
      {
        method: "GET",
        path: "/api/v1/purchase-orders/{id}",
        auth: "PurchaseOrders.Read",
        desc: "PO with items/approvals",
      },
      {
        method: "POST",
        path: "/api/v1/purchase-orders",
        auth: "PurchaseOrders.Create",
        desc: "Create PO with items",
      },
      {
        method: "POST",
        path: "/api/v1/purchase-orders/{id}/approve",
        auth: "PurchaseOrders.Approve",
        desc: "Approve PO",
      },
      { method: "POST", path: "/api/v1/grn", auth: "PurchaseOrders.Receive", desc: "Create GRN" },
    ],
  },
  {
    name: "Analytics",
    icon: BarChart3,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/analytics/executive",
        auth: "Analytics.Read",
        desc: "Executive summary",
      },
      {
        method: "GET",
        path: "/api/v1/analytics/inventory",
        auth: "Analytics.Read",
        desc: "Inventory analytics",
      },
      {
        method: "GET",
        path: "/api/v1/analytics/procurement",
        auth: "Analytics.Read",
        desc: "Procurement analytics",
      },
      {
        method: "GET",
        path: "/api/v1/analytics/supplier",
        auth: "Analytics.Read",
        desc: "Supplier analytics",
      },
      {
        method: "GET",
        path: "/api/v1/analytics/warehouse",
        auth: "Analytics.Read",
        desc: "Warehouse analytics",
      },
      {
        method: "GET",
        path: "/api/v1/analytics/product",
        auth: "Analytics.Read",
        desc: "Product analytics",
      },
      { method: "GET", path: "/api/v1/kpis/{key}", auth: "Analytics.Read", desc: "KPI data" },
    ],
  },
  {
    name: "AI Platform",
    icon: Brain,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/ai/executive/daily-brief",
        auth: "AI.Use",
        desc: "AI daily brief",
      },
      {
        method: "GET",
        path: "/api/v1/ai/executive/health-score",
        auth: "AI.Use",
        desc: "Business health score",
      },
      {
        method: "POST",
        path: "/api/v1/ai/executive/chat",
        auth: "AI.Use",
        desc: "Executive chat with context",
      },
      {
        method: "GET",
        path: "/api/v1/ai/executive/conversations",
        auth: "AI.Use",
        desc: "Conversation history",
      },
      {
        method: "GET",
        path: "/api/v1/ai/procurement/reorder",
        auth: "AI.Use",
        desc: "Reorder recommendations",
      },
      {
        method: "GET",
        path: "/api/v1/ai/suppliers/{id}/analysis",
        auth: "AI.Use",
        desc: "Supplier AI analysis",
      },
      {
        method: "POST",
        path: "/api/v1/ai/analytics/query",
        auth: "AI.Use",
        desc: "NL→SQL analytics query",
      },
      { method: "GET", path: "/api/v1/ai/tools", auth: "AI.Use", desc: "List 18 AI tools" },
    ],
  },
  {
    name: "Simulation & Workflows",
    icon: Zap,
    endpoints: [
      {
        method: "GET",
        path: "/api/v1/simulation/status",
        auth: "Simulation.Read",
        desc: "Simulation status",
      },
      {
        method: "POST",
        path: "/api/v1/simulation/start",
        auth: "Simulation.Manage",
        desc: "Start simulation",
      },
      {
        method: "GET",
        path: "/api/v1/simulation/events",
        auth: "Simulation.Read",
        desc: "Event log",
      },
      { method: "GET", path: "/api/v1/workflows", auth: "Automation.Read", desc: "List workflows" },
      {
        method: "POST",
        path: "/api/v1/workflows",
        auth: "Automation.Create",
        desc: "Create workflow",
      },
      {
        method: "POST",
        path: "/api/v1/workflows/{id}/execute",
        auth: "Automation.Execute",
        desc: "Execute workflow",
      },
      {
        method: "GET",
        path: "/api/v1/workflows/analytics",
        auth: "Automation.Read",
        desc: "Workflow analytics",
      },
      {
        method: "GET",
        path: "/api/v1/scenarios/baseline",
        auth: "Scenario.Read",
        desc: "Business baseline",
      },
      { method: "POST", path: "/api/v1/scenarios/run", auth: "Scenario.Run", desc: "Run scenario" },
    ],
  },
];

const METHOD_COLORS: Record<string, string> = {
  GET: "bg-green-100 text-green-700 dark:bg-green-950/30 dark:text-green-400",
  POST: "bg-blue-100 text-blue-700 dark:bg-blue-950/30 dark:text-blue-400",
  PUT: "bg-orange-100 text-orange-700 dark:bg-orange-950/30 dark:text-orange-400",
  DELETE: "bg-red-100 text-red-700 dark:bg-red-950/30 dark:text-red-400",
};

export default function APIExplorerPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Code2 className="h-6 w-6 text-primary" /> API Explorer
        </h1>
        <p className="text-muted-foreground">
          {API_MODULES.reduce((sum, m) => sum + m.endpoints.length, 0)} endpoints across{" "}
          {API_MODULES.length} modules
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {API_MODULES.map((mod) => (
          <Card key={mod.name}>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <mod.icon className="h-4 w-4 text-primary" />
                {mod.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b bg-muted/50">
                    <th className="py-1.5 px-3 text-left font-medium">Method</th>
                    <th className="py-1.5 px-3 text-left font-medium">Path</th>
                    <th className="py-1.5 px-3 text-left font-medium">Auth</th>
                  </tr>
                </thead>
                <tbody>
                  {mod.endpoints.map((ep, i) => (
                    <tr key={i} className="border-b last:border-0 hover:bg-muted/30">
                      <td className="py-1.5 px-3">
                        <span
                          className={`rounded px-1.5 py-0.5 font-mono font-medium text-[10px] ${METHOD_COLORS[ep.method] || ""}`}
                        >
                          {ep.method}
                        </span>
                      </td>
                      <td className="py-1.5 px-3 font-mono text-[11px]">{ep.path}</td>
                      <td className="py-1.5 px-3 text-muted-foreground">{ep.auth}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="bg-primary/5 border-primary/20">
        <CardContent className="py-4 text-center">
          <p className="text-sm">
            Interactive API documentation available at{" "}
            <a
              href="http://localhost:8000/api/docs"
              target="_blank"
              className="text-primary font-medium hover:underline"
            >
              /api/docs
            </a>{" "}
            (Swagger UI) and{" "}
            <a
              href="http://localhost:8000/api/redoc"
              target="_blank"
              className="text-primary font-medium hover:underline"
            >
              /api/redoc
            </a>{" "}
            (ReDoc)
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
