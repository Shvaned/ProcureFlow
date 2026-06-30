"use client";

import { useState, useEffect, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiClient } from "@/services/api-client";
import { Search, AlertTriangle, Clock, ChevronLeft, ChevronRight, RefreshCw } from "lucide-react";

interface InvItem {
  id: string; product_id: string; warehouse_id: string;
  available_quantity: number; reserved_quantity: number;
  lot_number: string | null; expiry_date: string | null;
}
interface TxnItem { id: string; type: string; before: number; after: number; change: number; reason: string; created_at: string; }
interface AlertItem { id: string; product_id: string; available: number; reorder_level: number | null; }
interface ExpiryItem { id: string; product_id: string; expiry_date: string | null; available_quantity: number; }

export default function InventoryPage() {
  const [items, setItems] = useState<InvItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [expiring, setExpiring] = useState<ExpiryItem[]>([]);
  const [selectedTxn, setSelectedTxn] = useState<{ id: string; txns: TxnItem[] } | null>(null);
  const [txnLoading, setTxnLoading] = useState(false);

  const fetchInv = useCallback(async (p: number) => {
    setLoading(true);
    setError("");
    try {
      const r = await apiClient.get<{ data: { items: InvItem[] }; metadata: { pagination: { total: number } } }>(
        "/api/v1/inventory", { page: String(p), page_size: "20" }
      );
      setItems(r.data?.items || []);
      setTotal(r.metadata?.pagination?.total || 0);
    } catch { setError("Failed to load inventory"); }
    setLoading(false);
  }, []);

  const fetchAlerts = useCallback(async () => {
    try {
      const [low, exp] = await Promise.all([
        apiClient.get<{ data: AlertItem[] }>("/api/v1/inventory/alerts/low-stock"),
        apiClient.get<{ data: ExpiryItem[] }>("/api/v1/inventory/alerts/expiring", { days: "30" }),
      ]);
      setAlerts(low.data || []);
      setExpiring(exp.data || []);
    } catch {}
  }, []);

  useEffect(() => { fetchInv(page); fetchAlerts(); }, [page, fetchInv, fetchAlerts]);

  const viewTxns = async (invId: string) => {
    setTxnLoading(true);
    try {
      const r = await apiClient.get<{ data: TxnItem[] }>(`/api/v1/inventory/${invId}/transactions`);
      setSelectedTxn({ id: invId, txns: r.data || [] });
    } catch { setSelectedTxn({ id: invId, txns: [] }); }
    setTxnLoading(false);
  };

  const totalPages = Math.max(1, Math.ceil(total / 20));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Inventory</h1>
          <p className="text-muted-foreground">Multi-warehouse inventory management</p>
        </div>
        <Button variant="outline" onClick={() => { fetchInv(page); fetchAlerts(); }} disabled={loading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh
        </Button>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}

      {/* Alert Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="border-orange-500/30">
          <CardContent className="flex items-center justify-between py-4">
            <div><p className="text-sm text-muted-foreground">Low Stock</p><p className="text-2xl font-bold text-orange-500">{alerts.length}</p></div>
            <AlertTriangle className="h-8 w-8 text-orange-500/50" />
          </CardContent>
        </Card>
        <Card className="border-red-500/30">
          <CardContent className="flex items-center justify-between py-4">
            <div><p className="text-sm text-muted-foreground">Expiring Soon</p><p className="text-2xl font-bold text-red-500">{expiring.length}</p></div>
            <Clock className="h-8 w-8 text-red-500/50" />
          </CardContent>
        </Card>
        <Card>
          <CardContent className="py-4"><p className="text-sm text-muted-foreground">Total Records</p><p className="text-2xl font-bold">{total}</p></CardContent>
        </Card>
        <Card>
          <CardContent className="py-4"><p className="text-sm text-muted-foreground">Page</p><p className="text-2xl font-bold">{page}/{totalPages}</p></CardContent>
        </Card>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input className="w-full rounded-md border pl-10 pr-4 py-2 text-sm" placeholder="Search inventory..."
          value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      {/* Inventory Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="py-16 text-center text-muted-foreground">Loading inventory...</div>
          ) : items.length === 0 ? (
            <div className="py-16 text-center text-muted-foreground">No inventory records found. Create products and warehouses first.</div>
          ) : (
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="py-3 px-4 font-medium">Product ID</th><th className="py-3 px-4 font-medium">Warehouse</th><th className="py-3 px-4 font-medium text-right">Available</th><th className="py-3 px-4 font-medium text-right">Reserved</th><th className="py-3 px-4 font-medium">Lot #</th><th className="py-3 px-4 font-medium">Expiry</th><th className="py-3 px-4"></th></tr></thead>
              <tbody>
                {items.filter(i => search === "" || i.product_id.includes(search) || i.lot_number?.includes(search)).map((i) => (
                  <tr key={i.id} className="border-b hover:bg-muted/50">
                    <td className="py-3 px-4 font-mono text-xs">{i.product_id.slice(0, 8)}...</td>
                    <td className="py-3 px-4 text-muted-foreground">{i.warehouse_id.slice(0, 8)}...</td>
                    <td className="py-3 px-4 text-right font-medium">{i.available_quantity}</td>
                    <td className="py-3 px-4 text-right">{i.reserved_quantity}</td>
                    <td className="py-3 px-4 text-xs">{i.lot_number || "--"}</td>
                    <td className="py-3 px-4 text-xs">{i.expiry_date ? new Date(i.expiry_date).toLocaleDateString() : "--"}</td>
                    <td className="py-3 px-4"><Button variant="ghost" size="sm" onClick={() => viewTxns(i.id)}>History</Button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>
            <ChevronLeft className="mr-1 h-4 w-4" /> Previous
          </Button>
          <span className="text-sm text-muted-foreground">Page {page} of {totalPages}</span>
          <Button variant="outline" size="sm" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>
            Next <ChevronRight className="ml-1 h-4 w-4" />
          </Button>
        </div>
      )}

      {/* Transaction History Modal */}
      {selectedTxn && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base">Transaction History</CardTitle>
              <Button variant="ghost" size="sm" onClick={() => setSelectedTxn(null)}>Close</Button>
            </div>
          </CardHeader>
          <CardContent>
            {txnLoading ? <div className="py-8 text-center text-muted-foreground">Loading...</div> :
             selectedTxn.txns.length === 0 ? <div className="py-8 text-center text-muted-foreground">No transactions</div> : (
              <table className="w-full text-sm">
                <thead><tr className="border-b text-left"><th className="py-2 font-medium">Type</th><th className="py-2 font-medium">Before</th><th className="py-2 font-medium">After</th><th className="py-2 font-medium">Change</th><th className="py-2 font-medium">Reason</th><th className="py-2 font-medium">Date</th></tr></thead>
                <tbody>{selectedTxn.txns.map((t, i) => (
                  <tr key={i} className="border-b">
                    <td className="py-2"><span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium">{t.type}</span></td>
                    <td className="py-2">{t.before}</td><td className="py-2">{t.after}</td>
                    <td className={`py-2 font-medium ${t.change < 0 ? "text-red-500" : "text-green-500"}`}>{t.change > 0 ? "+" : ""}{t.change}</td>
                    <td className="py-2 text-xs text-muted-foreground max-w-[200px] truncate">{t.reason}</td>
                    <td className="py-2 text-xs">{new Date(t.created_at).toLocaleString()}</td>
                  </tr>
                ))}</tbody>
              </table>
            )}
          </CardContent>
        </Card>
      )}

      {/* Alert Details */}
      {alerts.length > 0 && (
        <Card className="border-orange-500/20">
          <CardHeader><CardTitle className="text-base">Low Stock Alerts ({alerts.length})</CardTitle></CardHeader>
          <CardContent>
            <table className="w-full text-sm">
              <thead><tr className="border-b text-left"><th className="py-2 font-medium">Product</th><th className="py-2 font-medium text-right">Available</th><th className="py-2 font-medium text-right">Reorder Level</th></tr></thead>
              <tbody>{alerts.slice(0, 10).map(a => (
                <tr key={a.id} className="border-b"><td className="py-2 font-mono text-xs">{a.product_id.slice(0, 8)}...</td><td className="py-2 text-right text-orange-500">{a.available}</td><td className="py-2 text-right">{a.reorder_level}</td></tr>
              ))}</tbody>
            </table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
