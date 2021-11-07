<script>
	import {currentPage} from "./store"

	import Nav from "./components/Nav.svelte"
	import LoginForm from "./components/LoginForm.svelte"
	import CelebrityList from "./components/CelebrityList.svelte"
	import Celebrity from "./components/Celebrity.svelte"
	import userPredictions from "./components/UserPredictions.svelte"
import UserPredictions from "./components/UserPredictions.svelte"
</script>

<Nav/>

<div class="w3-container w3-content" style="max-width:1400px;margin-top:80px"> 
	{#if $currentPage === "login"}
		<LoginForm/>
	{:else if $currentPage === "celebrity-list"}
		<CelebrityList/>
	{:else if $currentPage === "celebrity"}
		<Celebrity/>
	{:else if $currentPage === "user-predictions"}
		<UserPredictions/>
	{/if}
</div>
