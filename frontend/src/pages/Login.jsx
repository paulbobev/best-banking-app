import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { setCurrentUser } from "../currentUser";

function Login() {
  const [accountId, setAccountId] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState(null);
  const [loggingIn, setLoggingIn] = useState(false);
  const navigate = useNavigate();

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
      setCurrentUser({ accountId });
      setPassword("");
      navigate("/lookup");
    } catch (err) {
      setLoginError(err.message);
    } finally {
      setLoggingIn(false);
    }
  }

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

          <button type="submit" className="primary-button" disabled={loggingIn}>
            {loggingIn ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="auth-switch">
          New here? <Link to="/accounts/new">Create an account</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
