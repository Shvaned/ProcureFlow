"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import {
  Truck,
  Search,
  Star,
  AlertTriangle,
  BarChart3,
  FileText,
  Lightbulb,
  CheckCircle,
  XCircle,
  ChevronDown,
  TrendingUp,
  TrendingDown,
  Shield,
  RefreshCw,
  Zap,
} from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface SupplierData {
  id: string;
  code: string;
  legal_name: string;
  email: string | null;
  country: string | null;
  rating: number;
  is_preferred: boolean;
  is_active: boolean;
}
interface Dashboard {
  supplier: any;
  performance: any;
  procurement: any;
  risk_level: string;
  scorecard: any;
}
interface Comparison {
  suppliers: any[];
  count: number;
  recommendation: string;
}
interface Risk {
  type: string;
  severity: string;
  description: string;
  mitigation?: string;
  supplier?: string;
}
interface Recommendation {
  supplier_name: string;
  recommendations: any[];
  priority_actions: string[];
}

export default function SupplierIntelligence() {
  const [tab, setTab] = useState<"dashboard" | "compare" | "risks" | "recommendations">(
    "dashboard"
  );
  const [suppliers, setSuppliers] = useState<SupplierData[]>([]);
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState("");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [comparison, setComparison] = useState<Comparison | null>(null);
  const [compareIds, setCompareIds] = useState<string[]>([]);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(false);
  const [quotationForm, setQuotationForm] = useState({
    items: [{ product_name: "", quantity: 1, unit_price: 0 }],
  });
  const [quotationResult, setQuotationResult] = useState<any>(null);

  const tabs = [
    { key: "dashboard" as const, label: "Dashboard", icon: BarChart3 },
    { key: "compare" as const, label: "Compare", icon: Truck },
    { key: "risks" as const, label: "Risk Assessment", icon: AlertTriangle },
    { key: "recommendations" as const, label: "Recommendations", icon: Lightbulb },
  ];

  useEffect(() => {
    apiClient
      .get<{ data: { items: SupplierData[] } }>("/api/v1/suppliers", { page: "1", page_size: "50" })
      .then((r) => setSuppliers(r.data?.items || []))
      .catch(() => {});
  }, []);

  const fetchDashboard = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: Dashboard }>(
        `/api/v1/suppliers/${selectedId}/dashboard`
      );
      setDashboard(r.data || null);
    } catch {}
    setLoading(false);
  };

  const fetchComparison = async () => {
    if (compareIds.length < 2) return;
    setLoading(true);
    try {
      const r = await apiClient.post<{ data: Comparison }>("/api/v1/suppliers/compare", {
        supplier_ids: compareIds,
      });
      setComparison(r.data || null);
    } catch {}
    setLoading(false);
  };

  const fetchRisks = async () => {
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: Risk[] }>("/api/v1/suppliers/risks");
      setRisks(r.data || []);
    } catch {}
    setLoading(false);
  };

  const fetchRecommendations = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: Recommendation }>(
        `/api/v1/suppliers/${selectedId}/recommendations`
      );
      setRecommendations(r.data || null);
    } catch {}
    setLoading(false);
  };

  const analyzeQuotation = async () => {
    if (!selectedId) return;
    setLoading(true);
    try {
      const r = await apiClient.post<{ data: any }>(
        `/api/v1/suppliers/${selectedId}/quotation-analysis`,
        quotationForm
      );
      setQuotationResult(r.data);
    } catch {
      setQuotationResult({ error: "Analysis failed" });
    }
    setLoading(false);
  };

  const riskColor = (level: string) =>
    ({
      low: "text-green-500 bg-green-50 dark:bg-green-950/20",
      medium: "text-yellow-500 bg-yellow-50 dark:bg-yellow-950/20",
      high: "text-orange-500 bg-orange-50 dark:bg-orange-950/20",
      critical: "text-red-500 bg-red-50 dark:bg-red-950/20",
    })[level] || "";

  const filteredSuppliers = suppliers.filter(
    (s) => search === "" || s.legal_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-primary/10 p-2">
            <Truck className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Supplier Intelligence</h1>
            <p className="text-xs text-muted-foreground">AI-powered procurement decision support</p>
          </div>
        </div>
      </div>

      {/* Supplier Selector */}
      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            className="w-full rounded-md border pl-10 pr-4 py-2 text-sm"
            placeholder="Search suppliers..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <select
          className="rounded-md border px-3 py-2 text-sm"
          value={selectedId}
          onChange={async (e) => {
            setSelectedId(e.target.value);
            if (e.target.value) {
              fetchDashboard();
              fetchRecommendations();
            }
          }}
        >
          <option value="">Select a supplier</option>
          {filteredSuppliers.map((s) => (
            <option key={s.id} value={s.id}>
              {s.legal_name} ({s.rating?.toFixed(1)}★)
            </option>
          ))}
        </select>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b pb-2">
        {tabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium transition-colors ${tab === t.key ? "bg-primary text-primary-foreground" : "hover:bg-muted"}`}
          >
            <t.icon className="h-4 w-4" />
            {t.label}
          </button>
        ))}
      </div>

      {loading && (
        <div className="flex items-center gap-2 py-4">
          <RefreshCw className="h-4 w-4 animate-spin" />
          <span className="text-sm text-muted-foreground">Loading...</span>
        </div>
      )}

      {/* Dashboard Tab */}
      {tab === "dashboard" && dashboard && (
        <div className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardContent className="py-4">
                <p className="text-xs text-muted-foreground">Rating</p>
                <p className="text-2xl font-bold flex items-center gap-1">
                  <Star className="h-5 w-5 fill-orange-400 text-orange-400" />
                  {dashboard.supplier.rating?.toFixed(1)}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs text-muted-foreground">Risk Level</p>
                <p
                  className={`text-xl font-bold rounded-full inline-block px-3 py-1 mt-1 ${riskColor(dashboard.risk_level)}`}
                >
                  {dashboard.risk_level}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs text-muted-foreground">Open POs</p>
                <p className="text-2xl font-bold">{dashboard.procurement.open_pos}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs text-muted-foreground">Total Spend</p>
                <p className="text-2xl font-bold">
                  ₹{((dashboard.procurement.total_spend || 0) / 100000).toFixed(1)}L
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {[
                  ["On-Time Delivery", `${dashboard.performance.on_time_delivery_pct || 0}%`],
                  ["Quality Rating", `${dashboard.performance.quality_rating || 0}/5`],
                  ["Delivery Rating", `${dashboard.performance.delivery_rating || 0}/5`],
                  ["Lead Time", `${dashboard.performance.avg_lead_time_days || "--"} days`],
                  ["Late Deliveries", dashboard.performance.late_deliveries_count || 0],
                  ["Rejected Goods", dashboard.performance.rejected_goods_count || 0],
                ].map(([l, v]) => (
                  <div key={l as string} className="flex justify-between text-sm">
                    <span className="text-muted-foreground">{l}</span>
                    <span className="font-medium">{v}</span>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Recent Purchase Orders</CardTitle>
              </CardHeader>
              <CardContent>
                {dashboard.procurement.recent_pos?.length > 0 ? (
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="border-b">
                        <th className="py-1 text-left">PO</th>
                        <th className="py-1 text-left">Status</th>
                        <th className="py-1 text-right">Amount</th>
                      </tr>
                    </thead>
                    <tbody>
                      {dashboard.procurement.recent_pos.map((po: any, i: number) => (
                        <tr key={i} className="border-b">
                          <td className="py-1 font-mono">{po.po_number}</td>
                          <td className="py-1">{po.status}</td>
                          <td className="py-1 text-right">₹{po.total?.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-sm text-muted-foreground">No purchase orders</p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Quotation Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Quotation Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid gap-2 md:grid-cols-3">
                {quotationForm.items.map((item, i) => (
                  <div key={i} className="flex gap-1">
                    <input
                      className="flex-1 rounded border px-2 py-1 text-xs"
                      placeholder="Product"
                      value={item.product_name}
                      onChange={(e) => {
                        const items = [...quotationForm.items];
                        items[i].product_name = e.target.value;
                        setQuotationForm({ items });
                      }}
                    />
                    <input
                      type="number"
                      className="w-16 rounded border px-2 py-1 text-xs"
                      placeholder="Qty"
                      value={item.quantity}
                      onChange={(e) => {
                        const items = [...quotationForm.items];
                        items[i].quantity = parseInt(e.target.value) || 1;
                        setQuotationForm({ items });
                      }}
                    />
                    <input
                      type="number"
                      step="0.01"
                      className="w-20 rounded border px-2 py-1 text-xs"
                      placeholder="Price"
                      value={item.unit_price}
                      onChange={(e) => {
                        const items = [...quotationForm.items];
                        items[i].unit_price = parseFloat(e.target.value) || 0;
                        setQuotationForm({ items });
                      }}
                    />
                  </div>
                ))}
              </div>
              <Button
                size="sm"
                variant="outline"
                onClick={() =>
                  setQuotationForm({
                    items: [
                      ...quotationForm.items,
                      { product_name: "", quantity: 1, unit_price: 0 },
                    ],
                  })
                }
              >
                + Add Item
              </Button>
              <div>
                <Button size="sm" onClick={analyzeQuotation} disabled={loading}>
                  <Zap className="mr-1 h-3 w-3" /> Analyze Quotation
                </Button>
              </div>
              {quotationResult && (
                <Card className="bg-muted/30 border-dashed">
                  <CardContent className="py-3">
                    <div className="grid gap-2 text-sm">
                      <div className="flex justify-between">
                        <span>Quoted Total</span>
                        <span className="font-medium">
                          ₹{quotationResult.quoted_total?.toLocaleString() || 0}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Recommendation</span>
                        <span
                          className={`font-medium ${quotationResult.recommendation?.includes("Accept") ? "text-green-500" : "text-orange-500"}`}
                        >
                          {quotationResult.recommendation || "--"}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Confidence</span>
                        <span className="font-medium">{quotationResult.confidence || 0}%</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Compare Tab */}
      {tab === "compare" && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Select Suppliers to Compare</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2 mb-4">
                {filteredSuppliers.slice(0, 20).map((s) => (
                  <button
                    key={s.id}
                    onClick={() =>
                      setCompareIds((prev) =>
                        prev.includes(s.id) ? prev.filter((id) => id !== s.id) : [...prev, s.id]
                      )
                    }
                    className={`rounded-full border px-3 py-1.5 text-xs transition-colors ${compareIds.includes(s.id) ? "bg-primary text-primary-foreground border-primary" : "hover:bg-muted"}`}
                  >
                    {s.legal_name?.slice(0, 20)} ({s.rating?.toFixed(1)}★)
                  </button>
                ))}
              </div>
              <Button onClick={fetchComparison} disabled={compareIds.length < 2}>
                Compare {compareIds.length} Suppliers
              </Button>
            </CardContent>
          </Card>

          {comparison && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">
                  Comparison Results ({comparison.count} suppliers)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b text-left">
                        <th className="py-2 px-3 font-medium">Supplier</th>
                        <th className="py-2 px-3 font-medium text-center">Rating</th>
                        <th className="py-2 px-3 font-medium text-center">Quality</th>
                        <th className="py-2 px-3 font-medium text-center">Delivery</th>
                        <th className="py-2 px-3 font-medium text-center">On-Time %</th>
                        <th className="py-2 px-3 font-medium text-center">Overall</th>
                      </tr>
                    </thead>
                    <tbody>
                      {comparison.suppliers.map((s, i) => (
                        <tr
                          key={i}
                          className={`border-b ${i === 0 ? "bg-green-50 dark:bg-green-950/10" : ""}`}
                        >
                          <td className="py-2 px-3">
                            {s.name}
                            {i === 0 && (
                              <span className="ml-2 text-xs text-green-500">← Recommended</span>
                            )}
                          </td>
                          <td className="py-2 px-3 text-center">{s.rating?.toFixed(1)}</td>
                          <td className="py-2 px-3 text-center">{s.quality || "--"}</td>
                          <td className="py-2 px-3 text-center">{s.delivery || "--"}</td>
                          <td className="py-2 px-3 text-center">{s.on_time_pct || 0}%</td>
                          <td className="py-2 px-3 text-center font-bold">
                            {s.overall_score?.toFixed(1) || "--"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="mt-4 p-3 rounded-md bg-primary/5 text-sm">
                  {comparison.recommendation}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Risks Tab */}
      {tab === "risks" && (
        <div className="space-y-4">
          <Button onClick={fetchRisks} variant="outline">
            <AlertTriangle className="mr-2 h-4 w-4" /> Scan for Risks
          </Button>
          <div className="grid gap-3">
            {risks.map((r, i) => (
              <Card
                key={i}
                className={
                  r.severity === "high"
                    ? "border-red-500/30"
                    : r.severity === "medium"
                      ? "border-orange-500/30"
                      : ""
                }
              >
                <CardContent className="py-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-medium ${riskColor(r.severity)}`}
                        >
                          {r.severity}
                        </span>
                        <span className="text-sm font-medium">{r.type}</span>
                      </div>
                      <p className="text-sm">{r.description}</p>
                      {r.mitigation && (
                        <p className="text-xs text-muted-foreground mt-1">
                          Mitigation: {r.mitigation}
                        </p>
                      )}
                    </div>
                    {r.severity === "high" ? (
                      <AlertTriangle className="h-5 w-5 text-red-500" />
                    ) : r.severity === "medium" ? (
                      <AlertTriangle className="h-5 w-5 text-orange-500" />
                    ) : (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
            {risks.length === 0 && (
              <div className="py-8 text-center text-muted-foreground">
                No risks to display. Scan for risks above.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Recommendations Tab */}
      {tab === "recommendations" && (
        <div className="space-y-4">
          <Button onClick={fetchRecommendations} variant="outline" disabled={!selectedId}>
            <Lightbulb className="mr-2 h-4 w-4" /> Get Recommendations
          </Button>
          {recommendations && (
            <div className="space-y-3">
              <Card>
                <CardContent className="py-4">
                  <h3 className="font-semibold">{recommendations.supplier_name}</h3>
                </CardContent>
              </Card>
              {recommendations.recommendations.map((r, i) => (
                <Card key={i} className="hover:border-primary/30 transition-colors">
                  <CardContent className="py-4">
                    <div className="flex items-start gap-3">
                      <Lightbulb className="h-5 w-5 text-primary mt-0.5" />
                      <div>
                        <p className="font-medium text-sm">{r.action}</p>
                        <p className="text-sm text-muted-foreground">{r.reason}</p>
                        {r.savings_estimate && (
                          <p className="text-xs text-green-500 mt-1">{r.savings_estimate}</p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
              {recommendations.priority_actions.length > 0 && (
                <Card className="bg-primary/5 border-primary/20">
                  <CardContent className="py-3">
                    <p className="text-sm font-medium mb-2">Priority Actions</p>
                    {recommendations.priority_actions.map((a, i) => (
                      <div key={i} className="flex items-center gap-2 text-sm">
                        <CheckCircle className="h-4 w-4 text-primary" />
                        {a}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}
            </div>
          )}
          {!selectedId && (
            <div className="py-8 text-center text-muted-foreground">
              Select a supplier above to get recommendations.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
