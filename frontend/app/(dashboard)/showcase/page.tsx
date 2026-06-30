"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Sparkles, BarChart3, Code2, Database, Brain, Shield, Zap, Workflow, Layers, ArrowRight, CheckCircle, Star, Users, Truck, ShoppingCart, Warehouse, Package, Eye } from "lucide-react";

const MODULES = [
  { name: "Auth & RBAC", desc: "JWT + refresh tokens, 6 roles, 49 permissions, Argon2 hashing", icon: Shield, tech: "FastAPI, JWT, PostgreSQL" },
  { name: "Product Catalog", desc: "20,000+ SKU support, categories hierarchy, brands, units, attributes", icon: Package, tech: "FastAPI, SQLAlchemy 2" },
  { name: "Multi-Warehouse Inventory", desc: "Transaction-driven, FIFO/FEFO, lots, serials, 60+ tables", icon: Warehouse, tech: "PostgreSQL, asyncpg" },
  { name: "Supplier Management", desc: "500+ suppliers, contacts, performance scorecards, GST compliance", icon: Truck, tech: "SQLAlchemy, Pydantic v2" },
  { name: "Smart Procurement", desc: "Purchase orders, approvals, GRNs, AI-powered recommendations", icon: ShoppingCart, tech: "Clean Architecture" },
  { name: "Executive Analytics", desc: "KPIs, dashboards, drill-down, export, 12+ chart types", icon: BarChart3, tech: "Recharts, FastAPI" },
  { name: "AI Copilot", desc: "Executive briefs, procurement copilot, NL→SQL, OpenRouter integration", icon: Brain, tech: "OpenRouter, Structured Outputs" },
  { name: "AI Supplier Intelligence", desc: "Quotation analysis, comparison, risk assessment, negotiation insights", icon: Eye, tech: "Tool Registry, Prompt Registry" },
  { name: "Workflow Automation", desc: "Visual designer, execution engine, templates, 12 API endpoints", icon: Workflow, tech: "Deterministic engine" },
  { name: "Business Simulation", desc: "Digital twin, 12 scenarios, sandboxed, never modifies production data", icon: Zap, tech: "Scenario Service" },
  { name: "NL→SQL Analytics", desc: "Natural language to safe SQL, auto-charts, schema whitelist", icon: Code2, tech: "SQL Validator, Query Executor" },
  { name: "Scenario Lab", desc: "What-if analysis, business impact, AI advisor, baseline comparison", icon: Layers, tech: "Sandboxed execution" },
];

const METRICS = [
  { label: "API Endpoints", value: "100+", icon: Code2 },
  { label: "Database Models", value: "60+", icon: Database },
  { label: "AI Tools", value: "18", icon: Brain },
  { label: "Frontend Pages", value: "35+", icon: Eye },
  { label: "Test Cases", value: "12", icon: CheckCircle },
  { label: "User Stories", value: "104", icon: Users },
  { label: "Scenarios", value: "12", icon: Zap },
  { label: "Permissions", value: "49", icon: Shield },
];

const TECH_STACK = [
  { layer: "Frontend", items: "Next.js 15 · React 19 · TypeScript · Tailwind · shadcn/ui · TanStack Query · Zustand · Recharts" },
  { layer: "Backend", items: "FastAPI · Python 3.12 · SQLAlchemy 2 · Pydantic v2 · Alembic · Uvicorn" },
  { layer: "Database", items: "Neon PostgreSQL · asyncpg · Connection Pooling · 60+ Tables · 13 Bounded Contexts" },
  { layer: "AI", items: "OpenRouter · Structured Outputs · 5 Prompt Files · 18 Tools · Registry Pattern" },
  { layer: "DevOps", items: "Docker · Docker Compose · GitHub Actions · Nginx · SSL" },
  { layer: "Security", items: "JWT · RBAC · Argon2 · CSRF · Rate Limiting · Security Headers · OWASP" },
];

const DECISIONS = [
  { title: "Clean Architecture", why: "Controller → Service → Repository ensures business logic isolation and testability across 100+ endpoints" },
  { title: "Transaction-Driven Inventory", why: "Every quantity change creates an immutable transaction. Full audit trail. SAP/Oracle-grade correctness." },
  { title: "AI as Intelligence Layer", why: "AI explains, recommends, compares. ERP calculates, validates, executes. Never the other way around." },
  { title: "Structured AI Outputs", why: "Every AI response validates against Pydantic schemas. No raw text parsing. No hallucinated business values." },
  { title: "Tool-Based AI Access", why: "LLMs never touch the database. 18 approved tools call business services through the service layer." },
  { title: "Deterministic Workflows", why: "AI helps build workflows. The execution engine is 100% deterministic, auditable, and versioned." },
];

export default function ShowcasePage() {
  return (
    <div className="space-y-8 pb-16">
      {/* Hero */}
      <div className="text-center py-8">
        <div className="inline-flex items-center gap-2 rounded-full border bg-muted px-4 py-1.5 text-sm mb-4">
          <Sparkles className="h-3.5 w-3.5 text-primary" />
          Enterprise Procurement & Inventory Intelligence
        </div>
        <h1 className="text-4xl font-bold mb-3">ProcureFlow AI</h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          A production-grade enterprise SaaS platform combining deterministic ERP with an AI intelligence layer.
          Built with Clean Architecture, 100+ API endpoints, 60+ database models, and 18 AI tools.
        </p>
      </div>

      {/* Metrics */}
      <div className="grid gap-4 md:grid-cols-4 lg:grid-cols-8">
        {METRICS.map(m => (
          <Card key={m.label}><CardContent className="py-4 text-center">
            <m.icon className="h-5 w-5 mx-auto mb-1 text-primary" />
            <p className="text-xl font-bold">{m.value}</p>
            <p className="text-xs text-muted-foreground">{m.label}</p>
          </CardContent></Card>
        ))}
      </div>

      {/* Tech Stack */}
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Code2 className="h-5 w-5 text-primary" /> Technology Stack</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          {TECH_STACK.map(t => (
            <div key={t.layer} className="flex gap-4">
              <span className="text-sm font-semibold min-w-[80px]">{t.layer}</span>
              <span className="text-sm text-muted-foreground">{t.items}</span>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Modules Grid */}
      <div>
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Package className="h-5 w-5 text-primary" /> Platform Modules</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {MODULES.map(m => (
            <Card key={m.name} className="hover:shadow-md transition-shadow">
              <CardContent className="py-6">
                <m.icon className="h-6 w-6 text-primary mb-3" />
                <h3 className="font-semibold text-sm">{m.name}</h3>
                <p className="text-xs text-muted-foreground mt-1">{m.desc}</p>
                <p className="text-xs text-primary mt-2 font-mono">{m.tech}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Architecture Decisions */}
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Star className="h-5 w-5 text-primary" /> Key Architecture Decisions</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          {DECISIONS.map((d, i) => (
            <div key={i} className="border-l-2 border-primary pl-4">
              <h3 className="font-semibold text-sm">{d.title}</h3>
              <p className="text-sm text-muted-foreground">{d.why}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Interview Quick Facts */}
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Users className="h-5 w-5 text-primary" /> Interview Quick Reference</CardTitle></CardHeader>
        <CardContent>
          <div className="grid gap-3 md:grid-cols-2 text-sm">
            <div><strong>5-min demo:</strong> Dashboard → AI Executive Brief → Products → Scenario Lab</div>
            <div><strong>15-min technical:</strong> Above + Architecture Explorer + API Docs + AI Tools</div>
            <div><strong>30-min walkthrough:</strong> Full platform tour including Workflows, NL→SQL, Simulation</div>
            <div><strong>Key trade-off:</strong> Monorepo over microservices — chose velocity and shared types for this stage</div>
            <div><strong>AI safety:</strong> AI never calculates business values. ERP services are the single source of truth.</div>
            <div><strong>Scale target:</strong> Designed for 10+ developers, 100K+ users, millions of inventory records</div>
          </div>
        </CardContent>
      </Card>

      <div className="text-center text-sm text-muted-foreground pt-8 border-t">
        Built with Clean Architecture · 13 Bounded Contexts · 60+ SQLAlchemy Models · 100+ API Endpoints · 18 AI Tools · 12 Scenarios · 6 Workflow Templates
      </div>
    </div>
  );
}
