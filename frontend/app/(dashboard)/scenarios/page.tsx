"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Zap, Play, BarChart3, FileText, Lightbulb, ArrowRight, TrendingUp, TrendingDown, AlertTriangle, Package, DollarSign, RefreshCw, Plus, Eye } from "lucide-react";

interface Baseline { snapshot_at: string; products: number; warehouses: number; suppliers: number; inventory_value: number; available_quantity: number; procurement_spend: number; open_pos: number; low_stock_items: number; out_of_stock_items: number; supplier_avg_rating: number; }
interface Template { name: string; category: string; params: any; description: string; }
interface Simulation { id: string; name: string; params: any; baseline: Baseline; impact: any; summary: string; run_at: string; }
interface Comparison { scenarios: Simulation[]; count: number; baseline?: Baseline; }
interface AiAdvice { scenario_name: string; ai_advice: string; confidence: number; }

export default function ScenarioLab() {
  const [tab, setTab] = useState<"templates" | "builder" | "results" | "compare" | "advice">("templates");
  const [baseline, setBaseline] = useState<Baseline | null>(null);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [comparison, setComparison] = useState<Comparison | null>(null);
  const [aiAdvice, setAiAdvice] = useState<AiAdvice | null>(null);
  const [loading, setLoading] = useState(false);
  const [customParams, setCustomParams] = useState({ name: "", demand_pct: 0, cost_increase_pct: 0, lead_time_days: 0, inventory_shortage_pct: 0, currency_change_pct: 0 });

  const tabs = [
    { key: "templates" as const, label: "Templates", icon: FileText },
    { key: "builder" as const, label: "Custom", icon: Plus },
    { key: "results" as const, label: "Results", icon: Eye },
    { key: "compare" as const, label: "Compare", icon: BarChart3 },
    { key: "advice" as const, label: "AI Advisor", icon: Lightbulb },
  ];

  useEffect(() => {
    apiClient.get<{ data: Baseline }>("/api/v1/scenarios/baseline").then(r => setBaseline(r.data)).catch(() => {});
    apiClient.get<{ data: Template[] }>("/api/v1/scenarios/templates").then(r => setTemplates(r.data || [])).catch(() => {});
  }, []);

  const runTemplate = async (t: Template) => {
    setLoading(true);
    try {
      const r = await apiClient.post<{ data: Simulation }>("/api/v1/scenarios/run", { name: t.name, params: t.params });
      setSimulations(prev => [...prev, r.data!]);
      setTab("results");
    } catch {}
    setLoading(false);
  };

  const runCustom = async () => {
    if (!customParams.name.trim()) return;
    setLoading(true);
    try {
      const params: any = {};
      if (customParams.demand_pct) params.demand_pct = customParams.demand_pct;
      if (customParams.cost_increase_pct) params.cost_increase_pct = customParams.cost_increase_pct;
      if (customParams.lead_time_days) params.lead_time_days = customParams.lead_time_days;
      if (customParams.inventory_shortage_pct) params.inventory_shortage_pct = customParams.inventory_shortage_pct;
      if (customParams.currency_change_pct) params.currency_change_pct = customParams.currency_change_pct;
      const r = await apiClient.post<{ data: Simulation }>("/api/v1/scenarios/run", { name: customParams.name, params });
      setSimulations(prev => [...prev, r.data!]);
      setCustomParams({ name: "", demand_pct: 0, cost_increase_pct: 0, lead_time_days: 0, inventory_shortage_pct: 0, currency_change_pct: 0 });
      setTab("results");
    } catch {}
    setLoading(false);
  };

  const runComparison = async () => {
    if (simulations.length < 2) return; setLoading(true);
    try {
      const ids = simulations.map(s => s.id);
      const r = await apiClient.post<{ data: Comparison }>("/api/v1/scenarios/compare", { scenario_ids: ids });
      setComparison(r.data!); setTab("compare");
    } catch {}
    setLoading(false);
  };

  const getAdvice = async (id: string) => {
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: AiAdvice }>(`/api/v1/scenarios/${id}/advice`);
      setAiAdvice(r.data!); setTab("advice");
    } catch {}
    setLoading(false);
  };

  const impactColor = (val: number) => val > 0 ? "text-green-500" : val < 0 ? "text-red-500" : "text-muted-foreground";
  const impactIcon = (val: number) => val > 0 ? <TrendingUp className="h-4 w-4 text-green-500" /> : <TrendingDown className="h-4 w-4 text-red-500" />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-primary/10 p-2"><Zap className="h-5 w-5 text-primary" /></div>
          <div><h1 className="text-xl font-bold">Business Scenario Lab</h1><p className="text-xs text-muted-foreground">Digital Twin — safely simulate business decisions before applying them</p></div>
        </div>
      </div>

      {/* Baseline Cards */}
      {baseline && (
        <div className="grid gap-4 md:grid-cols-5">
          <Card><CardContent className="py-3"><p className="text-xs text-muted-foreground">Inventory Value</p><p className="text-lg font-bold">₹{(baseline.inventory_value / 100000).toFixed(1)}L</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs text-muted-foreground">Available Qty</p><p className="text-lg font-bold">{baseline.available_quantity.toLocaleString()}</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs text-muted-foreground">Procurement Spend</p><p className="text-lg font-bold">₹{(baseline.procurement_spend / 100000).toFixed(1)}L</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs text-muted-foreground">Low Stock</p><p className="text-lg font-bold text-orange-500">{baseline.low_stock_items}</p></CardContent></Card>
          <Card><CardContent className="py-3"><p className="text-xs text-muted-foreground">Out of Stock</p><p className="text-lg font-bold text-red-500">{baseline.out_of_stock_items}</p></CardContent></Card>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 border-b pb-2">
        {tabs.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)} className={`flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium transition-colors ${tab === t.key ? "bg-primary text-primary-foreground" : "hover:bg-muted"}`}><t.icon className="h-4 w-4" />{t.label}</button>
        ))}
      </div>

      {loading && <div className="flex items-center gap-2 py-4"><RefreshCw className="h-4 w-4 animate-spin" /><span className="text-sm text-muted-foreground">Running simulation...</span></div>}

      {/* Templates Tab */}
      {tab === "templates" && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {templates.map((t, i) => (
            <Card key={i} className="hover:border-primary/50 transition-colors cursor-pointer" onClick={() => runTemplate(t)}>
              <CardContent className="py-6">
                <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary mb-2 inline-block">{t.category}</span>
                <h3 className="font-semibold text-sm mt-2">{t.name}</h3>
                <p className="text-xs text-muted-foreground mt-1">{t.description}</p>
                <div className="mt-3 flex flex-wrap gap-1">
                  {Object.entries(t.params).map(([k, v]) => <span key={k} className="rounded-full bg-muted px-2 py-0.5 text-xs">{k}: {String(v)}</span>)}
                </div>
                <p className="text-xs text-primary mt-3 flex items-center gap-1"><Play className="h-3 w-3" /> Click to run simulation</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Custom Builder Tab */}
      {tab === "builder" && (
        <Card>
          <CardHeader><CardTitle className="text-base">Custom Scenario Builder</CardTitle></CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div><label className="text-sm font-medium">Scenario Name</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.name} onChange={e => setCustomParams({...customParams, name: e.target.value})} placeholder="My Scenario" /></div>
              <div><label className="text-sm font-medium">Demand Change (%)</label><input type="number" className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.demand_pct} onChange={e => setCustomParams({...customParams, demand_pct: parseInt(e.target.value) || 0})} /></div>
              <div><label className="text-sm font-medium">Cost Increase (%)</label><input type="number" className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.cost_increase_pct} onChange={e => setCustomParams({...customParams, cost_increase_pct: parseInt(e.target.value) || 0})} /></div>
              <div><label className="text-sm font-medium">Lead Time Delay (days)</label><input type="number" className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.lead_time_days} onChange={e => setCustomParams({...customParams, lead_time_days: parseInt(e.target.value) || 0})} /></div>
              <div><label className="text-sm font-medium">Inventory Shortage (%)</label><input type="number" className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.inventory_shortage_pct} onChange={e => setCustomParams({...customParams, inventory_shortage_pct: parseInt(e.target.value) || 0})} /></div>
              <div><label className="text-sm font-medium">Currency Change (%)</label><input type="number" className="w-full rounded-md border px-3 py-2 text-sm" value={customParams.currency_change_pct} onChange={e => setCustomParams({...customParams, currency_change_pct: parseInt(e.target.value) || 0})} /></div>
            </div>
            <Button className="mt-4" onClick={runCustom}><Play className="mr-2 h-4 w-4" /> Run Custom Scenario</Button>
          </CardContent>
        </Card>
      )}

      {/* Results Tab */}
      {tab === "results" && (
        <div className="space-y-4">
          {simulations.length === 0 ? <div className="py-16 text-center text-muted-foreground">No simulations yet. Run a template or create a custom scenario.</div> :
            simulations.map((s, i) => (
              <Card key={i}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div><CardTitle className="text-base">{s.name}</CardTitle><p className="text-xs text-muted-foreground">{new Date(s.run_at).toLocaleString()}</p></div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" onClick={() => getAdvice(s.id)}><Lightbulb className="mr-1 h-3 w-3" /> AI Advice</Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm mb-3">{s.summary}</p>
                  <div className="grid gap-2 md:grid-cols-3">
                    {Object.entries(s.impact).map(([key, val]: [string, any]) => (
                      <Card key={key} className="bg-muted/30">
                        <CardContent className="py-3">
                          <p className="text-xs text-muted-foreground capitalize">{key.replace(/_/g, " ")}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-sm font-medium">{val.baseline}</span>
                            <ArrowRight className="h-3 w-3 text-muted-foreground" />
                            <span className="text-sm font-bold">{val.simulated}</span>
                            {val.change_pct !== undefined && (
                              <span className={`text-xs ml-1 ${impactColor(val.change_pct)}`}>
                                {val.change_pct > 0 ? "+" : ""}{val.change_pct}%
                              </span>
                            )}
                          </div>
                          {val.unit && <span className="text-xs text-muted-foreground">{val.unit}</span>}
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          {simulations.length >= 2 && <Button variant="outline" onClick={runComparison}><BarChart3 className="mr-2 h-4 w-4" /> Compare All Scenarios</Button>}
        </div>
      )}

      {/* Compare Tab */}
      {tab === "compare" && comparison && (
        <div className="space-y-4">
          <Card>
            <CardHeader><CardTitle className="text-sm">Scenario Comparison ({comparison.count} scenarios)</CardTitle></CardHeader>
            <CardContent>
              {comparison.scenarios.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead><tr className="border-b text-left"><th className="py-2 px-3 font-medium">Scenario</th><th className="py-2 px-3 font-medium">Params</th><th className="py-2 px-3 font-medium">Key Impact</th></tr></thead>
                    <tbody>{comparison.scenarios.map((s, i) => (
                      <tr key={i} className="border-b"><td className="py-2 px-3 font-medium">{s.name}</td>
                        <td className="py-2 px-3"><div className="flex flex-wrap gap-1">{Object.entries(s.params).map(([k, v]) => <span key={k} className="rounded-full bg-muted px-1.5 py-0.5 text-xs">{k}: {String(v)}</span>)}</div></td>
                        <td className="py-2 px-3">{s.impact && Object.keys(s.impact).length > 0 ? Object.keys(s.impact).slice(0, 3).join(", ") : "No impact"}</td>
                      </tr>
                    ))}</tbody>
                  </table>
                </div>
              ) : <p className="text-sm text-muted-foreground">No scenarios to compare</p>}
            </CardContent>
          </Card>
          {comparison.baseline && <div className="text-xs text-muted-foreground text-center">Baseline captured at: {new Date(comparison.baseline.snapshot_at).toLocaleString()}</div>}
        </div>
      )}

      {/* AI Advisor Tab */}
      {tab === "advice" && aiAdvice && (
        <Card className="border-primary/20">
          <CardHeader><CardTitle className="text-base flex items-center gap-2"><Lightbulb className="h-4 w-4 text-primary" /> AI Scenario Advisor — {aiAdvice.scenario_name}</CardTitle></CardHeader>
          <CardContent>
            <div className="prose prose-sm dark:prose-invert max-w-none">
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{aiAdvice.ai_advice}</p>
            </div>
            <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
              <span className="rounded-full bg-muted px-2 py-1">Confidence: {aiAdvice.confidence}%</span>
              <span className="rounded-full bg-muted px-2 py-1">Generated: {new Date().toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
