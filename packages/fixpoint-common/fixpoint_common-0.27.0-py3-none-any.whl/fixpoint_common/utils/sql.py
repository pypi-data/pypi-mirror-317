"""SQL utility code"""

__all__ = ["format_where_clause", "param", "ParamNameKind", "pg_format_where_clause"]

from enum import Enum
from typing import Any, Dict


class ParamNameKind(Enum):
    """In SQL query parameters, the kind of DB we are using

    Postgres and SQLite use different formats for representing query parameters,
    so we need to differentiate what kind of DB we are formatting queries for.
    """

    SQLITE: str = "sqlite"
    POSTGRES: str = "postgres"


def param(kind: ParamNameKind, param_name: str) -> str:
    """Format a query parameter for an SQL query"""
    if kind == ParamNameKind.SQLITE:
        return f":{param_name}"
    elif kind == ParamNameKind.POSTGRES:
        return f"%({param_name})s"
    else:
        raise ValueError(f"Invalid ParamNameKind: {kind}")


def format_where_clause(kind: ParamNameKind, conditions: Dict[str, Any]) -> str:
    """Format a WHERE clause for an SQL query"""

    if not conditions:
        return ""

    def _param(pn: str) -> str:
        return param(kind, pn)

    conditions_parts = []
    for key in conditions.keys():
        conditions_parts.append(f"{key} = {_param(key)}")

    conditions_str = " AND ".join(conditions_parts)
    return f"WHERE {conditions_str}"


def pg_format_where_clause(params: Dict[str, Any]) -> str:
    """
    Format a WHERE clause for a PostgreSQL query and return parameters.
    """
    return format_where_clause(ParamNameKind.POSTGRES, params)
