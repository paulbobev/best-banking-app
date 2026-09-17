import { useState } from "react";
import "./App.css";
import CreateAccount from "./CreateAccount.jsx";

function App() {
  const [screen, setScreen] = useState("login"); // 'login' | 'create' | 'account'
  const [session, setSession] = useState(null); // { accountId } once logged in

  const [accountId, setAccountId] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState(null);
  const [loggingIn, setLoggingIn] = useState(false);

  const [transactions, setTransactions] = useState([]);
  const [txError, setTxError] = useState(null);
  const [loadingTx, setLoadingTx] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setLoginError(null);
    setLoggingIn(true);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ accountId, password }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Invalid account ID or password");
      }
      setSession({ accountId });
      setPassword("");
      setScreen("account");
      await loadTransactions(accountId);
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoggingIn(false);
    }
  }

  async function loadTransactions(id) {
    setTxError(null);
    setLoadingTx(true);
    try {
      const res = await fetch(`/api/accounts/${id}/transactions`);
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Could not load transactions");
      }
      setTransactions(await res.json());
    } catch (err) {
      setTxError(err.message);
      setTransactions([]);
    } finally {
      setLoadingTx(false);
    }
  }

  function handleLogout() {
    setSession(null);
    setAccountId("");
    setTransactions([]);
    setTxError(null);
    setLoginError(null);
    setScreen("login");
  }

  function handleAccountCreated(account) {
    // New account created — drop them back on the login screen to sign in,
    // pre-filling the account ID if the API returned one.
    setAccountId(account?.accountId ?? "");
    setScreen("login");
  }

  if (screen === "create") {
    return (
      <CreateAccount
        onCreated={handleAccountCreated}
        onBack={() => setScreen("login")}
      />
    );
  }

  if (screen === "login") {
    return (
      <div id="center">
        <div className="auth-card">
          <h1 className="auth-title">Sign in</h1>
          <p className="auth-subtitle">
            Enter your account ID and password to view your account.
          </p>

          <form className="auth-form" onSubmit={handleLogin}>
            <label className="field">
              <span>Account ID</span>
              <input
                value={accountId}
                onChange={(e) => setAccountId(e.target.value)}
                placeholder="e.g. 100293"
                autoComplete="username"
                required
              />
            </label>

            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                autoComplete="current-password"
                required
              />
            </label>

            {loginError && <p className="form-error">{loginError}</p>}

            <button
              type="submit"
              className="primary-button"
              disabled={loggingIn}
            >
              {loggingIn ? "Signing in…" : "Sign in"}
            </button>
          </form>

          <p className="auth-switch">
            New here?{" "}
            <button
              type="button"
              className="link-button"
              onClick={() => setScreen("create")}
            >
              Create an account
            </button>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div id="center" className="account-view">
      <div className="account-header">
        <div>
          <h1>Account {session.accountId}</h1>
          <p className="account-subtitle">Recent transactions</p>
        </div>
        <button
          type="button"
          className="secondary-button"
          onClick={handleLogout}
        >
          Log out
        </button>
      </div>

      {txError && <p className="form-error">{txError}</p>}

      {loadingTx ? (
        <p className="muted">Loading transactions…</p>
      ) : transactions.length === 0 ? (
        <p className="muted">No transactions to show.</p>
      ) : (
        <table className="tx-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Amount</th>
              <th>Date</th>
            </tr>
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
      )}
    </div>
  );
}

export default App;
