<script>
    import api from '../api'

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
            console.log("*** success", response)
        })
        .catch(function (error) {
            console.log("*** error", error)
        })
    }

    // $: console.log("*** username", username)
    // $: console.log("*** password", password)
</script>

<section>
    <form on:submit|preventDefault={login}>
        Username: <input bind:value={username}/><br/>
        Password: <input bind:value={password} type="password"/><br/>
        <button>Login</button>
    </form>
</section>