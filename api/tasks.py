from datetime import datetime

from .crud import get_celebrity, update_celebrity
from .db import Session
from .models import Celebrity
from .twitter import get_user_by_username, get_user_tweets


def update_celebrity_data(celebrity_id: int) -> None:
    db = Session()
    celebrity = get_celebrity(db, celebrity_id)
    data = get_user_by_username(celebrity.twitter_username)

    if not data:
        return

    # When in an event, the db session cannot be used for any more updates.
    # Omitting the `db` param will force `update_celebrity` to create a separate db connection.
    # TODO: is there a cleaner way to do this??
    if True:  # celery always eager
        db = None

    update_celebrity(db, celebrity, twitter_id=data["id"], twitter_name=data["name"])


def fetch_celebrity_daily_tweets(celebrity_id: int, dt: datetime) -> None:
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end = dt.replace(hour=23, minute=59, second=59, microsecond=59).isoformat()
    celebrity = Celebrity.query.filter_by(id=celebrity_id).first()

    if not celebrity:
        return

    tweets = get_user_tweets(celebrity.twitter_id, start_time=start, end_time=end)
    print("*** fetch_celebrity_daily_tweets", tweets)
    # TODO: daily task to run this, calculate totals (like, etc..), and store.
