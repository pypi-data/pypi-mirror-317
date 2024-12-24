# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.
# Copyright 2023 The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Note: This file is mainly copied from transformers.logger
# https://github.com/huggingface/transformers/blob/v4.35.2/src/transformers/utils/logging.py
import logging
import os
import re
import threading

from openmind_datasets.conf import OM_MAPPING

_lock = threading.Lock()
_global_handler = None

log_levels = {
    "detail": logging.DEBUG,  # self defined level, it will return full log info.
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

_default_log_level = logging.WARNING


def set_verbosity(verbosity: int) -> None:
    """Set the verbosity level for root logger"""

    _configure_library_root_logger()
    get_logger().setLevel(verbosity)


def set_verbosity_info():
    """Set the verbosity to the `INFO` level."""
    return set_verbosity(log_levels.get("info"))


def set_verbosity_warning():
    """Set the verbosity to the `WARNING` level."""
    return set_verbosity(log_levels.get("warning"))


def set_verbosity_debug():
    """Set the verbosity to the `DEBUG` level."""
    return set_verbosity(log_levels.get("debug"))


def set_verbosity_error():
    """Set the verbosity to the `ERROR` level."""
    return set_verbosity(log_levels.get("error"))


def set_verbosity_critical():
    """Set the verbosity to the `CRITICAL` level."""
    return set_verbosity(log_levels.get("critical"))


def _get_library_name() -> str:
    return __name__.split(".")[0]


def _get_default_logging_level():
    """
    If LOGGER_VERBOSITY env var is set to one of the valid choices return that as the
    new default level. If it is not - fall back to `_default_log_level`
    """
    env_level_str = os.getenv("LOGGER_VERBOSITY", None)
    if env_level_str:
        if env_level_str in log_levels:
            return log_levels[env_level_str]
        else:
            logging.getLogger().warning(
                f"Unknown option LOGGER_VERBOSITY={env_level_str}, " f"has to be one of: {', '.join(log_levels.keys())}"
            )
    return _default_log_level


def _configure_library_root_logger():
    global _global_handler
    with _lock:
        if _global_handler:
            return
        _global_handler = logging.StreamHandler()
        # Apply our default configuration to the library root logger.
        library_root_logger = logging.getLogger(_get_library_name())
        library_root_logger.addHandler(_global_handler)
        library_root_logger.setLevel(_get_default_logging_level())
        # if logging level is debug, we add pathname and lineno to formatter for easy
        # debugging
        if os.getenv("LOGGER_VERBOSITY", None) == "detail":
            formatter = logging.Formatter("[%(levelname)s|%(pathname)s:%(lineno)s] %(asctime)s >> %(message)s")
            _global_handler.setFormatter(formatter)
        library_root_logger.propagate = False


class StringFilter(logging.Filter):
    """
    replace some keywords for logger
    """

    def filter(self, record):
        # Cannot perform global keyword replacement, can only replace one sentence at a time.
        # In some cases, not replacing may be correct.
        if isinstance(record.msg, str):
            replace_dict = OM_MAPPING
            replace_dict = dict((re.escape(k), v) for k, v in replace_dict.items())
            pattern = re.compile("|".join(replace_dict.keys()))
            record.msg = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], record.msg)
        return True


def get_logger(name=None) -> logging.Logger:
    """
    Return a logger with the specified name. If name is not specified, return the root
    logger
    """
    if name is None:
        name = _get_library_name()

    _configure_library_root_logger()
    logger = logging.getLogger(name)
    logger.addFilter(StringFilter())
    return logger
