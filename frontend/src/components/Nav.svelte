<script>
    import {currentPage} from "../store"
    import {gotoPage} from "../nav"

    $: console.log("*** Nav currentPage", $currentPage)
</script>

<nav>
    <div class="w3-top">
        <div class="w3-bar w3-theme-d2 w3-left-align w3-large">
            <a href="/" class="w3-bar-item w3-button w3-padding-large w3-theme-d4"><i class="fa fa-home w3-margin-right"></i>Logo</a>

            <a 
                href="/celebrities"
                class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white"
                title="Celebrities"
                on:click|preventDefault={() => gotoPage("celebrity-list")}
            ><i class="fa fa-globe"></i></a>
            
            <a 
                href="/predictions"
                class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white"
                title="Predictions"
                on:click|preventDefault={() => gotoPage("predictions")}
            ><i class="far fa-list-alt"></i></a>

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