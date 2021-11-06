<script>
    import {celebrities} from "../store"
    import api from '../api'

    async function getCelebrities() {
        const response = await api.get("/celebrity")
        $celebrities = response.data
    }
</script>

<nav>
    <ul>
        <li><a href="/" on:click|preventDefault={getCelebrities}>Celebrities</a></li>
    </ul>
    <div class="w3-top">
        <div class="w3-bar w3-theme-d2 w3-left-align w3-large">
            <a href="/" class="w3-bar-item w3-button w3-padding-large w3-theme-d4"><i class="fa fa-home w3-margin-right"></i>Logo</a>
            <a 
                href="/celebrities"
                class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white"
                title="Celebrities"
                on:click|preventDefault={getCelebrities}
            ><i class="fa fa-globe"></i></a>
            <a href="/" class="w3-bar-item w3-button w3-hide-small w3-padding-large w3-hover-white" title="Messages"><i class="fa fa-envelope"></i></a>
            <div class="w3-dropdown-hover w3-hide-small">
                <button class="w3-button w3-padding-large" title="Notifications"><i class="fa fa-bell"></i><span class="w3-badge w3-right w3-small w3-green">3</span></button>     
                <div class="w3-dropdown-content w3-card-4 w3-bar-block" style="width:300px">
                    <a href="/" class="w3-bar-item w3-button">One new friend request</a>
                    <a href="/" class="w3-bar-item w3-button">John Doe posted on your wall</a>
                    <a href="/" class="w3-bar-item w3-button">Jane likes your post</a>
                </div>
            </div>
            <a href="/" class="w3-bar-item w3-button w3-hide-small w3-right w3-padding-large w3-hover-white" title="Account Settings"><i class="fa fa-user"></i></a>
        </div>
    </div>
</nav>