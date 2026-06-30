"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { ShoppingCart, TrendingUp, Download } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface ProcData { total_purchase_orders: number; total_spend: number; by_status: { status: string; count: number; spend: number }[]; }

export default function ProcurementAnalytics() {
  const [data, setData] = useState<ProcData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<{ data: ProcData }>("/api/v1/analytics/procurement").then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="py-16 text-center text-muted-foreground">Loading procurement analytics...</div>;
  const chartData = data?.by_status?.map(s => ({ name: s.status, spend: Math.round(s.spend / 1000), count: s.count })) || [];
  const totalSpend = Math.round((data?.total_spend || 0) / 100000);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Procurement Insights</h1><p className="text-muted-foreground">PO trends, approval analysis, spend breakdown</p></div>
        <Button variant="outline" size="sm"><Download className="mr-2 h-4 w-4" /> Export</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card><CardContent className="py-4"><p className="text-xs uppercase text-muted-foreground">Total POs</p><p className="text-2xl font-bold">{data?.total_purchase_orders || 0}</p></CardContent></Card>
        <Card><CardContent className="py-4"><p className="text-xs uppercase text-muted-foreground">Total Spend</p><p className="text-2xl font-bold">₹{totalSpend}L</p></CardContent></Card>
        <Card><CardContent className="py-4"><p className="text-xs uppercase text-muted-foreground">Draft POs</p><p className="text-2xl font-bold">{chartData.find(s => s.name === "draft")?.count || 0}</p></CardContent></Card>
        <Card><CardContent className="py-4"><p className="text-xs uppercase text-muted-foreground">Approved POs</p><p className="text-2xl font-bold">{chartData.find(s => s.name === "approved")?.count || 0}</p></CardContent></Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card><CardHeader><CardTitle>Spend by Status (₹K)</CardTitle></CardHeader><CardContent><ResponsiveContainer width="100%" height={300}><BarChart data={chartData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" style={{ fontSize: 12 }} /><YAxis style={{ fontSize: 12 }} /><Tooltip /><Bar dataKey="spend" fill="#f59e0b" radius={[4,4,0,0]} /></BarChart></ResponsiveContainer></CardContent></Card>
        <Card><CardHeader><CardTitle>PO Count by Status</CardTitle></CardHeader><CardContent><ResponsiveContainer width="100%" height={300}><BarChart data={chartData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" style={{ fontSize: 12 }} /><YAxis style={{ fontSize: 12 }} /><Tooltip /><Bar dataKey="count" fill="#3b82f6" radius={[4,4,0,0]} /></BarChart></ResponsiveContainer></CardContent></Card>
      </div>
    </div>
  );
}
