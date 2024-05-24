from typing import Any, Dict


# this is a backwards compatibility function that is here because
# this lib v1.0.0 was initially released with only
# "sender" and "from_" as supported attributes.
# here because "from" is a reserved keyword
def replace_params(params: Dict[Any, Any]) -> Dict[Any, Any]:
    if "from" in params:
        return params
    if "from_" in params:
        params["from"] = params["from_"]
        params.pop("from_")
    elif "sender" in params:
        params["from"] = params["sender"]
        params.pop("sender")
    return params
