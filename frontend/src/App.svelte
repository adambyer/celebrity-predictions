<script>
	import {onMount} from "svelte"
	import Router, {location} from "svelte-spa-router"

	import {
		isLoading,
	} from "./store"
	import routes from "./routes"
	import {gotoPage} from "./nav"

	import Loading from "./components/common/Loading.svelte"
	import Alert from "./components/common/Alert.svelte"
	import Nav from "./components/Nav.svelte"

	onMount(() => {
		// This is needed to force any needed fetches on page reload.
		gotoPage($location)
	})
</script>

<Nav/>

<div class="w3-container w3-content" style="max-width:1400px;margin-top:80px">
	<Alert/>

	{#if $isLoading}
        <Loading/>
    {/if}

	<Router routes={routes}/>
</div>

<style lang="scss">
	.w3-container {
		display: flex;
		align-items: flex-start;
		justify-content: center;
	}
</style>
