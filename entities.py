"""Whitelisted Home Assistant entities addressable by this gateway.

This module defines alias-to-entity-id mappings for supported domains.
Only entities listed here should be exposed to external callers.
"""

from __future__ import annotations

from typing import Final

LIGHTS: Final[dict[str, str]] = {...}
COVERS: Final[dict[str, str]] = {...}

LIGHTS: dict[str, str] = {
    "bath_light": "light.gastebad_licht",
    "bath_mirror": "light.gastebad_spiegel_licht",
    "room_couch": "light.gastezimmer_couch_licht_2",
    "room_main": "light.gastezimmer_licht",
}

COVERS: dict[str, str] = {
    "room_blind": "cover.gastezimmer_2",
}
