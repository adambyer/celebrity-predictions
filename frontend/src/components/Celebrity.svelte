<script>
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"
    import Tooltip, {Wrapper} from "@smui/tooltip"

    import {celebrity} from "../store"
    import {celebrityTitle} from "../celebrity_helpers"
    import {
        formatDate,
        formatDateAndTime,
    } from "../date_helpers"
    import {sortByDate} from "../sort_helpers"
    import Loading from "./Loading.svelte"

    $: isLoading = $celebrity === null
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

    // $: console.log("*** celebrity", $celebrity)
    // $: console.log("*** isLoading", isLoading)
    // $: console.log("*** headerTextWidth", headerTextWidth)
    // $: console.log("*** headerImageElement.style.width", (headerImageElement ? headerImageElement.style.width : 0))
</script> 

<section>
    {#if isLoading}
        <Loading/>
    {/if}

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

            <div class="header-right">
                <div class="header-top">
                    <div>
                        <Wrapper>
                            <i class="fas fa-plus-circle fa-2x add-icon" on:click={() => {}}></i>
                            <Tooltip>Add a Prediction for {$celebrity.twitter_name}</Tooltip>
                        </Wrapper>
                    </div>
                </div>

                <div class="metrics">
                    <DataTable>
                        <Head>
                            <Row>
                                <Cell></Cell>
                                <Cell><i class="fab fa-twitter" title="Tweets"></i></Cell>
                                <Cell><i class="far fa-heart" title="Likes"></i></Cell>
                                <Cell><i class="fas fa-retweet" title="Retweets"></i></Cell>
                                <Cell><i class="fas fa-reply" title="Replies"></i></Cell>
                                <Cell><i class="fas fa-quote-right" title="Quotes"></i></Cell>
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
                            <div><i class="far fa-heart metric-icon" title="Likes"></i>{tweet.like_count}</div>
                            <div><i class="fas fa-retweet metric-icon" title="Retweets"></i>{tweet.retweet_count}</div>
                            <div><i class="fas fa-reply metric-icon" title="Replies"></i>{tweet.reply_count}</div>
                            <div><i class="fas fa-quote-right metric-icon" title="Quotes"></i>{tweet.quote_count}</div>
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