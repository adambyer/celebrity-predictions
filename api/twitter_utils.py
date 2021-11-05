
def get_tweet_metric_totals(tweets: list) -> dict:
    like_count = 0
    quote_count = 0
    reply_count = 0
    retweet_count = 0

    for t in tweets:
        like_count += t["public_metrics"]["like_count"]
        quote_count += t["public_metrics"]["quote_count"]
        reply_count += t["public_metrics"]["reply_count"]
        retweet_count += t["public_metrics"]["retweet_count"]

    return {
        "like_count": like_count,
        "quote_count": quote_count,
        "reply_count": reply_count,
        "retweet_count": retweet_count,
    }
