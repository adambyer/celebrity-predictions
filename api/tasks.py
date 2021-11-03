from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError

from .constants import PredictionMetricEnum
from .crud import (
    create_celebrity_daily_metric,
    create_prediction_result,
    get_celebrity,  
    get_celebrity_ids_for_predictions,
    update_celebrity,
)
from .db import Session
from .model_types import CelebrityDailyMetricCreateType, PredictionResultCreateType
from .prediction_utils import get_prediction_points
from .twitter import get_user_by_username, get_user_tweets


def _create_prediction_results(
    db: Session,
    predictions: list,
    metric: PredictionMetricEnum,
    metric_date: date,
    actual_amount: int,
) -> None:
    for p in predictions:
        if p.metric == metric.value:
            pr = PredictionResultCreateType(**{
                "user_id": p.user_id,
                "celebrity_id": p.celebrity_id,
                "amount": p.amount,
                "metric": metric.value,
                "metric_date": metric_date,
                "points": get_prediction_points(p.amount, actual_amount),
            })

            try:
                create_prediction_result(db, pr)
            except IntegrityError:
                # TODO: this seems to be needed. Is it the correct way?
                db.rollback()


def _get_tweet_metric_totals(tweets: list) -> tuple:
    like_total = 0
    quote_total = 0
    reply_total = 0
    retweet_total = 0

    for t in tweets:
        like_total += t["public_metrics"]["like_count"]
        quote_total += t["public_metrics"]["quote_count"]
        reply_total += t["public_metrics"]["reply_count"]
        retweet_total += t["public_metrics"]["retweet_count"]

    return (
        like_total,
        quote_total,
        reply_total,
        retweet_total,
    )


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
    d: date = (datetime.utcnow() - timedelta(days=1)).date(),
) -> None:
    db = Session()
    celebrity_ids = get_celebrity_ids_for_predictions(db)

    for celebrity_id in celebrity_ids:
        # TODO: make this a task
        import_celebrity_daily_tweet_metrics(celebrity_id, d)

    db.close()


def import_celebrity_daily_tweet_metrics(
    celebrity_id: int,

    # Default to yesterday.
    d: date = (datetime.utcnow() - timedelta(days=1)).date(),
) -> None:
    db = Session()
    start = f"{datetime.combine(d, datetime.min.time()).isoformat()}Z"
    end = f"{datetime.combine(d, datetime.max.time()).replace(microsecond=0).isoformat()}Z"
    celebrity = get_celebrity(db, celebrity_id)

    if not celebrity or not celebrity.predictions:
        return

    tweets = get_user_tweets(celebrity.twitter_id, start_time=start, end_time=end)
    like_total, quote_total, reply_total, retweet_total = _get_tweet_metric_totals(tweets)

    for metric in PredictionMetricEnum:
        if not any([p.metric == metric.value for p in celebrity.predictions]):
            continue

        daily_metric = {
            "celebrity_id": celebrity.id,
            "metric_date": d,
            "metric": metric.value,
        }

        if metric is PredictionMetricEnum.LIKE:
            daily_metric["amount"] = like_total
        elif metric is PredictionMetricEnum.REPLY:
            daily_metric["amount"] = reply_total
        elif metric is PredictionMetricEnum.RETWEET:
            daily_metric["amount"] = retweet_total
        elif metric is PredictionMetricEnum.QUOTE:
            daily_metric["amount"] = quote_total

        try:
            create_celebrity_daily_metric(db, CelebrityDailyMetricCreateType(**daily_metric))
        except IntegrityError:
            # TODO: this seems to be needed. Is it the correct way?
            db.rollback()

        _create_prediction_results(db, celebrity.predictions, metric, d, daily_metric["amount"])

    db.close()
