from typing import Union

from .cache import get_list, set_list
from .constants import CACHE_KEY_CELEBRITY_TWEETS, CELEBRITY_TWEETS_CACHE_SECONDS
from .crud import get_celebrity
from .db import Session
from .models import Celebrity
from .twitter import get_user_tweets


def get_tweets(celebrity_: Union[Celebrity, int]) -> list:
    db = Session()

    if isinstance(celebrity_, int):
        celebrity = get_celebrity(db, celebrity_)
    else:
        celebrity = celebrity_

    if not celebrity or not celebrity.twitter_id:
        return []

    cache_key = CACHE_KEY_CELEBRITY_TWEETS.format(celebrity.id)
    tweets = get_list(cache_key) or []

    if not tweets:
        tweets = get_user_tweets(celebrity.twitter_id, limit=10)
        set_list(cache_key, tweets, ex=CELEBRITY_TWEETS_CACHE_SECONDS)

    return tweets
