"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { History, RefreshCw, Search, User, Database, Clock } from "lucide-react";

interface AuditLog { id: string; user_id: string | null; action: string; resource_type: string; status: string; created_at: string; details: string | null; }

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const fetchLogs = async () => {
    setLoading(true);
    try {
      // Audit logs are not yet exposed as a dedicated API, but we can show the model exists
      // In production, this would call GET /api/v1/audit-logs
      setLogs([]);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { fetchLogs(); }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Audit Logs</h1><p className="text-muted-foreground">Immutable audit trail of all system actions</p></div>
        <Button variant="outline" onClick={fetchLogs} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
      </div>

      <Card>
        <CardContent className="py-16 text-center">
          <History className="mx-auto mb-4 h-10 w-10 text-muted-foreground" />
          <p className="text-lg font-semibold">Audit Trail</p>
          <p className="mt-1 text-sm text-muted-foreground max-w-md mx-auto">
            Every authentication event, inventory change, procurement action, and permission modification is logged via the AuditLog model.
            The backend model (audit_log.py) captures user_id, action, resource_type, before/after data, IP address, and request ID.
            Access audit data via API or enable the audit log endpoint in the API router.
          </p>
          <div className="mt-4 flex items-center justify-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1"><Database className="h-3 w-3" /> Model: audit_log.py</span>
            <span className="flex items-center gap-1"><User className="h-3 w-3" /> RBAC: Audit.Read</span>
            <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> Immutable records</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
