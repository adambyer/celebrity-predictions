import dayjs from "dayjs"

export function formatDate(dateString) {
    const d = new Date(dateString)
    return dayjs(d).format("MMM D")
}

export function formatDateAndTime(dateString) {
    const d = new Date(dateString)
    return dayjs(d).format("MMM D, h:mm A")
}