
import { useState } from 'react'
import AdmissionDashboard from './AdmissionDashboard'
import './App.css'

function App() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showDashboard, setShowDashboard] = useState(false)

  function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!email.trim() || !password) {
      setError('Please fill in both fields.')
      return
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailPattern.test(email.trim())) {
      setError('Please enter a valid email address.')
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }

    // Frontend demo only: this does not authenticate the user.
    setShowDashboard(true)
  }

  if (showDashboard) {
    return (
      <AdmissionDashboard
        onLogout={() => {
          setShowDashboard(false)
          setPassword('')
        }}
      />
    )
  }

  return (
    <div className="page">
      <div className="login-card">
        <div className="logo">C</div>

        <h1>College ERP</h1>
        <p className="subtitle">Your college, connected.</p>

        <h2>Welcome back</h2>
        <p className="description">
          Sign in to access your account
        </p>

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
      </div>
    </div>
  )
}

export default App

