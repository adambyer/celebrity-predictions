<script>
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
    } from "@smui/data-table"

    import {
        isLoading,
        celebrity,
    } from "../store"
    import {celebrityTitle} from "../celebrity_helpers"
    import {
        formatDate,
        formatDateAndTime,
    } from "../date_helpers"
    import {sortByDate} from "../sort_helpers"
    import {gotoPage} from "../nav"
    import {
        PAGE_CREATE_PREDICTION,
        METRIC,
    } from "../constants"
    import MetricLabel from "./common/MetricLabel.svelte"

    $: tweets = $celebrity ? $celebrity.tweets.sort((a, b) => sortByDate(a, b, "created_at")) : []
    $: metrics = $celebrity ? $celebrity.metrics.sort((a, b) => sortByDate(a, b, "metric_date")) : []

    // Get the original size (larger) profile image so we have more control.
    $: profileImage = $celebrity ? $celebrity.twitter_profile_image_url.replace("_normal", "") : ""

    // Dynamically set the header image to the same width as the text.
    // TODO: is there a better way to do this?
    let headerTextElement = null
    let headerImageElement = null
    $: headerTextWidth = headerTextElement ? headerTextElement.offsetWidth : 0
    $: if (headerTextElement && headerImageElement) {
        headerImageElement.style.width = `${headerTextWidth}px`
    }
</script> 

<section>
    {#if $celebrity}
        <div class="header">
            <div class="header-left">
                <h2 class="header-top" bind:this={headerTextElement}>
                    {celebrityTitle($celebrity)}
                </h2>

                <div>
                    <img alt="Celebrity" src={profileImage} bind:this={headerImageElement}/>
                </div>
            </div>

            <div>
                <div class="header-top">
                    <div>
                        <i
                            class="fas fa-plus-circle fa-2x add-icon"
                            on:click={() => gotoPage(PAGE_CREATE_PREDICTION, $celebrity.twitter_username)}
                            title={`Add a Prediction for ${celebrityTitle($celebrity)}`}
                        ></i>
                    </div>
                </div>

                <div>
                    <DataTable>
                        <Head>
                            <Row>
                                <Cell></Cell>
                                <Cell>
                                    <MetricLabel metric={METRIC.TWEET} iconOnly={true}/>
                                </Cell>
                                <Cell>
                                    <MetricLabel metric={METRIC.LIKE} iconOnly={true}/>
                                </Cell>
                                <Cell>
                                    <MetricLabel metric={METRIC.RETWEET} iconOnly={true}/>
                                </Cell>
                                <Cell>
                                    <MetricLabel metric={METRIC.REPLY} iconOnly={true}/>
                                </Cell>
                                <Cell>
                                    <MetricLabel metric={METRIC.QUOTE} iconOnly={true}/>
                                </Cell>
                            </Row>
                        </Head>
                        <Body>
                            {#each metrics as metric, i}
                                <Row>
                                    <Cell>{i === 0 ? "Today so far" : formatDate(metric.metric_date)}</Cell>
                                    <Cell>{metric.tweet_count}</Cell>
                                    <Cell>{metric.like_count}</Cell>
                                    <Cell>{metric.retweet_count}</Cell>
                                    <Cell>{metric.reply_count}</Cell>
                                    <Cell>{metric.quote_count}</Cell>
                                </Row>
                            {/each}
                        </Body>
                    </DataTable>
                </div>
            </div>
        </div>

        <h3>Latest Tweets</h3>

        <DataTable class="latest-tweets">
            <Body>
                {#each tweets as tweet}
                    <Row class="tweet-row">
                        <Cell class="tweet">
                            <div class="tweet-text">{tweet.text}</div>
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
                        </Cell>

                        <Cell class="tweet-info">
                            <div class="tweet-date">{formatDateAndTime(tweet.created_at)}</div>
                            <div>
                                <MetricLabel metric={METRIC.LIKE} iconOnly={true} className="metric-icon"/>
                                {tweet.like_count}
                            </div>
                            <div>
                                <MetricLabel metric={METRIC.RETWEET} iconOnly={true} className="metric-icon"/>
                                {tweet.retweet_count}
                            </div>
                            <div>
                                <MetricLabel metric={METRIC.REPLY} iconOnly={true} className="metric-icon"/>
                                {tweet.reply_count}
                            </div>
                            <div>
                                <MetricLabel metric={METRIC.QUOTE} iconOnly={true} className="metric-icon"/>
                                {tweet.quote_count}
                            </div>
                        </Cell>
                    </Row>
                {/each}
            </Body>
        </DataTable>
    {/if}
</section>

<style lang="scss">
    .header {
        display: flex;
        margin-bottom: 25px;

        .header-left {
            margin-right: 50px;
        }

        .header-top {
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            margin: 0 0 15px 0;
            height: 50px;
        }
    }

    // TODO: is there a better way than using `global` for all of this?
    :global(.mdc-data-table) {
        margin-bottom: 20px;
    }

    :global(.latest-tweets) {
        :global(.tweet-row) {
            :global(.tweet), :global(.tweet-info) {
                border: 1px solid gray;
                border-radius: 2px;
                padding: 15px;
                vertical-align: top;
                font-size: 20px;
            }

            :global(.tweet) {
                white-space: normal;

                :global(.tweet-text) {
                    margin-bottom: 15px;
                }

                :global(.tweet-image) {
                    width: 300px;
                    margin-bottom: 5px;
                }
            }

            :global(.tweet-info) {
                :global(.tweet-date) {
                    font-weight: bold;
                    margin-bottom: 30px
                }

                :global(.metric-icon) {
                    display: inline-block;
                    margin: 0 15px 12px 0;
                    min-width: 35px;
                }
            }
        }
    }
</style>