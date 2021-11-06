import {get} from 'svelte/store'

import {currentPage, celebrities, celebrityTwitterUsername, celebrity} from "./store"
import API from "./api"

export async function gotoPage(page) {
    currentPage.set(page)
    console.log("*** gotoPage", page)

    if (page === "celebrity-list") {
        const response = await API.get("/celebrity")
        celebrities.set(response.data)
    } else if (page === "celebrity") {
        celebrity.set({})
        const response = await API.get(`celebrity/${get(celebrityTwitterUsername)}`)
        celebrity.set(response.data)
    }
}