import {getRequest} from "./api"

export async function celebritySearch(value) {
    const url = "/celebrity"
    const response = await getRequest(url, {search: value, limit: 10})

    if (!("data" in response)) {
        return []
    }
    
    return response.data.map(c => ({
        value: c.id,
        label: `${c.twitter_name} (${c.twitter_username})`,
    }))
}