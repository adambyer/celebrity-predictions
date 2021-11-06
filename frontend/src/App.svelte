<script>
	import Nav from "./components/Nav.svelte"
	import LoginForm from "./components/LoginForm.svelte"
	import CelebrityList from "./components/CelebrityList.svelte"
	import Celebrity from "./components/Celebrity.svelte"
</script>

<Nav/>

<div class="w3-container w3-content" style="max-width:1400px;margin-top:80px"> 
	<LoginForm/>

	<CelebrityList/>

	<Celebrity/>
</div>
