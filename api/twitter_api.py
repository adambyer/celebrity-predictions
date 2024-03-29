import logging
import os
import requests
from typing import Optional, List

TWITTER_API_TOKEN = os.environ.get("TWITTER_API_TOKEN")
TWITTER_BASE_URL = "https://api.twitter.com/2"
logger = logging.getLogger(__name__)


def _get(url: str, params: dict = {}) -> Optional[dict]:
    logging.info(f"Twitter API GET. url:{url} params:{str(params)}")
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
        logger.error(
            f"request error: {response.text} status: {response.status_code} "
            f"url:{url} params:{str(params)}"
        )

    return None


def _get_tweets_from_payload(payload: dict) -> list:
    media = {}
    if "includes" in payload and "media" in payload["includes"]:
        media = {m["media_key"]: m for m in payload["includes"]["media"]}

    tweets = payload["data"]

    # Media data is separate from the tweets in the response. Put them together.
    for tweet in tweets:
        if "media" not in tweet:
            tweet["media"] = []

        if "attachments" in tweet and "media_keys" in tweet["attachments"]:
            for media_key in tweet["attachments"]["media_keys"]:
                if media_key in media:
                    tweet["media"].append(media[media_key])

            del tweet["attachments"]

    return tweets


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
        "expansions": "attachments.media_keys",
        "media.fields": "preview_image_url,type,url,public_metrics",
    }

    if limit and limit < 100:
        params["max_results"] = limit

    if start_time:
        params["start_time"] = start_time

    if end_time:
        params["end_time"] = end_time

    tweets: Optional[List[dict]] = None

    while (
        tweets is None
        or (
            "pagination_token" in params
            and (limit and len(tweets) < limit)
        )
    ):
        payload = _get(url, params)

        if payload and "data" in payload:
            new_tweets = _get_tweets_from_payload(payload)
            tweets = (tweets or []) + new_tweets
            next_token = payload["meta"].get("next_token")

            if next_token:
                params["pagination_token"] = next_token
            elif "pagination_token" in params:
                del params["pagination_token"]
        else:
            return []

    return tweets
