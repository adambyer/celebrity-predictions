from flask import Flask

from .models import Celebrity
from .twitter import get_user_by_username


def fetch_celebrity_data(app: Flask, celebrity_id: int) -> None:
    with app.app_context():
        celebrity = Celebrity.query.filter_by(id=celebrity_id).first()

        if not celebrity:
            return

        data = get_user_by_username(celebrity.twitter_username)

        if data:
            celebrity.twitter_id = data["id"]
            celebrity.twitter_name = data["name"]
            celebrity.save()
