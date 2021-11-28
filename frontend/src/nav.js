import {get} from "svelte/store"

import {
    isLoading,
    isLoggedIn,
    currentUser,
    currentPage,
    celebrities,
    celebrityTwitterUsername,
    celebrity,
    userPredictions,
    userLockedPredictionResults,
    requestedPage,
    leaders,
} from "./store"
import {getRequest} from "./api"
import {
    PAGE_ACCOUNT_SETTINGS,
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_USER_PREDICTIONS,
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

    if (!get(requestedPage)) {
        celebrityTwitterUsername.set(twitterUsername)
    }

    if (PAGES_REQUIRING_AUTH.includes(page) && !get(isLoggedIn)) {
        requestedPage.set(page)
        authRequired()
        return
    }

    requestedPage.set("")
    currentPage.set(page)

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
        const accountResponse = await getRequest("/user/account")

        if (accountResponse) {
            currentUser.set(accountResponse.data)
        }
    } else if (page === PAGE_CELEBRITY_LIST) {
        const celebrityListResponse = await getRequest("/celebrity")

        if (celebrityListResponse) {
            celebrities.set(celebrityListResponse.data)
        }
    } else if (page === PAGE_CELEBRITY) {
        const celebrityResponse = await getRequest(`/celebrity/${get(celebrityTwitterUsername)}`)

        if (celebrityResponse) {
            celebrity.set(celebrityResponse.data)
        }
    } else if (page === PAGE_USER_PREDICTIONS) {
        const predictionsResponse = await getRequest("/user/prediction")
        
        if (predictionsResponse) {
            userPredictions.set(predictionsResponse.data)
        }

        const resultsResponse = await getRequest("/user/prediction-results/locked")
        
        if (resultsResponse) {
            userLockedPredictionResults.set(resultsResponse.data)
        }
    } else if (page === PAGE_LEADERBOARD) {
        const leadersResponse = await getRequest("/prediction/leaders")

        if (leadersResponse) {
            leaders.set(leadersResponse.data)
        }
    }

    isLoading.set(false)
}