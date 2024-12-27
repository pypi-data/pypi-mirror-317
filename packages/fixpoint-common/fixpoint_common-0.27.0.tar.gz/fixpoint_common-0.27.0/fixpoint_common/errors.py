"""Package-wide errors and exceptions for Fixpoint."""

__all__ = [
    "FixpointException",
    "NotFoundError",
    "ConfigError",
]


class FixpointException(Exception):
    """The base class for all Fixpoint exceptions."""


class NotFoundError(FixpointException):
    """The requested resource was not found."""


class ConfigError(FixpointException):
    """Error in configuration"""


class UnauthorizedError(FixpointException):
    """The request is unauthorized."""
