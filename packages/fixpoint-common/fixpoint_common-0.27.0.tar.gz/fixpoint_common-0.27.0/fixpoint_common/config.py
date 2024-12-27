"""Configuration settings"""

__all__ = [
    "DiskPaths",
    "get_env_api_url",
    "get_env_auth_disabled",
    "get_env_debug",
    "get_env_openai_api_key",
    "get_env_or_fail",
    "get_env_runmode",
    "get_env_value",
    "maybe_get_env_value",
    "prefer_val_or_must_get_env",
    "RunMode",
]

import os
from typing import Literal, Optional

from fixpoint_common.errors import ConfigError
from fixpoint_common.constants import API_BASE_URL


RunMode = Literal["postgres", "disk"]


def prefer_val_or_must_get_env(
    key: str, preferred: Optional[str] = None, default: Optional[str] = None
) -> str:
    """Get an environment variable or fail"""
    if preferred is not None:
        return preferred
    return get_env_or_fail(key, default)


def get_env_or_fail(key: str, default: Optional[str] = None) -> str:
    """Get an environment variable or fail"""
    value = os.environ.get(key, default)
    if value is None:
        raise ConfigError(f"Environment variable {key} is not set")
    return value


class DiskPaths:
    """Disk path for storage and config."""

    DEFAULT_PATH: str = os.path.expanduser("~/.cache/fixpoint")

    base_path: str

    def __init__(self, base_path: str):
        self.base_path = os.path.expanduser(base_path)

    def ensure_exists(self) -> None:
        """Ensure the base path exists"""
        os.makedirs(self.base_path, exist_ok=True)

    @property
    def agent_cache(self) -> str:
        """Path to the agent cache"""
        return os.path.join(self.base_path, "agent_cache")

    @property
    def callcache(self) -> str:
        """Path to the callcache"""
        return os.path.join(self.base_path, "callcache")

    @property
    def sqlite_path(self) -> str:
        """Path to the sqlite database"""
        return os.path.join(self.base_path, "db.sqlite")


def get_env_runmode(default: RunMode) -> RunMode:
    """Get the run mode from the environment"""
    run_mode = os.environ.get("RUN_MODE")
    if run_mode == "postgres":
        return "postgres"
    elif run_mode == "disk":
        return "disk"
    elif run_mode is None:
        return default
    else:
        raise ValueError(f"Invalid run mode: {run_mode}")


def get_env_api_url() -> str:
    """Get the API URL from the environment, or default value"""
    maybe = maybe_get_env_value("FIXPOINT_API_URL")
    if maybe:
        return maybe
    return os.environ.get("FIXPOINT_API_BASE_URL", API_BASE_URL)


def get_env_openai_api_key(override: Optional[str] = None) -> str:
    """Get the OpenAI API key from the environment"""
    return get_env_value("OPENAI_API_KEY", override=override)


def get_env_serp_api_key() -> str:
    """Get the SerpApi key for patents extraction from the environment"""
    return get_env_value("SERP_API_KEY")


def get_env_debug() -> bool:
    """Get the debug flag from the environment"""
    return get_env_value("DEBUG", default="false").lower() == "true"


def get_env_auth_disabled(default: Optional[str] = None) -> bool:
    """Get the auth disabled flag from the environment"""
    return get_env_value("AUTH_DISABLED", default=default).lower() == "true"


def maybe_get_env_value(
    key: str, *, override: Optional[str] = None, default: Optional[str] = None
) -> Optional[str]:
    """Get an environment variable or return None if it's not set"""
    if override:
        return override
    return os.environ.get(key, default)


def get_env_value(
    key: str, *, override: Optional[str] = None, default: Optional[str] = None
) -> str:
    """Get an environment variable or fail if it's not set"""
    if override:
        return override
    value = os.environ.get(key, default)
    if not value:
        raise ValueError(f"{key} environment variable not set")
    return value
