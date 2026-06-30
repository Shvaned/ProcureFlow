# ProcureFlow AI — System Architecture

**Version:** 1.0.0
**Date:** 2026-06-30

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Next.js 15 (React 19 + TypeScript)        │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │  │
│  │  │  shadcn  │ │TanStack  │ │ Zustand  │ │ Recharts │ │  │
│  │  │    UI    │ │  Table   │ │  Store   │ │  Charts  │ │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS + JWT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       API LAYER                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               FastAPI (Python 3.12+)                    │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │           Middleware Stack                       │  │  │
│  │  │  CORS → Auth → RBAC → Logging → Rate Limit      │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              Controllers                        │  │  │
│  │  │  Auth | Users | Products | Inventory | ...      │  │  │
│  │  └────────────┬────────────────────────────────────┘  │  │
│  │               ▼                                        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              Services (Business Logic)           │  │  │
│  │  │  ProductService | InventoryService | ...        │  │  │
│  │  └────────────┬────────────────────────────────────┘  │  │
│  │               ▼                                        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │            Repositories (Data Access)            │  │  │
│  │  │  ProductRepo | InventoryRepo | ...              │  │  │
│  │  └────────────┬────────────────────────────────────┘  │  │
│  └───────────────┼────────────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Neon PostgreSQL                           │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  SQLAlchemy 2 ORM + Alembic Migrations          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Next.js | 15 | React framework, App Router |
| React | 19 | UI library |
| TypeScript | 5.x | Type safety |
| TailwindCSS | 3.x | Utility-first CSS |
| shadcn/ui | Latest | Component library |
| TanStack Query | 5.x | Server state management |
| Zustand | 4.x | Client state management |
| React Hook Form | 7.x | Form management |
| Zod | 3.x | Schema validation |
| Recharts | 2.x | Charting library |
| React Flow | Latest | Workflow visualization |
| TanStack Table | 8.x | Data tables |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.11x | API framework |
| Python | 3.12+ | Runtime |
| SQLAlchemy | 2.x | ORM |
| Alembic | Latest | Database migrations |
| Pydantic | 2.x | Data validation |
| Uvicorn | Latest | ASGI server |
| APScheduler | Latest | Background scheduling |

### Database
| Technology | Purpose |
|-----------|---------|
| Neon PostgreSQL | Serverless PostgreSQL |
| UUID | Primary keys |
| Foreign Keys | Referential integrity |

### AI
| Technology | Purpose |
|-----------|---------|
| OpenRouter | AI provider gateway |
| Pydantic | Structured output validation |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| Docker Compose | Orchestration |
| GitHub Actions | CI/CD |

---

## 3. Request Flow

```
Browser
  │
  ├─1─► Next.js Server (SSR/CSR)
  │       │
  │       ├─2─► FastAPI (/api/v1/*)
  │       │       │
  │       │       ├─3─► Middleware (CORS, Auth, RBAC, Logging)
  │       │       │       │
  │       │       │       ├─4─► Controller
  │       │       │       │       │
  │       │       │       │       ├─5─► Service (Business Logic)
  │       │       │       │       │       │
  │       │       │       │       │       ├─6─► Repository
  │       │       │       │       │       │       │
  │       │       │       │       │       │       ├─7─► Database
  │       │       │       │       │       │       │
  │       │       │       │       │       │       ▼
  │       │       │       │       │       │     Query Result
  │       │       │       │       │       ▼
  │       │       │       │       │     Model
  │       │       │       │       ▼
  │       │       │       │     DTO
  │       │       │       ▼
  │       │       │     StandardResponse JSON
  │       │       ▼
  │       │     HTTP Response
  │       ▼
  │     React Component with data
  ▼
User sees rendered UI
```

---

## 4. Authentication Flow

### Login
```
User → POST /api/v1/auth/login {email, password}
  → AuthService.authenticate()
    → Validate credentials (Argon2)
    → Generate access_token (short-lived, 15 min)
    → Generate refresh_token (long-lived, 7 days)
    → Store session (user_id, IP, device, browser)
    → Return tokens
  → Frontend stores tokens (httpOnly cookie or secure storage)
  → User redirected to dashboard
```

### Authenticated Request
```
Request → AuthMiddleware
  → Extract Bearer token
  → Validate JWT signature + expiry
  → Lookup user + permissions
  → Attach CurrentUser to request context
  → RBAC check (if endpoint requires specific permissions)
  → Allow / Deny
```

### Token Refresh
```
Token expired → 401 Response
  → Frontend interceptor catches 401
  → POST /api/v1/auth/refresh {refresh_token}
  → AuthService.refresh()
    → Validate refresh_token
    → Rotate tokens (issue new access + refresh)
    → Invalidate old refresh_token
  → Retry original request with new access_token
```

---

## 5. AI Flow

```
User asks a question (e.g., "Why did inventory value increase?")
  │
  ▼
AI Controller receives request
  │
  ▼
Context Builder fetches relevant ERP data via Services
  │  (InventoryService, SupplierService, AnalyticsService, etc.)
  │  Returns structured context (never raw SQL or ORM objects)
  ▼
Prompt Service loads prompt from file + injects context variables
  │
  ▼
AI Service sends to OpenRouter
  │  Model receives: system prompt + context + user question
  │  Model returns: structured JSON
  ▼
Structured Output Service validates against Pydantic schema
  │  If invalid → retry (up to configurable max)
  │  If valid → return DTO
  ▼
Response formatted + logged (tokens, cost, latency)
  │
  ▼
User receives AI response with citations, recommendations, follow-ups
```

### AI Governance Boundary
```
┌──────────────────────────────────────────────┐
│                AI LAYER                       │
│  May: explain, summarize, compare, recommend  │
│  ─────────────────────────────────────────── │
│  Never: calculate, approve, modify, execute   │
└──────────────┬───────────────────────────────┘
               │ Tool Runtime (controlled)
               ▼
┌──────────────────────────────────────────────┐
│           BUSINESS LOGIC LAYER                │
│  Deterministic calculations, validations,     │
│  business rules, transactions                 │
└──────────────┬───────────────────────────────┘
               │ Repository
               ▼
┌──────────────────────────────────────────────┐
│              DATABASE                         │
│  Source of truth                              │
└──────────────────────────────────────────────┘
```

---

## 6. Database Flow

### Write Path
```
Controller receives write request
  → Pydantic validation (DTO)
  → Permission check
  → Service method
    → Business rule validation
    → Begin transaction (Unit of Work)
    → Apply business logic
    → Repository.save() / update() / delete()
    → Commit transaction
    → Create audit log
  → Return response DTO
```

### Read Path
```
Controller receives read request
  → Pydantic validation (Filter DTO)
  → Permission check
  → Service method
    → Repository query
    → Apply filters, sorting, pagination
    → Execute query
    → Map to response DTOs
  → Return paginated response
```

### Migration Flow
```
Developer creates migration: alembic revision -m "description"
  → auto-generates upgrade() and downgrade()
  → Review and adjust manually
  → alembic upgrade head (applied on startup in production)
```

---

## 7. Business Simulation Flow

```
Simulation Scheduler (APScheduler)
  │
  ├─ Every tick (configurable interval):
  │   1. Evaluate current scenario rules
  │   2. Select random business events (weighted by scenario)
  │   3. Execute events through existing Business Services
  │      (never bypass services — uses same path as real users)
  │   4. Record events in Event Log
  │   5. Update Simulation Dashboard
  │
  └─ Events include:
      - Customer orders (inventory consumption)
      - Supplier shipments (inventory receipt)
      - Purchase requests/orders
      - Warehouse transfers
      - Stock adjustments (damage, expiry)
      - Supplier delays
      - Price fluctuations
```

---

## 8. Workflow Automation Flow

```
Trigger detected (e.g., inventory below safety stock)
  │
  ▼
Workflow Engine evaluates conditions
  │
  ├─ Conditions met → Proceed
  │    ├─ Action: Generate draft PO
  │    ├─ Action: Create notification
  │    ├─ Action: Request approval
  │    └─ Action: Execute (after approval)
  │
  └─ Conditions not met → Skip / Log
  │
  ▼
Execution recorded in audit trail
```

---

## 9. Security Architecture

### Defense in Depth
```
Layer 1: Network — HTTPS, CORS policy
Layer 2: Application — Input validation, output sanitization, JWT
Layer 3: Authorization — RBAC, permission decorators
Layer 4: Data — Parameterized queries, encryption at rest
Layer 5: Audit — Every sensitive action logged
```

### Permission Model
```
User ─┬─► Roles ─┬─► Permissions
      │          │
      │          ├─ Inventory.Read
      │          ├─ Inventory.Write
      │          ├─ PurchaseOrders.Approve
      │          └─ ...
      │
      └─► Direct Permissions (optional override)
```

---

## 10. Deployment Architecture

### Development
```
┌──────────────────┐    ┌──────────────────┐
│ Next.js Dev       │    │ FastAPI (Uvicorn) │
│ localhost:3000    │───►│ localhost:8000     │
└──────────────────┘    └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Neon PostgreSQL   │
                        │ (cloud dev branch) │
                        └──────────────────┘
```

### Production (Docker Compose)
```
┌──────────────────┐    ┌──────────────────┐
│ Frontend Container│    │ Backend Container │
│ Next.js (built)   │───►│ FastAPI (Uvicorn) │
│ Port: 3000        │    │ Port: 8000        │
└──────────────────┘    └────────┬─────────┘
                                 │
                        ┌────────▼─────────┐
                        │ Neon PostgreSQL   │
                        │ (cloud prod)      │
                        └──────────────────┘
```

---

## 11. Monorepo Structure

```
procureflow/
├── frontend/          # Next.js 15 application
│   ├── app/           # App Router pages
│   ├── components/    # Shared UI components
│   ├── features/      # Feature-specific modules
│   ├── hooks/         # Custom React hooks
│   ├── providers/     # Context providers
│   ├── services/      # API client services
│   ├── lib/           # Utility functions
│   ├── types/         # TypeScript types
│   └── styles/        # Global styles
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # Route handlers (controllers)
│   │   ├── models/    # SQLAlchemy models (by domain)
│   │   ├── schemas/   # Pydantic DTOs
│   │   ├── services/  # Business logic
│   │   ├── repositories/ # Data access
│   │   ├── dependencies/ # DI providers
│   │   ├── middleware/   # Auth, logging, CORS
│   │   ├── core/      # Configuration, exceptions
│   │   ├── utils/     # Utility functions
│   │   └── ai/        # AI platform
│   │       ├── providers/
│   │       ├── services/
│   │       ├── prompts/
│   │       ├── schemas/
│   │       ├── runtime/
│   │       └── tools/
│   ├── migrations/    # Alembic migrations
│   ├── tests/
│   └── alembic.ini
├── shared/            # Shared types/constants
├── docs/              # Documentation
├── docker/            # Docker configs
├── scripts/           # Utility scripts
├── .github/           # CI/CD, templates
└── docker-compose.yml
```

---

## 12. Key Architectural Principles

1. **Clean Architecture**: Controller → Service → Repository → Database. No shortcuts.
2. **Business Logic in Services Only**: Never in controllers, components, or repositories.
3. **AI as Intelligence Layer**: Explains, recommends, summarizes. Never decides.
4. **Transaction-Driven Inventory**: Every quantity change is an immutable transaction.
5. **Structured AI Outputs**: Every AI response validates against a Pydantic schema.
6. **Tool-Based AI Access**: AI accesses ERP only through approved tools that call services.
7. **Permission-Based Access**: Every endpoint validates authorization server-side.
8. **Auditability**: Every important action is logged with user, timestamp, and context.
9. **API Versioning**: All endpoints under /api/v1/ with backward compatibility.
10. **Observability**: Correlation IDs, structured logging, performance metrics everywhere.
