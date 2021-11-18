import {get} from "svelte/store"

import {
    isLoggedIn,
    currentPage,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    userPredictions,
    requestedPage,
} from "./store"
import {getRequest} from "./api"
import {
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_USER_PREDICTIONS,
    PAGES_REQUIRING_AUTH,
} from "./constants"
import {
    authRequired,
} from "./auth_helpers"

export async function gotoPage(page) {
    if (PAGES_REQUIRING_AUTH.includes(page) && !get(isLoggedIn)) {
        requestedPage.set(page)
        authRequired()
        return
    }
    
    currentPage.set(page)

    if (page === PAGE_CELEBRITY_LIST) {
        const response = await getRequest("/celebrity")

        if (response) {
            celebrities.set(response.data)
        }
    } else if (page === PAGE_CELEBRITY) {
        celebrity.set(null)
        const response = await getRequest(`/celebrity/${get(celebrityTwitterUsername)}`)

        if (response) {
            celebrity.set(response.data)
        }
    } else if (page === PAGE_USER_PREDICTIONS) {
        userPredictions.set([])
        const response = await getRequest("/user/prediction")
        
        if (response) {
            userPredictions.set(response.data)
        }
    }
}