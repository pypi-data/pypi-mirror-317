# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
from functools import wraps

from openmind_hub import DatasetCardData


def dataset_infos_dict_to_dataset_card_data_wrapper(fn):
    @wraps(fn)
    def wrapper(self, dataset_card_data: DatasetCardData):
        if dataset_card_data["license"] is None:
            dataset_card_data["license"] = "unknown"
        return fn(self, dataset_card_data)

    return wrapper
