import { Link, Route, Routes } from 'react-router-dom'
import CreateAccount from './pages/CreateAccount'
import Dashboard from './pages/Dashboard'
import DevPage from './pages/DevPage'
import Login from './pages/Login'
import TransactionLookup from './pages/TransactionLookup'
import './App.css'

function App() {
  return (
    <>
      <nav className="flex gap-6 border-b px-8 py-4 text-sm">
        <Link to="/">Dashboard</Link>
        <Link to="/lookup">Transaction Lookup</Link>
        <Link to="/login">Sign in</Link>
        <Link to="/dev">Dev Tools</Link>
      </nav>

      <main className="p-8">
      <Routes>
        <Route path="/dev" element={<DevPage/>} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/lookup" element={<TransactionLookup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/accounts/new" element={<CreateAccount />} />
        <Route path="*" element={<p>Page not found</p>} />
      </Routes>
      </main>
    </>
  )
}

export default App
