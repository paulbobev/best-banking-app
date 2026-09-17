import { clearCurrentUser, getToken } from './currentUser'

/* fetch wrapper that attaches the bearer token and turns a failed response
   into a thrown Error carrying the API's own detail message. */
export async function apiFetch(path, options = {}) {
    const token = getToken()

    const headers = { ...options.headers }
    if (options.body) headers['Content-Type'] = 'application/json'
    if (token) headers.Authorization = `Bearer ${token}`

    const res = await fetch(path, { ...options, headers })

    /* Only treat this as an expiry if we actually sent a token. Without
       that check a failed sign in would report itself as a dead session. */
    if (res.status === 401 && token) {
        clearCurrentUser()
        throw new Error('Your session has expired. Please sign in again.')
    }

    if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail || `Request failed (${res.status})`)
    }

    if (res.status === 204) return null
    return res.json()
}
