<script>
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"

    import {celebrity} from "../store"
</script>

<section>
    {#if $celebrity.id}
        <div class="header">
            <div>
                <img alt="Celebrity" src={$celebrity.twitter_profile_image_url}/>
            </div>

            <h2>{$celebrity.twitter_name || $celebrity.twitter_username}</h2>
        </div>

        <DataTable style="width: 100%;">
            <Head>
                <Row>
                    <Cell>
                        <Label>Tweet</Label>
                    </Cell>
                    <Cell>
                        <Label>When</Label>
                    </Cell>
                    <Cell>
                        <Label>Likes</Label>
                    </Cell>
                    <Cell>
                        <Label>Retweets</Label>
                    </Cell>
                    <Cell>
                        <Label>Replies</Label>
                    </Cell>
                    <Cell>
                        <Label>Quotes</Label>
                    </Cell>
                </Row>
            </Head>
            <Body>
                {#each $celebrity.tweets as tweet}
                    <Row>
                        <Cell>{tweet.text}</Cell>
                        <Cell>{tweet.created_at}</Cell>
                        <Cell>{tweet.like_count}</Cell>
                        <Cell>{tweet.retweet_count}</Cell>
                        <Cell>{tweet.reply_count}</Cell>
                        <Cell>{tweet.quote_count}</Cell>
                    </Row>
                {/each}
            </Body>
        </DataTable>
    {/if}
</section>

<style lang="scss">
    :global(.mdc-data-table__cell) {
        max-width: 500px;
        white-space: normal;
    }

    .header {
        display: flex;

        h2 {
            margin-left: 20px;
        }
    }
</style>