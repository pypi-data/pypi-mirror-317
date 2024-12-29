from typing import Union, Dict, Any
from finalsa.common.lambdas.sqs.SqsEvent import SqsEvent
from pydantic import BaseModel


def get_handler_filled_args(attrrs: Dict[str, Any], payload: Union[Dict, str], parsed_event: SqsEvent) -> Dict:
    filled_args = {}
    for key, value in attrrs.items():
        if key == 'return':
            continue
        if isinstance(value, type):
            if issubclass(value, SqsEvent):
                filled_args[key] = parsed_event
                continue
            elif issubclass(value, BaseModel):
                filled_args[key] = value(**payload)
                continue
        if key == "message":
            filled_args[key] = payload
        elif key in payload:
            filled_args[key] = payload[key]
    return filled_args
