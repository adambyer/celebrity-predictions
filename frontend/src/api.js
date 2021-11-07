import axios from "axios"
import {get} from "svelte/store"

import {accessToken} from "./store"

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})

export async function getRequest(url) {
    const config = {
        headers: { Authorization: `Bearer ${get(accessToken)}`}
    }
    return await API.get(url, config)
}

export async function patchRequest(url, data) {
    const config = {
        headers: { Authorization: `Bearer ${get(accessToken)}`}
    }
    return await API.patch(url, data, config)
}

export default API
