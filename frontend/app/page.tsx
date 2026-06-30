"use client";

import { useState, useEffect } from "react";
import { useAuthStore } from "@/providers/auth-provider";
import { LandingPage } from "@/components/landing/landing-page";
import { Sidebar } from "@/components/layout/sidebar";
import { Navbar } from "@/components/layout/navbar";
import { apiClient } from "@/services/api-client";

interface ExecData {
  total_products: number;
  total_suppliers: number;
  total_warehouses: number;
  total_inventory_value: number;
  open_purchase_orders: number;
  pending_approvals: number;
  low_stock_items: number;
  out_of_stock_items: number;
}

export default function Home() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [data, setData] = useState<ExecData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isAuthenticated) return;
    apiClient
      .get<{ data: ExecData }>("/api/v1/analytics/executive")
      .then((r) => setData(r.data))
      .catch(() => setError("Could not load dashboard data"));
  }, [isAuthenticated]);

  if (!isAuthenticated) return <LandingPage />;

  const cards = data
    ? [
        { label: "Inventory Value", value: `₹${data.total_inventory_value.toLocaleString()}` },
        { label: "Open POs", value: data.open_purchase_orders.toString() },
        { label: "Suppliers", value: data.total_suppliers.toString() },
        { label: "Warehouses", value: data.total_warehouses.toString() },
        { label: "Products", value: data.total_products.toString() },
        { label: "Pending Approvals", value: data.pending_approvals.toString() },
        { label: "Low Stock Items", value: data.low_stock_items.toString() },
        { label: "Out of Stock", value: data.out_of_stock_items.toString() },
      ]
    : [];

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="ml-60 flex flex-1 flex-col">
        <Navbar />
        <main className="flex-1 p-6">
          <div className="space-y-6">
            <div>
              <h1 className="text-2xl font-bold">Dashboard</h1>
              <p className="text-muted-foreground">Welcome to ProcureFlow AI</p>
            </div>
            {error && (
              <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                {error}
              </div>
            )}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {cards.map(({ label, value }) => (
                <div key={label} className="rounded-lg border bg-card p-4">
                  <p className="text-sm text-muted-foreground">{label}</p>
                  <p className="mt-2 text-2xl font-bold">{value}</p>
                </div>
              ))}
              {!data && !error && cards.length === 0 && (
                <div className="col-span-full py-8 text-center text-muted-foreground">
                  Loading dashboard...
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
