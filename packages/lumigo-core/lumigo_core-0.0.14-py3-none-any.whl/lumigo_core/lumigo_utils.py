import decimal
import hashlib
import json
import time
from typing import Any, Dict, List


def get_current_ms_time() -> int:
    """
    :return: the current time in milliseconds
    """
    return int(time.time() * 1000)


class DecimalEncoder(json.JSONEncoder):
    # copied from python's runtime: runtime/lambda_runtime_marshaller.py:7-11
    def default(self, o: Any) -> Any:
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, (set, bytes)):
            return list(o)
        raise TypeError(
            f"Object of type {o.__class__.__name__} is not JSON serializable"
        )


class JsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, (set, bytes)):
            return list(o)
        return super(JsonEncoder, self).default(o)


def aws_dump(d: Any, decimal_safe: bool = False, **kwargs) -> str:  # type: ignore[no-untyped-def]
    if decimal_safe:
        return json.dumps(d, cls=DecimalEncoder, **kwargs)
    return json.dumps(d, cls=JsonEncoder, **kwargs)


def md5hash(d: Dict[Any, Any]) -> str:
    h = hashlib.md5()
    h.update(aws_dump(d, sort_keys=True).encode())
    return h.hexdigest()


# Function to convert ASCII values to a UTF-8 string
def ascii_to_string(ascii_array: List[int]) -> str:
    return "".join(chr(num) for num in ascii_array)


# Check if value is a list of integers
def is_number_list(lst: List[Any]) -> bool:
    return isinstance(lst, list) and all(isinstance(item, int) for item in lst)
