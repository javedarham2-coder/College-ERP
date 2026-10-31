
import { useEffect, useState } from 'react';
import './App.css';

function getInitialTheme() {
  try {
    return localStorage.getItem('student-portal-theme') || 'dark';
  } catch {
    return 'dark';
  }
}

export default function App() {
  const [theme, setTheme] = useState(getInitialTheme);
  const [studentId, setStudentId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    document.documentElement.dataset.studentTheme = theme;

    try {
      localStorage.setItem('student-portal-theme', theme);
    } catch {
      // Theme still works for this session if storage is unavailable.
    }
  }, [theme]);

  function handleSubmit(event) {
    event.preventDefault();
    setError('');

    if (!studentId.trim() || !password) {
      setError('Please enter both your student ID and password.');
      return;
    }

    setError(
      'Student authentication is not connected yet. This is a frontend preview.'
    );
  }

  return (
    <main className={`student-login-page ${theme === 'light' ? 'login-page-theme-light' : 'login-page-theme-dark'}`}>
      <div className="ambient ambient-one" aria-hidden="true" />
      <div className="ambient ambient-two" aria-hidden="true" />

      <header className="login-topbar">

<a className="topbar-brand" href="#student-login" aria-label="College ERP student portal">
  <img
    className="college-logo"
    src="/college-logo.png"
    alt="College logo"
  />
  <span>
    <strong>Dr. Virendra Swarup Memorial Trust Group of Institutions</strong>
    <small>STUDENT INFORMATION SYSTEM</small>
  </span>
</a>


        <button
          type="button"
          className="theme-toggle"
          onClick={() => setTheme((current) => current === 'dark' ? 'light' : 'dark')}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
          <span aria-hidden="true">{theme === 'dark' ? '☼' : '☾'}</span>
          <span>{theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>
        </button>
      </header>

      <section className="login-layout" id="student-login">
        <aside className="login-intro">
          <span className="intro-eyebrow">
            YOUR ACADEMIC JOURNEY
          </span>
<p className="intro-description">
  Access your academic profile, attendance, fee records and examination
  results through your college's student information portal.
</p>


          <p className="intro-description">
            Stay connected with your academic life. Access your profile,
            attendance, fee information and results in one place.
          </p>

          <div className="intro-highlights">
            <div className="highlight-item">
              <span className="highlight-icon" aria-hidden="true">01</span>
              <span>
                <strong>Academic overview</strong>
                <small>Your student information, organized.</small>
              </span>
            </div>

            <div className="highlight-item">
              <span className="highlight-icon" aria-hidden="true">02</span>
              <span>
                <strong>Progress at a glance</strong>
                <small>Stay informed about your academics.</small>
              </span>
            </div>
          </div>

          <div className="intro-rule">
            <span />
            <small>LEARN · GROW · ACHIEVE</small>
          </div>
        </aside>

        <section className="login-card" aria-labelledby="login-heading">
          <div className="card-topline">
            <span className="secure-indicator">
              <span className="secure-dot" />
              STUDENT ACCESS
            </span>
            <span className="card-index">PORTAL / 01</span>
          </div>

          <div className="card-heading">
            <p className="card-kicker">WELCOME BACK</p>
            <h2 id="login-heading">Sign in to continue<span>.</span></h2>
            <p>Enter your student credentials to access your portal.</p>
          </div>

          <form className="student-login-form" onSubmit={handleSubmit} noValidate>
            <div className="form-field">
              <label htmlFor="studentId">Student ID or email</label>
              <input
                id="studentId"
                name="studentId"
                type="text"
                autoComplete="username"
                placeholder="e.g. student@college.edu"
                value={studentId}
                onChange={(event) => setStudentId(event.target.value)}
                aria-invalid={Boolean(error && !studentId.trim())}
              />
            </div>

            <div className="form-field">
              <div className="label-row">
                <label htmlFor="studentPassword">Password</label>
                <span className="field-note">Keep it secure</span>
              </div>

              <div className="password-control">
                <input
                  id="studentPassword"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  aria-invalid={Boolean(error && !password)}
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? 'HIDE' : 'SHOW'}
                </button>
              </div>
            </div>

            {error && (
              <p className="login-message" role="status">
                {error}
              </p>
            )}

            <button className="sign-in-button" type="submit">
              <span>Sign in to student portal</span>
              <span className="button-arrow" aria-hidden="true">↗</span>
            </button>

            <p className="form-security-note">
              Use the credentials provided by your institution.
            </p>
          </form>

          <div className="card-footer">
            <span className="footer-seal" aria-hidden="true">C</span>
            <span>
              <strong>College ERP</strong>
              <small>Student services, in one place.</small>
            </span>
          </div>
        </section>
      </section>

      <footer className="login-footer">
        <span>COLLEGE ERP · STUDENT SERVICES</span>
        <span>FRONTEND PREVIEW · AUTHENTICATION NOT CONNECTED</span>
      </footer>
    </main>
  );
}

