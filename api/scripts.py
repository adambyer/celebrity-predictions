from datetime import datetime, timedelta

from api.tasks import import_celebrity_daily_tweet_metrics


def import_metrics(celebrity_id: int, days_ago: int) -> None:
    now = datetime.utcnow()
    import_celebrity_daily_tweet_metrics(celebrity_id, now - timedelta(days=days_ago))
