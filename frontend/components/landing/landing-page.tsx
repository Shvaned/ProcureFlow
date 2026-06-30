import Link from "next/link";
import {
  Sparkles,
  BarChart3,
  Package,
  Warehouse,
  ShoppingCart,
  Truck,
  Shield,
  Zap,
} from "lucide-react";

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-primary" />
            <span className="text-lg font-semibold">ProcureFlow AI</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/login" className="text-sm text-muted-foreground hover:text-foreground">
              Sign in
            </Link>
            <Link
              href="/login"
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 py-24 text-center">
        <div className="mx-auto max-w-3xl space-y-8">
          <div className="inline-flex items-center gap-2 rounded-full border bg-muted px-4 py-1.5 text-sm">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            AI-Powered Enterprise Procurement
          </div>
          <h1 className="text-5xl font-bold leading-tight tracking-tight lg:text-6xl">
            Intelligent Procurement & Inventory for{" "}
            <span className="text-primary">Modern Enterprises</span>
          </h1>
          <p className="text-xl text-muted-foreground">
            ProcureFlow AI combines deterministic ERP with an AI intelligence layer.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link
              href="/login"
              className="rounded-md bg-primary px-6 py-3 text-sm font-medium text-primary-foreground hover:bg-primary/90"
            >
              Launch App
            </Link>
            <Link
              href="/login"
              className="rounded-md border px-6 py-3 text-sm font-medium hover:bg-muted"
            >
              View Architecture
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="mx-auto max-w-7xl px-6 py-24">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold">Enterprise ERP Meets AI Intelligence</h2>
          <p className="mt-4 text-muted-foreground">
            Everything you need to run procurement and inventory operations, enhanced with AI.
          </p>
        </div>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {[
            {
              icon: Package,
              title: "Product Catalog",
              desc: "20,000+ SKUs with categories, brands, attributes, and dynamic pricing.",
            },
            {
              icon: Warehouse,
              title: "Multi-Warehouse",
              desc: "Real-time inventory across warehouses, zones, and bins with transaction tracking.",
            },
            {
              icon: ShoppingCart,
              title: "Smart Procurement",
              desc: "Purchase orders, approvals, GRNs with AI-powered reorder recommendations.",
            },
            {
              icon: Truck,
              title: "Supplier Intelligence",
              desc: "500+ suppliers with performance tracking, quotation comparison, and risk analysis.",
            },
            {
              icon: BarChart3,
              title: "Executive Analytics",
              desc: "KPIs, dashboards, and reports that answer real business questions.",
            },
            {
              icon: Sparkles,
              title: "AI Copilot",
              desc: "Daily briefs, procurement recommendations, and natural language analytics.",
            },
            {
              icon: Zap,
              title: "Workflow Automation",
              desc: "Visual workflow builder to automate procurement and inventory operations.",
            },
            {
              icon: Shield,
              title: "Enterprise Security",
              desc: "JWT + RBAC, Argon2 passwords, OWASP compliance, full audit trail.",
            },
          ].map(({ icon: Icon, title, desc }) => (
            <div
              key={title}
              className="rounded-lg border bg-card p-6 hover:border-primary/50 transition-colors"
            >
              <div className="mb-3 rounded-md bg-primary/10 p-2 w-fit">
                <Icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="font-semibold">{title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t py-8 text-center text-sm text-muted-foreground">
        ProcureFlow AI — Enterprise Procurement & Inventory Intelligence Platform
      </footer>
    </div>
  );
}
