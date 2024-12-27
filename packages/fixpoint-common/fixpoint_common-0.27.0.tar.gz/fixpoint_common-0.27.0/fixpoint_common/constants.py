"""Constants shared across the package"""

__all__ = [
    "TASK_MAIN_ID",
    "STEP_MAIN_ID",
    "TASK_CLOSED_ID",
    "STEP_CLOSED_ID",
    "NULL_COL_ID",
    "API_BASE_URL",
    "DEFAULT_API_CLIENT_TIMEOUT",
    "DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES",
    "NO_AUTH_EMAIL",
    "NO_AUTH_ORG_ID",
    "NO_AUTH_USER_ID",
    "NO_AUTH_AUTH_TOKEN",
]

TASK_MAIN_ID = "__main__"
STEP_MAIN_ID = "__main__"

TASK_CLOSED_ID = "__closed__"
STEP_CLOSED_ID = "__closed__"

NULL_COL_ID = "__null__"

API_BASE_URL = "https://api.fixpoint.co"

DEFAULT_API_CLIENT_TIMEOUT = 10.0

# 50 MB
DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES = 50 * 1024 * 1024

NO_AUTH_ORG_ID = "org-__NO_AUTH__"
NO_AUTH_USER_ID = "user-__NO_AUTH__"
NO_AUTH_AUTH_TOKEN = "token-__NO_AUTH__"
NO_AUTH_EMAIL = "email-__NO_AUTH__"
