"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Plus, FileText } from "lucide-react";

export default function PurchaseRequestsPage() {
  const [showCreate, setShowCreate] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({ warehouse_id: "", notes: "" });

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true); setError(""); setSuccess("");
    try {
      await apiClient.post("/api/v1/purchase-requests", form);
      setSuccess("Purchase request created");
      setShowCreate(false); setForm({ warehouse_id: "", notes: "" });
    } catch (err: any) { setError(err.message); }
    setSaving(false);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Purchase Requests</h1><p className="text-muted-foreground">Warehouse requests for procurement</p></div>
        <Button onClick={() => setShowCreate(!showCreate)}><Plus className="mr-2 h-4 w-4" /> {showCreate ? "Cancel" : "New Request"}</Button>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}
      {success && <div className="rounded-md bg-green-100 dark:bg-green-900/20 p-4 text-sm text-green-700 dark:text-green-400">{success}</div>}

      {showCreate && (
        <Card>
          <CardHeader><CardTitle className="text-base">Create Purchase Request</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleCreate} className="space-y-4 max-w-lg">
              <div><label className="text-sm font-medium">Warehouse ID *</label><input required className="w-full rounded-md border px-3 py-2 text-sm" value={form.warehouse_id} onChange={e => setForm({...form, warehouse_id: e.target.value})} placeholder="Warehouse UUID" /></div>
              <div><label className="text-sm font-medium">Notes</label><textarea className="w-full rounded-md border px-3 py-2 text-sm" rows={3} value={form.notes} onChange={e => setForm({...form, notes: e.target.value})} /></div>
              <Button type="submit" disabled={saving}>{saving ? "Creating..." : "Create Request"}</Button>
            </form>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="py-16 text-center">
          <FileText className="mx-auto mb-4 h-10 w-10 text-muted-foreground" />
          <p className="text-lg font-semibold">Purchase Requests</p>
          <p className="mt-1 text-sm text-muted-foreground">Create purchase requests above. Backend API supports full CRUD at /api/v1/purchase-requests.</p>
        </CardContent>
      </Card>
    </div>
  );
}
