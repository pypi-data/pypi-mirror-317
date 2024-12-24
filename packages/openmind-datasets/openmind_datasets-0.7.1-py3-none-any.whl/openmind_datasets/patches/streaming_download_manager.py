# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
from functools import wraps
from typing import Optional

from datasets import config
from datasets.download.download_config import DownloadConfig


def prepare_single_hop_path_and_storage_options_wrapper(fn):
    @wraps(fn)
    def wrapper(urlpath: str, download_config: Optional[DownloadConfig] = None):
        media_str = "/media"
        if urlpath.startswith(config.HF_ENDPOINT) and media_str in urlpath:
            api_str = "api/v1/file/"
            rindex = urlpath.find(api_str) + len(api_str)
            lindex = urlpath.rfind(media_str)
            repo_id, revision = urlpath[rindex:lindex].rsplit("/", 1)
            urlpath = "hf://datasets/" + repo_id + "@" + revision + urlpath[lindex + len(media_str):]
        return fn(urlpath, download_config)

    return wrapper
