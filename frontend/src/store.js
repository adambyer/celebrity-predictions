import Cookies from "js-cookie"
import {writable} from "svelte/store"

import {
    COOKIE_ACCESS_TOKEN,
} from "./constants"


// This can't be in auth_helpers (circular reference).
function hasAccessToken() {
    return !!Cookies.get(COOKIE_ACCESS_TOKEN)
}


export const isLoggedIn = writable(hasAccessToken())
export const isLoading = writable(false)
export const currentUser = writable(null)
export const currentPage = writable("home")
export const requestedPage = writable("")
export const alertMessage = writable("")
export const celebrities = writable([])
export const celebrityTwitterUsername = writable("")
export const celebrity = writable(null)
export const userPredictions = writable([])
export const userLockedPredictionResults = writable([])
export const leadersAllTime = writable([])
export const leadersDaily = writable([])
