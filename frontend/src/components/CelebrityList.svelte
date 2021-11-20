<script>
    import Textfield from "@smui/textfield"

    import {getRequest} from "../api"
    import {celebrities, celebrityTwitterUsername} from "../store"
    import {gotoPage} from "../nav"

    async function showCelebrity(twitterUsername) {
        $celebrityTwitterUsername = twitterUsername
        gotoPage("celebrity")
    }

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

<section>
    <div class="header">
        <h2 class="header-text">
            {#if searchValue}
                <span>Celebrities matching "{searchValue}"</span>
            {:else}
                <span>Most Active Celebrities</span>
            {/if}
        </h2>

        <div>
            <Textfield
                bind:value={searchValue}
                label="Search"
                on:input={() => handleSearchInput()}
            />
        </div>
    </div>

    <table>
        {#each display_celebrities as celebrity}
        <tr>
            <td><a href="/" on:click|preventDefault={showCelebrity(celebrity.twitter_username)}>{celebrity.twitter_name}</a></td>
        </tr>
        {/each}
    </table>
</section>

<style lang="scss">
    .header {
        display: flex;

        .header-text {
            margin-right: 15px;
        }
    }
</style>