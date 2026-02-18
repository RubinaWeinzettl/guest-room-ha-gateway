"""FastAPI entry point for the guest-room Home Assistant gateway."""

import httpx

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel

from entities import LIGHTS
from config import get_settings

import entities
print("USING ENTITIES FROM:", entities.__file__)

settings = get_settings()
app = FastAPI()
app.state.ha_base_url = settings.ha_base_url
app.state.ha_token = settings.ha_token

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://guest-room-ha-gateway.ddev.site"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    """Return a basic liveness status for the service."""

    return {"status": "ok"}

@app.get("/ha-test")
def ha_test():
    """Call the Home Assistant REST API root endpoint and return its response."""

    url = f"{app.state.ha_base_url}/api/"
    headers = {"Authorization": f"Bearer {app.state.ha_token}"}

    try:
        resp = httpx.get(url, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text,
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


class LightCommand(BaseModel):
    """Request payload for switching a light on or off."""

    on: bool


@app.post("/api/lights/{alias}")
def set_light(alias: str, cmd: LightCommand):
    """Switch a whitelisted light entity on or off via Home Assistant.

    Args:
        alias: Public alias identifying the light to control.
        cmd: Command payload containing the desired on/off state.

    Returns:
        A small status object confirming what was requested.

    Raises:
        HTTPException: If alias is unknown or the HA call fails.
    """

    entity_id = LIGHTS.get(alias)
    if not entity_id:
        raise HTTPException(status_code=404, detail="Unknown light alias")

    service = "turn_on" if cmd.on else "turn_off"
    url = f"{app.state.ha_base_url}/api/services/light/{service}"
    headers = {"Authorization": f"Bearer {app.state.ha_token}"}
    payload = {"entity_id": entity_id}

    try:
        resp = httpx.post(url, headers=headers, json=payload, timeout=10.0)
        resp.raise_for_status()
        return {"alias": alias, "entity_id": entity_id, "on": cmd.on, "result": "ok"}
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text,
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
@app.get("/api/lights")
def list_lights():
    """Return all whitelisted light aliases."""
    return {"aliases": sorted(LIGHTS.keys())}

