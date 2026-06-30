"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Package,
  Warehouse,
  ShoppingCart,
  Truck,
  ArrowLeftRight,
  BarChart3,
  Sparkles,
  Settings,
  Users,
  Shield,
  History,
  Zap,
  Star,
  type LucideIcon,
} from "lucide-react";

interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
  permission?: string;
}

const mainNav: NavItem[] = [
  { label: "Dashboard", href: "/", icon: LayoutDashboard },
  { label: "Products", href: "/products", icon: Package },
  { label: "Inventory", href: "/inventory", icon: Warehouse },
  { label: "Warehouses", href: "/warehouses", icon: Building },
  { label: "Suppliers", href: "/suppliers", icon: Truck },
  { label: "Purchase Orders", href: "/purchase-orders", icon: ShoppingCart },
  { label: "Transfers", href: "/transfers", icon: ArrowLeftRight },
];

const aiNav: NavItem[] = [
  { label: "AI Workspace", href: "/ai", icon: Sparkles },
  { label: "Analytics", href: "/analytics", icon: BarChart3 },
  { label: "Scenario Lab", href: "/scenarios", icon: Zap },
  { label: "Showcase", href: "/showcase", icon: Star },
];

const adminNav: NavItem[] = [
  { label: "Users", href: "/users", icon: Users },
  { label: "Roles", href: "/roles", icon: Shield },
  { label: "Audit Logs", href: "/audit-logs", icon: History },
  { label: "Settings", href: "/settings", icon: Settings },
];

function Building(props: React.ComponentProps<"svg">) {
  return (
    <svg {...props} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
      />
    </svg>
  );
}

function NavSection({ title, items }: { title: string; items: NavItem[] }) {
  const pathname = usePathname();

  return (
    <div className="px-3 py-2">
      <h2 className="mb-2 px-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </h2>
      <nav className="flex flex-col gap-1">
        {items.map((item) => {
          const isActive = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-60 border-r bg-card">
      <div className="flex h-14 items-center gap-2 border-b px-6">
        <Sparkles className="h-5 w-5 text-primary" />
        <span className="font-semibold">ProcureFlow</span>
      </div>
      <div className="flex flex-col gap-2 overflow-y-auto py-4">
        <NavSection title="Main" items={mainNav} />
        <NavSection title="Intelligence" items={aiNav} />
        <NavSection title="Administration" items={adminNav} />
      </div>
    </aside>
  );
}
