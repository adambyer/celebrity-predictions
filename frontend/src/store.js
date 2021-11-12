import {writable} from "svelte/store"

export const currentPage = writable("home")
export const requestedPage = writable("")
export const celebrities = writable([])
export const celebrityTwitterUsername = writable("")
export const celebrity = writable({})
export const userPredictions = writable([])
export const alertMessage = writable("")
