export function sortByDate(a, b, property) {
    if (a[property] > b[property]) {
        return -1
    } else if (a[property] < b[property]) {
        return 1
    }
    return 0
}