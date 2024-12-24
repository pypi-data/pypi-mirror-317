# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
import importlib
import os

from packaging import version

from datasets import config
from datasets.utils.logging import get_logger

logger = get_logger(__name__)


def ms_adaptor_execution():
    use_ms = os.environ.get("USE_MS", "AUTO").upper()
    config.USE_MS = use_ms
    config.MS_AVAILABLE = False
    if use_ms in config.ENV_VARS_TRUE_AND_AUTO_VALUES:
        ms_available = importlib.util.find_spec("mindspore") is not None
        config.MS_AVAILABLE = ms_available
        if ms_available:
            try:
                ms_version = version.parse(importlib.metadata.version("mindspore"))
                config.MS_VERSION = ms_version
                logger.info(f"Mindspore version {ms_version} available.")

                from datasets.formatting import _register_formatter
                from openmind_datasets.ms.ms_formatter import MSFormatter

                _register_formatter(MSFormatter, "mindspore", aliases=["ms"])

                from datasets import Dataset
                from openmind_datasets.ms.ms_ds_convertor import to_ms_dataset

                setattr(Dataset, "to_ms_dataset", to_ms_dataset)
            except importlib.metadata.PackageNotFoundError:
                pass
