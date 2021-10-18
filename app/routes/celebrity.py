from datetime import datetime
from flask import Blueprint, render_template

from app.cache import get_list, set_list
from app.constants import CACHE_KEY_CELEBRITY_TWEETS, CELEBRITY_TWEETS_CACHE_SECONDS
from app.models import Celebrity
from app.twitter import get_user_tweets

bp = Blueprint("celebrity", __name__, url_prefix="/celebrity")


@bp.route("/")
def celebrities() -> str:
    celebrities = Celebrity.query.filter(Celebrity.twitter_id.isnot(None))
    context = {
        "celebrities": celebrities,
    }
    return render_template("celebrities.html", **context)


@bp.route("/<twitter_username>")
def celebrity(twitter_username: str) -> str:
    celebrity = Celebrity.query.filter_by(twitter_username=twitter_username).first()
    tweets = []
    name = twitter_username

    if celebrity.twitter_id:
        cache_key = CACHE_KEY_CELEBRITY_TWEETS.format(celebrity.id)
        tweets = get_list(cache_key) or []

        if not tweets:
            tweets = get_user_tweets(celebrity.twitter_id) or []
            set_list(cache_key, tweets, ex=CELEBRITY_TWEETS_CACHE_SECONDS)

    if celebrity.twitter_name:
        name = celebrity.twitter_name

    context = {
        "name": name,
        "tweets": tweets,
    }
    return render_template("celebrity.html", **context)
