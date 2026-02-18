"""Whitelisted Home Assistant entities addressable by this gateway.

This module defines alias-to-entity-id mappings for supported domains.
Only entities listed here should be exposed to external callers.
"""

from __future__ import annotations

from typing import Final

# Aliases for allowed `light` domain entities.
LIGHTS: Final[dict[str, str]] = {
    "ceiling": "light.guest_room_ceiling",
    "lamp": "light.guest_room_lamp",
}

# Aliases for allowed `cover` domain entities.
COVERS: Final[dict[str, str]] = {
    "blinds": "cover.guest_room_blinds",
    "shade": "cover.guest_room_shade",
}
