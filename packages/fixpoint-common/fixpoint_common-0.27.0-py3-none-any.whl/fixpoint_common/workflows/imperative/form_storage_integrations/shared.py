"""Shared queries for form storage"""

__all__ = [
    "new_get_form_query",
    "new_create_form_query",
    "new_update_form_query",
    "new_list_forms_query",
]

import json
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel

from fixpoint_common.types import Form
from fixpoint_common.utils.sql import ParamNameKind, param, format_where_clause


def new_get_form_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    id: str,  # pylint: disable=redefined-builtin
) -> Tuple[str, Dict[str, str]]:
    """Make query and params for getting a form"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        SELECT
            id,
            workflow_id,
            workflow_run_id,
            metadata,
            path,
            contents,
            form_schema,
            versions,
            task,
            step
        FROM {table}
        WHERE id = {_param("id")}
        AND org_id = {_param("org_id")}
    """

    return query, {"id": id, "org_id": org_id}


def new_create_form_query(
    kind: ParamNameKind, table: str, org_id: str, form: Form[BaseModel]
) -> Tuple[str, Dict[str, str]]:
    """Make query and params for creating a form"""
    fdict = form.serialize()
    fdict["metadata"] = json.dumps(fdict["metadata"])
    fdict["contents"] = json.dumps(fdict["contents"])
    fdict["form_schema"] = json.dumps(fdict["form_schema"])
    fdict["versions"] = json.dumps(fdict["versions"])
    fdict["org_id"] = org_id

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        INSERT INTO {table} (
            id,
            workflow_id,
            workflow_run_id,
            metadata,
            path,
            contents,
            form_schema,
            versions,
            task,
            step,
            org_id
        ) VALUES (
            {_param("id")},
            {_param("workflow_id")},
            {_param("workflow_run_id")},
            {_param("metadata")},
            {_param("path")},
            {_param("contents")},
            {_param("form_schema")},
            {_param("versions")},
            {_param("task")},
            {_param("step")},
            {_param("org_id")}
        )
    """

    return query, fdict


def new_update_form_query(
    kind: ParamNameKind, table: str, org_id: str, form: Form[BaseModel]
) -> Tuple[str, Dict[str, str]]:
    """Make query and params for updating a form"""
    form_dict = {
        "id": form.id,
        "metadata": json.dumps(form.metadata),
        "contents": form.contents.model_dump_json(),
        "org_id": org_id,
    }

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        UPDATE {table}
        SET metadata = {_param("metadata")},
            contents = {_param("contents")}
        WHERE id = {_param("id")}
        AND org_id = {_param("org_id")}
    """

    return query, form_dict


def new_list_forms_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    path: Optional[str] = None,
    workflow_run_id: Optional[str] = None,
) -> Tuple[str, Dict[str, str]]:
    """Make query and params for listing forms"""
    params: Dict[str, Any] = {
        "org_id": org_id,
    }
    if path:
        params["path"] = path
    if workflow_run_id:
        params["workflow_run_id"] = workflow_run_id
    where_clause = format_where_clause(kind, params)

    query = f"""
        SELECT
            id,
            workflow_id,
            workflow_run_id,
            metadata,
            path,
            contents,
            form_schema,
            versions,
            task,
            step
        FROM {table}
        {where_clause}
    """

    return query, params
