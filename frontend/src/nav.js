import Cookies from "js-cookie"
import {get} from "svelte/store"

import {
    alertMessage,
    currentPage,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    userPredictions,
    requestedPage,
} from "./store"
import {getRequest} from "./api"
import {
    PAGE_LOGIN,
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_USER_PREDICTIONS,
    PAGES_REQUIRING_AUTH,
    COOKIE_ACCESS_TOKEN,
} from "./constants"

export async function gotoPage(page) {
    if (PAGES_REQUIRING_AUTH.includes(page) && !Cookies.get(COOKIE_ACCESS_TOKEN)) {
        alertMessage.set("Login Required")
        currentPage.set(PAGE_LOGIN)
        requestedPage.set(page)
        return
    }

    currentPage.set(page)
    requestedPage.set("")

    if (page === PAGE_CELEBRITY_LIST) {
        const response = await getRequest("/celebrity")
        celebrities.set(response.data)
    } else if (page === PAGE_CELEBRITY) {
        celebrity.set({})
        const response = await getRequest(`/celebrity/${get(celebrityTwitterUsername)}`)
        celebrity.set(response.data)
    } else if (page === PAGE_USER_PREDICTIONS) {
        userPredictions.set([])
        const response = await getRequest("/user/prediction")
        userPredictions.set(response.data)
    }
}