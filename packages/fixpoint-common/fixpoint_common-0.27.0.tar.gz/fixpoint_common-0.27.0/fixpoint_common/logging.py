"""Logging for the Fixpoint common code."""

__all__ = ["LOGGER_NAME", "CALLCACHE_LOGGER_NAME", "logger", "callcache_logger"]

import logging

LOGGER_NAME = "fixpoint_common"
CALLCACHE_LOGGER_NAME = "fixpoint_common.callcache"

logger = logging.getLogger(LOGGER_NAME)
callcache_logger = logger.getChild(CALLCACHE_LOGGER_NAME)
