from collections import defaultdict
from sqlalchemy.orm import Session
from typing import Optional, List, Dict

from .constants import PredictionMetricEnum
from .crud.prediction_crud import get_prediction_results
from .model_types import (
    CelebrityDailyMetricsType,
    LeaderType,
)


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


def get_leaders(db: Session) -> dict:
    prediction_results = get_prediction_results(db, True)
    user_totals: dict = defaultdict(lambda: {"pr": None, "points": 0})

    for pr in prediction_results:
        user_totals[pr.user_id]["pr"] = pr
        user_totals[pr.user_id]["points"] += pr.points

    all_time: List[LeaderType] = [
        LeaderType(user=ut["pr"].user, points=ut["points"])
        for ut in user_totals.values()
    ]

    return {
        "All Time Leaders": sorted(all_time, key=lambda lt: lt.points, reverse=True),
    }
