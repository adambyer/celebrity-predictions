const url_root = "http://127.0.0.1:8000"
let axios = null

requirejs(["axios"], (a) => {
    axios = a
})

function login() {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    const formData = new FormData()

    formData.append("username", username)
    formData.append("password", password)

    axios({
        method: "post",
        url: `${url_root}/token`,
        data: formData,
        headers: { "Content-Type": "multipart/form-data" },
    })
    .then(function (response) {
        console.log("*** success", response)
    })
    .catch(function (error) {
        console.log("*** error", error)
    })
}

function getCelebrities() {
    axios({
        method: "get",
        url: `${url_root}/celebrity`,
    })
    .then(function (response) {
        const table = document.getElementById("celebrity-table")
        response.data.forEach(c => {
            const row = `<tr><td><a href="javascript:void(0)" onclick="showCelebrity('${c.twitter_username}');event.preventDefault();">${c.twitter_username}</a></td><td>${c.twitter_name}</td><td>${c.twitter_description}</td></tr>`
            table.insertAdjacentHTML('beforeend', row)
        })
    })
    .catch(function (error) {
        console.log("*** getCelebrities error", error)
    })
}

function showCelebrity(twitter_username) {
    console.log("*** showCelebrity", twitter_username)
    axios({
        method: "get",
        url: `${url_root}/celebrity/${twitter_username}`,
    })
    .then(function (response) {
        console.log("*** showCelebrity success", response)
        const img = document.getElementById("celebrity-image")
        img.setAttribute("src", response.data.twitter_profile_image_url)

        const table = document.getElementById("tweet-table")
        response.data.tweets.forEach(t => {
            const row = `<tr><td><a href="javascript:void(0)">${t.text}</a></td><td>Likes: ${t.public_metrics.like_count}</td><td>${t.created_at}</td></tr>`
            table.insertAdjacentHTML('beforeend', row)
        })
    })
    .catch(function (error) {
        console.log("*** showCelebrity error", error)
    })
}