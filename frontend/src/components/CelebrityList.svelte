<script>
    import {celebrities, celebrity} from "../store"
    import API from "../api"

    async function showCelebrity(twitter_username) {
        const response = await API.get(`celebrity/${twitter_username}`)
        $celebrity = response.data
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