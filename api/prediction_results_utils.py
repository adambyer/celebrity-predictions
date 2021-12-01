from collections import defaultdict
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from typing import Optional

from .cache import get_structure, set_structure
from .constants import (
    CACHE_KEY_LEADERS_ALL_TIME,
    CACHE_KEY_LEADERS_DAILY,
    LEADERS_CACHE_SECONDS,
    DATE_FORMAT,
    PredictionMetricEnum,
)
from .crud.prediction_results_crud import (
    get_scored_prediction_results,
    get_user_points_by_date,
)
from .model_types import (
    CelebrityDailyMetricsType,
    LeaderType,
)

logger = logging.getLogger(__name__)


def get_metric_total(
    metrics: CelebrityDailyMetricsType,
    metric: str,
) -> Optional[int]:
    if metric == PredictionMetricEnum.LIKE.value:
        return metrics.like_count
    elif metric == PredictionMetricEnum.QUOTE.value:
        return metrics.quote_count
    elif metric == PredictionMetricEnum.REPLY.value:
        return metrics.reply_count
    elif metric == PredictionMetricEnum.RETWEET.value:
        return metrics.retweet_count
    elif metric == PredictionMetricEnum.TWEET.value:
        return metrics.tweet_count

    return None


def get_prediction_points(prediction_amount: int, actual_amount: int) -> int:
    # Points range from 100 to -100.
    # Points are based on how close the prediction came to the actual amount.
    # <20% gets positive points.
    # >=20% and <=50% gets zero points.
    # >50% gets negative points.
    #
    # Examples:
    #
    # prediction_amount = 9
    # actual_amount = 10
    # points: 100 - (10 * 5) = 50
    #
    # prediction_amount = 13
    # actual_amount = 10
    # points: -((70 - 50) * 2) = -40

    if actual_amount == 0:
        return -100

    distance = abs(prediction_amount - actual_amount) / actual_amount
    distance_amount = int(round(distance * 100))

    if distance < 0.2:
        return 100 - (distance_amount * 5)
    elif distance > 0.5:
        return -((distance_amount - 50) * 2)

    return 0


def get_leaders_all_time(
    db: Session,
    force_refresh: bool = False,
) -> list:
    leaders = None

    if not force_refresh:
        leaders = get_structure(CACHE_KEY_LEADERS_ALL_TIME)

    if leaders and isinstance(leaders, list):
        logger.info(f"using cache. key:{CACHE_KEY_LEADERS_ALL_TIME}")
    else:
        prediction_results = get_scored_prediction_results(db)
        user_totals: dict = defaultdict(lambda: {"pr": None, "points": 0})

        for pr in prediction_results:
            user_totals[pr.user_id]["pr"] = pr
            user_totals[pr.user_id]["points"] += pr.points

        leaders = sorted(
            [
                {
                    "user": {
                        "username": ut["pr"].user.username,
                    },
                    "points": ut["points"],
                }
                for ut in user_totals.values()
            ],
            key=lambda leader: leader["points"], reverse=True
        )[:10]
        set_structure(CACHE_KEY_LEADERS_ALL_TIME, leaders, LEADERS_CACHE_SECONDS)

    return [LeaderType(**leader) for leader in leaders]


def get_leaders_daily(
    db: Session,
    force_refresh: bool = False,
) -> list:
    leaders = None

    if not force_refresh:
        leaders = get_structure(CACHE_KEY_LEADERS_DAILY)

    if leaders and isinstance(leaders, list):
        logger.info(f"using cache. key:{CACHE_KEY_LEADERS_DAILY}")
    else:
        start_date = (datetime.utcnow() - timedelta(days=10)).date()
        user_points_by_date = get_user_points_by_date(db, start_date=start_date)
        date_leaders: dict = {}

        for p in user_points_by_date:
            metric_date = datetime.strftime(p["metric_date"], DATE_FORMAT)

            if metric_date not in date_leaders or p["total_points"] > date_leaders[metric_date]["total_points"]:
                date_leaders[metric_date] = p

        leaders = sorted(
            [
                {
                    "user": {
                        "username": dl["username"],
                    },
                    "metric_date": metric_date,
                    "points": dl["total_points"],
                }
                for metric_date, dl in date_leaders.items()
            ],
            key=lambda leader: leader["metric_date"], reverse=True
        )
        set_structure(CACHE_KEY_LEADERS_DAILY, leaders, LEADERS_CACHE_SECONDS)

    return [LeaderType(**leader) for leader in leaders]
