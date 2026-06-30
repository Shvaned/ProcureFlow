"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Warehouse, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface WhData {
  warehouses: {
    id: string;
    name: string;
    inventory_value: number;
    available_quantity: number;
    is_active: boolean;
  }[];
}

export default function WarehouseAnalytics() {
  const [data, setData] = useState<WhData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<{ data: WhData }>("/api/v1/analytics/warehouse")
      .then((r) => {
        setData(r.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="py-16 text-center text-muted-foreground">Loading warehouse analytics...</div>
    );

  const chartData =
    data?.warehouses?.map((w) => ({
      name: w.name?.slice(0, 12) || "Unknown",
      value: Math.round((w.inventory_value || 0) / 100000),
      quantity: w.available_quantity || 0,
    })) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Warehouse Analytics</h1>
          <p className="text-muted-foreground">Utilization, capacity, inventory distribution</p>
        </div>
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" /> Export
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total Warehouses</p>
            <p className="text-2xl font-bold">{data?.warehouses?.length || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Active</p>
            <p className="text-2xl font-bold text-green-500">
              {data?.warehouses?.filter((w) => w.is_active).length || 0}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total Inv Value</p>
            <p className="text-2xl font-bold">₹{chartData.reduce((sum, w) => sum + w.value, 0)}L</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total Units</p>
            <p className="text-2xl font-bold">
              {chartData.reduce((sum, w) => sum + w.quantity, 0).toLocaleString()}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Inventory Value by Warehouse (₹L)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" style={{ fontSize: 12 }} />
                <YAxis style={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="value" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Warehouse Details</CardTitle>
          </CardHeader>
          <CardContent>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="py-2 font-medium">Warehouse</th>
                  <th className="py-2 font-medium text-right">Value (₹L)</th>
                  <th className="py-2 font-medium text-right">Units</th>
                  <th className="py-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {chartData.map((w, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-2">{w.name}</td>
                    <td className="py-2 text-right">{w.value}</td>
                    <td className="py-2 text-right">{w.quantity.toLocaleString()}</td>
                    <td className="py-2">
                      <span className="rounded-full bg-green-100 dark:bg-green-900/30 px-2 py-0.5 text-xs text-green-700 dark:text-green-400">
                        Active
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
