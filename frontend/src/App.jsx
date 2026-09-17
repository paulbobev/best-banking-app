import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from './layouts/AppLayout'
import CreateAccount from './pages/CreateAccount'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import TransactionLookup from './pages/TransactionLookup'
import Settings from './pages/Settings'
import './App.css'

/* The homepage is still the one page not written yet, so / drops straight
   into the app and the guard sorts out where you actually land. */
function App() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Public: no sidebar, no token needed. */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<CreateAccount />} />

            {/* AppLayout draws the sidebar around all of these. */}
            <Route element={<AppLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/lookup" element={<TransactionLookup />} />
                <Route path="/accounts/new" element={<CreateAccount />} />
                <Route path="/settings" element={<Settings />} />
            </Route>

            <Route path="*" element={<p>Page not found</p>} />
        </Routes>
    )
}

export default App
