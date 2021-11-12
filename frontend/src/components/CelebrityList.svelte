<script>
    import {celebrities, celebrityTwitterUsername} from "../store"
    import {gotoPage} from "../nav"

    async function showCelebrity(twitterUsername) {
        $celebrityTwitterUsername = twitterUsername
        gotoPage("celebrity")
    }
</script>

<section>
    <h2>Celebrities</h2>
    <table>
        {#each $celebrities as celebrity}
        <tr>
            <td><a href="/" on:click|preventDefault={showCelebrity(celebrity.twitter_username)}>{celebrity.twitter_name}</a></td>
        </tr>
        {/each}
    </table>
</section>