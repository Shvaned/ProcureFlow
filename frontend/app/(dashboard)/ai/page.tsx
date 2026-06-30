"use client";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles, BarChart3, ShoppingCart, Truck, Zap } from "lucide-react";

const modules = [
  { label: "Executive Copilot", href: "/ai/executive", icon: Sparkles, desc: "Daily briefs, health score, risk detection" },
  { label: "Procurement Copilot", href: "/ai/procurement", icon: ShoppingCart, desc: "Reorder recommendations, supplier comparison" },
  { label: "Supplier Intelligence", href: "/ai/suppliers", icon: Truck, desc: "Quotation analysis, supplier scorecards" },
  { label: "Analytics Assistant", href: "/ai/analytics", icon: BarChart3, desc: "Natural language analytics & charts" },
  { label: "Automation Studio", href: "/ai/automation", icon: Zap, desc: "Visual workflow builder & automation" },
];

export default function AIWorkspacePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">AI Workspace</h1>
        <p className="text-muted-foreground">Enterprise AI copilots and intelligence tools</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {modules.map(({ label, href, icon: Icon, desc }) => (
          <Link key={href} href={href}>
            <Card className="h-full transition-colors hover:border-primary/50">
              <CardContent className="flex flex-col gap-2 py-6">
                <Icon className="h-6 w-6 text-primary" />
                <h3 className="font-semibold">{label}</h3>
                <p className="text-sm text-muted-foreground">{desc}</p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
