"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Zap, Plus, Play, Pause, BarChart3, History, FileText, Trash2, Sparkles, CheckCircle, XCircle, Clock, RefreshCw, ArrowRight, Layers } from "lucide-react";

interface Workflow { id: string; name: string; description: string; status: string; version: number; trigger_config: any; flow_definition: any; created_at: string; }
interface Template { name: string; trigger: string; actions: string[]; description: string; }
interface Execution { id: string; workflow_id: string; status: string; started_at: string | null; completed_at: string | null; duration_ms: number; retry_count: number; error_message: string | null; }
interface Analytics { total_executions: number; succeeded: number; failed: number; success_rate: number; avg_duration_ms: number; active_workflows: number; }

export default function AutomationStudio() {
  const [tab, setTab] = useState<"workflows" | "templates" | "history" | "analytics" | "builder">("workflows");
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [aiInput, setAiInput] = useState("");
  const [aiResult, setAiResult] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [form, setForm] = useState({ name: "", description: "", trigger_config: "" });

  const tabs = [
    { key: "workflows" as const, label: "Workflows", icon: Layers },
    { key: "templates" as const, label: "Templates", icon: FileText },
    { key: "history" as const, label: "History", icon: History },
    { key: "analytics" as const, label: "Analytics", icon: BarChart3 },
    { key: "builder" as const, label: "AI Builder", icon: Sparkles },
  ];

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [wf, tpl, exec, an] = await Promise.all([
        apiClient.get<{ data: Workflow[] }>("/api/v1/workflows"),
        apiClient.get<{ data: Template[] }>("/api/v1/workflows/templates"),
        apiClient.get<{ data: Execution[] }>("/api/v1/workflows/executions"),
        apiClient.get<{ data: Analytics }>("/api/v1/workflows/analytics"),
      ]);
      setWorkflows(wf.data || []); setTemplates(tpl.data || []);
      setExecutions(exec.data || []); setAnalytics(an.data || null);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { fetchAll(); }, []);

  const createFromTemplate = async (name: string) => {
    await apiClient.post("/api/v1/workflows/templates/use", { template_name: name });
    fetchAll(); setTab("workflows");
  };

  const handleCreate = async () => {
    if (!form.name.trim()) return;
    await apiClient.post("/api/v1/workflows", form);
    setForm({ name: "", description: "", trigger_config: "" }); fetchAll();
  };

  const handlePublish = async (id: string) => { await apiClient.post(`/api/v1/workflows/${id}/publish`); fetchAll(); };
  const handleExecute = async (id: string) => { await apiClient.post(`/api/v1/workflows/${id}/execute`); fetchAll(); };
  const handleDelete = async (id: string) => { await apiClient.delete(`/api/v1/workflows/${id}`); fetchAll(); };

  const handleAiGenerate = async () => {
    if (!aiInput.trim()) return;
    setAiLoading(true);
    try {
      const r = await apiClient.post<{ data: { workflow_description: string } }>("/api/v1/ai/automation/workflows/generate", { description: aiInput });
      setAiResult(r.data?.workflow_description || "No response");
    } catch { setAiResult("AI generation failed"); }
    setAiLoading(false);
  };

  const statusBadge = (s: string) => {
    const colors: Record<string, string> = { draft: "bg-gray-100 text-gray-700", published: "bg-green-100 text-green-700", archived: "bg-muted text-muted-foreground" };
    return <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${colors[s] || ""}`}>{s}</span>;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-primary/10 p-2"><Zap className="h-5 w-5 text-primary" /></div>
          <div><h1 className="text-xl font-bold">Automation Studio</h1><p className="text-xs text-muted-foreground">Visual workflow automation platform</p></div>
        </div>
        <Button variant="outline" size="sm" onClick={fetchAll}><RefreshCw className="mr-2 h-3 w-3" /> Refresh</Button>
      </div>

      {/* Tab Bar */}
      <div className="flex gap-1 border-b pb-2">
        {tabs.map(t => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={`flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium transition-colors ${tab === t.key ? "bg-primary text-primary-foreground" : "hover:bg-muted"}`}>
            <t.icon className="h-4 w-4" />{t.label}
          </button>
        ))}
      </div>

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading...</div> : (
        <>
          {/* Workflows Tab */}
          {tab === "workflows" && (
            <div className="space-y-4">
              <Card>
                <CardHeader><CardTitle className="text-base">Create Workflow</CardTitle></CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <input className="flex-1 rounded-md border px-3 py-2 text-sm" placeholder="Workflow name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
                    <input className="flex-1 rounded-md border px-3 py-2 text-sm" placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
                    <input className="flex-1 rounded-md border px-3 py-2 text-sm" placeholder="Trigger (e.g., inventory_below_safety_stock)" value={form.trigger_config} onChange={e => setForm({...form, trigger_config: e.target.value})} />
                    <Button onClick={handleCreate}><Plus className="mr-1 h-4 w-4" /> Create</Button>
                  </div>
                </CardContent>
              </Card>

              {workflows.length === 0 ? (
                <div className="py-16 text-center text-muted-foreground">No workflows yet. Create one above or use a template.</div>
              ) : (
                <div className="grid gap-3">
                  {workflows.map(w => (
                    <Card key={w.id} className="hover:shadow-sm transition-shadow">
                      <CardContent className="flex items-center justify-between py-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2"><h3 className="font-semibold text-sm">{w.name}</h3>{statusBadge(w.status)}<span className="text-xs text-muted-foreground">v{w.version}</span></div>
                          {w.description && <p className="text-xs text-muted-foreground mt-1">{w.description}</p>}
                          <p className="text-xs text-muted-foreground mt-1">{new Date(w.created_at).toLocaleDateString()}</p>
                        </div>
                        <div className="flex gap-1">
                          {w.status === "draft" && <Button size="sm" variant="outline" onClick={() => handlePublish(w.id)}><Play className="mr-1 h-3 w-3" /> Publish</Button>}
                          {w.status === "published" && <Button size="sm" variant="outline" onClick={() => handleExecute(w.id)}><Zap className="mr-1 h-3 w-3" /> Execute</Button>}
                          <Button size="sm" variant="ghost" onClick={() => handleDelete(w.id)}><Trash2 className="h-3 w-3" /></Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Templates Tab */}
          {tab === "templates" && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {templates.map((t, i) => (
                <Card key={i} className="hover:border-primary/50 transition-colors cursor-pointer" onClick={() => createFromTemplate(t.name)}>
                  <CardContent className="py-6">
                    <FileText className="h-6 w-6 text-primary mb-3" />
                    <h3 className="font-semibold text-sm">{t.name}</h3>
                    <p className="text-xs text-muted-foreground mt-1">{t.description}</p>
                    <div className="mt-3 flex flex-wrap gap-1">
                      <span className="rounded-full bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 text-xs text-blue-700 dark:text-blue-400">Trigger: {t.trigger}</span>
                      {t.actions.slice(0, 2).map((a, j) => (
                        <span key={j} className="rounded-full bg-muted px-2 py-0.5 text-xs">{a}</span>
                      ))}
                      {t.actions.length > 2 && <span className="text-xs text-muted-foreground">+{t.actions.length - 2} more</span>}
                    </div>
                    <p className="text-xs text-primary mt-3 flex items-center gap-1">Click to create <ArrowRight className="h-3 w-3" /></p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* History Tab */}
          {tab === "history" && (
            <Card><CardContent className="p-0">
              {executions.length === 0 ? <div className="py-16 text-center text-muted-foreground">No executions yet</div> : (
                <table className="w-full text-sm">
                  <thead><tr className="border-b text-left"><th className="py-3 px-4 font-medium">Workflow ID</th><th className="py-3 px-4 font-medium">Status</th><th className="py-3 px-4 font-medium">Duration</th><th className="py-3 px-4 font-medium">Retries</th><th className="py-3 px-4 font-medium">Started</th></tr></thead>
                  <tbody>{executions.map(e => (
                    <tr key={e.id} className="border-b hover:bg-muted/50">
                      <td className="py-3 px-4 font-mono text-xs">{e.workflow_id.slice(0, 8)}...</td>
                      <td className="py-3 px-4">{e.status === "completed" ? <span className="flex items-center gap-1 text-green-600 text-xs"><CheckCircle className="h-3 w-3" />Completed</span> : e.status === "failed" ? <span className="flex items-center gap-1 text-red-600 text-xs"><XCircle className="h-3 w-3" />Failed</span> : <span className="text-xs">{e.status}</span>}</td>
                      <td className="py-3 px-4 text-xs">{e.duration_ms}ms</td>
                      <td className="py-3 px-4 text-xs">{e.retry_count}</td>
                      <td className="py-3 px-4 text-xs">{e.started_at ? new Date(e.started_at).toLocaleString() : "--"}</td>
                    </tr>
                  ))}</tbody>
                </table>
              )}
            </CardContent></Card>
          )}

          {/* Analytics Tab */}
          {tab === "analytics" && analytics && (
            <div className="space-y-4">
              <div className="grid gap-4 md:grid-cols-5">
                <Card><CardContent className="py-4"><p className="text-xs text-muted-foreground">Total Executions</p><p className="text-2xl font-bold">{analytics.total_executions}</p></CardContent></Card>
                <Card><CardContent className="py-4"><p className="text-xs text-muted-foreground">Success Rate</p><p className="text-2xl font-bold text-green-500">{analytics.success_rate}%</p></CardContent></Card>
                <Card><CardContent className="py-4"><p className="text-xs text-muted-foreground">Failed</p><p className="text-2xl font-bold text-red-500">{analytics.failed}</p></CardContent></Card>
                <Card><CardContent className="py-4"><p className="text-xs text-muted-foreground">Avg Duration</p><p className="text-2xl font-bold">{analytics.avg_duration_ms}ms</p></CardContent></Card>
                <Card><CardContent className="py-4"><p className="text-xs text-muted-foreground">Active Workflows</p><p className="text-2xl font-bold">{analytics.active_workflows}</p></CardContent></Card>
              </div>
            </div>
          )}

          {/* AI Builder Tab */}
          {tab === "builder" && (
            <div className="grid gap-6 lg:grid-cols-2">
              <Card>
                <CardHeader><CardTitle className="text-base flex items-center gap-2"><Sparkles className="h-4 w-4 text-primary" /> Natural Language → Workflow</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                  <textarea className="w-full rounded-md border p-4 text-sm" rows={4} placeholder="Describe your workflow... Example: When inventory falls below safety stock and supplier lead time exceeds 7 days, notify procurement and generate a draft purchase order."
                    value={aiInput} onChange={e => setAiInput(e.target.value)} />
                  <Button onClick={handleAiGenerate} disabled={aiLoading || !aiInput.trim()}>
                    {aiLoading ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                    {aiLoading ? "Generating..." : "Generate Workflow"}
                  </Button>
                  {aiResult && (
                    <Card className="bg-muted/30 border-dashed">
                      <CardContent className="py-4"><div className="text-sm leading-relaxed whitespace-pre-wrap">{aiResult}</div></CardContent>
                    </Card>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader><CardTitle className="text-base">Available Triggers &amp; Actions</CardTitle></CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm font-medium mb-2">Triggers</p>
                    <div className="flex flex-wrap gap-1">
                      {["Inventory Below Safety Stock", "Supplier Delay", "PO Created", "PO Approved", "Goods Received", "Warehouse Transfer", "Low Stock Alert", "Product Expiry", "Manual", "Scheduled"].map(t => (
                        <span key={t} className="rounded-full bg-blue-50 dark:bg-blue-950/30 px-2 py-0.5 text-xs text-blue-700 dark:text-blue-400">{t}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">Actions</p>
                    <div className="flex flex-wrap gap-1">
                      {["Create Draft PO", "Notify User", "Create Approval", "Generate Report", "AI Summary", "Supplier Comparison", "Transfer Inventory", "Create Audit Entry", "Run Analytics"].map(a => (
                        <span key={a} className="rounded-full bg-green-50 dark:bg-green-950/30 px-2 py-0.5 text-xs text-green-700 dark:text-green-400">{a}</span>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
}
