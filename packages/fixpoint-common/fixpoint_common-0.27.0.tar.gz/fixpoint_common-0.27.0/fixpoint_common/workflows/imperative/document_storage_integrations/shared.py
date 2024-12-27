"""Shared queries for document storage"""

__all__ = (
    "get_document_query",
    "create_document_query",
    "update_document_query",
    "list_documents_query",
)

import json
from typing import Any, Dict, Optional, Tuple

from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import Document
from fixpoint_common.utils.sql import ParamNameKind, param, format_where_clause


_select_columns = [
    "id",
    "workflow_id",
    "workflow_run_id",
    "path",
    "metadata",
    "contents",
    "task",
    "step",
    "versions",
    "media_type",
]

_create_columns = _select_columns + ["org_id"]


def get_document_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    id: str,  # pylint: disable=redefined-builtin
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for getting a document"""
    params: Dict[str, Any] = {"id": id, "org_id": org_id}
    if workflow_id:
        params["workflow_id"] = workflow_id
    if workflow_run_id:
        params["workflow_run_id"] = workflow_run_id

    where_clause = format_where_clause(kind, params)

    query = f"""
        SELECT
            {", ".join(_select_columns)}
        FROM {table}
        {where_clause}
    """
    return query, params


def create_document_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    document: Document,
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for creating a document"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    values = [_param(col) for col in _create_columns]

    query = f"""
        INSERT INTO {table} ({', '.join(_create_columns)})
        VALUES ({', '.join(values)})
    """

    doc_dict = document.model_dump()

    params = {
        "org_id": org_id,
        "id": doc_dict["id"],
        "workflow_id": doc_dict.get("workflow_id") or NULL_COL_ID,
        "workflow_run_id": doc_dict.get("workflow_run_id") or NULL_COL_ID,
        "path": doc_dict["path"],
        "metadata": json.dumps(doc_dict["metadata"]),
        "contents": doc_dict["contents"],
        "task": doc_dict.get("task"),
        "step": doc_dict.get("step"),
        "versions": json.dumps(doc_dict["versions"]),
        "media_type": doc_dict["media_type"],
    }
    return query, params


def update_document_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    document: Document,
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for updating a document"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    set_clause = ", ".join(
        [
            f"metadata = {_param('metadata')}",
            f"contents = {_param('contents')}",
            f"media_type = {_param('media_type')}",
        ]
    )

    query = f"""
        UPDATE {table}
        SET {set_clause}
        WHERE id = {_param("id")}
            AND workflow_id = {_param("workflow_id")}
            AND workflow_run_id = {_param("workflow_run_id")}
            AND org_id = {_param("org_id")}
    """

    doc_dict = document.model_dump()
    params = {
        "id": doc_dict["id"],
        "workflow_id": doc_dict.get("workflow_id") or NULL_COL_ID,
        "workflow_run_id": doc_dict.get("workflow_run_id") or NULL_COL_ID,
        "org_id": org_id,
        "metadata": json.dumps(doc_dict["metadata"]),
        "contents": doc_dict["contents"],
        "media_type": doc_dict["media_type"],
    }
    return query, params


def list_documents_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    *,
    path: Optional[str] = None,
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
    task: Optional[str] = None,
    step: Optional[str] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for listing documents"""
    params: Dict[str, Any] = {"org_id": org_id}
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

    where_clause = format_where_clause(kind, params)

    query = f"""
        SELECT
            id,
            workflow_id,
            workflow_run_id,
            path,
            metadata,
            contents,
            task,
            step,
            versions,
            media_type
        FROM {table}
        {where_clause}
    """
    return query, params
