"""Workflow Automation API — CRUD, execution, simulation, approvals, templates, analytics."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.providers import get_db
from app.middleware.auth import RequirePermission
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.services.workflow_service import WorkflowService

router = APIRouter()


@router.get("/workflows")
async def list_workflows(
    _: User = Depends(RequirePermission("Automation.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    workflows = await svc.list_workflows()
    return StandardResponse.ok(data=workflows, message=f"{len(workflows)} workflows")


@router.get("/workflows/{wf_id}")
async def get_workflow(
    wf_id: uuid.UUID,
    _: User = Depends(RequirePermission("Automation.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    wf = await svc.get_workflow(wf_id)
    return StandardResponse.ok(data=wf)


@router.post("/workflows")
async def create_workflow(
    body: dict,
    current_user: User = Depends(RequirePermission("Automation.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    wf = await svc.create_workflow(body, current_user.id)
    return StandardResponse.ok(data=wf, message="Workflow created")


@router.put("/workflows/{wf_id}")
async def update_workflow(
    wf_id: uuid.UUID, body: dict,
    _: User = Depends(RequirePermission("Automation.Update")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    wf = await svc.update_workflow(wf_id, body)
    return StandardResponse.ok(data=wf, message="Workflow updated")


@router.delete("/workflows/{wf_id}")
async def delete_workflow(
    wf_id: uuid.UUID,
    _: User = Depends(RequirePermission("Automation.Delete")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    await svc.delete_workflow(wf_id)
    return StandardResponse.ok(message="Workflow deleted")


@router.post("/workflows/{wf_id}/publish")
async def publish_workflow(
    wf_id: uuid.UUID,
    _: User = Depends(RequirePermission("Workflow.Publish")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    wf = await svc.publish_workflow(wf_id)
    return StandardResponse.ok(data=wf, message="Workflow published")


@router.post("/workflows/{wf_id}/simulate")
async def simulate_workflow(
    wf_id: uuid.UUID,
    _: User = Depends(RequirePermission("Automation.Execute")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    result = await svc.simulate_workflow(wf_id)
    return StandardResponse.ok(data=result)


@router.post("/workflows/{wf_id}/execute")
async def execute_workflow(
    wf_id: uuid.UUID,
    current_user: User = Depends(RequirePermission("Automation.Execute")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    result = await svc.execute_workflow(wf_id, current_user.id)
    return StandardResponse.ok(data=result, message="Workflow executed")


@router.get("/workflows/executions")
async def get_executions(
    wf_id: uuid.UUID | None = None,
    _: User = Depends(RequirePermission("Automation.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    execs = await svc.get_execution_history(wf_id)
    return StandardResponse.ok(data=execs)


@router.get("/workflows/analytics")
async def workflow_analytics(
    _: User = Depends(RequirePermission("Automation.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    data = await svc.get_analytics()
    return StandardResponse.ok(data=data)


@router.get("/workflows/templates")
async def list_templates(
    _: User = Depends(RequirePermission("Automation.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    templates = await svc.get_templates()
    return StandardResponse.ok(data=templates)


@router.post("/workflows/templates/use")
async def use_template(
    body: dict,
    current_user: User = Depends(RequirePermission("Automation.Create")),
    db: AsyncSession = Depends(get_db),
):
    svc = WorkflowService(db)
    wf = await svc.create_from_template(body.get("template_name", ""), current_user.id)
    return StandardResponse.ok(data=wf, message="Workflow created from template")
