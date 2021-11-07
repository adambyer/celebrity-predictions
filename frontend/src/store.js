import {writable} from "svelte/store"

export const currentPage = writable("home")
export const celebrities = writable([])
export const celebrityTwitterUsername = writable("")
export const celebrity = writable({})
export const predictions = writable([])

// TODO: cookie?
export const accessToken = writable("")
