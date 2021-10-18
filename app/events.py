import flask
from sqlalchemy.engine.base import Connection
from sqlalchemy.event import listens_for
from sqlalchemy.orm import Mapper
from threading import Thread

from .models import Celebrity
from .tasks import fetch_celebrity_data


@listens_for(Celebrity, "after_insert")
def celebrity_after_insert(
    mapper: Mapper, connect: Connection, target: Celebrity
) -> None:
    # TODO: make this a task when using celery (and not always eager)

    # Any better way than passing the app here??
    app = flask.current_app._get_current_object()  # type: ignore
    Thread(target=fetch_celebrity_data, args=(app, target.id)).start()
