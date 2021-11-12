import Cookies from "js-cookie"
import axios from "axios"

import {COOKIE_ACCESS_TOKEN} from "./constants"

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})

function _getAccessToken() {
    return Cookies.get(COOKIE_ACCESS_TOKEN)
}

export async function getRequest(url) {
    const accessToken = _getAccessToken()
    const config = {
        headers: { Authorization: `Bearer ${accessToken}`}
    }
    return await API.get(url, config)
}

export async function patchRequest(url, data) {
    const accessToken = _getAccessToken()
    const config = {
        headers: { Authorization: `Bearer ${accessToken}`}
    }
    return await API.patch(url, data, config)
}

export default API
