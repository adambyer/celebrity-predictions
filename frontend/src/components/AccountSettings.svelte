<script>
    import Textfield from "@smui/textfield"
    import HelperText from "@smui/textfield/helper-text"
    import CharacterCounter from "@smui/textfield/character-counter"
    import Button, {Label} from "@smui/button"

    import {
        postRequest,
    } from "../api"
    import {
        gotoPage,
    } from "../nav"
    import {
        isLoggedIn,
        currentUser,
        alertMessage,
    } from "../store"
    import {
        PAGE_LOGIN,
    } from "../constants"
    import {
        deleteAccessToken,
    } from "../auth_helpers"

    async function save() {
        if (password !== passwordConfirm) {
            $alertMessage = "Passwords do not match"
            return
        }

        const user = {
            username,
            email_address: emailAddress,
        }

        if (password) {
            user.password = password
        }

        const url = $isLoggedIn ? "/user/account" : "/register"
        const errorMessage = (
            $isLoggedIn
            ? "Unable to save account settings. Please try again."
            : "Unable to create account. Please try again."
        )
        const successMessage = (
            $isLoggedIn
            ? "Account Settings Saved!"
            : "Account Created!"
        )

        try {
            const response = await postRequest(url, user) 
        } catch(error) {
            $alertMessage = errorMessage
            return
        }

        $alertMessage = successMessage

        if ($isLoggedIn) {
            deleteAccessToken()
        }

        gotoPage(PAGE_LOGIN)
    }

    let username = ""
    let emailAddress = ""
    let password = ""
    let passwordConfirm = ""

    const saveButtonText = $isLoggedIn ? "Save" : "Create"
    const headerText = $isLoggedIn ? "Account Setttings" : "Create Account"

    $: if ($currentUser && !username) {
        username = $currentUser.username
        emailAddress = $currentUser.email_address
    }

    $: isReady = !!(
        username
        && emailAddress
        && (
            $isLoggedIn
            ? (
                (password && passwordConfirm)
                || (!password && !passwordConfirm)
            ) : (
                password
                && passwordConfirm
            )
        )
    )
</script>

<section class="standard-border content">
    <div class="header">
        <h2>{headerText}</h2>
    </div>
    
    <form on:submit|preventDefault={save}>
        <div class="row">
            <Textfield bind:value={username} label="Username" variant="outlined" required={true} input$maxlength={20}>
                <svelte:fragment slot="helper">
                    <HelperText>Helper Text</HelperText>
                    <CharacterCounter>0 / 20</CharacterCounter>
                </svelte:fragment>
            </Textfield>
        </div>

        <div class="row">
            <Textfield bind:value={emailAddress} label="Email Address" variant="outlined" required={true}/>
        </div>

        <div class="row">
            <Textfield bind:value={password} label="Password" variant="outlined" type="password" required={!$isLoggedIn}/>
        </div>

        <div class="row">
            <Textfield bind:value={passwordConfirm} label="Confirm Password" variant="outlined" type="password" required={!$isLoggedIn}/>
        </div>

        <div class="row">
            <Button
                variant="raised"
                disabled={!isReady}
            >
                <Label>{saveButtonText}</Label>
            </Button>
        </div>
    </form>
</section>

<style lang="scss">
    @import "../css/constants";

    :global(.mdc-text-field) {
        width: 300px;
    }

    :global(.mdc-text-field-character-counter) {
        color: $primary-white !important;
    }

    .content {
        padding: 15px;
        width: fit-content;

        .row {
            margin-bottom: 10px;
        }
    }
</style>