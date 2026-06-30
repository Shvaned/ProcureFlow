"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import { Users, Plus, CheckCircle, XCircle, RefreshCw, Search } from "lucide-react";

interface User { id: string; email: string; name: string; is_active: boolean; is_locked: boolean; roles: { name: string }[]; }

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const r = await apiClient.get<{ data: User[] }>("/api/v1/users");
      setUsers(r.data || []);
    } catch { setError("Failed to load users"); }
    setLoading(false);
  };

  useEffect(() => { fetchUsers(); }, []);

  const filtered = users.filter(u => search === "" || u.email.includes(search) || u.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold">Users</h1><p className="text-muted-foreground">{users.length} users · Role-based access control</p></div>
        <Button variant="outline" onClick={fetchUsers} disabled={loading}><RefreshCw className={`mr-2 h-4 w-4 ${loading ? "animate-spin" : ""}`} /> Refresh</Button>
      </div>

      {error && <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">{error}</div>}
      <div className="relative"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" /><input className="w-full rounded-md border pl-10 pr-4 py-2 text-sm" placeholder="Search users by name or email..." value={search} onChange={e => setSearch(e.target.value)} /></div>

      {loading ? <div className="py-16 text-center text-muted-foreground">Loading users...</div> :
       filtered.length === 0 ? <div className="py-16 text-center text-muted-foreground">No users found.</div> :
       <Card><CardContent className="p-0">
        <table className="w-full text-sm">
          <thead><tr className="border-b text-left"><th className="py-3 px-4 font-medium">User</th><th className="py-3 px-4 font-medium">Email</th><th className="py-3 px-4 font-medium">Roles</th><th className="py-3 px-4 font-medium">Status</th></tr></thead>
          <tbody>{filtered.map(u => (
            <tr key={u.id} className="border-b hover:bg-muted/50">
              <td className="py-3 px-4 font-medium">{u.name}</td>
              <td className="py-3 px-4 text-xs">{u.email}</td>
              <td className="py-3 px-4"><div className="flex flex-wrap gap-1">{u.roles?.map(r => <span key={r.name} className="rounded-full bg-muted px-2 py-0.5 text-xs">{r.name}</span>)}</div></td>
              <td className="py-3 px-4">{u.is_active ? <span className="flex items-center gap-1 text-green-600 text-xs"><CheckCircle className="h-3 w-3" /> Active</span> : <span className="flex items-center gap-1 text-red-600 text-xs"><XCircle className="h-3 w-3" /> Inactive</span>}</td>
            </tr>
          ))}</tbody>
        </table>
      </CardContent></Card>}
    </div>
  );
}
