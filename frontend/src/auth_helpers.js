import Cookies from "js-cookie"

import {
    COOKIE_ACCESS_TOKEN,
    PAGE_LOGIN,
} from "./constants"
import {
    alertMessage,
    currentPage,
    isLoggedIn,
} from "./store"
import {
    gotoPage,
} from "./nav"

export function authRequired() {
    alertMessage.set("Login Required")
    currentPage.set(PAGE_LOGIN)
}

export function hasAccessToken() {
    return !!Cookies.get(COOKIE_ACCESS_TOKEN)
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
    gotoPage(PAGE_LOGIN)
    alertMessage.set("You have been logged out")
}