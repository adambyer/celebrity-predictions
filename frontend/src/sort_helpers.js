export function sortByCreatedAt(a, b) {
    if (a.created_at > b.created_at) {
        return -1
    } else if (a.created_at < b.created_at) {
        return 1
    }
    return 0
}