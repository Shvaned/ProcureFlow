"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Plus, Building, MapPin, RefreshCw } from "lucide-react";

interface Warehouse { id: string; code: string; name: string; city: string | null; country: string | null; warehouse_type: string; is_active: boolean; }
interface Zone { id: string; name: string; code: string; zone_type: string; }

export default function WarehousesPage() {
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [zones, setZones] = useState<Record<string, Zone[]>>({});
  const [zonesLoading, setZonesLoading] = useState<Record<string, boolean>>({});
  const [form, setForm] = useState({ code: "", name: "", city: "", country: "", warehouse_type: "Distribution" });
  const [saving, setSaving] = useState(false);

  const fetchWarehouses = async () => {
    setLoading(true); setError("");
    try {
      const r = await apiClient.get<{ data: Warehouse[] }>("/api/v1/warehouses");
      setWarehouses(r.data || []);
    } catch { setError("Failed to load warehouses"); }
    setLoading(false);
  };

  useEffect(() => { fetchWarehouses(); }, []);

  const loadZones = async (whId: string) => {
    if (zones[whId]) return;
    setZonesLoading(prev => ({ ...prev, [whId]: true }));
    try {
      const r = await apiClient.get<{ data: Zone[] }>(`/api/v1/warehouses/${whId}/zones`);
      setZones(prev => ({ ...prev, [whId]: r.data || [] }));
    } catch {}
    setZonesLoading(prev => ({ ...prev, [whId]: false }));
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    try {
      await apiClient.post("/api/v1/warehouses", form);
      setShowCreate(false); setForm({ code: "", name: "", city: "", country: "", warehouse_type: "Distribution" });
      fetchWarehouses();
    } catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Warehouses</h1><p className="text-muted-foreground">Manage warehouses, zones, and bins</p></div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={fetchWarehouses} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
          <Button onClick={() => setShowCreate(!showCreate)}><Plus className="mr-2 h-4 w-4" /> {showCreate ? "Cancel" : "Add Warehouse"}</Button>
        </div>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}

      {showCreate && (
        <Card>
          <CardHeader><CardTitle className="text-base">New Warehouse</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="grid gap-4 md:grid-cols-3">
              <div><label className="text-sm font-medium">Code *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.code} onChange={e => setForm({...form, code: e.target.value})} placeholder="WH-MUM" /></div>
              <div><label className="text-sm font-medium">Name *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.name} onChange={e => setForm({...form, name: e.target.value})} placeholder="Mumbai DC" /></div>
              <div><label className="text-sm font-medium">Type</label><select className="w-full rounded-md border px-3 py-2 text-sm" value={form.warehouse_type} onChange={e => setForm({...form, warehouse_type: e.target.value})}><option>Distribution</option><option>Cold Storage</option><option>Returns</option></select></div>
              <div><label className="text-sm font-medium">City</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={form.city} onChange={e => setForm({...form, city: e.target.value})} /></div>
              <div><label className="text-sm font-medium">Country</label><input className="w-full rounded-md border px-3 py-2 text-sm" value={form.country} onChange={e => setForm({...form, country: e.target.value})} placeholder="India" /></div>
              <div className="flex items-end"><Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create Warehouse"}</Button></div>
            </form>
          </CardContent>
        </Card>
      )}

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading warehouses...</div> :
       warehouses.length === 0 ? <div className="py-16 text-center text-muted-foreground">No warehouses. Create your first warehouse above.</div> :
       warehouses.map(wh => (
        <Card key={wh.id}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Building className="h-5 w-5 text-primary" />
                <div>
                  <CardTitle className="text-base">{wh.name}</CardTitle>
                  <p className="text-sm text-muted-foreground">{wh.code} · {wh.warehouse_type}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {wh.city && <span className="flex items-center gap-1 text-sm text-muted-foreground"><MapPin className="h-3 w-3" />{wh.city}{wh.country ? `, ${wh.country}` : ""}</span>}
                <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${wh.is_active ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" : "bg-muted text-muted-foreground"}`}>{wh.is_active ? "Active" : "Inactive"}</span>
                <Button variant="ghost" size="sm" onClick={() => loadZones(wh.id)}>Zones</Button>
              </div>
            </div>
          </CardHeader>
          {zones[wh.id] && (
            <CardContent className="border-t pt-4">
              {zonesLoading[wh.id] ? <p className="text-sm text-muted-foreground">Loading...</p> :
               zones[wh.id].length === 0 ? <p className="text-sm text-muted-foreground">No zones defined</p> :
               <div className="grid gap-2 md:grid-cols-3">
                 {zones[wh.id].map(z => (
                   <div key={z.id} className="rounded-md border p-3"><p className="text-sm font-medium">{z.name}</p><p className="text-xs text-muted-foreground">{z.code} · {z.zone_type}</p></div>
                 ))}
               </div>}
            </CardContent>
          )}
        </Card>
      ))}
    </div>
  );
}
