"""Storage for workflow metadata (runs, attempts, etc.)"""

__all__ = [
    "WorkflowStorage",
    "InMemWorkflowStorage",
    "OnDiskWorkflowStorage",
    "ApiWorkflowStorage",
    "get_workflow_run_query",
    "store_workflow_run_query",
]

import sqlite3
from typing import Dict, Optional, Protocol, Tuple

import httpx

from fixpoint_common.constants import DEFAULT_API_CLIENT_TIMEOUT
from fixpoint_common.types import WorkflowRunAttemptData
from fixpoint_common.config import get_env_api_url
from fixpoint_common._storage.definitions import WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE
from fixpoint_common.utils.http import route_url, new_api_key_http_header
from fixpoint_common.utils.sql import ParamNameKind, param


class WorkflowStorage(Protocol):
    """Protocol for storing workflow metadata (runs, attempts, etc.)"""

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the latest stored workflow run attempt"""

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""

    async def async_get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Async gets the latest stored workflow run attempt"""

    async def async_store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Async stores the workflow run"""


class InMemWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data in memory

    In-memory workflow only works for a single org_id, so it just ignores the
    `org_id` arguments in its methods.
    """

    # key is run ID
    _runs: Dict[Tuple[str, str], WorkflowRunAttemptData]

    def __init__(self) -> None:
        self._runs: Dict[Tuple[str, str], WorkflowRunAttemptData] = {}

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the stored workflow run"""
        return self._runs.get((workflow_id, workflow_run_id), None)

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        self._runs[(workflow_run.workflow_id, workflow_run.workflow_run_id)] = (
            workflow_run
        )

    async def async_get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Async gets the latest stored workflow run attempt"""
        return self.get_workflow_run(org_id, workflow_id, workflow_run_id)

    async def async_store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Async stores the workflow run"""
        self.store_workflow_run(org_id, workflow_run)


def get_workflow_run_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    workflow_id: str,
    workflow_run_id: str,
) -> Tuple[str, Dict[str, str]]:
    """Generate a query to get the latest workflow run attempt"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        SELECT id, workflow_id, workflow_run_id FROM {table}
        WHERE
            workflow_id = {_param("workflow_id")}
            AND workflow_run_id = {_param("workflow_run_id")}
            AND org_id = {_param("org_id")}
        ORDER BY created_at DESC
        LIMIT 1
        """
    args = {
        "workflow_id": workflow_id,
        "workflow_run_id": workflow_run_id,
        "org_id": org_id,
    }
    return query, args


def store_workflow_run_query(
    kind: ParamNameKind, table: str, org_id: str, workflow_run: WorkflowRunAttemptData
) -> Tuple[str, Dict[str, str]]:
    """Generate a query to store a workflow run attempt"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        INSERT INTO {table}
            (id, workflow_id, workflow_run_id, org_id)
        VALUES ({','.join(_param(pn) for pn in ["id", "workflow_id", "workflow_run_id", "org_id"])})
        """
    args = {
        "id": workflow_run.attempt_id,
        "workflow_id": workflow_run.workflow_id,
        "workflow_run_id": workflow_run.workflow_run_id,
        "org_id": org_id,
    }
    return query, args


class OnDiskWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data on disk"""

    _conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        with self._conn:
            self._conn.execute(WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE)

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the stored workflow run"""
        with self._conn:
            query, args = get_workflow_run_query(
                ParamNameKind.SQLITE,
                "workflow_run_attempts",
                org_id,
                workflow_id,
                workflow_run_id,
            )
            cursor = self._conn.execute(query, args)
            row = cursor.fetchone()
            if row is None:
                return None
            attempt_id, wfid, wfrunid = row

        return WorkflowRunAttemptData(
            attempt_id=attempt_id,
            workflow_id=wfid,
            workflow_run_id=wfrunid,
        )

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        with self._conn:
            query, args = store_workflow_run_query(
                ParamNameKind.SQLITE,
                "workflow_run_attempts",
                org_id,
                workflow_run,
            )
            self._conn.execute(query, args)

    async def async_get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Async gets the latest stored workflow run attempt"""
        # TODO(dbmikus) actually make this async
        return self.get_workflow_run(org_id, workflow_id, workflow_run_id)

    async def async_store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Async stores the workflow run"""
        # TODO(dbmikus) actually make this async
        self.store_workflow_run(org_id, workflow_run)


class ApiWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data in the API"""

    _api_key: str
    _api_url: str
    _http_client: httpx.Client
    _async_http_client: httpx.AsyncClient

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
    ):
        self._api_key = api_key
        if api_url is None:
            api_url = get_env_api_url()
        self._api_url = api_url

        if http_client:
            self._http_client = http_client
        else:
            self._http_client = httpx.Client(timeout=DEFAULT_API_CLIENT_TIMEOUT)

        if async_http_client:
            self._async_http_client = async_http_client
        else:
            self._async_http_client = httpx.AsyncClient(
                timeout=DEFAULT_API_CLIENT_TIMEOUT
            )
        self._http_client.headers.update(new_api_key_http_header(self._api_key))
        self._async_http_client.headers.update(new_api_key_http_header(self._api_key))

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the latest stored workflow run attempt"""
        data = self._http_client.get(
            route_url(
                self._api_url,
                "workflows",
                workflow_id,
                "runs",
                workflow_run_id,
                "attempts",
                "latest",
            )
        )
        try:
            data.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise
        return WorkflowRunAttemptData.model_validate(data.json())

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        resp = self._http_client.post(
            route_url(
                self._api_url,
                "workflows",
                workflow_run.workflow_id,
                "runs",
                workflow_run.workflow_run_id,
                "attempts",
            ),
        )
        resp.raise_for_status()

    async def async_get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Async gets the latest stored workflow run attempt"""
        data = await self._async_http_client.get(
            route_url(
                self._api_url,
                "workflows",
                workflow_id,
                "runs",
                workflow_run_id,
                "attempts",
                "latest",
            )
        )
        data.raise_for_status()
        return WorkflowRunAttemptData.model_validate(data.json())

    async def async_store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Async stores the workflow run"""
        resp = await self._async_http_client.post(
            route_url(
                self._api_url,
                "workflows",
                workflow_run.workflow_id,
                "runs",
                workflow_run.workflow_run_id,
                "attempts",
            ),
        )
        resp.raise_for_status()
