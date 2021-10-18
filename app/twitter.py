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
    return payload["data"] if payload else None


def get_users_by_usernames(usernames: list) -> Optional[list]:
    url = "/users/by"
    params = {
        "usernames": ",".join(usernames),
    }

    payload = _get(url, params)
    return payload["data"] if payload else None


def get_user_tweets(
    twitter_id: int,
    max_results: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> list:
    """If no times, returns the most recent tweets."""
    url = f"/users/{twitter_id}/tweets"
    params = {
        "max_results": 100,
        "tweet.fields": "public_metrics,created_at",
    }

    if max_results:
        params["max_results"] = max_results

    if start_time:
        params["start_time"] = start_time

    if end_time:
        params["end_time"] = end_time

    tweets = None

    while tweets is None or "pagination_token" in params:
        payload = _get(url, params)

        if payload:
            tweets = (tweets or []) + payload["data"]
            next_token = payload["meta"].get("next_token")

            if next_token:
                params["pagination_token"] = next_token
            else:
                del params["pagination_token"]
        else:
            tweets = []

    return tweets
