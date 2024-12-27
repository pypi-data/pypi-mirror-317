"""Shared query functions for human task storage"""

__all__ = (
    "get_query",
    "create_query",
    "update_query",
    "list_query",
)

import json
from typing import Any, Dict, Optional

from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import ListHumanTaskEntriesRequest
from fixpoint_common.utils.sql import ParamNameKind, param, format_where_clause


def get_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    id: str,  # pylint: disable=redefined-builtin
    workflow_id: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
) -> tuple[str, Dict[str, Any]]:
    """
    Generate a query to retrieve a human task entry.

    Args:
        kind (ParamNameKind): The type of parameter naming to use.
        table (str): The name of the table to query.
        org_id (str): The organization ID.
        id (str): The ID of the entry to retrieve.
        workflow_id (Optional[str]): The workflow ID, if applicable.
        workflow_run_id (Optional[str]): The workflow run ID, if applicable.

    Returns:
        tuple[str, Dict[str, Any]]: A tuple containing the query string and parameters.
    """
    params: Dict[str, Any] = {"id": id, "org_id": org_id}
    if workflow_id:
        params["workflow_id"] = workflow_id
    if workflow_run_id:
        params["workflow_run_id"] = workflow_run_id

    query = f"""
    SELECT
        id,
        task_id,
        workflow_id,
        workflow_run_id,
        status,
        metadata,
        source_node,
        created_at,
        updated_at,
        entry_fields
    FROM {table}
    """ + format_where_clause(
        kind, params
    )

    return query, params


def create_query(
    kind: ParamNameKind, table: str, org_id: str, task: Any
) -> tuple[str, Dict[str, Any]]:
    """
    Generate a query to create a new human task entry.

    Args:
        kind (ParamNameKind): The type of parameter naming to use.
        table (str): The name of the table to insert into.
        org_id (str): The organization ID.
        task (Any): The task object containing the data to insert.

    Returns:
        tuple[str, Dict[str, Any]]: A tuple containing the query string and parameters.
    """

    def _param(pn: str) -> str:
        return param(kind, pn)

    serialized_entry_fields = [ef.model_dump() for ef in task.entry_fields]
    query = f"""
    INSERT INTO {table} (
        id,
        task_id,
        workflow_id,
        workflow_run_id,
        status,
        metadata,
        source_node,
        created_at,
        updated_at,
        entry_fields,
        org_id
    )
    VALUES (
        {_param("id")},
        {_param("task_id")},
        {_param("workflow_id")},
        {_param("workflow_run_id")},
        {_param("status")},
        {_param("metadata")},
        {_param("source_node")},
        {_param("created_at")},
        {_param("updated_at")},
        {_param("entry_fields")},
        {_param("org_id")}
    )
    """
    params = {
        "id": task.id,
        "task_id": task.task_id,
        "workflow_id": task.workflow_id,
        "workflow_run_id": task.workflow_run_id,
        "status": task.status,
        "metadata": json.dumps(task.metadata),
        "source_node": task.source_node,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "entry_fields": json.dumps(serialized_entry_fields),
        "org_id": org_id,
    }
    return query, params


def update_query(
    kind: ParamNameKind, table: str, org_id: str, task: Any
) -> tuple[str, Dict[str, Any]]:
    """
    Generate a query to update an existing human task entry.

    Args:
        kind (ParamNameKind): The type of parameter naming to use.
        table (str): The name of the table to update.
        org_id (str): The organization ID.
        task (Any): The task object containing the updated data.

    Returns:
        tuple[str, Dict[str, Any]]: A tuple containing the query string and parameters.
    """

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
    UPDATE {table}
    SET status = {_param("status")},
        entry_fields = {_param("entry_fields")},
        metadata = {_param("metadata")}
    WHERE id = {_param("id")}
        AND workflow_id = {_param("workflow_id")}
        AND workflow_run_id = {_param("workflow_run_id")}
        AND org_id = {_param("org_id")}
    """
    params = {
        "status": task.status,
        "entry_fields": json.dumps([ef.model_dump() for ef in task.entry_fields]),
        "id": task.id,
        "workflow_id": task.workflow_id or NULL_COL_ID,
        "workflow_run_id": task.workflow_run_id or NULL_COL_ID,
        "org_id": org_id,
        "metadata": json.dumps(task.metadata),
    }
    return query, params


def list_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    req: ListHumanTaskEntriesRequest,
) -> tuple[str, Dict[str, Any]]:
    """
    Generate a query to list human task entries.

    Args:
        kind (ParamNameKind): The type of parameter naming to use.
        table (str): The name of the table to query.
        org_id (str): The organization ID.
        req (ListHumanTaskEntriesRequest): The request object containing
            optional query filters for the list of human tasks.
    Returns:
        tuple[str, Dict[str, Any]]: A tuple containing the query string and parameters.
    """
    params: Dict[str, Any] = {"org_id": org_id}
    if req.task_id:
        params["task_id"] = req.task_id
    if req.workflow_id:
        params["workflow_id"] = req.workflow_id
    if req.workflow_run_id:
        params["workflow_run_id"] = req.workflow_run_id
    if req.metadata:
        params["metadata"] = json.dumps(req.metadata)
    if req.status:
        params["status"] = req.status.value

    query = f"""
    SELECT
        id,
        task_id,
        workflow_id,
        workflow_run_id,
        status,
        metadata,
        source_node,
        created_at,
        updated_at,
        entry_fields
    FROM {table}
    """ + format_where_clause(
        kind, params
    )
    # Sampling size must be a positive integer
    if req.sampling_size is not None and req.sampling_size <= 0:
        raise ValueError("Sampling size must be a positive integer")

    if req.sampling_size is not None:
        query += f" ORDER BY random() LIMIT {param(kind, 'sampling_size')}"
        params["sampling_size"] = req.sampling_size

    return query, params
