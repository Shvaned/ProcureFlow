"""Business Scenario Lab API — sandboxed simulation, never modifies production data."""
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.middleware.auth import get_current_user, RequirePermission
from app.services.scenario_service import ScenarioService
from app.models.identity.user import User
from app.schemas.common import StandardResponse

router = APIRouter()
_scenario_svc: ScenarioService | None = None


def get_scenario_service(db: AsyncSession = Depends(get_db)) -> ScenarioService:
    global _scenario_svc
    if _scenario_svc is None:
        _scenario_svc = ScenarioService(db)
    return _scenario_svc


@router.get("/scenarios/baseline")
async def get_baseline(
    _: User = Depends(RequirePermission("Scenario.Read")),
    svc: ScenarioService = Depends(get_scenario_service),
):
    data = await svc.get_baseline()
    return StandardResponse.ok(data=data)


@router.get("/scenarios/templates")
async def list_templates(
    _: User = Depends(RequirePermission("Scenario.Read")),
    svc: ScenarioService = Depends(get_scenario_service),
):
    data = await svc.get_templates()
    return StandardResponse.ok(data=data)


@router.post("/scenarios/run")
async def run_scenario(
    body: dict,
    _: User = Depends(RequirePermission("Scenario.Run")),
    svc: ScenarioService = Depends(get_scenario_service),
):
    name = body.get("name", "Custom Scenario")
    params = body.get("params", {})
    result = await svc.run_scenario(name, params)
    return StandardResponse.ok(data=result, message=f"Scenario '{name}' simulated")


@router.post("/scenarios/compare")
async def compare_scenarios(
    body: dict,
    _: User = Depends(RequirePermission("Scenario.Read")),
    svc: ScenarioService = Depends(get_scenario_service),
):
    ids = body.get("scenario_ids", [])
    result = await svc.compare_scenarios(ids)
    return StandardResponse.ok(data=result)


@router.get("/scenarios/{scenario_id}/advice")
async def get_ai_advice(
    scenario_id: str,
    _: User = Depends(RequirePermission("Scenario.Read")),
    svc: ScenarioService = Depends(get_scenario_service),
):
    result = await svc.get_ai_advice(scenario_id)
    return StandardResponse.ok(data=result)
