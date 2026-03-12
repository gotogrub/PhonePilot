from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class ScenarioStep(BaseModel):
    action: str
    target: str | None = None
    value: str | None = None
    wait: float | None = None
    condition: str | None = None


class Scenario(BaseModel):
    name: str
    description: str = ""
    steps: list[ScenarioStep]
    schedule: str | None = None


scenarios_db: dict[str, Scenario] = {}


@router.get("")
async def list_scenarios():
    return list(scenarios_db.values())


@router.post("")
async def create_scenario(scenario: Scenario):
    scenarios_db[scenario.name] = scenario
    return {"status": "created", "name": scenario.name}


@router.get("/{name}")
async def get_scenario(name: str):
    if name not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenarios_db[name]


@router.put("/{name}")
async def update_scenario(name: str, scenario: Scenario):
    if name not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    scenarios_db[name] = scenario
    return {"status": "updated"}


@router.delete("/{name}")
async def delete_scenario(name: str):
    if name not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    del scenarios_db[name]
    return {"status": "deleted"}


@router.post("/{name}/run")
async def run_scenario(name: str):
    if name not in scenarios_db:
        raise HTTPException(status_code=404, detail="Scenario not found")
    raise HTTPException(status_code=501, detail="Scenario execution not yet implemented")
