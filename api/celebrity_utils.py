from datetime import date, datetime, timedelta
import pytz

from .cache import get_structure, set_structure
from .constants import (
    CACHE_KEY_CELEBRITY_TWEETS,
    CELEBRITY_TWEETS_CACHE_SECONDS,
)
from .crud.celebrity_crud import get_celebrity_daily_metrics
from .db import Session
from .models import Celebrity
from .twitter_api import get_user_tweets
from .twitter_utils import get_tweet_metric_totals


def _format_date(d: date) -> str:
    return datetime(d.year, d.month, d.day, tzinfo=pytz.UTC).isoformat()


def get_tweet_data(
    db: Session,
    celebrity: Celebrity,
) -> dict:
    if not celebrity.twitter_id:
        return {
            "tweets": [],
            "metrics": {},
        }

    cache_key = CACHE_KEY_CELEBRITY_TWEETS.format(celebrity.id)
    tweet_data = get_structure(cache_key)

    if tweet_data and isinstance(tweet_data, dict):
        return tweet_data

    now = datetime.utcnow()
    start_time = f"{datetime.combine(now, datetime.min.time()).isoformat()}Z"

    # Fetching all tweets from today so we can get metrics.
    tweets = get_user_tweets(celebrity.twitter_id, start_time=start_time)

    todays_metrics = get_tweet_metric_totals(tweets)
    todays_metrics["tweet_count"] = len(tweets)

    start_date = (now - timedelta(days=5)).date()
    end_date = (now - timedelta(days=1)).date()
    celebrity_daily_metrics = get_celebrity_daily_metrics(db, celebrity.id, start_date, end_date)
    todays_metrics["metric_date"] = now.date().isoformat()
    metrics = [
        todays_metrics,
    ]

    if celebrity_daily_metrics:
        for m in celebrity_daily_metrics:
            metrics.append({
                "metric_date": m.metric_date.isoformat(),
                "like_count": m.like_count,
                "quote_count": m.quote_count,
                "reply_count": m.reply_count,
                "retweet_count": m.retweet_count,
                "tweet_count": m.tweet_count,
            })

    # But we also need the latest tweets regardless of date.
    tweets = [
        {
            "text": tweet["text"],
            "created_at": tweet["created_at"],
            "like_count": tweet["public_metrics"]["like_count"],
            "quote_count": tweet["public_metrics"]["quote_count"],
            "reply_count": tweet["public_metrics"]["reply_count"],
            "retweet_count": tweet["public_metrics"]["retweet_count"],
            "media": tweet["media"],
        }
        for tweet in get_user_tweets(celebrity.twitter_id, limit=10)
    ]

    tweet_data = {
        "tweets": tweets,
        "metrics": metrics,
    }
    set_structure(cache_key, tweet_data, ex=CELEBRITY_TWEETS_CACHE_SECONDS)

    return tweet_data
