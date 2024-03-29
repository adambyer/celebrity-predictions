<script>
    import {fade} from "svelte/transition"
    import Textfield from "@smui/textfield"
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"

    import {getRequest} from "../api"
    import {celebrities} from "../store"
    import {gotoPage} from "../nav"
    import {celebrityTitle} from "../celebrity_helpers"
    import {
        PAGE_CREATE_PREDICTION,
    } from "../constants"
    import CelebrityLink from "./common/CelebrityLink.svelte"

    async function handleSearchInput() {
        if (timer) {
            clearTimeout(timer)
        }

        if (!searchValue) {
            display_celebrities = $celebrities
            return
        }

        timer = setTimeout(async () => (await search()), 300)
    }

    async function search() {
        const response = await getRequest("/celebrity", {search: searchValue})
        display_celebrities = response.data
    }

    let timer = null
    let searchValue = null
    let display_celebrities = []

    $: if ($celebrities) {
        display_celebrities = $celebrities
    }
</script>

<section class="content" in:fade={{duration: 500}}>
    <div class="header">
        <h2 class="header-text">
            {#if searchValue}
                <span>Celebrities matching "{searchValue}"</span>
            {:else}
                <span>Most Active Today</span>
            {/if}
        </h2>

        <div class="search-container">
            <Textfield
                bind:value={searchValue}
                label="Search"
                on:input={() => handleSearchInput()}
            />
        </div>
    </div>

    {#if display_celebrities.length === 0}
        {#if searchValue}
            <p>There are no celebrities matching your search.</p>
        {:else}
            <p>There are no active celebrites yet today. Try a search.</p>
        {/if}
    {:else}
        <DataTable>
            <Head>
                <Row>
                    <Cell></Cell>
                    <Cell><i class="fab fa-twitter" title="Tweets"></i></Cell>
                    <Cell><i class="far fa-heart" title="Likes"></i></Cell>
                    <Cell><i class="fas fa-retweet" title="Retweets"></i></Cell>
                    <Cell><i class="fas fa-reply" title="Replies"></i></Cell>
                    <Cell><i class="fas fa-quote-right" title="Quotes"></i></Cell>
                    <Cell></Cell>
                </Row>
            </Head>
            <Body>
                {#each display_celebrities as celebrity}
                    <Row>
                        <Cell>
                            <CelebrityLink celebrity={celebrity}/>
                        </Cell>
                        <Cell>{celebrity.metrics.length > 0 ? celebrity.metrics[0].tweet_count : 0}</Cell>
                        <Cell>{celebrity.metrics.length > 0 ? celebrity.metrics[0].like_count : 0}</Cell>
                        <Cell>{celebrity.metrics.length > 0 ? celebrity.metrics[0].retweet_count : 0}</Cell>
                        <Cell>{celebrity.metrics.length > 0 ? celebrity.metrics[0].reply_count : 0}</Cell>
                        <Cell>{celebrity.metrics.length > 0 ? celebrity.metrics[0].quote_count : 0}</Cell>
                        <Cell>
                            <i
                                class="fas fa-plus-circle fa-2x add-icon"
                                on:click={() => gotoPage(PAGE_CREATE_PREDICTION, celebrity.twitter_username)}
                                title={`Add a Prediction for ${celebrityTitle(celebrity)}`}
                            ></i>
                        </Cell>
                    </Row>
                {/each}
            </Body>
        </DataTable>
    {/if}
</section>

<style lang="scss">
    .content {
        min-width: 650px;

        .header {
            display: flex;
            justify-content: space-between;

            .header-text {
                margin-right: 15px;
            }

            .search-container {
                width: 160px;
                padding-right: 5px;

                :global(.mdc-text-field) {
                    width: 100% !important;

                    :global(.mdc-floating-label) {
                        right: 0;
                        left: initial;
                    }

                    :global(.mdc-line-ripple::before), :global(.mdc-line-ripple::after) {
                        border-bottom-color: red;
                    }
                }
            }
        }
    }
</style>