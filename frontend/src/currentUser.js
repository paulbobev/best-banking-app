/* Small wrapper around localStorage so the signed in user survives a refresh */

const KEY = 'currentUser'

/* Stores the user object returned by the API at sign in */
export function setCurrentUser(user) {
    localStorage.setItem(KEY, JSON.stringify(user))
}

/* Returns the stored user, or null if nobody is signed in */
export function getCurrentUser() {
    const raw = localStorage.getItem(KEY)
    if (!raw) return null
    try {
        return JSON.parse(raw)
    } catch {
        return null
    }
}

/* Removes the stored user */
export function clearCurrentUser() {
    localStorage.removeItem(KEY)
}
