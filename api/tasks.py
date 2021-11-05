from datetime import date, datetime, timedelta
import logging
from sqlalchemy.exc import IntegrityError

from .crud import (
    create_celebrity_daily_metrics,
    create_prediction_result,
    get_celebrity,
    get_celebrity_daily_metrics,
    get_celebrities,
    update_celebrity,
)
from .db import Session
from .model_types import CelebrityDailyMetricsCreateType, PredictionResultCreateType
from .prediction_utils import get_prediction_points, get_metric_total
from .twitter_api import get_user_by_username, get_user_tweets
from .twitter_utils import get_tweet_metric_totals

logger = logging.getLogger(__name__)


def update_celebrity_data(celebrity_id: int) -> None:
    db = Session()
    celebrity = get_celebrity(db, celebrity_id)

    if not celebrity:
        return

    if celebrity.twitter_id and celebrity.twitter_name:
        return

    data = get_user_by_username(celebrity.twitter_username)
    if not data:
        return

    # When in an event, the db session cannot be used for any more updates.
    # Omitting the `db` param will force `update_celebrity` to create a separate db connection.
    # TODO: is there a cleaner way to do this??
    if True:  # celery always eager
        db = None

    updates = {
        "twitter_id": data["id"],
        "twitter_name": data["name"],
        "twitter_verified": data["verified"],
        "twitter_description": data["description"],
        "twitter_profile_image_url": data["profile_image_url"],
    }
    update_celebrity(db, celebrity, **updates)
    db.close()


# TODO: make this a scheduled task.
def start_daily_scoring(
    # Default to yesterday.
    scoring_date: date = (datetime.utcnow() - timedelta(days=1)).date(),
) -> None:
    db = Session()
    celebrities = get_celebrities(db)

    for celebrity in celebrities:
        # TODO: make this a task
        import_celebrity_daily_tweet_metrics(celebrity.id, scoring_date)

    db.close()


def import_celebrity_daily_tweet_metrics(
    celebrity_id: int,

    # Default to yesterday.
    scoring_date: date = (datetime.utcnow() - timedelta(days=1)).date(),
) -> None:
    db = Session()
    start = f"{datetime.combine(scoring_date, datetime.min.time()).isoformat()}Z"
    end = f"{datetime.combine(scoring_date, datetime.max.time()).replace(microsecond=0).isoformat()}Z"
    celebrity = get_celebrity(db, celebrity_id)

    if not celebrity:
        return

    tweets = get_user_tweets(celebrity.twitter_id, start_time=start, end_time=end)
    metrics = get_tweet_metric_totals(tweets)

    metrics["celebrity_id"] = celebrity_id
    metrics["metric_date"] = scoring_date
    metrics["tweet_count"] = len(tweets)

    try:
        create_celebrity_daily_metrics(db, CelebrityDailyMetricsCreateType(**metrics))
    except IntegrityError:
        # TODO: this seems to be needed. Is it the correct way?
        db.rollback()

    create_prediction_results(db, celebrity.id, scoring_date)

    db.close()


def create_prediction_results(
    db: Session,
    celebrity_id: int,
    scoring_date: date,
) -> None:
    db = Session()
    celebrity = get_celebrity(db, celebrity_id)
    metrics = get_celebrity_daily_metrics(db, celebrity_id, scoring_date)

    if not celebrity or not metrics:
        return

    for p in celebrity.predictions:
        actual_amount = get_metric_total(metrics, p.metric)

        if actual_amount is None:
            logger.error(f"invalid metric: {p.metric}")
            continue

        pr = PredictionResultCreateType(**{
            "user_id": p.user_id,
            "celebrity_id": p.celebrity_id,
            "amount": p.amount,
            "metric": p.metric,
            "metric_date": scoring_date,
            "points": get_prediction_points(p.amount, actual_amount),
        })

        try:
            create_prediction_result(db, pr)
        except IntegrityError:
            # TODO: this seems to be needed. Is it the correct way?
            db.rollback()
