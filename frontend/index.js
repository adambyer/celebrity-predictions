const url_root = "http://127.0.0.1:8000"
let axios = null

requirejs(["axios"], (a) => {
    console.log("*** axios loaded")
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