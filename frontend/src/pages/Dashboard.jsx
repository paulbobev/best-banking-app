import { useEffect, useState } from 'react'
import UserCard from '../components/UserCard'
import { getCurrentUser } from '../currentUser'


/* Dashboard for the signed-in user */
function Dashboard() {
    const user = getCurrentUser()
    const [accounts, setAccounts] = useState(null)
    const [error, setError] = useState(null)

    useEffect(() => {
        if (!user) return

        async function loadAccounts() {
            try {
                const res = await fetch(
                    `/api/users/${encodeURIComponent(user.name)}/accounts`
                )
                if (!res.ok) throw new Error(`Could not load accounts (${res.status})`)
                setAccounts(await res.json())
            } catch (err) {
                setError(err.message)
            }
        }
        loadAccounts()
    }, [user?.name])

    if (!user) return <p className="text-muted-foreground">No user selected. Pick one at /dev.</p>
    if (error) return <p className="text-destructive">{error}</p>
    if (accounts === null) return <p className="text-muted-foreground">Loading dashboard...</p>

    return (
        <div className="mx-auto max-w-3xl">
            <UserCard user={{ ...user, accounts }} />
        </div>
    )
}

export default Dashboard
