# ProcureFlow AI — Coding Standards

**Version:** 1.0.0
**Date:** 2026-06-30

---

## 1. General Principles

- Prefer clarity over cleverness.
- Prefer composition over inheritance.
- Prefer small, focused modules over large classes.
- Prefer explicitness over magic.
- Code should be understandable by engineers unfamiliar with the project.
- Never optimize prematurely. Measure first.

---

## 2. Naming Conventions

### Python (Backend)

| Element | Convention | Example |
|---------|-----------|---------|
| Files | snake_case | `inventory_service.py` |
| Classes | PascalCase | `InventoryService` |
| Functions/Methods | snake_case | `calculate_reorder_point()` |
| Variables | snake_case | `inventory_transaction` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS` |
| Private members | _leading_underscore | `_validate_inventory()` |
| Modules | lowercase, short | `inventory`, `products` |

### TypeScript (Frontend)

| Element | Convention | Example |
|---------|-----------|---------|
| Files | kebab-case | `inventory-table.tsx` |
| Components | PascalCase | `InventoryTable` |
| Functions | camelCase | `calculateReorderPoint()` |
| Variables | camelCase | `inventoryTransaction` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS` |
| Types/Interfaces | PascalCase | `InventoryItem`, `IPurchaseOrder` |
| Hooks | use + PascalCase | `useInventory` |
| Providers | PascalCase + Provider | `AuthProvider` |

### Database

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | snake_case, plural | `purchase_orders` |
| Columns | snake_case | `created_at` |
| Foreign Keys | {table}_id | `supplier_id` |
| Indexes | ix_{table}_{column} | `ix_products_sku` |
| Unique Constraints | uq_{table}_{column} | `uq_products_barcode` |
| Enums | snake_case | `purchase_order_status` |

---

## 3. File Organization

### Python

```python
# File: inventory_service.py
# Order of contents:
# 1. Module docstring (only if non-obvious)
# 2. Imports (stdlib → third-party → local)
# 3. Module-level constants
# 4. Classes (one primary class per file)
# 5. Module-level helper functions (if any)
```

### TypeScript

```typescript
// File: inventory-table.tsx
// Order of contents:
// 1. Imports (React → third-party → local)
// 2. Types/interfaces
// 3. Constants
// 4. Component definition
// 5. Helper functions
// 6. Export
```

---

## 4. Backend Standards

### Controllers

```python
# Controllers only:
# - Receive requests
# - Validate inputs (Pydantic DTOs)
# - Check permissions (dependency injection)
# - Delegate to services
# - Return standard responses

# Never in controllers:
# - Business logic
# - Database access
# - Direct repository calls

@router.get("/inventory", response_model=StandardResponse[InventoryListResponse])
async def list_inventory(
    filters: InventoryFilterDTO = Depends(),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(RequirePermission("Inventory.Read")),
    inventory_service: InventoryService = Depends(get_inventory_service),
) -> StandardResponse[InventoryListResponse]:
    result = await inventory_service.list_inventory(filters, pagination)
    return StandardResponse.success(data=result)
```

### Services

```python
# Services contain:
# - Business rules
# - Validation logic
# - Transaction coordination
# - Workflow orchestration

# Never in services:
# - Database session management (use Unit of Work)
# - Direct HTTP concerns
# - Response formatting

class InventoryService:
    def __init__(self, repo: InventoryRepository, uow: UnitOfWork):
        self.repo = repo
        self.uow = uow

    async def create_transaction(self, dto: CreateTransactionDTO) -> InventoryTransaction:
        # Business rules here
        async with self.uow:
            transaction = await self.repo.create(dto)
            await self.uow.commit()
        return transaction
```

### Repositories

```python
# Repositories only:
# - Read from database
# - Write to database
# - Search, filter, paginate

# Never in repositories:
# - Business rules
# - External API calls
# - AI execution
# - HTTP concerns

class InventoryRepository(GenericRepository[Inventory, UUID]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Inventory)

    async def find_by_product_and_warehouse(
        self, product_id: UUID, warehouse_id: UUID
    ) -> Optional[Inventory]:
        ...
```

### Error Handling

```python
# Exception hierarchy
class ProcureFlowException(Exception):
    """Base exception for all application errors."""
    
class NotFoundException(ProcureFlowException):
    """Resource not found."""
    
class ValidationException(ProcureFlowException):
    """Input validation failed."""
    
class BusinessRuleException(ProcureFlowException):
    """Business rule violation."""
    
class AuthorizationException(ProcureFlowException):
    """Permission denied."""

# Global exception handler maps exceptions to HTTP responses
# Never expose stack traces in production
```

### API Response

```python
# Standard response format for every endpoint
class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    metadata: dict | None = None
    errors: list[str] | None = None
    request_id: str
    timestamp: datetime
```

---

## 5. Frontend Standards

### Component Organization

```typescript
// components/data-table/data-table.tsx
// One primary component per file
// Co-locate sub-components in same directory

export function DataTable<T>({
  columns,
  data,
  pagination,
  sorting,
  filters,
  onRowSelect,
}: DataTableProps<T>) {
  // Component logic
}
```

### State Management

```typescript
// Zustand for client state (auth, UI)
// TanStack Query for server state (API data)

// Client state example
const useAuthStore = create<AuthState>((set) => ({
  user: null,
  login: async (credentials) => { ... },
  logout: () => { ... },
}));

// Server state example
export function useInventory(filters: InventoryFilters) {
  return useQuery({
    queryKey: ['inventory', filters],
    queryFn: () => inventoryService.list(filters),
  });
}
```

### Forms

```typescript
// React Hook Form + Zod for all forms
const productSchema = z.object({
  sku: z.string().min(1, "SKU is required"),
  name: z.string().min(1, "Name is required"),
  price: z.number().positive("Price must be positive"),
});

type ProductForm = z.infer<typeof productSchema>;

function ProductForm() {
  const form = useForm<ProductForm>({
    resolver: zodResolver(productSchema),
  });
  // ...
}
```

### Data Tables

```typescript
// TanStack Table with:
// - Server-side pagination
// - Server-side sorting
// - Server-side filtering
// - Column visibility toggle
// - Row selection (single & bulk)
// - CSV export
// - Responsive layout (horizontal scroll on mobile)
```

### Error Boundaries

```typescript
// Every route segment should have error.tsx
// Global error boundary in root layout
// Feature-level error boundaries for AI failures

function ProductsError({ error, reset }: ErrorProps) {
  return (
    <ErrorState
      title="Failed to load products"
      message={error.message}
      action={<Button onClick={reset}>Try again</Button>}
    />
  );
}
```

---

## 6. Database Standards

### Migrations

```python
# Alembic migrations only — never manual schema changes
# Additive migrations preferred over destructive
# Every migration includes upgrade() and downgrade()

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('sku', sa.String(50), nullable=False, unique=True),
        ...
    )

def downgrade():
    op.drop_table('products')
```

### Model Standards

```python
# Every model inherits from BaseEntity
# Use UUID PKs, timestamp mixin, soft delete mixin

class Product(BaseEntity, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "products"
    
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # ...
```

### Query Standards

```python
# Always use parameterized queries (SQLAlchemy handles this)
# Never use raw SQL for CRUD operations
# Use repository methods for data access
# Optimize N+1 queries with joinedload/selectinload
```

---

## 7. AI Standards

### Prompts

```markdown
# Prompts stored in backend/app/ai/prompts/
# Markdown format with variable placeholders
# Variables: {{variable_name}}
# Never embed prompts in Python/TypeScript code
```

### Structured Outputs

```python
# Every AI response validates against a Pydantic schema
class ExecutiveSummary(BaseModel):
    business_health_score: int = Field(ge=0, le=100)
    health_explanation: str
    top_risks: list[RiskItem]
    top_opportunities: list[OpportunityItem]
    recommended_actions: list[ActionItem]

# Validation and retry
async def get_structured_output(prompt, schema):
    for attempt in range(MAX_RETRIES):
        response = await openrouter.complete(prompt)
        try:
            return schema.model_validate_json(response)
        except ValidationError:
            continue
    raise AIException("Failed to generate valid structured output")
```

### AI Boundaries

```python
# AI NEVER:
# - Accesses repositories directly
# - Executes SQL
# - Modifies business data
# - Makes financial calculations
# - Approves anything

# AI ONLY:
# - Explains, summarizes, compares, recommends, classifies
# - Communicates through approved Tools
# - Returns structured JSON
```

---

## 8. Testing Standards

### Python

```python
# pytest for all backend tests
# pytest-asyncio for async tests
# pytest-cov for coverage

# Test naming: test_{method}_{scenario}_{expected_result}
def test_create_product_with_duplicate_sku_raises_conflict():
    ...

# Test structure: Arrange → Act → Assert
# Mock external dependencies (OpenRouter, email, storage)
# Use test factories for data setup
# Every test is independent (no shared state)
```

### TypeScript

```typescript
// Vitest for frontend tests
// React Testing Library for components
// MSW for API mocking

describe('InventoryTable', () => {
  it('shows loading state while fetching data', () => { ... });
  it('shows empty state when no inventory', () => { ... });
  it('shows error state when API fails', () => { ... });
});
```

---

## 9. Git Standards

### Commits

```
Phase X: Brief description of what was implemented

Detailed explanation if needed. Focus on WHY, not WHAT.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### Branches

- `main` — production-ready code
- Phase work done directly on `main` (single-developer project)

### Quality Gates

Before every commit:
- Build passes (frontend + backend)
- Tests pass
- Lint passes
- Formatting passes

---

## 10. Code Quality Tools

### Python
- **Black**: Formatting (line length: 100)
- **isort**: Import sorting
- **Ruff**: Linting (replaces flake8, isort, pylint)
- **mypy**: Type checking (strict mode)

### TypeScript
- **ESLint**: Linting
- **Prettier**: Formatting
- **TypeScript**: Strict mode

### Pre-commit
- Runs on staged files before commit
- Black + isort + Ruff (Python)
- ESLint + Prettier (TypeScript)
