import Cookies from "js-cookie"

import {
    COOKIE_ACCESS_TOKEN,
} from "./constants"
import {
    alertMessage,
    isLoggedIn,
    currentUser,
} from "./store"

export function authRequired() {
    alertMessage.set("Login Required")
    deleteAccessToken()
}

export function setAccessToken(accessToken) {
    Cookies.set(COOKIE_ACCESS_TOKEN, accessToken)
    isLoggedIn.set(true)
}

export function getAccessToken() {
    return Cookies.get(COOKIE_ACCESS_TOKEN)
}

export function deleteAccessToken() {
    Cookies.remove(COOKIE_ACCESS_TOKEN)
    isLoggedIn.set(false)
    currentUser.set(null)
}