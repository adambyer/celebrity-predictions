import logging
import os
import requests
from typing import Optional

TWITTER_TOKEN = os.environ.get("TWITTER_API_TOKEN")
TWITTER_BASE_URL = "https://api.twitter.com/2"
logger = logging.getLogger(__name__)


def _get(url: str, params: dict = {}) -> Optional[dict]:
    url = f"{TWITTER_BASE_URL}{url}"
    headers = {
        "Authorization": "Bearer {}".format(TWITTER_TOKEN),
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
        )
    except requests.exceptions.ReadTimeout:
        logger.error(f"request read timeout: {url}")
        return None
    except Exception as e:
        logger.error(f"request exception: {str(e)}")
        return None

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"request error: status: {response.status_code}")

    return None


def get_user_by_username(username: str) -> Optional[dict]:
    url = f"/users/by/username/{username}"
    payload = _get(url)

    if payload:
        return payload["data"]

    return None


def get_users_by_usernames(usernames: list) -> Optional[list]:
    url = "/users/by"
    params = {
        "usernames": ",".join(usernames),
    }

    payload = _get(url, params)

    if payload:
        return payload["data"]

    return None
