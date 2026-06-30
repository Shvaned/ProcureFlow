"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Sparkles, Send, Database, Clock, BarChart3, Table2, Download, ChevronDown, ChevronUp, CheckCircle, XCircle, AlertTriangle, RefreshCw } from "lucide-react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4", "#f97316"];

interface QueryResult {
  question: string; sql_generated: string; sql_valid: boolean; validation_errors: string[];
  tables_used: string[]; columns: string[]; rows: Record<string, any>[];
  row_count: number; execution_ms: number; chart_type: string;
  ai_explanation: string; total_latency_ms: number; suggested_followups: string[];
}

const SUPPORTED = [
  "Show inventory value by warehouse",
  "What products are low in stock?",
  "Show top suppliers by rating",
  "Which purchase orders are pending?",
  "Compare spend by PO status",
  "Show products by category",
];

export default function AnalyticsCopilot() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<QueryResult[]>([]);
  const [chartView, setChartView] = useState<Record<number, string>>({});
  const [expandedSQL, setExpandedSQL] = useState<Record<number, boolean>>({});
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [results, loading]);

  const ask = async (question: string) => {
    if (!question.trim() || loading) return;
    setInput(""); setLoading(true);
    try {
      const r = await apiClient.post<{ data: QueryResult }>("/api/v1/ai/analytics/query", { question });
      setResults(prev => [...prev, r.data!]);
    } catch {
      setResults(prev => [...prev, { question, sql_generated: "-- Query failed", sql_valid: false, validation_errors: ["Request failed"], tables_used: [], columns: [], rows: [], row_count: 0, execution_ms: 0, chart_type: "table", ai_explanation: "", total_latency_ms: 0, suggested_followups: [] }]);
    }
    setLoading(false);
  };

  const exportCSV = (r: QueryResult) => {
    if (!r.rows.length) return;
    const csv = [r.columns.join(","), ...r.rows.map(row => r.columns.map(c => JSON.stringify(row[c] ?? "")).join(","))].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "analytics-export.csv"; a.click();
  };

  const renderChart = (r: QueryResult, idx: number) => {
    const ct = chartView[idx] || r.chart_type;
    const data = r.rows.map((row, i) => ({ ...row, _key: i }));
    if (!r.columns.length || !r.rows.length) return null;
    const [labelCol, ...numCols] = r.columns;
    const valCol = numCols[0] || labelCol;

    if (ct === "bar" || ct === "column") return <ResponsiveContainer width="100%" height={280}><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey={labelCol} style={{ fontSize: 11 }} /><YAxis style={{ fontSize: 11 }} /><Tooltip /><Bar dataKey={valCol} fill="#3b82f6" radius={[4,4,0,0]} /></BarChart></ResponsiveContainer>;
    if (ct === "pie") return <ResponsiveContainer width="100%" height={280}><PieChart><Pie data={data} cx="50%" cy="50%" outerRadius={100} dataKey={valCol} nameKey={labelCol} label={({ name, value }) => `${name?.toString().slice(0,10)}: ${value}`}><Tooltip />{data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}</Pie></PieChart></ResponsiveContainer>;
    if (ct === "line") return <ResponsiveContainer width="100%" height={280}><LineChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey={labelCol} style={{ fontSize: 11 }} /><YAxis style={{ fontSize: 11 }} /><Tooltip /><Line type="monotone" dataKey={valCol} stroke="#3b82f6" strokeWidth={2} /></LineChart></ResponsiveContainer>;
    return null;
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] flex-col">
      <div className="mb-4 flex items-center gap-3">
        <div className="rounded-lg bg-primary/10 p-2"><BarChart3 className="h-5 w-5 text-primary" /></div>
        <div><h1 className="text-xl font-bold">Analytics Copilot</h1><p className="text-xs text-muted-foreground">Natural language → SQL → Charts. Ask business questions, get answers.</p></div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2 mb-4">
        {results.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="rounded-full bg-primary/10 p-6 mb-6"><BarChart3 className="h-12 w-12 text-primary" /></div>
            <h2 className="text-xl font-bold mb-2">NL → SQL Analytics</h2>
            <p className="text-muted-foreground max-w-md mb-6">Ask questions in plain English. I generate safe SQL, execute it against your ERP, and visualize the results.</p>
            <div className="flex flex-wrap justify-center gap-2 max-w-xl">
              {SUPPORTED.map((q, i) => (
                <button key={i} onClick={() => ask(q)} className="rounded-full border px-4 py-2 text-sm hover:bg-muted hover:border-primary/50 transition-colors">{q}</button>
              ))}
            </div>
          </div>
        )}

        {results.map((r, idx) => (
          <div key={idx} className="space-y-3">
            {/* Question */}
            <div className="flex justify-end"><div className="bg-primary text-primary-foreground rounded-2xl rounded-br-md px-4 py-3 max-w-[80%]"><p className="text-sm">{r.question}</p></div></div>

            {/* Response Card */}
            <Card className={r.sql_valid ? "border-green-500/20" : "border-red-500/20"}>
              <CardContent className="py-4 space-y-3">
                {/* Meta bar */}
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <span className={`flex items-center gap-1 rounded-full px-2 py-1 ${r.sql_valid ? "bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400" : "bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400"}`}>
                    {r.sql_valid ? <CheckCircle className="h-3 w-3" /> : <XCircle className="h-3 w-3" />}
                    {r.sql_valid ? "Valid SQL" : "Validation failed"}
                  </span>
                  <span className="flex items-center gap-1 rounded-full bg-muted px-2 py-1"><Clock className="h-3 w-3" />{r.execution_ms}ms</span>
                  <span className="flex items-center gap-1 rounded-full bg-muted px-2 py-1"><Database className="h-3 w-3" />{r.row_count} rows</span>
                  <span className="flex items-center gap-1 rounded-full bg-muted px-2 py-1"><Clock className="h-3 w-3" />{r.total_latency_ms}ms total</span>
                  {r.tables_used.map(t => <span key={t} className="rounded-full bg-primary/10 px-2 py-1 text-primary">{t}</span>)}
                </div>

                {/* SQL Display */}
                <div>
                  <button onClick={() => setExpandedSQL({ ...expandedSQL, [idx]: !expandedSQL[idx] })} className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground mb-1">
                    <Database className="h-3 w-3" />
                    Generated SQL {expandedSQL[idx] ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                  </button>
                  {expandedSQL[idx] && <pre className="rounded-md bg-muted p-3 text-xs font-mono overflow-x-auto">{r.sql_generated}</pre>}
                </div>

                {/* Validation Errors */}
                {r.validation_errors.length > 0 && (
                  <div className="rounded-md bg-red-50 dark:bg-red-950/20 p-3 text-xs text-red-700 dark:text-red-400">
                    {r.validation_errors.map((e, i) => <div key={i} className="flex items-center gap-1"><AlertTriangle className="h-3 w-3" />{e}</div>)}
                  </div>
                )}

                {/* Chart */}
                {r.rows.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs font-medium">Visualization</span>
                      <div className="flex gap-1">
                        {["bar", "pie", "line", "table"].map(ct => (
                          <button key={ct} onClick={() => setChartView({ ...chartView, [idx]: ct })} className={`rounded px-2 py-0.5 text-xs ${(chartView[idx] || r.chart_type) === ct ? "bg-primary text-primary-foreground" : "bg-muted hover:bg-muted/80"}`}>{ct}</button>
                        ))}
                      </div>
                      <Button variant="ghost" size="sm" className="ml-auto" onClick={() => exportCSV(r)}><Download className="mr-1 h-3 w-3" /> CSV</Button>
                    </div>
                    {(chartView[idx] || r.chart_type) === "table" ? (
                      <div className="overflow-x-auto rounded-md border">
                        <table className="w-full text-sm"><thead><tr>{r.columns.map(c => <th key={c} className="bg-muted px-3 py-2 text-left text-xs font-medium">{c}</th>)}</tr></thead>
                          <tbody>{r.rows.slice(0, 50).map((row, i) => <tr key={i} className="border-t hover:bg-muted/30">{r.columns.map(c => <td key={c} className="px-3 py-1.5 text-xs">{row[c]?.toString()?.slice(0, 40)}</td>)}</tr>)}</tbody></table>
                        {r.row_count > 50 && <div className="px-3 py-2 text-xs text-muted-foreground border-t">Showing 50 of {r.row_count} rows</div>}
                      </div>
                    ) : renderChart(r, idx)}
                  </div>
                )}

                {/* AI Explanation */}
                {r.ai_explanation && (
                  <div className="rounded-md bg-muted/50 p-3 text-sm leading-relaxed">
                    <div className="flex items-center gap-1 text-xs text-muted-foreground mb-1"><Sparkles className="h-3 w-3" /> AI Insight</div>
                    {r.ai_explanation}
                  </div>
                )}

                {/* Follow-ups */}
                {r.suggested_followups?.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {r.suggested_followups.map((q, i) => (
                      <button key={i} onClick={() => ask(q)} className="rounded-full border px-3 py-1 text-xs hover:bg-muted hover:border-primary/50 transition-colors">{q}</button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 py-4">
            <RefreshCw className="h-4 w-4 animate-spin text-muted-foreground" />
            <span className="text-sm text-muted-foreground">Generating SQL and analyzing data...</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div className="border-t pt-4">
        <div className="flex gap-2">
          <input className="flex-1 rounded-full border px-5 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Ask: Show inventory value by warehouse..." value={input}
            onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === "Enter" && ask(input)} disabled={loading} />
          <Button size="icon" className="rounded-full h-12 w-12" onClick={() => ask(input)} disabled={loading || !input.trim()}>
            {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {SUPPORTED.slice(0, 4).map((q, i) => (
            <button key={i} onClick={() => ask(q)} className="rounded-full border px-3 py-1 text-xs text-muted-foreground hover:bg-muted hover:text-foreground transition-colors">{q}</button>
          ))}
        </div>
      </div>
    </div>
  );
}
