from celery import shared_task
from datetime import date, datetime, timedelta
import logging
from sqlalchemy.exc import IntegrityError

from .celery_config import task_always_eager
from .constants import DATE_FORMAT
from .crud.celebrity_crud import (
    create_celebrity_daily_metrics,
    get_celebrity,
    get_celebrity_daily_metrics,
    get_celebrities,
    update_celebrity,
)
from .crud.prediction_crud import create_prediction_result
from .db import Session
from .model_types import CelebrityDailyMetricsCreateType, PredictionResultCreateType
from .prediction_utils import get_prediction_points, get_metric_total
from .twitter_api import get_user_by_username, get_user_tweets
from .twitter_utils import get_tweet_metric_totals

logger = logging.getLogger(__name__)


@shared_task
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
    if task_always_eager:
        db = None

    updates = {
        "twitter_id": data["id"],
        "twitter_name": data["name"],
        "twitter_verified": data["verified"],
        "twitter_description": data["description"],
        "twitter_profile_image_url": data["profile_image_url"],
    }
    update_celebrity(db, celebrity, **updates)

    if db:
        db.close()


@shared_task
def start_daily_scoring(
    # Default to yesterday.
    scoring_date: date = (datetime.utcnow() - timedelta(days=1)).date(),
) -> None:
    db = Session()
    celebrities = get_celebrities(db)

    for celebrity in celebrities:
        import_celebrity_daily_tweet_metrics.delay(celebrity.id, scoring_date)

    db.close()


@shared_task
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
        # Record already exists.
        # TODO: this seems to be needed. Is it the correct way?
        db.rollback()

    scoring_date_string = date.strftime(scoring_date, DATE_FORMAT)
    create_prediction_results.delay(celebrity.id, scoring_date_string)

    db.close()


@shared_task
def create_prediction_results(
    celebrity_id: int,

    # Has to be a string because tasks use JSON.
    scoring_date_string: str,
) -> None:
    scoring_date = datetime.strptime(scoring_date_string, DATE_FORMAT).date()
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

        try:
            pr = PredictionResultCreateType(**{
                "user_id": p.user_id,
                "celebrity_id": p.celebrity_id,
                "amount": p.amount,
                "metric": p.metric,
                "metric_date": scoring_date,
                "points": get_prediction_points(p.amount, actual_amount),
            })
        except Exception as e:
            logger.exception(f"Why is this being swallowed up? {str(e)}", extra=pr.dict())

        try:
            create_prediction_result(db, pr)
        except IntegrityError:
            # Record already exists.
            # TODO: this seems to be needed. Is it the correct way?
            db.rollback()
