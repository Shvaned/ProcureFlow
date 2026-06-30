"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import {
  Sparkles,
  TrendingUp,
  TrendingDown,
  Package,
  ShoppingCart,
  Warehouse,
  AlertTriangle,
  DollarSign,
  BarChart3,
  Download,
} from "lucide-react";
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
  Legend,
} from "recharts";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4"];
const CHART_STYLE = { fontSize: 12, fontFamily: "Inter, sans-serif" };

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
interface InvAnalytics {
  total_records: number;
  total_available: number;
  total_reserved: number;
  total_damaged: number;
  total_value: number;
}
interface ProcAnalytics {
  total_purchase_orders: number;
  total_spend: number;
  by_status: { status: string; count: number; spend: number }[];
}
interface SupAnalytics {
  total_suppliers: number;
  average_rating: number;
  top_suppliers: { name: string; rating: number }[];
}
interface WhAnalytics {
  warehouses: { id: string; name: string; inventory_value: number; available_quantity: number }[];
}
interface ProdAnalytics {
  by_category: { category: string; count: number }[];
  by_brand: { brand: string; count: number }[];
}
interface AiSummary {
  answer: string;
  context: any;
}

export default function ExecutiveDashboard() {
  const [exec, setExec] = useState<ExecData | null>(null);
  const [inv, setInv] = useState<InvAnalytics | null>(null);
  const [proc, setProc] = useState<ProcAnalytics | null>(null);
  const [sup, setSup] = useState<SupAnalytics | null>(null);
  const [wh, setWh] = useState<WhAnalytics | null>(null);
  const [prod, setProd] = useState<ProdAnalytics | null>(null);
  const [aiSummary, setAiSummary] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [e, i, p, s, w, pr] = await Promise.all([
        apiClient.get<{ data: ExecData }>("/api/v1/analytics/executive"),
        apiClient.get<{ data: InvAnalytics }>("/api/v1/analytics/inventory"),
        apiClient.get<{ data: ProcAnalytics }>("/api/v1/analytics/procurement"),
        apiClient.get<{ data: SupAnalytics }>("/api/v1/analytics/supplier"),
        apiClient.get<{ data: WhAnalytics }>("/api/v1/analytics/warehouse"),
        apiClient.get<{ data: ProdAnalytics }>("/api/v1/analytics/product"),
      ]);
      setExec(e.data);
      setInv(i.data);
      setProc(p.data);
      setSup(s.data);
      setWh(w.data);
      setProd(pr.data);
    } catch {}
    setLoading(false);
  };

  const fetchAiSummary = async () => {
    setAiLoading(true);
    try {
      const r = await apiClient.post<{ data: { answer: string } }>("/api/v1/ai/executive/chat", {
        question:
          "Provide a brief executive summary of the business. Highlight the top metrics, key risks, and 3 recommended actions. Be specific with numbers. Keep it under 200 words.",
      });
      setAiSummary(r.data?.answer || "AI summary unavailable");
    } catch {
      setAiSummary("AI service is currently unavailable.");
    }
    setAiLoading(false);
  };

  useEffect(() => {
    fetchAll();
    fetchAiSummary();
  }, []);

  const exportCSV = () => {
    if (!exec) return;
    const csv = [
      "metric,value",
      `Products,${exec.total_products}`,
      `Suppliers,${exec.total_suppliers}`,
      `Warehouses,${exec.total_warehouses}`,
      `Inventory Value,${exec.total_inventory_value}`,
      `Open POs,${exec.open_purchase_orders}`,
      `Pending Approvals,${exec.pending_approvals}`,
      `Low Stock,${exec.low_stock_items}`,
      `Out of Stock,${exec.out_of_stock_items}`,
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "executive-summary.csv";
    a.click();
  };

  if (loading)
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        Loading analytics...
      </div>
    );

  const kpiCards = exec
    ? [
        {
          label: "Inventory Value",
          value: `₹${(exec.total_inventory_value / 100000).toFixed(1)}L`,
          icon: Package,
          trend: "+12%",
          up: true,
        },
        {
          label: "Open POs",
          value: exec.open_purchase_orders.toString(),
          icon: ShoppingCart,
          trend: `${exec.pending_approvals} pending`,
          up: null,
        },
        {
          label: "Suppliers",
          value: exec.total_suppliers.toString(),
          icon: Truck,
          trend: `${sup?.average_rating?.toFixed(1)}★ avg`,
          up: true,
        },
        {
          label: "Warehouses",
          value: exec.total_warehouses.toString(),
          icon: Warehouse,
          trend: `${exec.total_products} products`,
          up: null,
        },
        {
          label: "Low Stock",
          value: exec.low_stock_items.toString(),
          icon: AlertTriangle,
          trend: exec.low_stock_items > 5 ? "Needs attention" : "OK",
          up: exec.low_stock_items > 5,
        },
        {
          label: "Out of Stock",
          value: exec.out_of_stock_items.toString(),
          icon: DollarSign,
          trend: exec.out_of_stock_items > 0 ? "Critical" : "None",
          up: false,
        },
      ]
    : [];

  const whChartData =
    wh?.warehouses?.map((w) => ({
      name: w.name?.slice(0, 12) || "Unknown",
      value: Math.round(w.inventory_value / 100000),
    })) || [];
  const procChartData =
    proc?.by_status?.map((s) => ({
      name: s.status,
      spend: Math.round(s.spend / 1000),
      count: s.count,
    })) || [];
  const catChartData =
    prod?.by_category
      ?.slice(0, 6)
      .map((c) => ({ name: c.category?.slice(0, 15) || "Other", value: c.count })) || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Executive Dashboard</h1>
          <p className="text-muted-foreground">Real-time business intelligence and analytics</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={fetchAll}>
            <BarChart3 className="mr-2 h-4 w-4" /> Refresh
          </Button>
          <Button variant="outline" size="sm" onClick={exportCSV}>
            <Download className="mr-2 h-4 w-4" /> Export
          </Button>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
        {kpiCards.map((kpi) => (
          <Card key={kpi.label} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardContent className="py-4">
              <div className="flex items-center justify-between mb-2">
                <kpi.icon className="h-4 w-4 text-muted-foreground" />
                {kpi.trend &&
                  kpi.up !== null &&
                  (kpi.up ? (
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  ) : (
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  ))}
              </div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">{kpi.label}</p>
              <p className="mt-1 text-xl font-bold">{kpi.value}</p>
              {kpi.trend && (
                <p
                  className={`mt-1 text-xs ${kpi.up === true ? "text-green-500" : kpi.up === false ? "text-red-500" : "text-muted-foreground"}`}
                >
                  {kpi.trend}
                </p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Warehouse Value Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Inventory Value by Warehouse (₹L)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={whChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" style={CHART_STYLE} />
                <YAxis style={CHART_STYLE} />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Procurement Status Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Procurement by Status (₹K)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={procChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" style={CHART_STYLE} />
                <YAxis style={CHART_STYLE} />
                <Tooltip />
                <Bar dataKey="spend" fill="#22c55e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Category Distribution + AI Summary */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Products by Category</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={catChartData}
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  dataKey="value"
                  label={({ name, value }) => `${name} (${value})`}
                >
                  <Tooltip />
                  {catChartData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* AI Executive Summary */}
        <Card className="border-primary/20">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" /> AI Executive Summary
              </CardTitle>
              <Button variant="ghost" size="sm" onClick={fetchAiSummary} disabled={aiLoading}>
                <Sparkles className={`mr-1 h-3 w-3 ${aiLoading ? "animate-pulse" : ""}`} />{" "}
                {aiLoading ? "Analyzing..." : "Regenerate"}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {aiSummary ? (
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{aiSummary}</p>
              </div>
            ) : (
              <div className="py-8 text-center text-muted-foreground text-sm">
                Click &quot;Regenerate&quot; to load AI summary
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Quick Stats Table */}
      <div className="grid gap-6 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Inventory Health</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <StatRow label="Total Records" value={inv?.total_records || 0} />
            <StatRow label="Available Qty" value={inv?.total_available || 0} />
            <StatRow label="Reserved Qty" value={inv?.total_reserved || 0} />
            <StatRow label="Damaged Qty" value={inv?.total_damaged || 0} />
            <StatRow
              label="Total Value"
              value={`₹${((inv?.total_value || 0) / 100000).toFixed(1)}L`}
              highlight
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Supplier Performance</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <StatRow label="Total Suppliers" value={sup?.total_suppliers || 0} />
            <StatRow
              label="Average Rating"
              value={`${sup?.average_rating?.toFixed(1) || "0.0"} / 5.0`}
              highlight
            />
            {sup?.top_suppliers?.slice(0, 3).map((s, i) => (
              <StatRow key={i} label={s.name?.slice(0, 20)} value={`${s.rating?.toFixed(1)}★`} />
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Warehouse Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {wh?.warehouses?.slice(0, 4).map((w, i) => (
              <StatRow
                key={i}
                label={w.name}
                value={`₹${((w.inventory_value || 0) / 100000).toFixed(1)}L · ${w.available_quantity} units`}
              />
            ))}
            {(wh?.warehouses?.length || 0) === 0 && (
              <div className="text-sm text-muted-foreground">No warehouse data</div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatRow({
  label,
  value,
  highlight,
}: {
  label: string;
  value: string | number;
  highlight?: boolean;
}) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-muted-foreground">{label}</span>
      <span className={`font-medium ${highlight ? "text-primary" : ""}`}>{value}</span>
    </div>
  );
}
