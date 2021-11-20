from enum import Enum

DISABLE_EVENTS = False

CACHE_KEY_CELEBRITY_TWEETS = "celebrity-tweets-{}"  # by Celebrity.id
CELEBRITY_TWEETS_CACHE_SECONDS = 60 * 10

# JWT
# TODO: put this in env.
JWT_SECRET_KEY = "5837e037766240342d37ce3ce7444ff5fc14c26f4d4e8a4be64da4c70a62e863"
JWT_ALGORITHM = "HS256"

# TODO: what should this be and how do we deal with expired tokens?
JWT_EXPIRE_MINUTES = 60 * 24

DATE_FORMAT = "%Y-%m-%d"


class PredictionMetricEnum(Enum):
    LIKE = "like"
    QUOTE = "quote"
    REPLY = "reply"
    RETWEET = "retweet"
    TWEET = "tweet"
