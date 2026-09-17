import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import CreateAccount from './pages/CreateAccount'
import Dashboard from './pages/Dashboard'
import DevPage from './pages/DevPage'
import TransactionLookup from './pages/TransactionLookup'
import Settings from './pages/Settings'
import './App.css'

/* /login and /signup are unrouted until the homepage and sign in pages
   land. Login.jsx is still in pages/, just not reachable yet. */
function App() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* AppLayout draws the sidebar around all of these. */}
            <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/lookup" element={<TransactionLookup />} />
                <Route path="/accounts/new" element={<CreateAccount />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/dev" element={<DevPage />} />
            </Route>

            <Route path="*" element={<p>Page not found</p>} />
        </Routes>
    )
}

export default App
