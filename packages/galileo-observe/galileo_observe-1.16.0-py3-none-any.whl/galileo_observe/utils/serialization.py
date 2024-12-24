from json import dumps
from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1


def serialize_to_str(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, BaseModel):
        return obj.model_dump_json()
    elif isinstance(obj, BaseModelV1):
        return obj.json()
    elif isinstance(obj, (Dict, List)):
        return dumps(obj)
    return str(obj)
