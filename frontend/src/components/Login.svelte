<script>
    import Cookies from "js-cookie"

    import api from "../api"
    import {
        COOKIE_ACCESS_TOKEN,
        PAGE_HOME,
    } from "../constants"
    import {
        alertMessage,
        requestedPage,
    } from "../store"
    import {gotoPage} from "../nav"

    let username = ""
    let password = ""

    async function login() {
        const formData = new FormData()

        formData.append("username", username)
        formData.append("password", password)

        await api({
            method: "post",
            url: "/token",
            data: formData,
            headers: {"Content-Type": "multipart/form-data"},
        })
        .then(function (response) {
            Cookies.set(COOKIE_ACCESS_TOKEN, response.data.access_token)
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
        Username: <input bind:value={username}/><br/>
        Password: <input bind:value={password} type="password"/><br/>
        <button>Login</button>
    </form>
</section>