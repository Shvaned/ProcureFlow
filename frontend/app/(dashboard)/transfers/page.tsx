"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Plus, ArrowLeftRight } from "lucide-react";

export default function TransfersPage() {
  const [showCreate, setShowCreate] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({
    from_warehouse_id: "", to_warehouse_id: "", notes: "",
    items: [{ product_id: "", inventory_id: "", quantity: 1 }],
  });

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true); setError(""); setSuccess("");
    try {
      const r = await apiClient.post<{ data: { id: string } }>("/api/v1/transfers", form);
      setSuccess(`Transfer ${r.data?.id?.slice(0, 8)}... created successfully`);
      setShowCreate(false);
      setForm({ from_warehouse_id: "", to_warehouse_id: "", notes: "", items: [{ product_id: "", inventory_id: "", quantity: 1 }] });
    } catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Transfers</h1><p className="text-muted-foreground">Inter-warehouse stock transfers with audit trail</p></div>
        <Button onClick={() => setShowCreate(!showCreate)}><Plus className="mr-2 h-4 w-4" /> {showCreate ? "Cancel" : "New Transfer"}</Button>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}
      {success && <div className="rounded-md bg-green-100 dark:bg-green-900/20 p-4 text-sm text-green-700 dark:text-green-400">{success}</div>}

      {showCreate && (
        <Card>
          <CardHeader><CardTitle className="text-base">Create Stock Transfer</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="space-y-4">
              <div className="grid gap-4 md:grid-cols-3">
                <div><label className="text-sm font-medium">From Warehouse *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.from_warehouse_id} onChange={e => setForm({...form, from_warehouse_id: e.target.value})} placeholder="Source UUID" /></div>
                <div><label className="text-sm font-medium">To Warehouse *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.to_warehouse_id} onChange={e => setForm({...form, to_warehouse_id: e.target.value})} placeholder="Dest UUID" /></div>
                <div><label className="text-sm font-medium">Notes</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={form.notes} onChange={e => setForm({...form, notes: e.target.value})} /></div>
              </div>

              <div>
                <p className="text-sm font-medium mb-2">Transfer Items</p>
                {form.items.map((item, idx) => (
                  <div key={idx} className="mb-2 flex gap-2">
                    <input className="flex-1 rounded-md border px-3 py-1 text-sm" placeholder="Product ID" value={item.product_id} onChange={e => { const items = [...form.items]; items[idx].product_id = e.target.value; setForm({...form, items}); }} />
                    <input className="flex-1 rounded-md border px-3 py-1 text-sm" placeholder="Inventory ID" value={item.inventory_id} onChange={e => { const items = [...form.items]; items[idx].inventory_id = e.target.value; setForm({...form, items}); }} />
                    <input type="number" className="w-20 rounded-md border px-3 py-1 text-sm" placeholder="Qty" value={item.quantity} onChange={e => { const items = [...form.items]; items[idx].quantity = parseInt(e.target.value) || 1; setForm({...form, items}); }} />
                    {form.items.length > 1 && <Button variant="ghost" size="sm" onClick={() => setForm({...form, items: form.items.filter((_, i) => i !== idx)})}>×</Button>}
                  </div>
                ))}
                <Button variant="outline" size="sm" type="button" onClick={() => setForm({...form, items: [...form.items, { product_id: "", inventory_id: "", quantity: 1 }]})}>+ Add Item</Button>
              </div>

              <Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create Transfer"}</Button>
            </form>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="py-16 text-center">
          <ArrowLeftRight className="mx-auto mb-4 h-10 w-10 text-muted-foreground" />
          <p className="text-lg font-semibold">Stock Transfers</p>
          <p className="mt-1 text-sm text-muted-foreground">Create an inter-warehouse transfer above. Each transfer records a full audit trail.</p>
        </CardContent>
      </Card>
    </div>
  );
}
