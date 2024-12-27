"""On-disk document storage for workflows"""

import json
from typing import Any, List, Optional
import sqlite3

from fixpoint_common.constants import NULL_COL_ID
from fixpoint_common.types import Document
from fixpoint_common.errors import NotFoundError
from fixpoint_common._storage import definitions as storage_definitions
from fixpoint_common.utils.sql import ParamNameKind
from fixpoint_common.workflows.imperative._doc_storage import DocStorage
from fixpoint_common.workflows.imperative._doc_storage import _fix_doc_ids
from .shared import (
    get_document_query,
    create_document_query,
    update_document_query,
    list_documents_query,
)


class OnDiskDocStorage(DocStorage):
    """On-disk document storage for workflows"""

    _conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        with self._conn:
            self._conn.execute(storage_definitions.DOCS_SQLITE_TABLE)

    def get(
        self,
        org_id: str,
        id: str,  # pylint: disable=redefined-builtin
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        with self._conn:
            query, params = get_document_query(
                ParamNameKind.SQLITE,
                "documents",
                org_id,
                id=id,
                workflow_id=workflow_id,
                workflow_run_id=workflow_run_id,
            )
            dbcursor = self._conn.execute(query, params)
            row = dbcursor.fetchone()
            if not row:
                return None
            return self._load_row(row)

    def create(self, org_id: str, document: Document) -> None:
        document = _fix_doc_ids(document)
        query, params = create_document_query(
            ParamNameKind.SQLITE,
            "documents",
            org_id,
            document,
        )
        with self._conn:
            self._conn.execute(query, params)

    def update(self, org_id: str, document: Document) -> None:
        with self._conn:
            query, params = update_document_query(
                ParamNameKind.SQLITE,
                "documents",
                org_id,
                document,
            )
            cursor = self._conn.execute(query, params)
            if cursor.rowcount == 0:
                raise NotFoundError("Document not found")
            self._conn.commit()

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> List[Document]:
        with self._conn:
            query, params = list_documents_query(
                ParamNameKind.SQLITE,
                "documents",
                org_id,
                path=path,
                workflow_id=workflow_id,
                workflow_run_id=workflow_run_id,
                task=task,
                step=step,
            )
            dbcursor = self._conn.execute(query, params)
            return [self._load_row(row) for row in dbcursor]

    def _load_row(self, row: Any) -> Document:
        wid = row[1]
        if wid == NULL_COL_ID:
            wid = None
        wrid = row[2]
        if wrid == NULL_COL_ID:
            wrid = None

        return Document(
            id=row[0],
            workflow_id=wid,
            workflow_run_id=wrid,
            path=row[3],
            metadata=json.loads(row[4]),
            contents=row[5],
            versions=json.loads(row[8]),
            media_type=row[9],
        )
