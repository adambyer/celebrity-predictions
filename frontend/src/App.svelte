<script>
	import {currentPage} from "./store"
	import {
		PAGE_HOME,
		PAGE_CELEBRITY,
		PAGE_CELEBRITY_LIST,
		PAGE_USER_PREDICTIONS,
		PAGE_LOGIN,
	} from "./constants"

	import Home from "./components/Home.svelte"
	import Nav from "./components/Nav.svelte"
	import Login from "./components/Login.svelte"
	import CelebrityList from "./components/CelebrityList.svelte"
	import Celebrity from "./components/Celebrity.svelte"
	import UserPredictions from "./components/UserPredictions.svelte"
	import Alert from "./components/Alert.svelte"
</script>

<Nav/>

<div class="w3-container w3-content" style="max-width:1400px;margin-top:80px">
	<Alert/>

	{#if $currentPage === PAGE_HOME}
		<Home/>
	{:else if $currentPage === PAGE_LOGIN}
		<Login/>
	{:else if $currentPage === PAGE_CELEBRITY_LIST}
		<CelebrityList/>
	{:else if $currentPage === PAGE_CELEBRITY}
		<Celebrity/>
	{:else if $currentPage === PAGE_USER_PREDICTIONS}
		<UserPredictions/>
	{/if}
</div>
