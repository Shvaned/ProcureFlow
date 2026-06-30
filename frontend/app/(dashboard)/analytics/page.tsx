"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { apiClient } from "@/services/api-client";
import { BarChart3, TrendingUp, DollarSign, ShoppingCart, Package, Truck, Warehouse, ArrowRight } from "lucide-react";

interface ExecData { total_inventory_value: number; total_products: number; total_suppliers: number; total_warehouses: number; }

export default function AnalyticsHub() {
  const [data, setData] = useState<ExecData | null>(null);
  useEffect(() => {
    apiClient.get<{ data: ExecData }>("/api/v1/analytics/executive").then(r => setData(r.data)).catch(() => {});
  }, []);

  const modules = [
    { label: "Financial Overview", href: "/analytics/financial", icon: DollarSign, desc: "Revenue, margins, valuation, spend analysis", color: "text-green-500" },
    { label: "Procurement Insights", href: "/analytics/procurement", icon: ShoppingCart, desc: "PO trends, approval times, spend by supplier", color: "text-blue-500" },
    { label: "Inventory Insights", href: "/analytics/inventory", icon: Package, desc: "ABC analysis, aging, turnover, stock health", color: "text-orange-500" },
    { label: "Supplier Performance", href: "/analytics/supplier", icon: Truck, desc: "Scorecards, lead times, delivery accuracy", color: "text-purple-500" },
    { label: "Warehouse Analytics", href: "/analytics/warehouse", icon: Warehouse, desc: "Utilization, capacity, throughput, transfers", color: "text-cyan-500" },
  ];

  return (
    <div className="space-y-6">
      <div><h1 className="text-2xl font-bold">Analytics</h1><p className="text-muted-foreground">Executive business intelligence and operational analytics</p></div>

      <div className="grid gap-4 md:grid-cols-4">
        {[
          { label: "Inventory Value", value: data ? `₹${(data.total_inventory_value / 100000).toFixed(1)}L` : "--" },
          { label: "Products", value: data?.total_products?.toString() || "--" },
          { label: "Suppliers", value: data?.total_suppliers?.toString() || "--" },
          { label: "Warehouses", value: data?.total_warehouses?.toString() || "--" },
        ].map(k => (
          <Card key={k.label}><CardContent className="py-4"><p className="text-xs text-muted-foreground uppercase">{k.label}</p><p className="mt-1 text-xl font-bold">{k.value}</p></CardContent></Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {modules.map(m => (
          <Link key={m.href} href={m.href}>
            <Card className="h-full transition-all hover:border-primary/50 hover:shadow-md cursor-pointer group">
              <CardContent className="py-6">
                <div className="flex items-start justify-between">
                  <m.icon className={`h-6 w-6 ${m.color}`} />
                  <ArrowRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <h3 className="mt-3 font-semibold">{m.label}</h3>
                <p className="mt-1 text-sm text-muted-foreground">{m.desc}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
