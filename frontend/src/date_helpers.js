export function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString(
        'en-us',
        {
            year: "numeric",
            month: "short",
            day: "numeric",
        }
    )
}

export function formatDateAndTime(dateString) {
    return new Date(dateString).toLocaleDateString(
        'en-us',
        {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
            hour12: true,
        }
    )
}