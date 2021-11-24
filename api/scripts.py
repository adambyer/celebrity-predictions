from datetime import datetime, timedelta
import json
import logging
from sqlalchemy.exc import IntegrityError
from typing import Optional

from api.celebrity_utils import update_celebrity_data
from api.constants import DATE_FORMAT, DISABLE_EVENTS
from api.crud.celebrity_crud import create_celebrity
from api.db import Session
from api.model_types import CelebrityCreateType
from api.tasks import (
    import_celebrity_daily_metrics,
    import_all_celebrity_daily_metrics,
    start_daily_scoring,
)

logger = logging.getLogger(__name__)


def import_seed_celebrities() -> None:
    # TODO: Is there a more dynamic way to do this.
    # I tried using `global` to update `DISABLE_EVENTS` but that didn't work.
    if DISABLE_EVENTS is False:
        logger.warning("!!! Must set DISABLE_EVENTS to False !!!")
        return

    db = Session()

    with open("api/data/seed_twitter_usernames.json") as f:
        usernames = json.loads(f.read())

        for username in usernames:
            celebrity = CelebrityCreateType(twitter_username=username)

            try:
                print("*** importing", username)
                db_celebrity = create_celebrity(db, celebrity)
                print("*** imported", username, db_celebrity.id)
                update_celebrity_data(db, db_celebrity.id)
                print("*** updated", username, db_celebrity.id)

            except IntegrityError:
                db.rollback()

    db.close()
    print("*** import_seed_celebrities complete")


def import_metrics(celebrity_id: Optional[int], days_ago: int) -> None:
    metric_date = datetime.strftime(datetime.utcnow() - timedelta(days=days_ago), DATE_FORMAT)

    if celebrity_id:
        import_celebrity_daily_metrics(celebrity_id, metric_date)
    else:
        import_all_celebrity_daily_metrics(metric_date)


def start_scoring(days_ago: int = 1) -> None:
    metric_date = datetime.strftime(datetime.utcnow() - timedelta(days=days_ago), DATE_FORMAT)
    start_daily_scoring(metric_date)
