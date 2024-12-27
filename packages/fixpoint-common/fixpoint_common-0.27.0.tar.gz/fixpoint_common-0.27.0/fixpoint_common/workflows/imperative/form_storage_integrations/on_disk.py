"""On-disk form storage for workflows"""

import json
from typing import Any, Dict, List, Optional
import sqlite3

from pydantic import BaseModel

from fixpoint_common.types import Form
from fixpoint_common._storage.definitions import FORMS_SQLITE_TABLE
from fixpoint_common.utils.sql import ParamNameKind
from fixpoint_common.workflows.imperative._form_storage import FormStorage
from .shared import (
    new_get_form_query,
    new_create_form_query,
    new_update_form_query,
    new_list_forms_query,
)


class OnDiskFormStorage(FormStorage):
    """On-disk form storage for workflows"""

    _conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        with self._conn:
            self._conn.execute(FORMS_SQLITE_TABLE)

    def get(
        self, org_id: str, id: str  # pylint: disable=redefined-builtin
    ) -> Optional[Form[BaseModel]]:
        with self._conn:
            query, args = new_get_form_query(
                ParamNameKind.SQLITE,
                "forms_with_metadata",
                org_id,
                id,
            )
            dbcursor = self._conn.execute(query, args)
            row = dbcursor.fetchone()
            if not row:
                return None
            return self._load_row(row)

    def create(self, org_id: str, form: Form[BaseModel]) -> None:
        with self._conn:
            query, params = new_create_form_query(
                ParamNameKind.SQLITE,
                "forms_with_metadata",
                org_id,
                form,
            )
            self._conn.execute(query, params)

    def update(self, org_id: str, form: Form[BaseModel]) -> None:
        with self._conn:
            query, params = new_update_form_query(
                ParamNameKind.SQLITE,
                "forms_with_metadata",
                org_id,
                form,
            )
            self._conn.execute(query, params)

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> List[Form[BaseModel]]:
        params: Dict[str, Any] = {}
        with self._conn:
            query, params = new_list_forms_query(
                ParamNameKind.SQLITE,
                "forms_with_metadata",
                org_id,
                path,
                workflow_run_id,
            )
            dbcursor = self._conn.execute(query, params)
            return [self._load_row(row) for row in dbcursor]

    def _load_row(self, row: Any) -> Form[BaseModel]:
        return Form.deserialize(
            {
                "id": row[0],
                "workflow_id": row[1],
                "workflow_run_id": row[2],
                "metadata": json.loads(row[3]),
                "path": row[4],
                "contents": json.loads(row[5]),
                "form_schema": json.loads(row[6]),
                "versions": json.loads(row[7]),
                "task": row[8],
                "step": row[9],
            }
        )
