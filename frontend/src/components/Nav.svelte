<script>
    import Tooltip, { Wrapper } from '@smui/tooltip';

    import {gotoPage} from "../nav"
    import {
        PAGE_HOME,
        PAGE_CELEBRITY_LIST,
        PAGE_LOGIN,
        PAGE_USER_PREDICTIONS,
    } from "../constants"
    import {
        currentPage,
        isLoggedIn,
    } from "../store"
    import {
        deleteAccessToken,
    } from "../auth_helpers"

    function logOut() {
        deleteAccessToken()
        gotoPage(PAGE_LOGIN)
        alertMessage.set("You have been logged out")
    }
</script>

<nav>
    <div class="w3-top">
        <div class="w3-bar w3-theme-d2 w3-left-align w3-large">
            <Wrapper>
                <a 
                    href="/"
                    class="w3-bar-item w3-button w3-hide-small w3-padding-large"
                    class:current-page={$currentPage === PAGE_HOME}
                    on:click|preventDefault={() => gotoPage(PAGE_HOME)}
                ><i class="fa fa-home"></i></a>

                <Tooltip>Home</Tooltip>
            </Wrapper>

            <Wrapper>
                <a 
                    href="/celebrities"
                    class="w3-bar-item w3-button w3-hide-small w3-padding-large"
                    class:current-page={$currentPage === PAGE_CELEBRITY_LIST}
                    on:click|preventDefault={() => gotoPage(PAGE_CELEBRITY_LIST)}
                ><i class="fa fa-globe"></i></a>

                <Tooltip>Celebrities</Tooltip>
            </Wrapper>
            
            <Wrapper>
                <a
                    href="/predictions"
                    class="w3-bar-item w3-button w3-hide-small w3-padding-large"
                    class:current-page={$currentPage === PAGE_USER_PREDICTIONS}
                    on:click|preventDefault={() => gotoPage(PAGE_USER_PREDICTIONS)}
                ><i class="far fa-list-alt"></i></a>

                <Tooltip>Predictions</Tooltip>
            </Wrapper>

            <div class="w3-dropdown-hover w3-hide-small w3-right">
                <button class="w3-button w3-padding-large">
                    <i class="fa fa-user"></i>
                </button>   

                <div class="w3-dropdown-content w3-card-4 w3-bar-block account-options">
                    {#if $isLoggedIn}
                        <a href="/" class="w3-bar-item w3-button" on:click|preventDefault={() => logOut()}>Logout</a>
                    {:else}
                        <a href="/" class="w3-bar-item w3-button" on:click|preventDefault={() => gotoPage(PAGE_LOGIN)}>Login</a>
                    {/if}
                    <a href="/" class="w3-bar-item w3-button">Account Settings</a>
                </div>
            </div>
        </div>
    </div>
</nav>

<style lang="scss">
    .account-options {
        right: 0;
        width: 300px;
    }

    .current-page {
        background-color: #1a8cd3;
    }

    .w3-button {
        color: #f5f7f8 !important;

        &:hover {
            // background-color: unset !important;

            i {
                color: black !important;
            }
        }
    }

    .w3-dropdown-content {
        background-color: #1DA1F2;

        .w3-bar-item {
            &:hover {
                background-color: #1a8cd3;
            }
        }
    }
</style>