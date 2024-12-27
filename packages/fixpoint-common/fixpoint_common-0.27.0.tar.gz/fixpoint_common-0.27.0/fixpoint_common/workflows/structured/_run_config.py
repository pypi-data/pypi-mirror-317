"""Configuration for running workflows."""

__all__ = [
    "RunConfig",
    "CallCacheConfig",
]

from dataclasses import dataclass
from typing import Optional

import diskcache
import httpx

from fixpoint_common.constants import DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES
from fixpoint_common.callcache import (
    CallCache,
    StepInMemCallCache,
    TaskInMemCallCache,
    StepDiskCallCache,
    TaskDiskCallCache,
    StepApiCallCache,
    TaskApiCallCache,
)
from fixpoint_common.config import (
    prefer_val_or_must_get_env,
    RunMode,
    get_env_runmode,
    get_env_api_url,
    DiskPaths,
)
from ..imperative import StorageConfig


_ONE_WEEK = 60 * 60 * 24 * 7


@dataclass
class CallCacheConfig:
    """Configuration for task and step call caches."""

    steps: CallCache
    tasks: CallCache


@dataclass
class RunConfigEnvOverrides:
    """Environment variable overrides for RunConfig"""

    storage_path: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None


@dataclass
class RunConfig:
    """Configuration for running workflows.

    Configuration for running workflows, such as the storage backends to use.
    """

    storage: StorageConfig
    call_cache: CallCacheConfig

    @classmethod
    def from_env(
        cls,
        default_mode: RunMode,
        env_overrides: Optional[RunConfigEnvOverrides] = None,
    ) -> "RunConfig":
        """Create a RunConfig from environment variables"""
        if env_overrides is None:
            env_overrides = RunConfigEnvOverrides()

        run_mode = get_env_runmode(default_mode)

        if run_mode == "disk":
            return RunConfig.with_disk(
                storage_path=prefer_val_or_must_get_env(
                    "STORAGE_PATH", env_overrides.storage_path
                ),
                callcache_ttl_s=_ONE_WEEK,
            )
        else:
            raise ValueError(f"Invalid run mode: {run_mode}")

    @classmethod
    def with_defaults(cls) -> "RunConfig":
        """Configure run for default backend"""
        return cls.with_in_memory()

    @classmethod
    def with_disk(
        cls,
        *,
        storage_path: str,
        callcache_ttl_s: int,
        callcache_size_limit_bytes: int = DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES,
    ) -> "RunConfig":
        """Configure run for disk storage"""
        disk_paths = DiskPaths(storage_path)
        disk_paths.ensure_exists()
        storage_config = StorageConfig.with_disk(storage_path=storage_path)
        callcache_dir = disk_paths.callcache
        call_cache = diskcache.Cache(
            directory=callcache_dir, size_limit=callcache_size_limit_bytes
        )
        call_cache_config = CallCacheConfig(
            steps=StepDiskCallCache(cache=call_cache, ttl_s=callcache_ttl_s),
            tasks=TaskDiskCallCache(cache=call_cache, ttl_s=callcache_ttl_s),
        )
        return cls(storage_config, call_cache_config)

    @classmethod
    def with_in_memory(cls) -> "RunConfig":
        """Configure run for in-memory storage"""
        storage = StorageConfig.with_in_memory()
        call_cache = CallCacheConfig(
            steps=StepInMemCallCache(),
            tasks=TaskInMemCallCache(),
        )
        return cls(storage, call_cache)

    @classmethod
    def with_api(
        cls,
        api_key: str,
        api_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "RunConfig":
        """Configure run for API backend"""
        if api_url is None:
            api_url = get_env_api_url()

        storage = StorageConfig.with_api(api_key, api_url, http_client, ahttp_client)
        call_cache = CallCacheConfig(
            steps=StepApiCallCache(api_key, api_url, http_client, ahttp_client),
            tasks=TaskApiCallCache(api_key, api_url, http_client, ahttp_client),
        )
        return cls(storage, call_cache)
