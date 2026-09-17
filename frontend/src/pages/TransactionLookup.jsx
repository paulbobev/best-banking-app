import { useState } from 'react'

function TransactionLookup() {
  const [accountId, setAccountId] = useState('')
  const [transactions, setTransactions] = useState([])
  const [error, setError] = useState(null)

  async function lookup(e) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`/api/accounts/${accountId}/transactions`)
      if (!res.ok) throw new Error((await res.json()).detail)
      setTransactions(await res.json())
    } catch (err) {
      setError(err.message)
      setTransactions([])
    }
  }

  return (
    <>
      <form onSubmit={lookup}>
        <input
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          placeholder="Account ID"
        />
        <button type="submit">Look up</button>
      </form>

      {error && <p>{error}</p>}

      <table>
        <thead>
          <tr><th>Type</th><th>Amount</th><th>Date</th></tr>
        </thead>
        <tbody>
          {transactions.map((t, i) => (
            <tr key={i}>
              <td>{t.type}</td>
              <td>{t.amount}</td>
              <td>{t.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export default TransactionLookup
