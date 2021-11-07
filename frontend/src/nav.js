import {get} from 'svelte/store'

import {
    currentPage,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    userPredictions,
} from "./store"
import {getRequest} from "./api"

export async function gotoPage(page) {
    currentPage.set(page)

    if (page === "celebrity-list") {
        const response = await getRequest("/celebrity")
        celebrities.set(response.data)
    } else if (page === "celebrity") {
        celebrity.set({})
        const response = await getRequest(`/celebrity/${get(celebrityTwitterUsername)}`)
        celebrity.set(response.data)
    } else if (page === "user-predictions") {
        userPredictions.set([])
        const response = await getRequest("/user/prediction")
        console.log("*** response.data", response.data)
        userPredictions.set(response.data)
    }
}