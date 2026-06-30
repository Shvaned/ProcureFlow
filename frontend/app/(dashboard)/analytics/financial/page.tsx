"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { DollarSign, TrendingUp, Download } from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"];
const STYLE = { fontSize: 12 };

interface ProcData {
  total_purchase_orders: number;
  total_spend: number;
  by_status: { status: string; count: number; spend: number }[];
}
interface InvData {
  total_value: number;
  total_available: number;
  total_reserved: number;
  total_damaged: number;
}

export default function FinancialAnalytics() {
  const [proc, setProc] = useState<ProcData | null>(null);
  const [inv, setInv] = useState<InvData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiClient.get<{ data: ProcData }>("/api/v1/analytics/procurement"),
      apiClient.get<{ data: InvData }>("/api/v1/analytics/inventory"),
    ])
      .then(([p, i]) => {
        setProc(p.data);
        setInv(i.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading)
    return (
      <div className="py-16 text-center text-muted-foreground">Loading financial analytics...</div>
    );

  const spendData =
    proc?.by_status?.map((s) => ({
      name: s.status,
      spend: Math.round(s.spend / 1000),
      count: s.count,
    })) || [];
  const valuationData = [
    { name: "Inventory Value", value: Math.round((inv?.total_value || 0) / 100000) },
    { name: "Procurement Spend", value: Math.round((proc?.total_spend || 0) / 100000) },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Financial Overview</h1>
          <p className="text-muted-foreground">Valuation, spend analysis, and cost breakdown</p>
        </div>
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" /> Export
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Inventory Value</p>
            <p className="text-2xl font-bold">₹{((inv?.total_value || 0) / 100000).toFixed(1)}L</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Procurement Spend</p>
            <p className="text-2xl font-bold">₹{((proc?.total_spend || 0) / 100000).toFixed(1)}L</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Total POs</p>
            <p className="text-2xl font-bold">{proc?.total_purchase_orders || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4">
            <p className="text-xs uppercase text-muted-foreground">Gross Margin</p>
            <p className="text-2xl font-bold text-green-500">--</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Spend by PO Status (₹K)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={spendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" style={STYLE} />
                <YAxis style={STYLE} />
                <Tooltip />
                <Bar dataKey="spend" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Valuation vs Spend (₹L)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={valuationData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ₹${value}L`}
                >
                  <Tooltip />
                  {valuationData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
