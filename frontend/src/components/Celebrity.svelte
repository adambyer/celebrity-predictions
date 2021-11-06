<script>
    import {celebrity} from "../store"
</script>

<section>
    {#if $celebrity.id}
        <h2>Selected Celebrity</h2>
        <img alt="Celebrity" src={$celebrity.twitter_profile_image_url}/>
        <table>
            {#each $celebrity.tweets as tweet}
            <tr>
                <td>{tweet.text}</td>
            </tr>
            {/each}
        </table>
    {/if}
</section>