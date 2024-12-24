#  Copyright (c) Huawei Technologies Co., Ltd. 2024-2024. All rights reserved.
import os
import warnings
from functools import partial
from pathlib import Path
from typing import Optional

import datasets
import huggingface_hub
import openmind_hub

import openmind_datasets.utils.logging
import openmind_datasets.utils.warning
from openmind_datasets.conf import DEFAULT_OM_HUB_ENDPOINT
from openmind_datasets.ms_adaptor import ms_adaptor_execution
from openmind_datasets.patches.info import dataset_infos_dict_to_dataset_card_data_wrapper
from openmind_datasets.patches.streaming_download_manager import prepare_single_hop_path_and_storage_options_wrapper


def config_adaptation():
    from datasets import config
    # Datasets
    hub_endpoint = os.environ.get("OPENMIND_HUB_ENDPOINT", DEFAULT_OM_HUB_ENDPOINT)
    config.S3_DATASETS_BUCKET_PREFIX = hub_endpoint
    config.CLOUDFRONT_DATASETS_DISTRIB_PREFIX = hub_endpoint
    config.REPO_DATASETS_URL = hub_endpoint
    # Metrics
    config.S3_METRICS_BUCKET_PREFIX = hub_endpoint
    config.CLOUDFRONT_METRICS_DISTRIB_PREFIX = hub_endpoint
    config.REPO_METRICS_URL = hub_endpoint + ("/api/v1/file/evaluate-metric/{path}/main/media/{name}")
    # Hub
    config.HF_ENDPOINT = hub_endpoint
    config.HUB_DATASETS_URL = config.HF_ENDPOINT + "/datasets/{repo_id}/resolve/{revision}/{path}"
    config.HUB_DATASETS_HFFS_URL = "om://datasets/{repo_id}@{revision}/{path}"
    # Cache location
    config.DEFAULT_HF_CACHE_HOME = os.path.join(config.XDG_CACHE_HOME, "openmind")
    config.HF_CACHE_HOME = os.path.expanduser(os.getenv("OM_HOME", config.DEFAULT_HF_CACHE_HOME))
    config.DEFAULT_HF_DATASETS_CACHE = os.path.join(config.HF_CACHE_HOME, "datasets")
    config.HF_DATASETS_CACHE = Path(os.getenv("HF_DATASETS_CACHE", config.DEFAULT_HF_DATASETS_CACHE))
    config.DEFAULT_HF_METRICS_CACHE = os.path.join(config.HF_CACHE_HOME, "metrics")
    config.HF_METRICS_CACHE = Path(os.getenv("HF_METRICS_CACHE", config.DEFAULT_HF_METRICS_CACHE))
    config.DEFAULT_HF_MODULES_CACHE = os.path.join(config.HF_CACHE_HOME, "modules")
    config.HF_MODULES_CACHE = Path(os.getenv("HF_MODULES_CACHE", config.DEFAULT_HF_MODULES_CACHE))
    config.DEFAULT_DOWNLOADED_DATASETS_PATH = os.path.join(config.HF_DATASETS_CACHE, config.DOWNLOADED_DATASETS_DIR)
    config.DOWNLOADED_DATASETS_PATH = Path(
        os.getenv("HF_DATASETS_DOWNLOADED_DATASETS_PATH", config.DEFAULT_DOWNLOADED_DATASETS_PATH))
    config.DEFAULT_EXTRACTED_DATASETS_PATH = os.path.join(config.DEFAULT_DOWNLOADED_DATASETS_PATH,
                                                          config.EXTRACTED_DATASETS_DIR)
    config.EXTRACTED_DATASETS_PATH = Path(
        os.getenv("HF_DATASETS_EXTRACTED_DATASETS_PATH", config.DEFAULT_EXTRACTED_DATASETS_PATH))
    # Download count for the website
    config.HF_UPDATE_DOWNLOAD_COUNTS = (
            os.environ.get("OM_UPDATE_DOWNLOAD_COUNTS", "AUTO").upper() in config.ENV_VARS_TRUE_AND_AUTO_VALUES
    )
    # Remote dataset scripts support
    __HF_DATASETS_TRUST_REMOTE_CODE = os.environ.get("OM_DATASETS_TRUST_REMOTE_CODE", "1")
    config.HF_DATASETS_TRUST_REMOTE_CODE: Optional[bool] = (
        True
        if __HF_DATASETS_TRUST_REMOTE_CODE.upper() in config.ENV_VARS_TRUE_VALUES
        else False
        if __HF_DATASETS_TRUST_REMOTE_CODE.upper() in config.ENV_VARS_FALSE_VALUES
        else None
    )
    # Offline mode
    config.HF_DATASETS_OFFLINE = os.environ.get("OM_DATASETS_OFFLINE", "AUTO").upper() in config.ENV_VARS_TRUE_VALUES
    # TL;DR: env variable has priority over code
    __OM_DATASETS_DISABLE_PROGRESS_BARS = os.environ.get("OM_DATASETS_DISABLE_PROGRESS_BARS")
    config.HF_DATASETS_DISABLE_PROGRESS_BARS: Optional[bool] = (
        __OM_DATASETS_DISABLE_PROGRESS_BARS.upper() in config.ENV_VARS_TRUE_VALUES
        if __OM_DATASETS_DISABLE_PROGRESS_BARS is not None
        else None
    )
    # In-memory
    config.IN_MEMORY_MAX_SIZE = float(
        os.environ.get("OM_DATASETS_IN_MEMORY_MAX_SIZE", config.DEFAULT_IN_MEMORY_MAX_SIZE))
    # File names
    config.REPOYAML_FILENAME = ".openmind.yaml"
    # Temporary cache directory prefix
    config.TEMP_CACHE_DIR_PREFIX = "om_datasets-"

    datasets.arrow_reader.HF_GCP_BASE_URL = hub_endpoint + "/api/v1/file"


def datasets_adaptation():
    datasets.arrow_dataset.CommitOperationAdd = openmind_hub.CommitOperationAdd
    datasets.arrow_dataset.CommitOperationDelete = openmind_hub.CommitOperationDelete
    datasets.arrow_dataset.DatasetCard = openmind_hub.DatasetCard
    datasets.arrow_dataset.DatasetCardData = openmind_hub.DatasetCardData
    datasets.arrow_dataset.HfApi = openmind_hub.OmApi
    datasets.arrow_dataset.HfApi.hf_hub_download = openmind_hub.OmApi.om_hub_download
    datasets.arrow_dataset.RepoFile = openmind_hub.RepoFile

    datasets.data_files.HfFileSystem = openmind_hub.OmFileSystem

    datasets.dataset_dict.CommitOperationAdd = openmind_hub.CommitOperationAdd
    datasets.dataset_dict.CommitOperationDelete = openmind_hub.CommitOperationDelete
    datasets.dataset_dict.DatasetCard = openmind_hub.DatasetCard
    datasets.dataset_dict.DatasetCardData = openmind_hub.DatasetCardData
    datasets.dataset_dict.HfApi = openmind_hub.OmApi
    datasets.dataset_dict.RepoFile = openmind_hub.RepoFile

    datasets.download.streaming_download_manager.EntryNotFoundError = openmind_hub.EntryNotFoundError
    datasets.builder.DatasetNotOnHfGcsError = openmind_hub.RepositoryNotFoundError
    datasets.builder.MissingFilesOnHfGcsError = openmind_hub.EntryNotFoundError
    datasets.exceptions.HfFileSystem = openmind_hub.OmFileSystem

    datasets.info.DatasetCard = openmind_hub.DatasetCard
    datasets.info.DatasetCardData = openmind_hub.DatasetCardData

    datasets.load.DatasetCard = openmind_hub.DatasetCard
    datasets.load.DatasetCardData = openmind_hub.DatasetCardData
    datasets.load.HfApi = openmind_hub.OmApi
    datasets.load.HfFileSystem = openmind_hub.OmFileSystem
    datasets.load.hf_dataset_url = partial(openmind_hub.om_hub_url, repo_type="dataset")

    datasets.utils.hub.HfApi = openmind_hub.OmApi
    datasets.utils.hub.RepoFile = openmind_hub.RepoFile
    datasets.utils.hub.hf_hub_url = partial(openmind_hub.om_hub_url, repo_type="dataset")
    datasets.load.hf_hub_url = partial(openmind_hub.om_hub_url, repo_type="dataset")
    datasets.utils.metadata.DatasetCardData = openmind_hub.DatasetCardData

    datasets.info.DatasetInfosDict.to_dataset_card_data = dataset_infos_dict_to_dataset_card_data_wrapper(
        datasets.info.DatasetInfosDict.to_dataset_card_data)
    datasets.download.streaming_download_manager._prepare_single_hop_path_and_storage_options = (
        prepare_single_hop_path_and_storage_options_wrapper(
            datasets.download.streaming_download_manager._prepare_single_hop_path_and_storage_options))


def hub_adaptation():
    huggingface_hub.HfApi = openmind_hub.OmApi
    huggingface_hub.hf_api.HfApi = openmind_hub.OmApi
    huggingface_hub.hf_api.RepoFile = openmind_hub.RepoFile
    huggingface_hub.hf_api.DatasetInfo = openmind_hub.DatasetInfo
    huggingface_hub.list_datasets = openmind_hub.list_datasets
    huggingface_hub.list_metrics = openmind_hub.list_metrics
    huggingface_hub.hf_hub_url = openmind_hub.om_hub_url
    huggingface_hub.CommitOperationAdd = openmind_hub.CommitOperationAdd
    huggingface_hub.CommitOperationDelete = openmind_hub.CommitOperationDelete
    huggingface_hub.DatasetCard = openmind_hub.DatasetCard
    huggingface_hub.DatasetCardData = openmind_hub.DatasetCardData
    huggingface_hub.HfFileSystem = openmind_hub.OmFileSystem
    huggingface_hub.utils.RepositoryNotFoundError = openmind_hub.RepositoryNotFoundError
    huggingface_hub.utils.EntryNotFoundError = openmind_hub.EntryNotFoundError
    huggingface_hub.utils.build_hf_headers = openmind_hub.build_om_headers
    huggingface_hub.hf_file_system.HfApi = openmind_hub.OmApi


def utils_adaptation():
    datasets.utils.logging.get_logger = openmind_datasets.utils.logging.get_logger
    datasets.logging.get_logger = openmind_datasets.utils.logging.get_logger
    warnings.warn = openmind_datasets.utils.warning.warning_wrapper(warnings.warn)


def openmind_adaptor_execution():
    from datasets import config

    use_om = os.environ.get("USE_OM", "AUTO").upper()
    om_endpoint = os.environ.get("OPENMIND_HUB_ENDPOINT")
    if om_endpoint is not None and ("huggingface" in om_endpoint or "hf" in om_endpoint):
        use_om = "FALSE"
    if use_om in config.ENV_VARS_TRUE_AND_AUTO_VALUES:
        hub_adaptation()
        datasets_adaptation()
        config_adaptation()
        utils_adaptation()


def exe_adaptation():
    # feature: use with openmind
    openmind_adaptor_execution()
    # feature: use with mindspore
    ms_adaptor_execution()


exe_adaptation()
