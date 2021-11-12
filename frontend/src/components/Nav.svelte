<script>
    import Button from '@smui/button';
    import {Label} from '@smui/common';
    import Tooltip, { Wrapper } from '@smui/tooltip';

    import {currentPage} from "../store"
    import {gotoPage} from "../nav"

    $: console.log("*** Nav currentPage", $currentPage)
</script>

<nav>
    <div class="w3-top">
        <div class="w3-bar w3-theme-d2 w3-left-align w3-large">
            <Wrapper>
                <a href="/" class="w3-bar-item w3-button w3-padding-large w3-theme-d4"><i class="fa fa-home w3-margin-right"></i>Logo</a>

                <Tooltip>Home</Tooltip>
            </Wrapper>

            <Wrapper>
                <a 
                    href="/celebrities"
                    class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white"
                    on:click|preventDefault={() => gotoPage("celebrity-list")}
                ><i class="fa fa-globe"></i></a>

                <Tooltip>Celebrities</Tooltip>
            </Wrapper>
            
            <Wrapper>
                <a
                    href="/predictions"
                    class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white"
                    on:click|preventDefault={() => gotoPage("user-predictions")}
                ><i class="far fa-list-alt"></i></a>

                <Tooltip>Predictions</Tooltip>
            </Wrapper>

            <div class="w3-dropdown-hover w3-hide-small w3-right">
                <button class="w3-button w3-padding-large">
                    <i class="fa fa-user"></i>
                </button>   

                <div class="w3-dropdown-content w3-card-4 w3-bar-block account-options">
                    <a href="/" class="w3-bar-item w3-button" on:click|preventDefault={() => gotoPage("login")}>Login</a>
                    <a href="/" class="w3-bar-item w3-button">Account Settings</a>
                </div>
            </div>
        </div>
    </div>
</nav>

<style>
    .account-options {
        right: 0;
        width: 300px;
    }
</style>