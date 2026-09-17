import { useEffect, useState } from 'react'
import { apiFetch } from '../api'
import { Badge } from '@/components/ui/badge'
import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'


function AccountCard({account}) {

    const [transactions, setTransactions] = useState(null)

    useEffect(() => {
        async function loadTransactions() {
            try {
                setTransactions(
                    await apiFetch(`/api/accounts/${account.accountId}/transactions`)
                )
            } catch {
                /* Leave it null: the card still shows the balance and type */
            }
        }
        loadTransactions()
    }, [account.accountId])

    if (!account) return null

    const latestTransaction = transactions?.[0] ?? null
    const oldestTransaction = transactions?.[transactions.length - 1] ?? null
    const daysOpen = oldestTransaction ? daysSince(oldestTransaction.date) : null

    return (
        <Card className="text-left">
            <CardHeader>
                <CardDescription>Account #{account.accountId}</CardDescription>
                <CardTitle className="text-3xl tabular-nums">
                    ${Number(account.balance).toFixed(2)}
                </CardTitle>
                <CardAction>
                    <Badge variant="secondary">{account.accountType}</Badge>
                </CardAction>
            </CardHeader>
            <CardContent className="text-muted-foreground space-y-1 text-sm">
                <p>
                    {daysOpen !== null
                        ? `Open for ${daysOpen} day${daysOpen === 1 ? '' : 's'} (approx.)`
                        : 'Days open unknown'}
                </p>
                {latestTransaction ? (
                    <p>
                        Last transaction: {latestTransaction.type} $
                        {Number(latestTransaction.amount).toFixed(2)} on {latestTransaction.date}
                    </p>
                ) : (
                    <p>No transactions yet</p>
                )}
            </CardContent>
        </Card>
    )
}

// Transaction dates come as "YYYY-MM-DD HH:MM:SS"
function daysSince(dateStr) {
    const [datePart] = dateStr.split(' ')
    const [year, month, day] = datePart.split('-').map(Number)
    const date = new Date(year, month - 1, day)
    const diffMs = Date.now() - date.getTime()
    return Math.floor(diffMs / (1000 * 60 * 60 * 24))
}

export default AccountCard
