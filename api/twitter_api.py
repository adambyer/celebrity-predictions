import logging
import os
import requests
from typing import Optional

TWITTER_API_TOKEN = os.environ.get("TWITTER_API_TOKEN")
TWITTER_BASE_URL = "https://api.twitter.com/2"
logger = logging.getLogger(__name__)


def _get(url: str, params: dict = {}) -> Optional[dict]:
    url = f"{TWITTER_BASE_URL}{url}"
    headers = {
        "Authorization": "Bearer {}".format(TWITTER_API_TOKEN),
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
        logger.error(f"request error: {response.text} status: {response.status_code} url:{url}", extra=params)

    return None


def get_user_by_username(username: str) -> Optional[dict]:
    url = f"/users/by/username/{username}"
    params = {
        "user.fields": "description,profile_image_url,verified",
    }
    payload = _get(url, params)
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
    limit: Optional[int] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> list:
    """Get user tweets from Twitter.

    - If no times, returns the most recent tweets.
    """
    url = f"/users/{twitter_id}/tweets"
    params = {
        "max_results": 100,  # 100 is the max for each request
        "tweet.fields": "public_metrics,created_at",
    }

    if limit and limit < 100:
        params["max_results"] = limit

    if start_time:
        params["start_time"] = start_time

    if end_time:
        params["end_time"] = end_time

    tweets = None

    while (
        tweets is None
        or (
            "pagination_token" in params
            and (limit and len(tweets) < limit)
        )
    ):
        payload = _get(url, params)

        if payload and "data" in payload:
            tweets = (tweets or []) + payload["data"]
            next_token = payload["meta"].get("next_token")

            if next_token:
                params["pagination_token"] = next_token
            elif "pagination_token" in params:
                del params["pagination_token"]
        else:
            return []

    return tweets
