"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Shield, CheckCircle, RefreshCw } from "lucide-react";

interface Role { id: string; name: string; description: string | null; is_system: boolean; permissions: { name: string; group: string }[]; }

export default function RolesPage() {
  const [roles, setRoles] = useState<Role[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  const fetchRoles = async () => {
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: Role[] }>("/api/v1/roles");
      setRoles(r.data || []);
    } catch {}
    setLoading(false);
  };

  useEffect(() => { fetchRoles(); }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Roles & Permissions</h1><p className="text-muted-foreground">{roles.length} roles · 49 permissions across 12 groups</p></div>
        <Button variant="outline" onClick={fetchRoles} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
      </div>

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading roles...</div> :
       <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {roles.map(r => (
          <Card key={r.id} className="hover:shadow-sm transition-shadow cursor-pointer" onClick={() => setExpanded(expanded === r.id ? null : r.id)}>
            <CardContent className="py-6">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-sm">{r.name}</h3>
                  <p className="text-xs text-muted-foreground">{r.description || "No description"}</p>
                </div>
                {r.is_system && <span className="rounded-full bg-blue-50 dark:bg-blue-950/20 px-2 py-0.5 text-xs text-blue-700 dark:text-blue-400">System</span>}
              </div>
              <div className="flex flex-wrap gap-1">
                {r.permissions?.slice(0, expanded === r.id ? 99 : 5).map(p => (
                  <span key={p.name} className="rounded-full bg-muted px-1.5 py-0.5 text-xs font-mono">{p.name}</span>
                ))}
                {(r.permissions?.length || 0) > 5 && expanded !== r.id && <span className="text-xs text-muted-foreground">+{r.permissions.length - 5} more</span>}
              </div>
              {expanded === r.id && (
                <div className="mt-3 pt-3 border-t">
                  <p className="text-xs font-medium mb-1">All {r.permissions?.length || 0} Permissions</p>
                  <div className="space-y-1">{(r.permissions || []).map(p => <div key={p.name} className="flex items-center gap-2 text-xs"><CheckCircle className="h-3 w-3 text-green-500" /><span className="font-mono">{p.name}</span><span className="text-muted-foreground">({p.group})</span></div>)}</div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>}
    </div>
  );
}
