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
        console.log("*** getCelebrities success", response)
        response.data.forEach(c => {
            const table = document.getElementById("celebrity_table")
            const row = `<tr><td><a href="javascript:void(0)" onclick="showCelebrity('${c.twitter_profile_image_url}');event.preventDefault();">${c.twitter_username}</a></td><td>${c.twitter_name}</td><td>${c.twitter_description}</td></tr>`
            table.insertAdjacentHTML('beforeend', row)
        })
    })
    .catch(function (error) {
        console.log("*** getCelebrities error", error)
    })
}

function showCelebrity(image_url) {
    console.log("*** showCelebrity", image_url)
    const img = document.getElementById("celebrity_image")
    img.setAttribute("src", image_url)
}