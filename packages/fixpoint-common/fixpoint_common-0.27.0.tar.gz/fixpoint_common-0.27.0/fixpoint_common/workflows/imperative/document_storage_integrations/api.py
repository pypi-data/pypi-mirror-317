"""On-disk document storage for workflows"""

from typing import Any, Dict, List, Optional
import requests

from fixpoint_common.types import Document
from fixpoint_common.utils.http import new_api_key_http_header
from fixpoint_common.workflows.imperative._doc_storage import DocStorage


class ApiDocStorage(DocStorage):
    """API-based document storage for workflows"""

    _api_base_url: str
    _timeout: int
    _api_key: str

    def __init__(self, api_base_url: str, api_key: str, timeout: int = 10):
        self._api_base_url = api_base_url
        self._timeout = timeout
        self._api_key = api_key

    def get(
        self,
        org_id: str,  # pylint: disable=unused-argument
        id: str,  # pylint: disable=redefined-builtin
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        # In the API `get` method, we don't need to specify the org_id because
        # the server will retrieve that information based on the API key.
        params: Dict[str, Any] = {"id": id}
        if workflow_id:
            params["workflow_id"] = workflow_id
        if workflow_run_id:
            params["workflow_run_id"] = workflow_run_id

        response = requests.get(
            f"{self._api_base_url}/documents/{id}",
            params=params,
            timeout=self._timeout,
            headers=new_api_key_http_header(self._api_key),
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        return self._load_row(data)

    def create(
        self,
        org_id: str,  # pylint: disable=unused-argument
        document: Document,
    ) -> None:
        # In the API `create` method, we don't need to specify the org_id
        # because the server will retrieve that information based on the API key.
        response = requests.post(
            f"{self._api_base_url}/documents",
            json=document.model_dump(),
            timeout=self._timeout,
            headers=new_api_key_http_header(self._api_key),
        )
        response.raise_for_status()

    def update(
        self,
        org_id: str,  # pylint: disable=unused-argument
        document: Document,
    ) -> None:
        # In the API `update` method, we don't need to specify the org_id
        # because the server will retrieve that information based on the API key.
        response = requests.put(
            f"{self._api_base_url}/documents/{document.id}",
            json=document.model_dump(),
            timeout=self._timeout,
            headers=new_api_key_http_header(self._api_key),
        )
        response.raise_for_status()

    def list(
        self,
        org_id: str,  # pylint: disable=unused-argument
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> List[Document]:
        # In the API `list` method, we don't need to specify the org_id because
        # the server will retrieve that information based on the API key.
        params: Dict[str, Any] = {}
        if path:
            params["path"] = path
        if workflow_id:
            params["workflow_id"] = workflow_id
        if workflow_run_id:
            params["workflow_run_id"] = workflow_run_id
        if task:
            params["task"] = task
        if step:
            params["step"] = step

        response = requests.get(
            f"{self._api_base_url}/documents",
            params=params,
            timeout=self._timeout,
            headers=new_api_key_http_header(self._api_key),
        )
        response.raise_for_status()
        data = response.json()
        return [self._load_row(row) for row in data]

    def _load_row(self, row: Dict[str, Any]) -> Document:
        return Document(
            id=row["id"],
            workflow_id=row.get("workflow_id"),
            workflow_run_id=row.get("workflow_run_id"),
            path=row["path"],
            metadata=row["metadata"],
            contents=row["contents"],
            versions=row["versions"],
        )
