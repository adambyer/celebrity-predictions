<script>
    import {celebrityTitle} from "../../celebrity_helpers"
    import {PAGE_CELEBRITY} from "../../constants"
    import {gotoPage} from "../../nav"

    export let celebrity = null
</script>

<a
    href="/"
    on:click|preventDefault={() => gotoPage(PAGE_CELEBRITY, celebrity.twitter_username)}
>{celebrityTitle(celebrity)}</a>

<style lang="scss">
    a {
        color: blue;
    }
</style>