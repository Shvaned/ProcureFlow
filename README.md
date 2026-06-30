# ProcureFlow AI

**AI-powered Procurement & Inventory Intelligence Platform for Multi-Warehouse B2B Commerce**

A production-grade enterprise SaaS combining a deterministic ERP core with an AI intelligence layer. The AI explains, recommends, summarizes, and compares — but never makes business decisions. The ERP remains the source of truth.

---

## Architecture

```
Frontend (Next.js 15)  →  Backend (FastAPI)  →  PostgreSQL (Neon)
                                ↕
                          AI Layer (OpenRouter)
                              ↓
                    Structured Outputs + Tools
```

- **Frontend**: Next.js 15, React 19, TypeScript, TailwindCSS, shadcn/ui, TanStack Query/Table, Zustand, Recharts
- **Backend**: FastAPI, Python 3.12, SQLAlchemy 2, Pydantic v2, Alembic
- **Database**: Neon PostgreSQL (serverless, branching)
- **AI**: OpenRouter (model-agnostic), structured JSON outputs, tool-based ERP access
- **Deployment**: Docker + Docker Compose, Vercel/Railway ready

## Modules

| Module | Features |
|--------|----------|
| **Auth & RBAC** | JWT + refresh tokens, 6 roles, 48 permissions, Argon2 passwords |
| **Product Catalog** | Products, categories (hierarchy), brands, units, images, documents |
| **Warehouse & Inventory** | Multi-warehouse, zones, bins, transaction-driven inventory |
| **Supplier Management** | Suppliers, contacts, documents, performance tracking, scorecards |
| **Procurement** | Purchase requests, purchase orders, approvals, GRNs, receiving |
| **Executive Analytics** | KPIs, dashboards, inventory/supplier/procurement analytics |
| **Business Simulation** | Continuous business event engine with configurable scenarios |
| **AI Executive Copilot** | Daily briefs, business health score, risk/opportunity detection |
| **AI Procurement Copilot** | Reorder recommendations, supplier comparison, what-if analysis |
| **AI Supplier Intelligence** | Quotation parsing, supplier analysis, negotiation suggestions |
| **NL Analytics** | Natural language → SQL → charts with safe query validation |
| **Workflow Automation** | Visual workflow designer, execution engine, approval center |

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DATABASE_URL and OPENROUTER_API_KEY
uvicorn app.main:app --reload

# Frontend
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

### Docker

```bash
docker compose up
```

## Project Structure

```
procureflow/
├── frontend/          # Next.js 15 (App Router, TypeScript, Tailwind)
│   ├── app/           # Pages (dashboard, products, inventory, AI workspace)
│   ├── components/    # Reusable UI (Button, Card, DataTable, Modal, etc.)
│   ├── providers/     # Theme, Query, Auth, Toast providers
│   └── services/      # API client with JWT auto-injection
├── backend/           # FastAPI (Python 3.12)
│   ├── app/
│   │   ├── api/       # Route handlers (controllers)
│   │   ├── models/    # SQLAlchemy models (11 bounded contexts, 50+ tables)
│   │   ├── schemas/   # Pydantic DTOs
│   │   ├── services/  # Business logic
│   │   ├── repositories/ # Data access (generic CRUD + filtering)
│   │   ├── ai/        # AI platform (providers, prompts, tools)
│   │   ├── middleware/ # Auth, logging, RBAC, security headers
│   │   └── core/      # Config, exceptions, security, database
│   └── tests/
├── docs/              # 13 design documents (PRD, BRD, architecture, etc.)
├── docker/            # Docker configuration
├── .github/           # CI/CD workflows
└── docker-compose.yml
```

## Engineering Principles

- **Clean Architecture**: Controller → Service → Repository → Database
- **AI Governance**: AI explains, summarizes, compares, recommends. AI NEVER calculates, approves, modifies, or executes.
- **Transaction-Driven Inventory**: Every quantity change is an immutable transaction record.
- **Structured AI Outputs**: Every AI response validates against Pydantic schemas.
- **Tool-Based AI Access**: AI accesses ERP data only through approved tools that call business services.
- **RBAC**: Permission-based authorization enforced server-side on every endpoint.

## Documentation

Full documentation in `/docs`:
- PRD, BRD, Functional & Non-Functional Requirements
- User Personas (6) & User Stories (104)
- System Architecture with flow diagrams
- Database Planning (13 bounded contexts, entity maps)
- API Planning (~224 endpoints)
- Folder Structure & Coding Standards
- Design Language & UI Guidelines
- Implementation Roadmap (19 phases)

## License

MIT
