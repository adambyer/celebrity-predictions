import {get} from 'svelte/store'

import {
    currentPage,
    accessToken,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    predictions,
} from "./store"
import API from "./api"

export async function gotoPage(page) {
    currentPage.set(page)
    console.log("*** gotoPage", page, get(accessToken))

    if (page === "celebrity-list") {
        const response = await API.get("/celebrity")
        celebrities.set(response.data)
    } else if (page === "celebrity") {
        celebrity.set({})
        const response = await API.get(`/celebrity/${get(celebrityTwitterUsername)}`)
        celebrity.set(response.data)
    } else if (page === "predictions") {
        predictions.set({})
        const config = {
            headers: { Authorization: `Bearer ${get(accessToken)}`}
        }
        const response = await API.get("/user/prediction", config)
        predictions.set(response.data)
    }
}