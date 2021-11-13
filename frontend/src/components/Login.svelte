<script>
    import {onMount} from "svelte"
    import api from "../api"
    import {
        PAGE_HOME,
    } from "../constants"
    import {
        alertMessage,
        requestedPage,
    } from "../store"
    import {gotoPage} from "../nav"
    import {setAccessToken} from "../auth_helpers"

    let usernameInput = null
    let username = ""
    let password = ""

    onMount(() => {
        usernameInput.focus()
    })

    async function login() {
        const formData = new FormData()

        formData.append("username", username)
        formData.append("password", password)

        await api({
            method: "post",
            url: "/login",
            data: formData,
            headers: {"Content-Type": "multipart/form-data"},
        })
        .then(function (response) {
            setAccessToken(response.data.access_token)
            $alertMessage = "You are now logged in!"
            const page = $requestedPage || PAGE_HOME
            gotoPage(page)
        })
        .catch(function (error) {
            $alertMessage = "Invalid username or password. Please try again."
        })
    }
</script>

<section>
    <form on:submit|preventDefault={login}>
        Username: <input bind:value={username} bind:this={usernameInput}/><br/>
        Password: <input bind:value={password} type="password"/><br/>
        <button>Login</button>
    </form>
</section>