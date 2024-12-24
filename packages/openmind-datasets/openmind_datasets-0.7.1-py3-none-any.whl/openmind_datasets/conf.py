from collections import OrderedDict

DEFAULT_OM_HUB = "modelers"
DEFAULT_OM_HUB_ADDRESS = "modelers.cn"
DEFAULT_OM_HUB_ENDPOINT = "https://modelers.cn"

OM_MAPPING = OrderedDict({"on huggingface.co": f"on {DEFAULT_OM_HUB_ADDRESS}",
                          "Hugging Face": DEFAULT_OM_HUB,
                          "hf.co": DEFAULT_OM_HUB_ADDRESS,
                          "HF google": DEFAULT_OM_HUB,
                          })
