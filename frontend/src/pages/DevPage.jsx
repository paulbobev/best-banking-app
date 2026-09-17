import { useState } from 'react'
import UserCard from '../components/UserCard'
import { clearCurrentUser, getCurrentUser, setCurrentUser } from '../currentUser'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

/* Scratch page for poking the API during development */
function DevPage() {
    const [userId, setUserId] = useState('1')
    const [accountType, setAccountType] = useState('CHECKING')
    const [output, setOutput] = useState(null)
    const [allUsers, setAllUsers] = useState(null)
    const [names, setNames] = useState([])
    const [signedIn, setSignedIn] = useState(getCurrentUser())

    async function call(label, url, options) {
        try {
            const res = await fetch(url, options)
            const body = await res.json()
            setOutput({ label, status: res.status, body })
        } catch (err) {
            setOutput({ label, status: 'ERR', body: err.message })
        }
    }

    /* Rebuilds a user list from every account, for eyeballing all the seed data at once */
    async function loadEveryone() {
        const res = await fetch('/api/accounts')
        if (!res.ok) return setOutput({ label: 'GET /api/accounts', status: res.status, body: null })

        const accounts = await res.json()
        const byName = new Map()
        for (const acc of accounts) {
            if (!byName.has(acc.userName)) byName.set(acc.userName, [])
            byName.get(acc.userName).push(acc)
        }
        setAllUsers([...byName].map(([name, accounts]) => ({ name, accounts })))
    }

    /* The distinct owner names across all accounts, used to pick who is signed in */
    async function loadNames() {
        const res = await fetch('/api/accounts')
        if (!res.ok) return
        const accounts = await res.json()
        setNames([...new Set(accounts.map((acc) => acc.userName))])
    }

    /* Stands in for logging in until there is a real sign in page */
    function signInAs(name) {
        const user = { name }
        setCurrentUser(user)
        setSignedIn(user)
    }

    function signOut() {
        clearCurrentUser()
        setSignedIn(null)
    }

    return (
        <div className="mx-auto max-w-3xl space-y-6">
            <h2>Dev Tools</h2>

            <Card className="text-left">
                <CardHeader>
                    <CardTitle>
                        Signed in as: {signedIn?.name ?? 'nobody'}
                    </CardTitle>
                </CardHeader>
                <CardContent className="flex flex-wrap gap-2">
                    <Button variant="outline" onClick={loadNames}>
                        Load users
                    </Button>
                    {names.map((name) => (
                        <Button key={name} onClick={() => signInAs(name)}>
                            {name}
                        </Button>
                    ))}
                    {signedIn && (
                        <Button variant="destructive" onClick={signOut}>
                            Sign out
                        </Button>
                    )}
                </CardContent>
            </Card>

            <Card className="text-left">
                <CardHeader>
                    <CardTitle>API</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex flex-wrap items-center gap-2">
                        <Input
                            className="w-32"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            placeholder="User ID"
                        />

                        <Select value={accountType} onValueChange={setAccountType}>
                            <SelectTrigger className="w-40">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="CHECKING">CHECKING</SelectItem>
                                <SelectItem value="SAVINGS">SAVINGS</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="flex flex-wrap gap-2">
                        <Button
                            onClick={() =>
                                call('POST /api/accounts', '/api/accounts', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({
                                        userId: Number(userId),
                                        accountType,
                                    }),
                                })
                            }
                        >
                            Create account
                        </Button>

                        <Button
                            variant="outline"
                            onClick={() => call('GET /api/accounts', '/api/accounts')}
                        >
                            List all accounts
                        </Button>

                        <Button variant="outline" onClick={loadEveryone}>
                            Preview all user cards
                        </Button>
                    </div>

                    {output && (
                        <pre className="bg-muted overflow-auto rounded-md p-4 text-xs">
                            {output.label} → {output.status}
                            {'\n'}
                            {JSON.stringify(output.body, null, 2)}
                        </pre>
                    )}
                </CardContent>
            </Card>

            {allUsers?.map((user) => (
                <UserCard key={user.name} user={user} />
            ))}
        </div>
    )
}

export default DevPage
