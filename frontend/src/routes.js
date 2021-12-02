import {
    PAGE_HOME,
    PAGE_ACCOUNT_REGISTRATION,
    PAGE_ACCOUNT_SETTINGS,
    PAGE_LOGIN,
    PAGE_CELEBRITY,
    PAGE_CELEBRITY_LIST,
    PAGE_CREATE_PREDICTION,
    PAGE_PREDICTIONS,
    PAGE_LEADERBOARD,
} from "./constants"

import Home from "./components/Home.svelte"
import AccountSettings from "./components/AccountSettings.svelte"
import Login from "./components/Login.svelte"
import Celebrity from "./components/Celebrity.svelte"
import CelebrityList from "./components/CelebrityList.svelte"
import CreatePrediction from "./components/CreatePrediction.svelte"
import UserPredictions from "./components/UserPredictions.svelte"
import Leaderboard from "./components/Leaderboard.svelte"

export default {
    [PAGE_HOME]: Home,
    [PAGE_ACCOUNT_REGISTRATION]: AccountSettings,
    [PAGE_ACCOUNT_SETTINGS]: AccountSettings,
    [PAGE_LOGIN]: Login,
    [PAGE_CELEBRITY]: Celebrity,
    [PAGE_CELEBRITY_LIST]: CelebrityList,
    [PAGE_CREATE_PREDICTION]: CreatePrediction,
    [PAGE_PREDICTIONS]: UserPredictions,
    [PAGE_LEADERBOARD]: Leaderboard,
}