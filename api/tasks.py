from celery import shared_task
from datetime import date, datetime, timedelta
import logging
from sqlalchemy.exc import IntegrityError

from .celebrity_utils import update_celebrity_data as update_celebrity_data_util
from .celery_config import task_always_eager
from .constants import DATE_FORMAT
from .crud.celebrity_crud import (
    create_celebrity_daily_metrics,
    get_celebrity,
    get_celebrity_daily_metrics,
    get_celebrities,
)
from .crud.prediction_crud import get_predictions
from .crud.prediction_results import (
    create_prediction_result,
    update_prediction_result,
    get_prediction_results_for_scoring,
)
from .db import Session
from .model_types import CelebrityDailyMetricsCreateType, PredictionResultCreateType
from .prediction_utils import get_prediction_points, get_metric_total
from .twitter_api import get_user_tweets
from .twitter_utils import get_tweet_metric_totals

logger = logging.getLogger(__name__)


@shared_task
def create_prediction_results(
    # Has to be a string because tasks use JSON.
    metric_date_string: str,
) -> None:
    logger.info("create_prediction_results")
    db = Session()
    predictions = get_predictions(db)
    metric_date = datetime.strptime(metric_date_string, DATE_FORMAT).date()

    for p in predictions:
        try:
            pr = PredictionResultCreateType(**{
                "user_id": p.user_id,
                "celebrity_id": p.celebrity_id,
                "amount": p.amount,
                "metric": p.metric,
                "metric_date": metric_date,
            })
        except Exception:
            logger.exception("Invalid PredictionResultCreateType.", extra=pr.dict())

        try:
            create_prediction_result(db, pr)
        except IntegrityError:
            # Record already exists.
            # TODO: Rollback seems to be needed. Is it the correct way?
            db.rollback()


@shared_task
def update_celebrity_data(celebrity_id: int) -> None:
    logger.info(f"update_celebrity_data. celebrity_id:{celebrity_id}")
    db = Session()
    update_celebrity_data_util(db, celebrity_id)

    if db:
        db.close()


@shared_task
def start_daily_scoring(
    # Default to yesterday. Has to be a string because tasks use JSON.
    metric_date_string: str = date.strftime((datetime.utcnow() - timedelta(days=1)).date(), DATE_FORMAT)
) -> None:
    logger.info(f"start_daily_scoring. metric_date:{metric_date_string}")

    # First create the placeholder PredictionResult rows so they will be ready for the next day's scoring.
    create_prediction_results.delay(metric_date_string)

    db = Session()
    celebrities = get_celebrities(db)

    for celebrity in celebrities:
        import_celebrity_daily_tweet_metrics.delay(celebrity.id, metric_date_string)

    db.close()


@shared_task
def import_celebrity_daily_tweet_metrics(
    celebrity_id: int,

    # Default to yesterday. Has to be a string because tasks use JSON.
    metric_date_string: str = date.strftime((datetime.utcnow() - timedelta(days=1)).date(), DATE_FORMAT)
) -> None:
    logger.info(f"import_celebrity_daily_tweet_metrics begin. celebrity_id:{celebrity_id} metric_date:{metric_date_string}")
    db = Session()
    metric_date = datetime.strptime(metric_date_string, DATE_FORMAT).date()
    start = f"{datetime.combine(metric_date, datetime.min.time()).isoformat()}Z"
    end = f"{datetime.combine(metric_date, datetime.max.time()).replace(microsecond=0).isoformat()}Z"
    celebrity = get_celebrity(db, celebrity_id)

    if not celebrity:
        return

    tweets = get_user_tweets(celebrity.twitter_id, start_time=start, end_time=end)
    metrics = get_tweet_metric_totals(tweets)
    metrics["celebrity_id"] = celebrity_id
    metrics["metric_date"] = metric_date
    metrics["tweet_count"] = len(tweets)

    try:
        create_celebrity_daily_metrics(db, CelebrityDailyMetricsCreateType(**metrics))
    except IntegrityError:
        # Record already exists.
        # TODO: this seems to be needed. Is it the correct way?
        db.rollback()

    # Now update the results from the previous day that are waiting to be scored.
    results_date_string = date.strftime(metric_date - timedelta(days=1), DATE_FORMAT)
    update_prediction_results.delay(celebrity.id, results_date_string)

    # Can't close the connection if all this is running in the same process.
    if not task_always_eager:
        db.close()

    logger.info(f"import_celebrity_daily_tweet_metrics complete. celebrity_id:{celebrity_id} metric_date:{str(metric_date)}")


@shared_task
def update_prediction_results(
    celebrity_id: int,

    # Has to be a string because tasks use JSON.
    metric_date_string: str,
) -> None:
    logger.info(f"update_prediction_results. celebrity_id:{celebrity_id} metric_date:{metric_date_string}")
    metric_date = datetime.strptime(metric_date_string, DATE_FORMAT).date()
    db = Session()
    prediction_results = get_prediction_results_for_scoring(db, celebrity_id, metric_date)
    celebrity_daily_metrics = get_celebrity_daily_metrics(db, celebrity_id, metric_date, metric_date)
    metrics = celebrity_daily_metrics[0] if celebrity_daily_metrics else None

    for pr in prediction_results:
        actual_amount = get_metric_total(metrics, pr.metric)

        if actual_amount is None:
            logger.error(f"invalid metric: {pr.metric}")
            continue

        points = get_prediction_points(pr.amount, actual_amount)
        update_prediction_result(db, pr, points)
