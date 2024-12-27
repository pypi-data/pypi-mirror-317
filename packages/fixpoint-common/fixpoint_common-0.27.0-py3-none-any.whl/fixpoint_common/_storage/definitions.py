"""Definitions for storage tables"""

__all__ = [
    "DOCS_SQLITE_TABLE",
    "DOCS_POSTGRES_TABLE",
    "MEMORIES_SQLITE_TABLE",
    "MEMORIES_POSTGRES_TABLE",
    "WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE",
    "WORKFLOW_RUN_ATTEMPTS_POSTGRES_TABLE",
]

DOCS_SQLITE_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    path text NOT NULL,
    metadata jsonb NOT NULL,
    contents text NOT NULL,
    task text NULL,
    step text NULL,
    versions jsonb NULL,
    org_id text NOT NULL,
    media_type text NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (org_id, id, workflow_id, workflow_run_id)
);
"""

DOCS_POSTGRES_TABLE = """
CREATE TABLE if NOT EXISTS fixpoint.documents (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    path text NOT NULL,
    metadata jsonb NOT NULL,
    contents text NOT NULL,
    task text NULL,
    step text NULL,
    versions jsonb NULL,
    org_id text NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (org_id, id, workflow_id, workflow_run_id)
);
"""

FORMS_SQLITE_TABLE = """
CREATE TABLE IF NOT EXISTS forms_with_metadata (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    metadata jsonb NULL,
    "path" text NOT NULL,
    contents jsonb NOT NULL,
    form_schema text NOT NULL,
    versions jsonb NULL,
    task text NULL,
    step text NULL,
    org_id text NOT NULL,
    CONSTRAINT forms_with_metadata_pkey PRIMARY KEY (org_id, id, workflow_id, workflow_run_id)
);
"""

FORMS_POSTGRES_TABLE = """
CREATE TABLE IF NOT EXISTS fixpoint.forms_with_metadata (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    metadata jsonb NULL,
    "path" text NOT NULL,
    contents jsonb NOT NULL,
    form_schema text NOT NULL,
    versions jsonb NULL,
    task text NULL,
    step text NULL,
    org_id text NOT NULL,
    CONSTRAINT forms_with_metadata_pkey PRIMARY KEY (org_id, id, workflow_id, workflow_run_id)
);
"""

MEMORIES_SQLITE_TABLE = """
CREATE TABLE IF NOT EXISTS memories (
    id text NOT NULL PRIMARY KEY,
    agent_id text NOT NULL,
    messages jsonb NOT NULL,
    completion jsonb NULL,
    workflow_id text NULL,
    workflow_run_id text NULL,
    created_at timestamptz DEFAULT CURRENT_TIMESTAMP NULL,
    task_id text NULL,
    step_id text NULL,
    metadata jsonb NULL,
    org_id text NOT NULL
);
"""

MEMORIES_POSTGRES_TABLE = """
CREATE TABLE IF NOT EXISTS fixpoint.memories (
    id text NOT NULL PRIMARY KEY,
    agent_id text NOT NULL,
    messages jsonb NOT NULL,
    completion jsonb NULL,
    workflow_id text NULL,
    workflow_run_id text NULL,
    created_at timestamptz DEFAULT now() NULL,
    embedding extensions.vector NULL,
    task_id text NULL,
    step_id text NULL,
    metadata jsonb NULL,
    org_id text NOT NULL
);
"""


WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE = """
CREATE TABLE IF NOT EXISTS workflow_run_attempts (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
    org_id text NOT NULL,
    CONSTRAINT workflow_run_attempts_pkey PRIMARY KEY (id)
);
"""

WORKFLOW_RUN_ATTEMPTS_POSTGRES_TABLE = """
CREATE TABLE IF NOT EXISTS fixpoint.workflow_run_attempts (
    id text NOT NULL,
    workflow_id text NOT NULL,
    workflow_run_id text NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
    org_id text NOT NULL,
    CONSTRAINT workflow_run_attempts_pkey PRIMARY KEY (id)
);
"""

HUMAN_TASKS_POSTGRES_TABLE = """
CREATE TABLE IF NOT EXISTS fixpoint.task_entries(
    id text NOT NULL,
    task_id text NULL,
    workflow_id text NULL,
    workflow_run_id text NULL,
    status text NOT NULL,
    metadata jsonb NULL,
    source_node text NULL,
    created_at timestamp DEFAULT now() NULL,
    updated_at timestamp DEFAULT now() NULL,
    entry_fields jsonb NOT NULL,
    org_id text NOT NULL,
    CONSTRAINT task_entries_pkey PRIMARY KEY (id)
);
"""

RESEARCH_RECORDS_POSTGRES_TABLE = """
CREATE TABLE IF NOT EXISTS fixpoint.research_records (
    id text NOT NULL PRIMARY KEY,
    org_id text NOT NULL,
    research_document_id text NOT NULL,
    source TEXT NOT NULL,
    source_type TEXT NOT NULL,
    fields jsonb NOT NULL,
    workflow_id TEXT NOT NULL,
    workflow_run_id TEXT NOT NULL,
    status text NOT NULL,
    source_node text NULL,
    metadata jsonb NULL,
    created_at timestamp DEFAULT now() NULL,
    updated_at timestamp DEFAULT now() NULL
);
"""
