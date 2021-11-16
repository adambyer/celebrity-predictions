from datetime import datetime

from .cache import get_structure, set_structure
from .constants import CACHE_KEY_CELEBRITY_TWEETS, CELEBRITY_TWEETS_CACHE_SECONDS
from .models import Celebrity
from .twitter_api import get_user_tweets
from .twitter_utils import get_tweet_metric_totals


def get_tweet_data(celebrity: Celebrity) -> dict:
    if not celebrity.twitter_id:
        return {
            "tweets": [],
            "metrics": {},
        }

    cache_key = CACHE_KEY_CELEBRITY_TWEETS.format(celebrity.id)
    tweet_data = get_structure(cache_key)

    if not tweet_data or not isinstance(tweet_data, dict):
        start_time = f"{datetime.combine(datetime.utcnow(), datetime.min.time()).isoformat()}Z"

        # Fetching all tweets from today so we can get metrics.
        tweets = get_user_tweets(celebrity.twitter_id, start_time=start_time)

        metrics = get_tweet_metric_totals(tweets)
        metrics["tweet_count"] = len(tweets)

        # But we also need the latest tweets regardless of date.
        tweets = [
            {
                "text": tweet["text"],
                "created_at": tweet["created_at"],
                "like_count": tweet["public_metrics"]["like_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
            }
            for tweet in get_user_tweets(celebrity.twitter_id, limit=10)
        ]

        tweet_data = {
            "tweets": tweets,
            "metrics": metrics,
        }
        set_structure(cache_key, tweet_data, ex=CELEBRITY_TWEETS_CACHE_SECONDS)

    return tweet_data
