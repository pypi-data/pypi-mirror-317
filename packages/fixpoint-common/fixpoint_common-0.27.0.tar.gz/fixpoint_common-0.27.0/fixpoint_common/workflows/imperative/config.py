"""Configuration for imperative workflows

Configuration for imperative workflows, such as setting up storage.
"""

from dataclasses import dataclass
from typing import List, Optional

import httpx

from fixpoint_common.sqlite import new_sqlite_conn
from fixpoint_common.config import get_env_api_url, DiskPaths
from fixpoint_common.workflows.human import HumanInTheLoop
from fixpoint_common.workflows.human._unsupported_client import (
    UnsupportedHumanInTheLoop,
)
from .document_storage_integrations.api import (
    ApiDocStorage,
)
from .form_storage_integrations import (
    OnDiskFormStorage,
)
from .document_storage_integrations import (
    OnDiskDocStorage,
)
from ._doc_storage import DocStorage
from ._form_storage import FormStorage
from ._workflow_storage import (
    WorkflowStorage,
    InMemWorkflowStorage,
    OnDiskWorkflowStorage,
    ApiWorkflowStorage,
)


@dataclass
class StorageConfig:
    """Storage configuration for imperative workflows and its agents, etc."""

    forms_storage: Optional[FormStorage]
    docs_storage: Optional[DocStorage]
    workflow_storage: WorkflowStorage
    human_storage: HumanInTheLoop

    @classmethod
    def with_defaults(
        cls,
    ) -> "StorageConfig":
        """Configure default storage"""
        return cls.with_in_memory()

    @classmethod
    def with_disk(
        cls,
        *,
        storage_path: str,
    ) -> "StorageConfig":
        """Configure disk storage"""
        disk_paths = DiskPaths(storage_path)
        disk_paths.ensure_exists()
        sqlite_conn = new_sqlite_conn(disk_paths.sqlite_path)
        doc_conn = sqlite_conn
        form_conn = sqlite_conn

        return cls(
            # TODO(dbmikus) support on-disk storage for forms and docs
            # https://linear.app/fixpoint/issue/PRO-40/add-on-disk-step-and-task-storage-for-workflows
            forms_storage=OnDiskFormStorage(form_conn),
            docs_storage=OnDiskDocStorage(doc_conn),
            workflow_storage=OnDiskWorkflowStorage(sqlite_conn),
            human_storage=UnsupportedHumanInTheLoop(),
        )

    @classmethod
    def with_in_memory(
        cls,
    ) -> "StorageConfig":
        """Configure in-memory storage"""

        return cls(
            forms_storage=None,
            docs_storage=None,
            workflow_storage=InMemWorkflowStorage(),
            human_storage=UnsupportedHumanInTheLoop(),
        )

    @classmethod
    def with_api(
        cls,
        api_key: str,
        api_url: str | None = None,
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "StorageConfig":
        """Configure API storage"""
        if api_url is None:
            api_base_url = get_env_api_url()
        else:
            api_base_url = api_url

        return cls(
            forms_storage=None,
            docs_storage=ApiDocStorage(api_base_url=api_base_url, api_key=api_key),
            workflow_storage=ApiWorkflowStorage(
                api_key, api_url, http_client, ahttp_client
            ),
            # TODO(dbmikus) support API-based human-in-the-loop storage
            human_storage=UnsupportedHumanInTheLoop(),
        )


_def_storage: List[Optional[StorageConfig]] = [None]


def get_default_storage_config() -> StorageConfig:
    """Gets the default storage config singleton"""
    if _def_storage[0] is None:
        storage_cfg = StorageConfig.with_defaults()
        _def_storage[0] = storage_cfg
        return storage_cfg
    else:
        return _def_storage[0]
