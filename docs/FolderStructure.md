# ProcureFlow AI — Folder Structure

**Version:** 1.0.0
**Date:** 2026-06-30

---

## Root Structure

```
procureflow/
├── frontend/                    # Next.js 15 application
├── backend/                     # FastAPI application
├── shared/                      # Shared types, constants, validation
├── docs/                        # All project documentation
│   ├── api/                     # API documentation
│   ├── architecture/            # Architecture documentation
│   ├── diagrams/                # ER, sequence, flow diagrams
│   └── guides/                  # Developer, deployment, feature guides
├── docker/                      # Docker configuration files
├── scripts/                     # Build, deployment, utility scripts
├── .github/                     # GitHub Actions, templates
├── assets/                      # Static assets (logos, images)
├── docker-compose.yml           # Docker Compose configuration
├── docker-compose.prod.yml      # Production Docker Compose
├── .editorconfig                # Editor configuration
├── .gitignore                   # Git ignore rules
└── README.md                    # Project README
```

---

## Frontend Structure

```
frontend/
├── app/                         # Next.js App Router
│   ├── layout.tsx               # Root layout (providers, theme, metadata)
│   ├── page.tsx                 # Landing page
│   ├── loading.tsx              # Root loading state
│   ├── error.tsx                # Root error boundary
│   ├── not-found.tsx            # 404 page
│   ├── (auth)/                  # Auth route group
│   │   ├── login/
│   │   ├── forgot-password/
│   │   └── reset-password/
│   ├── (dashboard)/             # Protected dashboard route group
│   │   ├── layout.tsx           # Dashboard layout (sidebar, navbar)
│   │   ├── dashboard/           # Executive dashboard
│   │   ├── products/            # Product catalog
│   │   │   ├── page.tsx         # Product list
│   │   │   ├── new/
│   │   │   └── [id]/
│   │   ├── categories/
│   │   ├── brands/
│   │   ├── warehouses/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   ├── inventory/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   ├── transfers/
│   │   ├── adjustments/
│   │   ├── reservations/
│   │   ├── suppliers/
│   │   │   ├── page.tsx
│   │   │   ├── new/
│   │   │   └── [id]/
│   │   ├── purchase-orders/
│   │   │   ├── page.tsx
│   │   │   ├── new/
│   │   │   └── [id]/
│   │   ├── purchase-requests/
│   │   ├── grn/
│   │   ├── receipts/
│   │   ├── quotations/
│   │   ├── analytics/           # Analytics pages
│   │   ├── reports/
│   │   ├── kpis/
│   │   ├── ai/                  # AI workspace
│   │   │   ├── executive/
│   │   │   ├── procurement/
│   │   │   ├── suppliers/
│   │   │   ├── analytics/
│   │   │   └── automation/
│   │   ├── users/               # User management (admin)
│   │   ├── roles/               # Role management (admin)
│   │   ├── permissions/         # Permission management (admin)
│   │   ├── audit-logs/          # Audit log viewer
│   │   ├── settings/
│   │   └── profile/
│   └── (public)/                # Public pages
│       ├── landing/
│       └── docs/
├── components/                  # Shared UI components
│   ├── ui/                      # shadcn/ui components
│   ├── layout/                  # Layout components
│   │   ├── sidebar.tsx
│   │   ├── navbar.tsx
│   │   ├── breadcrumbs.tsx
│   │   ├── command-palette.tsx
│   │   └── footer.tsx
│   ├── data-table/              # TanStack Table wrapper
│   │   ├── data-table.tsx
│   │   ├── columns.tsx
│   │   ├── filters.tsx
│   │   ├── pagination.tsx
│   │   └── export.tsx
│   ├── charts/                  # Recharts wrappers
│   ├── forms/                   # Form components
│   ├── cards/                   # Card variants
│   ├── modals/                  # Modal variants
│   ├── skeletons/               # Loading skeletons
│   ├── empty-states/            # Empty state components
│   ├── error-states/            # Error state components
│   └── permission-gate/         # Permission-based rendering
├── features/                    # Feature-specific modules
│   ├── products/
│   ├── inventory/
│   ├── procurement/
│   ├── suppliers/
│   ├── warehouses/
│   ├── analytics/
│   └── ai/
├── hooks/                       # Custom React hooks
│   ├── use-auth.ts
│   ├── use-permissions.ts
│   ├── use-api.ts
│   ├── use-debounce.ts
│   ├── use-pagination.ts
│   └── use-local-storage.ts
├── providers/                   # Context providers
│   ├── theme-provider.tsx
│   ├── auth-provider.tsx
│   ├── query-provider.tsx
│   ├── toast-provider.tsx
│   └── command-provider.tsx
├── services/                    # API client services
│   ├── api-client.ts            # Base HTTP client
│   ├── auth.service.ts
│   ├── products.service.ts
│   ├── inventory.service.ts
│   ├── suppliers.service.ts
│   ├── procurement.service.ts
│   ├── analytics.service.ts
│   └── ai.service.ts
├── lib/                         # Utility functions
│   ├── utils.ts
│   ├── constants.ts
│   ├── validators.ts
│   ├── formatters.ts
│   ├── dates.ts
│   └── currency.ts
├── types/                       # TypeScript types
│   ├── api.ts
│   ├── auth.ts
│   ├── product.ts
│   ├── inventory.ts
│   ├── supplier.ts
│   ├── procurement.ts
│   └── ai.ts
├── styles/                      # Global styles
│   └── globals.css
├── public/                      # Static assets
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── .env.local.example
├── .eslintrc.json
├── .prettierrc
├── Dockerfile
└── package.json
```

---

## Backend Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration (env-driven)
│   ├── api/                     # Route handlers (controllers)
│   │   ├── __init__.py
│   │   ├── router.py            # Main API router (/api/v1)
│   │   ├── health.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── roles.py
│   │   ├── permissions.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   ├── brands.py
│   │   ├── units.py
│   │   ├── warehouses.py
│   │   ├── inventory.py
│   │   ├── transfers.py
│   │   ├── adjustments.py
│   │   ├── reservations.py
│   │   ├── suppliers.py
│   │   ├── purchase_orders.py
│   │   ├── purchase_requests.py
│   │   ├── grn.py
│   │   ├── receipts.py
│   │   ├── quotations.py
│   │   ├── invoices.py
│   │   ├── payments.py
│   │   ├── analytics.py
│   │   ├── reports.py
│   │   ├── simulation.py
│   │   ├── notifications.py
│   │   ├── audit.py
│   │   ├── files.py
│   │   └── ai/                  # AI-specific controllers
│   │       ├── executive.py
│   │       ├── procurement.py
│   │       ├── suppliers.py
│   │       ├── analytics.py
│   │       ├── tools.py
│   │       └── workflows.py
│   ├── models/                  # SQLAlchemy ORM models (by domain)
│   │   ├── base.py              # BaseEntity, mixins
│   │   ├── identity/
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── permission.py
│   │   │   └── session.py
│   │   ├── product/
│   │   │   ├── product.py
│   │   │   ├── category.py
│   │   │   ├── brand.py
│   │   │   ├── unit.py
│   │   │   └── attribute.py
│   │   ├── inventory/
│   │   │   ├── inventory.py
│   │   │   ├── transaction.py
│   │   │   ├── reservation.py
│   │   │   ├── adjustment.py
│   │   │   ├── transfer.py
│   │   │   └── snapshot.py
│   │   ├── warehouse/
│   │   │   ├── warehouse.py
│   │   │   ├── zone.py
│   │   │   └── bin.py
│   │   ├── supplier/
│   │   │   ├── supplier.py
│   │   │   ├── contact.py
│   │   │   ├── document.py
│   │   │   └── performance.py
│   │   ├── procurement/
│   │   │   ├── purchase_request.py
│   │   │   ├── purchase_order.py
│   │   │   ├── purchase_order_item.py
│   │   │   ├── approval.py
│   │   │   ├── grn.py
│   │   │   └── receipt.py
│   │   ├── finance/
│   │   │   ├── invoice.py
│   │   │   ├── payment.py
│   │   │   └── tax.py
│   │   ├── ai/
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   └── prompt.py
│   │   ├── automation/
│   │   │   ├── workflow.py
│   │   │   └── execution.py
│   │   ├── notification/
│   │   │   └── notification.py
│   │   └── audit/
│   │       └── audit_log.py
│   ├── schemas/                 # Pydantic DTOs (by domain)
│   │   ├── common.py            # StandardResponse, Pagination
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── warehouse.py
│   │   ├── supplier.py
│   │   ├── procurement.py
│   │   ├── analytics.py
│   │   └── ai.py
│   ├── services/                # Business logic (by domain)
│   │   ├── base.py              # BaseService, CRUDService
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── inventory_service.py
│   │   ├── warehouse_service.py
│   │   ├── supplier_service.py
│   │   ├── procurement_service.py
│   │   ├── analytics_service.py
│   │   ├── simulation_service.py
│   │   └── ai/
│   │       ├── ai_service.py
│   │       ├── prompt_service.py
│   │       ├── context_service.py
│   │       └── executive_service.py
│   ├── repositories/            # Data access (by domain)
│   │   ├── base.py              # BaseRepository, GenericRepository
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── inventory_repository.py
│   │   ├── warehouse_repository.py
│   │   ├── supplier_repository.py
│   │   └── procurement_repository.py
│   ├── dependencies/            # FastAPI DI providers
│   │   ├── database.py
│   │   ├── auth.py
│   │   ├── repositories.py
│   │   └── services.py
│   ├── middleware/               # FastAPI middleware
│   │   ├── auth.py
│   │   ├── rbac.py
│   │   ├── logging.py
│   │   ├── cors.py
│   │   └── rate_limit.py
│   ├── core/                    # Core infrastructure
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── exceptions_handlers.py
│   │   ├── security.py
│   │   ├── database.py
│   │   └── logging.py
│   ├── utils/                   # Utility functions
│   │   ├── pagination.py
│   │   ├── filtering.py
│   │   ├── sorting.py
│   │   ├── ids.py
│   │   └── dates.py
│   └── ai/                      # AI platform
│       ├── providers/           # AI provider implementations
│       │   ├── base.py
│       │   └── openrouter.py
│       ├── services/            # AI services
│       │   ├── context_builder.py
│       │   ├── structured_output.py
│       │   ├── token_service.py
│       │   └── cost_service.py
│       ├── prompts/             # Prompt files (.md)
│       │   ├── executive_summary.md
│       │   ├── procurement.md
│       │   ├── supplier_analysis.md
│       │   ├── catalog_generation.md
│       │   ├── analytics.md
│       │   ├── forecasting.md
│       │   ├── nl_sql.md
│       │   └── workflow.md
│       ├── schemas/             # AI output schemas
│       │   ├── executive.py
│       │   ├── procurement.py
│       │   ├── supplier.py
│       │   └── analytics.py
│       ├── runtime/             # AI agent runtime
│       │   ├── agent.py
│       │   ├── tool_registry.py
│       │   └── executor.py
│       ├── tools/               # ERP tools
│       │   ├── inventory.py
│       │   ├── supplier.py
│       │   ├── procurement.py
│       │   ├── warehouse.py
│       │   ├── executive.py
│       │   └── analytics.py
│       ├── registry/            # Model registry
│       │   └── model_registry.py
│       └── memory/              # Conversation memory
│           └── memory_service.py
├── migrations/                  # Alembic migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
├── tests/                       # Test suite
│   ├── unit/
│   ├── integration/
│   ├── factories/               # Test data factories
│   └── conftest.py
├── .env.example
├── pyproject.toml
├── Dockerfile
├── alembic.ini
└── requirements.txt
```

---

## Shared Structure

```
shared/
├── types/                       # Shared TypeScript types
├── constants/                   # Shared constants (status enums, etc.)
├── validation/                  # Shared validation schemas
└── README.md
```

---

## Key Organization Principles

1. **Domain-Driven**: Models, schemas, services, and repositories organized by business domain.
2. **Feature-Based Frontend**: Each feature has its own directory with components, hooks, and services.
3. **AI Isolated**: AI platform is a distinct module with its own providers, prompts, schemas, and tools.
4. **Documentation as Code**: All docs live inside the repo under `/docs`.
5. **No Flat Folders**: No domain folder should exceed 15 files — subdivide when needed.
6. **One Responsibility per File**: One class/service/model per file.
7. **Consistent Between Layers**: Frontend `services/` mirrors backend `api/` endpoints.
