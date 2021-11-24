<script>
    import {onMount} from "svelte"
    import Textfield from "@smui/textfield"
    import Button, {Label} from "@smui/button"

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

    $: isReady = !!(
        username
        && password
    )
</script>

<section class="content">
    <form on:submit|preventDefault={login}>
        <div class="row">
            <Textfield bind:value={username} bind:this={usernameInput} label="Username" variant="outlined" required={true}/>
        </div>

        <div class="row">
            <Textfield bind:value={password} label="Password" variant="outlined" required={true} type="password"/>
        </div>
        
        <div class="row">
            <Button
                variant="raised"
                disabled={!isReady}
            >
                <Label>Login</Label>
            </Button>
        </div>
    </form>
</section>

<style lang="scss">
    .content {
        padding: 15px;
        width: fit-content;

        .row {
            margin-bottom: 10px;
        }
    }
</style>