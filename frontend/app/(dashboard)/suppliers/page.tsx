"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiClient } from "@/services/api-client";
import { Plus, Search, ChevronLeft, ChevronRight, Truck, Star, Phone, Mail, Building, RefreshCw } from "lucide-react";
import Link from "next/link";

interface Supplier { id: string; code: string; legal_name: string; display_name: string | null; gst_number: string | null; country: string | null; email: string | null; phone: string | null; rating: number; is_active: boolean; }

export default function SuppliersPage() {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ code: "", legal_name: "", email: "", phone: "", country: "India" });
  const [saving, setSaving] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<any>(null);

  const fetchSuppliers = useCallback(async (p: number) => {
    setLoading(true); setError("");
    try {
      const r = await apiClient.get<{ data: { items: Supplier[] }; metadata: { pagination: { total: number } } }>(
        "/api/v1/suppliers", { page: String(p), page_size: "20" }
      );
      setSuppliers(r.data?.items || []);
      setTotal(r.metadata?.pagination?.total || 0);
    } catch { setError("Failed to load suppliers"); }
    setLoading(false);
  }, []);

  useEffect(() => { fetchSuppliers(page); }, [page, fetchSuppliers]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    try { await apiClient.post("/api/v1/suppliers", form); setShowCreate(false); setForm({ code: "", legal_name: "", email: "", phone: "", country: "India" }); fetchSuppliers(page); }
    catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  const viewDetail = async (id: string) => {
    if (selectedId === id) { setSelectedId(null); setDetail(null); return; }
    setSelectedId(id);
    try {
      const r = await apiClient.get<{ data: any }>(`/api/v1/suppliers/${id}`);
      setDetail(r.data);
    } catch { setDetail(null); }
  };

  const totalPages = Math.max(1, Math.ceil(total / 20));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Suppliers</h1><p className="text-muted-foreground">{total} suppliers · rating, performance, contact tracking</p></div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => fetchSuppliers(page)} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
          <Button onClick={() => setShowCreate(!showCreate)}><Plus className="mr-2 h-4 w-4" /> {showCreate ? "Cancel" : "Add Supplier"}</Button>
        </div>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}

      {showCreate && (
        <Card>
          <CardHeader><CardTitle className="text-base">New Supplier</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="grid gap-4 md:grid-cols-3">
              <div><label className="text-sm font-medium">Code *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.code} onChange={e => setForm({...form, code: e.target.value})} placeholder="SUP-0001" /></div>
              <div className="md:col-span-2"><label className="text-sm font-medium">Legal Name *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.legal_name} onChange={e => setForm({...form, legal_name: e.target.value})} placeholder="Acme Supplies Ltd" /></div>
              <div><label className="text-sm font-medium">Email</label><input type="email" className="w-full rounded-md border px-3 py-2 text-sm" value={form.email} onChange={e => setForm({...form, email: e.target.value})} /></div>
              <div><label className="text-sm font-medium">Phone</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={form.phone} onChange={e => setForm({...form, phone: e.target.value})} /></div>
              <div><label className="text-sm font-medium">Country</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={form.country} onChange={e => setForm({...form, country: e.target.value})} /></div>
              <div className="flex items-end"><Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create Supplier"}</Button></div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="relative"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" /><input className="w-full rounded-md border pl-10 pr-4 py-2 text-sm" placeholder="Search suppliers..." value={search} onChange={e => setSearch(e.target.value)} /></div>

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading...</div> :
       suppliers.length === 0 ? <div className="py-16 text-center text-muted-foreground">No suppliers. Add your first supplier above.</div> :
       <Card><CardContent className="p-0">
        <table className="w-full text-sm">
          <thead><tr className="border-b text-left"><th className="py-3 px-4 font-medium">Supplier</th><th className="py-3 px-4 font-medium">Code</th><th className="py-3 px-4 font-medium">Contact</th><th className="py-3 px-4 font-medium">Country</th><th className="py-3 px-4 font-medium text-center">Rating</th><th className="py-3 px-4 font-medium">Status</th><th className="py-3 px-4"></th></tr></thead>
          <tbody>
            {suppliers.filter(s => search === "" || s.legal_name.toLowerCase().includes(search.toLowerCase()) || s.code.toLowerCase().includes(search.toLowerCase())).map(s => (
              <><tr key={s.id} className="border-b hover:bg-muted/50">
                <td className="py-3 px-4"><div className="font-medium">{s.legal_name}</div>{s.display_name && <div className="text-xs text-muted-foreground">{s.display_name}</div>}</td>
                <td className="py-3 px-4 font-mono text-xs">{s.code}</td>
                <td className="py-3 px-4"><div className="text-xs">{s.email || "--"}</div><div className="text-xs text-muted-foreground">{s.phone || ""}</div></td>
                <td className="py-3 px-4 text-xs">{s.country || "--"}</td>
                <td className="py-3 px-4 text-center"><span className="inline-flex items-center gap-1"><Star className="h-3 w-3 fill-orange-400 text-orange-400" />{s.rating?.toFixed(1) || "0.0"}</span></td>
                <td className="py-3 px-4"><span className={`rounded-full px-2 py-0.5 text-xs font-medium ${s.is_active ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" : "bg-muted text-muted-foreground"}`}>{s.is_active ? "Active" : "Inactive"}</span></td>
                <td className="py-3 px-4"><Button variant="ghost" size="sm" onClick={() => viewDetail(s.id)}>{selectedId === s.id ? "Close" : "Details"}</Button></td>
              </tr>
              {selectedId === s.id && detail && (
                <tr key={`${s.id}-detail`}><td colSpan={7} className="bg-muted/30 p-6">
                  <div className="grid gap-4 md:grid-cols-3">
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Contact Information</h4>
                      {detail.contacts?.length > 0 ? detail.contacts.map((c: any) => (
                        <div key={c.id} className="mb-2 text-sm"><div className="font-medium">{c.name} {c.is_primary ? "(Primary)" : ""}</div><div className="text-xs text-muted-foreground">{c.email} · {c.phone} · {c.contact_type}</div></div>
                      )) : <p className="text-xs text-muted-foreground">No contacts</p>}
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Business Details</h4>
                      <div className="text-xs space-y-1"><div>GST: {detail.gst_number || "--"}</div><div>PAN: {detail.pan || "--"}</div><div>Payment Terms: {detail.payment_terms || "--"}</div><div>Currency: {detail.currency}</div><div>Preferred: {detail.is_preferred ? "Yes" : "No"}</div></div>
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Documents</h4>
                      {detail.documents?.length > 0 ? detail.documents.map((d: any) => (
                        <div key={d.id} className="text-xs">{d.name} ({d.document_type})</div>
                      )) : <p className="text-xs text-muted-foreground">No documents</p>}
                    </div>
                  </div>
                </td></tr>
              )}
              </>
            ))}
          </tbody>
        </table>
      </CardContent></Card>}

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
