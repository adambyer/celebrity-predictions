<script>
	import {
		isLoading,
		currentPage,
	} from "./store"

	import {
		PAGE_HOME,
		PAGE_ACCOUNT_REGISTRATION,
		PAGE_LOGIN,
		PAGE_ACCOUNT_SETTINGS,
		PAGE_CELEBRITY,
		PAGE_CELEBRITY_LIST,
		PAGE_USER_PREDICTIONS,
		PAGE_CREATE_PREDICTION,
	} from "./constants"

	import Loading from "./components/common/Loading.svelte"
	import Alert from "./components/common/Alert.svelte"
	import Home from "./components/Home.svelte"
	import Nav from "./components/Nav.svelte"
	import Login from "./components/Login.svelte"
	import AccountSettings from "./components/AccountSettings.svelte"
	import CelebrityList from "./components/CelebrityList.svelte"
	import Celebrity from "./components/Celebrity.svelte"
	import UserPredictions from "./components/UserPredictions.svelte"
	import CreatePrediction from "./components/CreatePrediction.svelte"
</script>

<Nav/>

<div class="w3-container w3-content" style="max-width:1400px;margin-top:80px">
	<Alert/>

	{#if $isLoading}
        <Loading/>
    {/if}

	{#if $currentPage === PAGE_HOME}
		<Home/>
	{:else if $currentPage === PAGE_LOGIN}
		<Login/>
	{:else if [PAGE_ACCOUNT_REGISTRATION, PAGE_ACCOUNT_SETTINGS].includes($currentPage)}
		<AccountSettings/>
	{:else if $currentPage === PAGE_CELEBRITY_LIST}
		<CelebrityList/>
	{:else if $currentPage === PAGE_CELEBRITY}
		<Celebrity/>
	{:else if $currentPage === PAGE_USER_PREDICTIONS}
		<UserPredictions/>
	{:else if $currentPage === PAGE_CREATE_PREDICTION}
		<CreatePrediction/>
	{/if}
</div>

<style lang="scss">
	.w3-container {
		display: flex;
		align-items: flex-start;
		justify-content: center;
	}
</style>
