export const PAGE_HOME = "home"
export const PAGE_ACCOUNT_REGISTRATION = "account-registration"
export const PAGE_LOGIN = "login"
export const PAGE_ACCOUNT_SETTINGS = "account-settings"
export const PAGE_CELEBRITY_LIST = "celebrity-list"
export const PAGE_CELEBRITY = "celebrity"
export const PAGE_USER_PREDICTIONS = "user-predictions"
export const PAGE_CREATE_PREDICTION = "create-prediction"

export const PAGES_REQUIRING_AUTH = [
    PAGE_ACCOUNT_SETTINGS,
    PAGE_USER_PREDICTIONS,
    PAGE_CREATE_PREDICTION,
]

export const PAGES_USING_AUTO_REFRESH = [
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_USER_PREDICTIONS,
]

export const REFRESH_PAGE_MINUTES = 10

export const COOKIE_ACCESS_TOKEN = "access-token"

export const METRIC = {
    LIKE: "like",
    QUOTE: "quote",
    REPLY: "reply",
    RETWEET: "retweet",
    TWEET: "tweet",
}

export const METRICS = [
    METRIC.LIKE,
    METRIC.QUOTE,
    METRIC.REPLY,
    METRIC.RETWEET,
    METRIC.TWEET,
]

export const METRIC_CLASSES = {
    [METRIC.LIKE]: "far fa-heart",
    [METRIC.QUOTE]: "fas fa-quote-right",
    [METRIC.REPLY]: "fas fa-reply",
    [METRIC.RETWEET]: "fas fa-retweet",
    [METRIC.TWEET]: "fab fa-twitter",
}

export const METRIC_LABELS = {
    [METRIC.LIKE]: "Like",
    [METRIC.QUOTE]: "Quote",
    [METRIC.REPLY]: "Reply",
    [METRIC.RETWEET]: "Retweet",
    [METRIC.TWEET]: "Tweet",
}

export const METRIC_LABELS_PLURAL = {
    [METRIC.LIKE]: "Likes",
    [METRIC.QUOTE]: "Quotes",
    [METRIC.REPLY]: "Replies",
    [METRIC.RETWEET]: "Retweets",
    [METRIC.TWEET]: "Tweets",
}
