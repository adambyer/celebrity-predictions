from sqlalchemy.engine.base import Connection
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper
from threading import Thread

from .models import Celebrity
from .tasks import update_celebrity_data


@listens_for(Celebrity, "after_insert")
def celebrity_after_insert(
    mapper: Mapper, connection: Connection, target: Celebrity
) -> None:
    if True:  # celery always eager
        Thread(target=update_celebrity_data, args=(target.id,)).start()
    else:
        # update_celebrity_data.delay(target.id)
        pass
