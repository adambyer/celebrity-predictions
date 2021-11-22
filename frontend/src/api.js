import axios from "axios"

import {
    authRequired,
    getAccessToken,
} from "./auth_helpers"

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})


export async function getRequest(url, params = {}) {
    const accessToken = getAccessToken()
    const config = {
        headers: {Authorization: `Bearer ${accessToken}`},
        params,
    }
    return await API.get(url, config).catch((error) => {
        if (error.response.status === 401) {
            authRequired()
            throw 401
        }
    })
}

export async function patchRequest(url, data) {
    const accessToken = getAccessToken()
    const config = {
        headers: {Authorization: `Bearer ${accessToken}`}
    }
    return await API.patch(url, data, config).catch((error) => {
        if (error.response.status === 401) {
            authRequired()
            throw 401
        }
    })
}

export async function postRequest(url, data) {
    const accessToken = getAccessToken()
    const config = {
        headers: {Authorization: `Bearer ${accessToken}`}
    }
    return await API.post(url, data, config).catch((error) => {
        if (error.response.status === 401) {
            authRequired()
            throw 401
        }
    })
}

export async function deleteRequest(url, data) {
    const accessToken = getAccessToken()
    const config = {
        headers: {Authorization: `Bearer ${accessToken}`}
    }
    return await API.delete(url, config).catch((error) => {
        if (error.response.status === 401) {
            authRequired()
            throw 401
        }
    })
}

export default API
