from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.providers import get_db
from app.middleware.auth import RequirePermission
from app.models.identity.user import User
from app.schemas.common import StandardResponse
from app.services.simulation_service import SimulationService

router = APIRouter()

_simulation_service: SimulationService | None = None


def get_simulation_service(db: AsyncSession = Depends(get_db)) -> SimulationService:
    global _simulation_service
    if _simulation_service is None:
        _simulation_service = SimulationService(db)
    return _simulation_service


@router.get("/simulation/status")
async def get_status(
    _: User = Depends(RequirePermission("Simulation.Read")),
    svc: SimulationService = Depends(get_simulation_service),
):
    return StandardResponse.ok(data={
        "running": svc.state.running,
        "paused": svc.state.paused,
        "speed": svc.state.speed,
        "scenario": svc.state.scenario,
        "total_events": svc.state.total_events,
    })


@router.post("/simulation/start")
async def start_simulation(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.running = True
    svc.state.paused = False
    return StandardResponse.ok(message="Simulation started")


@router.post("/simulation/stop")
async def stop_simulation(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.running = False
    return StandardResponse.ok(message="Simulation stopped")


@router.post("/simulation/pause")
async def pause_simulation(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.paused = True
    return StandardResponse.ok(message="Simulation paused")


@router.post("/simulation/resume")
async def resume_simulation(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.paused = False
    return StandardResponse.ok(message="Simulation resumed")


@router.post("/simulation/event")
async def trigger_event(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    result = await svc.generate_business_event()
    return StandardResponse.ok(data=result, message="Event triggered")


@router.put("/simulation/scenario")
async def set_scenario(
    body: dict,
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.scenario = body.get("scenario", "normal")
    return StandardResponse.ok(message=f"Scenario set to {svc.state.scenario}")


@router.put("/simulation/speed")
async def set_speed(
    body: dict,
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    svc.state.speed = float(body.get("speed", 1.0))
    return StandardResponse.ok(message=f"Speed set to {svc.state.speed}x")


@router.get("/simulation/events")
async def get_events(
    _: User = Depends(RequirePermission("Simulation.Read")),
    svc: SimulationService = Depends(get_simulation_service),
):
    return StandardResponse.ok(data=svc.state.event_log[-50:])


@router.post("/simulation/seed")
async def seed_data(
    _: User = Depends(RequirePermission("Simulation.Manage")),
    svc: SimulationService = Depends(get_simulation_service),
):
    result = await svc.generate_seed_data()
    return StandardResponse.ok(data=result, message="Seed data generated")
