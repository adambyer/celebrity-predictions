import {get} from "svelte/store"
import {push} from "svelte-spa-router"

import {
    isLoading,
    isLoggedIn,
    currentUser,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    userPredictions,
    userLockedPredictionResults,
    requestedPage,
    leadersAllTime,
    leadersDaily,
    alertMessage,
} from "./store"
import {getRequest} from "./api"
import {
    PAGE_LOGIN,
    PAGE_ACCOUNT_SETTINGS,
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_PREDICTIONS,
    PAGE_LEADERBOARD,
    PAGES_REQUIRING_AUTH,
    PAGES_USING_AUTO_REFRESH,
    REFRESH_PAGE_MINUTES,
} from "./constants"
import {
    authRequired,
} from "./auth_helpers"

let refreshTimer = null
const refreshPageMilliseconds = REFRESH_PAGE_MINUTES * 1000 * 60

async function startTimer(page, twitterUsername) {
    refreshTimer = setTimeout(async () => {
        await gotoPage(page, twitterUsername, true)
    }, refreshPageMilliseconds)
}

function clearTimer() {
    if (refreshTimer) {
        clearTimeout(refreshTimer)
        refreshTimer = null
    }
}

export async function gotoPage(
    page,
    twitterUsername = "",
    isRefresh = false,
) {
    clearTimer()
    alertMessage.set("")

    if (!get(requestedPage)) {
        celebrityTwitterUsername.set(twitterUsername)
    }

    if (PAGES_REQUIRING_AUTH.includes(page) && !get(isLoggedIn)) {
        requestedPage.set(page)
        authRequired()
        push(PAGE_LOGIN)
        return
    }

    requestedPage.set("")
    push(page)

    if (PAGES_USING_AUTO_REFRESH.includes(page)) {
        await startTimer(page, twitterUsername)

        if (!isRefresh) {
            isLoading.set(true)
            celebrity.set(null)
            userPredictions.set([])
            userLockedPredictionResults.set([])
        }
    }

    if (page === PAGE_ACCOUNT_SETTINGS) {
        let accountResponse = null

        try {
            accountResponse = await getRequest("/user/account")
        } catch(error) {}

        if (accountResponse) {
            currentUser.set(accountResponse.data)
        }
    } else if (page === PAGE_CELEBRITY_LIST) {
        let celebrityListResponse = null

        try {
            celebrityListResponse = await getRequest("/celebrity")
        } catch(error) {}

        if (celebrityListResponse) {
            celebrities.set(celebrityListResponse.data)
        }
    } else if (page === PAGE_CELEBRITY) {
        let celebrityResponse = null
        try {
            celebrityResponse = await getRequest(`/celebrity/${get(celebrityTwitterUsername)}`)
        } catch(error) {}

        if (celebrityResponse) {
            celebrity.set(celebrityResponse.data)
        }
    } else if (page === PAGE_PREDICTIONS) {
        let predictionsResponse = null

        try {
            predictionsResponse = await getRequest("/user/prediction")
        } catch(error) {}
        
        if (predictionsResponse) {
            userPredictions.set(predictionsResponse.data)
        }

        let resultsResponse = null

        try {
            resultsResponse = await getRequest("/user/prediction-results/locked")
        } catch(error) {}
        
        if (resultsResponse) {
            userLockedPredictionResults.set(resultsResponse.data)
        }
    } else if (page === PAGE_LEADERBOARD) {
        let leadersAllTimeResponse = null

        try {
            leadersAllTimeResponse = await getRequest("/prediction-results/leaders/all-time")
        } catch(error) {}

        if (leadersAllTimeResponse) {
            leadersAllTime.set(leadersAllTimeResponse.data)
        }

        let leadersDailyResponse = null

        try {
            leadersDailyResponse = await getRequest("/prediction-results/leaders/daily")
        } catch(error) {}

        if (leadersDailyResponse) {
            leadersDaily.set(leadersDailyResponse.data)
        }
    }

    isLoading.set(false)
}