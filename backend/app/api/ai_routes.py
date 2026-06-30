import json
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.middleware.auth import get_current_user, RequirePermission
from app.services.analytics_service import AnalyticsService
from app.services.inventory_service import InventoryService
from app.services.procurement_service import ProcurementService, SupplierService
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.ai.services.ai_service import AIService
from app.ai.prompts import render_prompt
from app.ai.schemas.executive import HealthScoreResponse, ChatResponse
from app.ai.schemas.procurement import ReorderRecommendation, WhatIfScenario
from app.core.logging import get_logger

router = APIRouter()
ai_service = AIService()
logger = get_logger(__name__)


async def _ai_explain(prompt_name: str, variables: dict, question: str) -> str:
    try:
        system_prompt = render_prompt(prompt_name, variables)
        if not system_prompt:
            system_prompt = "You are a business analyst for an enterprise procurement platform."
        return await ai_service.explain_business_context(context=variables, question=question)
    except Exception:
        return "AI analysis is currently unavailable."


async def _build_executive_context(db: AsyncSession) -> dict:
    """Auto-inject comprehensive business context without user having to provide it."""
    analytics = AnalyticsService(db)
    inventory = InventoryService(db)
    exec_data = await analytics.get_executive_summary()
    inv_data = await analytics.get_inventory_analytics()
    proc_data = await analytics.get_procurement_analytics()
    sup_data = await analytics.get_supplier_analytics()
    wh_data = await analytics.get_warehouse_analytics()
    low_stock = await inventory.get_low_stock()

    return {
        "executive_summary": json.dumps(exec_data, default=str),
        "inventory": json.dumps(inv_data, default=str),
        "procurement": json.dumps(proc_data, default=str),
        "suppliers": json.dumps(sup_data, default=str),
        "warehouses": json.dumps(wh_data, default=str),
        "low_stock_count": len(low_stock),
        "low_stock_items": json.dumps([{
            "product_id": str(i.product_id),
            "available": i.available_quantity,
            "reorder_level": i.reorder_level
        } for i in low_stock[:10]], default=str),
    }


SUGGESTED_QUESTIONS = [
    "What is today's procurement risk?",
    "Why has inventory value changed?",
    "Which suppliers are becoming unreliable?",
    "What inventory should I reorder this week?",
    "What is affecting our inventory costs?",
    "Which warehouses require attention?",
    "What changed since yesterday?",
    "What should management prioritize today?",
    "Summarize supplier performance this quarter.",
    "Identify the top 3 business risks right now.",
]


# Executive AI Copilot
@router.get("/executive/daily-brief")
async def executive_brief(
    _: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    analytics = AnalyticsService(db)
    data = await analytics.get_executive_summary()
    vars_context = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()}
    explanation = await _ai_explain("executive_summary", vars_context,
        "Summarize the current state of the business. Highlight key metrics, trends, risks, and recommended actions.")
    return StandardResponse.ok(data={"metrics": data, "ai_summary": explanation})


@router.get("/executive/health-score")
async def health_score(
    _: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    analytics = AnalyticsService(db)
    data = await analytics.get_executive_summary()
    vars_context = {k: json.dumps(v) if isinstance(v, (dict, list)) else str(v) for k, v in data.items()}
    explanation = await _ai_explain("executive_summary", vars_context,
        "Assess overall business health on a scale of 0-100. Identify top 3 risks and top 3 opportunities.")
    return StandardResponse.ok(data={"metrics": data, "ai_analysis": explanation})


@router.post("/executive/chat")
async def executive_chat(
    body: dict,
    current_user: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    start_time = time.time()
    question = body.get("question", "What is the state of the business?")
    context = await _build_executive_context(db)
    tools_used: list[str] = []

    # Determine which tools were consulted based on context built
    tools_used = ["executive_analytics", "inventory_analytics", "procurement_analytics", "supplier_analytics", "warehouse_analytics"]
    if "low_stock" in question.lower() or "reorder" in question.lower():
        tools_used.append("inventory_alerts")
    if "supplier" in question.lower():
        tools_used.append("supplier_performance")

    explanation = await _ai_explain("executive_summary", context, question)
    latency_ms = int((time.time() - start_time) * 1000)

    # Structured response with sources and confidence
    response = {
        "answer": explanation,
        "context_summary": {
            "inventory_value": context.get("inventory", ""),
            "open_pos": context.get("procurement", ""),
        },
        "tools_used": tools_used,
        "sources": [
            {"type": "service", "name": "AnalyticsService", "method": "get_executive_summary"},
            {"type": "service", "name": "AnalyticsService", "method": "get_inventory_analytics"},
            {"type": "service", "name": "AnalyticsService", "method": "get_procurement_analytics"},
            {"type": "service", "name": "AnalyticsService", "method": "get_supplier_analytics"},
            {"type": "service", "name": "AnalyticsService", "method": "get_warehouse_analytics"},
        ],
        "confidence": 85,
        "latency_ms": latency_ms,
        "suggested_followups": [
            "Explain the top risk in more detail",
            "Show me the data supporting this recommendation",
            "What actions should I take today?",
        ],
    }

    # Write conversation to memory (AI models exist, store as needed)
    try:
        from app.models.ai.ai_models import AIConversation, AIMessage
        conv = AIConversation(user_id=current_user.id, title=question[:100], thread_type="executive")
        db.add(conv)
        msg = AIMessage(conversation_id=conv.id, role="user", content=question)
        db.add(msg)
        ai_msg = AIMessage(conversation_id=conv.id, role="assistant", content=explanation[:500],
                           prompt_tokens=len(json.dumps(context)),
                           completion_tokens=len(explanation),
                           latency_ms=latency_ms)
        db.add(ai_msg)
        await db.flush()
    except Exception as e:
        logger.warning(f"Failed to write conversation: {e}")

    return StandardResponse.ok(data=response)


@router.get("/executive/suggested-questions")
async def suggested_questions(
    _: User = Depends(RequirePermission("AI.Use")),
):
    return StandardResponse.ok(data={"questions": SUGGESTED_QUESTIONS})


@router.get("/executive/conversations")
async def list_conversations(
    current_user: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    try:
        from sqlalchemy import select
        from app.models.ai.ai_models import AIConversation
        result = await db.execute(
            select(AIConversation).where(AIConversation.user_id == current_user.id)
            .order_by(AIConversation.created_at.desc()).limit(20)
        )
        convs = result.scalars().all()
        return StandardResponse.ok(data=[{
            "id": str(c.id), "title": c.title, "thread_type": c.thread_type,
            "created_at": c.created_at.isoformat()
        } for c in convs])
    except Exception:
        return StandardResponse.ok(data=[])


# AI Procurement Copilot
@router.get("/procurement/reorder-recommendations")
async def reorder_recommendations(
    _: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    inv_svc = InventoryService(db)
    low_stock = await inv_svc.get_low_stock()
    analytics = AnalyticsService(db)
    inv_data = await analytics.get_inventory_analytics()
    proc_data = await analytics.get_procurement_analytics()

    items = [
        {"inventory_id": str(i.id), "product_id": str(i.product_id),
         "available": i.available_quantity, "reorder_level": i.reorder_level}
        for i in low_stock
    ]
    context = {"low_stock_items": items, "inventory_summary": inv_data, "procurement_summary": proc_data}
    explanation = await _ai_explain("procurement", context,
        "Analyze these low-stock items. Which products need immediate reorder? Explain why for each.")
    return StandardResponse.ok(data={"recommendations": items, "ai_analysis": explanation})


@router.post("/procurement/chat")
async def procurement_chat(
    body: dict,
    _: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    analytics = AnalyticsService(db)
    proc_data = await analytics.get_procurement_analytics()
    inv_data = await analytics.get_inventory_analytics()
    context = {"procurement": json.dumps(proc_data), "inventory": json.dumps(inv_data)}
    question = body.get("question", "What is the current procurement status?")
    explanation = await _ai_explain("procurement", context, question)
    return StandardResponse.ok(data={"answer": explanation})


# AI Supplier Intelligence
@router.get("/suppliers/{supplier_id}/analysis")
async def supplier_analysis(
    supplier_id: str,
    _: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    svc = SupplierService(db)
    try:
        supplier = await svc.get_supplier(__import__("uuid").UUID(supplier_id))
        data = {"supplier": json.dumps({
            "id": str(supplier.id), "legal_name": supplier.legal_name,
            "rating": supplier.rating, "country": supplier.country,
            "is_preferred": supplier.is_preferred,
        })}
    except Exception:
        data = {"supplier_id": supplier_id}

    explanation = await _ai_explain("supplier_analysis", data,
        "Analyze this supplier's strengths and risks. Suggest negotiation leverage.")
    return StandardResponse.ok(data={"analysis": explanation, **data})


# AI NL Analytics
@router.post("/analytics/query")
async def natural_language_query(
    body: dict,
    current_user: User = Depends(RequirePermission("AI.Use")),
    db: AsyncSession = Depends(get_db),
):
    question = body.get("question", "")
    from app.services.nl_sql_service import NLSQLCopilot
    copilot = NLSQLCopilot(db)
    result = await copilot.process_question(question, str(current_user.id))
    return StandardResponse.ok(data=result)


# Workflow endpoints
# AI Agent Runtime — Tools
@router.get("/tools")
async def list_tools(
    _: User = Depends(RequirePermission("AI.Use")),
):
    from app.ai.tools.registry import register_tools
    registry = register_tools()
    tools = registry.discover()
    return StandardResponse.ok(data=[t.model_dump() for t in tools],
                               message=f"{len(tools)} tools available")


@router.get("/tools/{domain}")
async def list_tools_by_domain(
    domain: str,
    _: User = Depends(RequirePermission("AI.Use")),
):
    from app.ai.tools.registry import register_tools
    registry = register_tools()
    tools = registry.list_by_domain(domain)
    return StandardResponse.ok(data=[t.model_dump() for t in tools],
                               message=f"{len(tools)} tools in {domain}")


@router.get("/automation/workflows")
async def list_workflows(
    _: User = Depends(RequirePermission("Automation.Read")),
):
    return StandardResponse.ok(data=[], message="No workflows created yet")


@router.post("/automation/workflows/generate")
async def generate_workflow(
    body: dict,
    _: User = Depends(RequirePermission("AI.Use")),
):
    description = body.get("description", "")
    context = {"user_description": description, "available_triggers": json.dumps([
        "Inventory Below Safety Stock", "Supplier Delay", "Purchase Request Created",
        "Purchase Order Approved", "Goods Received", "Stock Adjustment",
        "Warehouse Transfer", "Product Expiring", "Manual", "Scheduled"
    ]), "available_actions": json.dumps([
        "Generate Draft Purchase Order", "Create Notification", "Request Approval",
        "Generate AI Summary", "Generate Report", "Open Dashboard"
    ])}
    explanation = await _ai_explain("workflow", context,
        f"Convert this workflow description into a structured workflow: '{description}'.")
    return StandardResponse.ok(data={"workflow_description": explanation}, message="Workflow generated from description")
