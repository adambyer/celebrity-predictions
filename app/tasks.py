from datetime import datetime
from flask import Flask

from .models import Celebrity
from .twitter import get_user_by_username, get_user_tweets


def fetch_celebrity_data(app: Flask, celebrity_id: int) -> None:
    with app.app_context():
        celebrity = Celebrity.query.filter_by(id=celebrity_id).first()

        if not celebrity:
            return

        data = get_user_by_username(celebrity.twitter_username)

        if data:
            celebrity.twitter_id = data["id"]
            celebrity.twitter_name = data["name"]
            celebrity.save()


def fetch_celebrity_daily_tweets(celebrity_id: int, dt: datetime) -> None:
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end = dt.replace(hour=23, minute=59, second=59, microsecond=59).isoformat()
    celebrity = Celebrity.query.filter_by(id=celebrity_id).first()

    if not celebrity:
        return

    tweets = get_user_tweets(celebrity.twitter_id, start_time=start, end_time=end)
    # TODO: daily task to run this, calculate totals (like, etc..), and store.
