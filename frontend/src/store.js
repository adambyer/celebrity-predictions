import {writable, readable} from "svelte/store"

import {hasAccessToken} from "./auth_helpers"

export const currentPage = writable("home")
export const requestedPage = writable("")
export const celebrities = writable([])
export const celebrityTwitterUsername = writable("")
export const celebrity = writable(null)
export const userPredictions = writable([])
export const alertMessage = writable("")
export const isLoggedIn = writable(hasAccessToken())
