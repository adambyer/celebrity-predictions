<script>
    import {celebrity} from "../store"
    import {formatDate} from "../date_helpers"
    import {sortByCreatedAt} from "../sort_helpers"

    $: tweets = $celebrity.tweets ? $celebrity.tweets.sort(sortByCreatedAt) : []
</script>

<section>
    {#if $celebrity.id}
        <div class="header">
            <div>
                <img alt="Celebrity" src={$celebrity.twitter_profile_image_url}/>
            </div>

            <h2>{$celebrity.twitter_name || $celebrity.twitter_username}</h2>
        </div>

        <h3>Latest Tweets</h3>

        <div class="latest-tweets">
            {#each tweets as tweet}
                <div class="tweet-row">
                    <div class="tweet">
                        <p>{tweet.text}</p>
                        <div>
                            {#each tweet.media as media}
                                <div>
                                    {#if media.type === "video"}
                                        <img src={media.preview_image_url} alt={celebrity.twitter_name} class="tweet-image"/>
                                    {:else}
                                        <img src={media.url} alt={celebrity.twitter_name} class="tweet-image"/>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    </div>

                    <div class="tweet-info">
                        <div>{formatDate(tweet.created_at)}</div>
                        <div><i class="far fa-heart metric-icon"></i>{tweet.like_count}</div>
                        <div><i class="fas fa-retweet metric-icon"></i>{tweet.retweet_count}</div>
                        <div><i class="fas fa-reply metric-icon"></i>{tweet.reply_count}</div>
                        <div><i class="fas fa-quote-right metric-icon"></i>{tweet.quote_count}</div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</section>

<style lang="scss">
    .header {
        display: flex;

        h2 {
            margin-left: 20px;
        }
    }

    .latest-tweets {
        .tweet-row {
            display: flex;

            .tweet, .tweet-info {
                border: 1px solid gray;
                border-radius: 2px;
                padding: 10px;
            }

            .tweet {
                flex-basis: 80%;

                .tweet-image {
                    width: 300px;
                }
            }

            .tweet-info {
                flex-basis: 20%;

                .metric-icon {
                    padding-right: 10px;
                }
            }
        }

    }
</style>