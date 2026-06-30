"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Plus, Search, ChevronLeft, ChevronRight, FileText, CheckCircle, XCircle, RefreshCw } from "lucide-react";

interface PO { id: string; po_number: string; supplier_id: string; warehouse_id: string; status: string; total_amount: number; expected_delivery_date: string | null; created_at: string; }
interface PODetail { id: string; po_number: string; status: string; total_amount: number; currency: string; items: { id: string; product_id: string; quantity: number; received_quantity: number; unit_cost: number; line_total: number; }[]; approvals: { status: string; notes: string | null; decided_at: string | null; }[]; }

export default function PurchaseOrdersPage() {
  const [pos, setPos] = useState<PO[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [detail, setDetail] = useState<PODetail | null>(null);
  const [form, setForm] = useState({ supplier_id: "", warehouse_id: "", expected_delivery_date: "", items: [{ product_id: "", quantity: 1, unit_cost: 0 }] });
  const [saving, setSaving] = useState(false);

  const fetchPOs = useCallback(async (p: number) => {
    setLoading(true); setError("");
    try {
      const r = await apiClient.get<{ data: { items: PO[] }; metadata: { pagination: { total: number } } }>(
        "/api/v1/purchase-orders", { page: String(p), page_size: "20" }
      );
      setPos(r.data?.items || []);
      setTotal(r.metadata?.pagination?.total || 0);
    } catch { setError("Failed to load purchase orders"); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchPOs(page); }, [page, fetchPOs]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    try {
      await apiClient.post("/api/v1/purchase-orders", { ...form, currency: "INR" });
      setShowCreate(false); fetchPOs(page);
    } catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  const viewDetail = async (poId: string) => {
    try {
      const r = await apiClient.get<{ data: PODetail }>(`/api/v1/purchase-orders/${poId}`);
      setDetail(r.data);
    } catch { setDetail(null); }
  };

  const approvePO = async (poId: string) => {
    try { await apiClient.post(`/api/v1/purchase-orders/${poId}/approve`, {}); fetchPOs(page); setDetail(null); }
    catch (err: any) { setError(err.message); }
  };

  const statusBadge = (s: string) => {
    const colors: Record<string, string> = { draft: "bg-gray-100 text-gray-700", approved: "bg-blue-100 text-blue-700", sent: "bg-purple-100 text-purple-700", partially_received: "bg-orange-100 text-orange-700", received: "bg-green-100 text-green-700", cancelled: "bg-red-100 text-red-700", closed: "bg-muted text-muted-foreground" };
    return <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${colors[s] || "bg-muted"}`}>{s}</span>;
  };

  const totalPages = Math.max(1, Math.ceil(total / 20));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Purchase Orders</h1><p className="text-muted-foreground">{total} POs · draft, approved, received tracking</p></div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => fetchPOs(page)} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
          <Button onClick={() => { setShowCreate(!showCreate); setDetail(null); }}><Plus className="mr-2 h-4 w-4" /> {showCreate ? "Cancel" : "New PO"}</Button>
        </div>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}

      {showCreate && (
        <Card>
          <CardHeader><CardTitle className="text-base">Create Purchase Order</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="grid gap-4 md:grid-cols-4">
              <div><label className="text-sm font-medium">Supplier ID *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.supplier_id} onChange={e => setForm({...form, supplier_id: e.target.value})} placeholder="UUID" /></div>
              <div><label className="text-sm font-medium">Warehouse ID *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.warehouse_id} onChange={e => setForm({...form, warehouse_id: e.target.value})} placeholder="UUID" /></div>
              <div><label className="text-sm font-medium">Expected Delivery</label><input type="date" className="w-full rounded-md border px-3 py-2 text-sm" value={form.expected_delivery_date} onChange={e => setForm({...form, expected_delivery_date: e.target.value})} /></div>
              <div className="flex items-end"><Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create PO"}</Button></div>
            </form>
            <div className="mt-4 space-y-2">
              <p className="text-sm font-medium">Items</p>
              {form.items.map((item, idx) => (
                <div key={idx} className="flex gap-2">
                  <input className="flex-1 rounded-md border px-3 py-1 text-sm" placeholder="Product ID" value={item.product_id} onChange={e => { const items = [...form.items]; items[idx].product_id = e.target.value; setForm({...form, items}); }} />
                  <input type="number" className="w-20 rounded-md border px-3 py-1 text-sm" placeholder="Qty" value={item.quantity} onChange={e => { const items = [...form.items]; items[idx].quantity = parseInt(e.target.value) || 1; setForm({...form, items}); }} />
                  <input type="number" step="0.01" className="w-28 rounded-md border px-3 py-1 text-sm" placeholder="Unit Cost" value={item.unit_cost} onChange={e => { const items = [...form.items]; items[idx].unit_cost = parseFloat(e.target.value) || 0; setForm({...form, items}); }} />
                  <Button variant="ghost" size="sm" onClick={() => setForm({...form, items: form.items.filter((_, i) => i !== idx)})}>×</Button>
                </div>
              ))}
              <Button variant="outline" size="sm" onClick={() => setForm({...form, items: [...form.items, { product_id: "", quantity: 1, unit_cost: 0 }]})}>+ Add Item</Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="relative"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" /><input className="w-full rounded-md border pl-10 pr-4 py-2 text-sm" placeholder="Search by PO number..." value={search} onChange={e => setSearch(e.target.value)} /></div>

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading...</div> :
       pos.length === 0 ? <div className="py-16 text-center text-muted-foreground">No purchase orders. Create your first PO above.</div> :
       <Card><CardContent className="p-0">
        <table className="w-full text-sm">
          <thead><tr className="border-b text-left"><th className="py-3 px-4 font-medium">PO Number</th><th className="py-3 px-4 font-medium">Status</th><th className="py-3 px-4 font-medium text-right">Amount</th><th className="py-3 px-4 font-medium">Delivery</th><th className="py-3 px-4 font-medium">Created</th><th className="py-3 px-4"></th></tr></thead>
          <tbody>
            {pos.filter(p => search === "" || p.po_number.toLowerCase().includes(search.toLowerCase())).map(p => (
              <tr key={p.id} className="border-b hover:bg-muted/50">
                <td className="py-3 px-4 font-mono text-xs font-medium">{p.po_number}</td>
                <td className="py-3 px-4">{statusBadge(p.status)}</td>
                <td className="py-3 px-4 text-right font-medium">₹{p.total_amount?.toLocaleString()}</td>
                <td className="py-3 px-4 text-xs">{p.expected_delivery_date ? new Date(p.expected_delivery_date).toLocaleDateString() : "--"}</td>
                <td className="py-3 px-4 text-xs text-muted-foreground">{new Date(p.created_at).toLocaleDateString()}</td>
                <td className="py-3 px-4"><Button variant="ghost" size="sm" onClick={() => viewDetail(p.id)}>View</Button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent></Card>}

      {detail && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">{detail.po_number} · {statusBadge(detail.status)} · ₹{detail.total_amount?.toLocaleString()}</CardTitle>
              <div className="flex gap-2">
                {detail.status === "draft" && <Button size="sm" onClick={() => approvePO(detail.id)}><CheckCircle className="mr-1 h-4 w-4" /> Approve</Button>}
                <Button variant="ghost" size="sm" onClick={() => setDetail(null)}><XCircle className="mr-1 h-4 w-4" /> Close</Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="py-2 font-medium">Product</th><th className="py-2 font-medium text-right">Qty</th><th className="py-2 font-medium text-right">Received</th><th className="py-2 font-medium text-right">Unit Cost</th><th className="py-2 font-medium text-right">Line Total</th></tr></thead>
              <tbody>{detail.items.map((item, i) => (
                <tr key={i} className="border-b"><td className="py-2 font-mono text-xs">{item.product_id.slice(0, 12)}...</td><td className="py-2 text-right">{item.quantity}</td><td className="py-2 text-right">{item.received_quantity}</td><td className="py-2 text-right">₹{item.unit_cost?.toLocaleString()}</td><td className="py-2 text-right font-medium">₹{item.line_total?.toLocaleString()}</td></tr>
              ))}</tbody>
            </table>
            {detail.approvals?.length > 0 && <div className="mt-4"><p className="text-sm font-medium mb-2">Approval History</p>{detail.approvals.map((a, i) => <div key={i} className="text-xs text-muted-foreground">{a.status} · {a.notes || "No notes"} · {a.decided_at ? new Date(a.decided_at).toLocaleString() : "Pending"}</div>)}</div>}
          </CardContent>
        </Card>
      )}

      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(page - 1)}><ChevronLeft className="mr-1 h-4 w-4" /> Previous</Button>
          <span className="text-sm text-muted-foreground">Page {page} of {totalPages} ({total} total)</span>
          <Button variant="outline" size="sm" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next <ChevronRight className="ml-1 h-4 w-4" /></Button>
        </div>
      )}
    </div>
  );
}
