"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Package, Download } from "lucide-react";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"];

interface InvData {
  total_records: number;
  total_available: number;
  total_reserved: number;
  total_damaged: number;
  total_value: number;
}
interface ProdData {
  by_category: { category: string; count: number }[];
}

export default function InventoryAnalytics() {
  const [inv, setInv] = useState<InvData | null>(null);
  const [prod, setProd] = useState<ProdData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiClient.get<{ data: InvData }>("/api/v1/analytics/inventory"),
      apiClient.get<{ data: ProdData }>("/api/v1/analytics/product"),
    ])
      .then(([i, p]) => {
        setInv(i.data);
        setProd(p.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="py-16 text-center text-muted-foreground">Loading inventory analytics...</div>
    );

  const stockData = [
    { name: "Available", value: inv?.total_available || 0 },
    { name: "Reserved", value: inv?.total_reserved || 0 },
    { name: "Damaged", value: inv?.total_damaged || 0 },
  ];
  const catData =
    prod?.by_category
      ?.slice(0, 8)
      .map((c) => ({ name: c.category?.slice(0, 15) || "Other", value: c.count })) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Inventory Insights</h1>
          <p className="text-muted-foreground">ABC analysis, aging, stock health, turnover</p>
        </div>
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" /> Export
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-5">
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total Records</p>
            <p className="text-xl font-bold">{inv?.total_records || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Available</p>
            <p className="text-xl font-bold text-green-500">{inv?.total_available || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Reserved</p>
            <p className="text-xl font-bold text-blue-500">{inv?.total_reserved || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Damaged</p>
            <p className="text-xl font-bold text-red-500">{inv?.total_damaged || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Value</p>
            <p className="text-xl font-bold">₹{((inv?.total_value || 0) / 100000).toFixed(1)}L</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Stock Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stockData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  <Tooltip />
                  {stockData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Products by Category</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={catData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" style={{ fontSize: 12 }} />
                <YAxis type="category" dataKey="name" width={120} style={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
