import json
import redis
from typing import Optional

r = redis.Redis(
    host="localhost",
    port="6379",
    db=0,
)


def set_list(key: str, value: list, ex: int = None) -> None:
    value_encoded = json.dumps(value)
    r.set(key, value_encoded, ex=ex)


def get_list(key: str) -> Optional[list]:
    value = r.get(key)

    if value:
        return json.loads(value)

    return None
