
import { useState } from 'react'
import AdmissionDashboard from './AdmissionDashboard'
import './App.css'

function App() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showDashboard, setShowDashboard] = useState(false)
  const [theme, setTheme] = useState(
    () => localStorage.getItem('college-erp-theme') || 'light'
  )

  function toggleTheme() {
    setTheme(current => {
      const next = current === 'light' ? 'dark' : 'light'
      localStorage.setItem('college-erp-theme', next)
      return next
    })
  }

  function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!email.trim() || !password) {
      setError('Please fill in both fields.')
      return
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setError('Please enter a valid email address.')
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }

    // Demo only. This does not authenticate the user.
    setShowDashboard(true)
  }

  if (showDashboard) {
    return (
      <AdmissionDashboard
        theme={theme}
        onToggleTheme={toggleTheme}
        onLogout={() => {
          setShowDashboard(false)
          setPassword('')
          setError('')
        }}
      />
    )
  }

  return (
    <div className={`page theme-${theme}`}>
      <button
        className="theme-toggle"
        type="button"
        onClick={toggleTheme}
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      >
        {theme === 'light' ? '☾ Dark mode' : '☀ Light mode'}
      </button>

      <main className="login-card">
        <div className="login-brand">
          <img
            className="college-logo"
            src="/college-logo.png"
            alt="College logo"
            onError={event => {
              event.currentTarget.style.display = 'none'
            }}
          />
          <h1>College ERP</h1>
          <p className="subtitle">Your college, connected.</p>
        </div>

        <section className="login-welcome">
          <h2>Welcome back</h2>
          <p className="description">
            Sign in to access your account
          </p>
        </section>

        <form onSubmit={handleSubmit} noValidate>
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            type="email"
            placeholder="you@college.edu"
            value={email}
            onChange={event => {
              setEmail(event.target.value)
              setError('')
            }}
            autoComplete="username"
            aria-invalid={Boolean(error)}
          />

          <label htmlFor="password">Password</label>
          <div className="password-wrapper">
            <input
              id="password"
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter your password"
              value={password}
              onChange={event => {
                setPassword(event.target.value)
                setError('')
              }}
              autoComplete="current-password"
              aria-invalid={Boolean(error)}
            />
            <button
              className="toggle-password"
              type="button"
              onClick={() => setShowPassword(value => !value)}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>

          {error && (
            <p className="form-error" role="alert">{error}</p>
          )}

          <button className="submit-button" type="submit">
            Sign in
          </button>
        </form>

        <p className="footer">
          College ERP · Student &amp; Staff Portal
        </p>
      </main>
    </div>
  )
}

export default App
