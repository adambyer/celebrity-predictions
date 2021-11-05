import json
import redis
from typing import Union

r = redis.Redis(
    host="localhost",
    port="6379",
    db=0,
)


def set_structure(key: str, value: Union[list, dict], ex: int = None) -> None:
    value_encoded = json.dumps(value)
    r.set(key, value_encoded, ex=ex)


def get_structure(key: str) -> Union[list, dict, None]:
    value = r.get(key)

    if value:
        return json.loads(value)

    return None
