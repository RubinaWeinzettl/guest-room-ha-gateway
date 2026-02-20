"""Application configuration utilities for the FastAPI service.

This module loads required Home Assistant settings from a local `.env` file
using `python-dotenv` and exposes a typed settings object for application use.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Typed container for required Home Assistant configuration values.

    Attributes:
        ha_base_url: Base URL for the Home Assistant instance.
        ha_token: Long-lived access token used for Home Assistant API calls.
    """

    ha_base_url: str
    ha_token: str


def _load_local_env() -> None:
    """Load environment variables from the project's local `.env` file.

    The function attempts to load `.env` from the same directory as this
    module and does not override variables that are already present in the
    process environment.
    """

    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


def _require_env(name: str) -> str:
    """Return a required environment variable or raise a clear error.

    Args:
        name: Environment variable name to resolve.

    Returns:
        The non-empty environment variable value.

    Raises:
        RuntimeError: If the variable is missing or empty.
    """

    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable '{name}'. "
            "Define it in your local .env file."
        )
    return value


def get_settings() -> Settings:
    """Load and return Home Assistant settings for the application.

    Returns:
        A `Settings` instance populated from environment variables.
    """

    _load_local_env()
    return Settings(
        ha_base_url=_require_env("HA_BASE_URL"),
        ha_token=_require_env("HA_TOKEN"),
    )
