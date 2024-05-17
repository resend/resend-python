from typing import Any, Dict


# we need this workaround here because "from" is a reserved keyword
# in python, so accept either "sender" or "from_" in the SendParams class
def replace_params(params: Dict[Any, Any]) -> Dict[Any, Any]:
    if "from_" in params:
        params["from"] = params["from_"]
        params.pop("from_")
    elif "sender" in params:
        params["from"] = params["sender"]
        params.pop("sender")
    return params
