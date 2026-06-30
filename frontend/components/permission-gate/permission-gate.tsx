"use client";

import { type ReactNode } from "react";
import { Lock } from "lucide-react";

interface PermissionGateProps {
  permission: string;
  children: ReactNode;
  fallback?: ReactNode;
}

export function PermissionGate({ permission, children, fallback }: PermissionGateProps) {
  if (typeof window === "undefined") return <>{children}</>;
  try {
    const raw = localStorage.getItem("auth-storage");
    if (!raw) return fallback ? <>{fallback}</> : <PermissionDenied />;
    const parsed = JSON.parse(raw);
    const perms = parsed?.state?.user?.permissions || [];
    if (perms.includes(permission)) return <>{children}</>;
  } catch {}
  return fallback ? <>{fallback}</> : <PermissionDenied />;
}

export function PermissionDenied() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="mb-4 rounded-full bg-muted p-4">
        <Lock className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold">Access Denied</h3>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">
        You do not have permission to access this page. Contact your administrator.
      </p>
    </div>
  );
}
