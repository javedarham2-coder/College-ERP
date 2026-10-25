
import { useMemo, useState } from 'react'
import './AdmissionDashboard.css'

const initialApplications = [
  { id: 'APP-1001', name: 'Aarav Sharma', email: 'aarav@example.com', course: 'B.Tech CSE', date: '2026-10-20', status: 'Pending' },
  { id: 'APP-1002', name: 'Ananya Verma', email: 'ananya@example.com', course: 'B.Tech ECE', date: '2026-10-19', status: 'Approved' },
  { id: 'APP-1003', name: 'Rohan Singh', email: 'rohan@example.com', course: 'BBA', date: '2026-10-18', status: 'Pending' },
  { id: 'APP-1004', name: 'Priya Gupta', email: 'priya@example.com', course: 'B.Com', date: '2026-10-17', status: 'Rejected' },
  { id: 'APP-1005', name: 'Kabir Khan', email: 'kabir@example.com', course: 'B.Tech CSE', date: '2026-10-16', status: 'Pending' },
]

const navItems = [
  { label: 'Overview', icon: '◫' },
  { label: 'Applications', icon: '▤' },
  { label: 'Reports', icon: '▥' },
]

function AdmissionDashboard({ onLogout }) {
  const [applications, setApplications] = useState(initialApplications)
  const [activeNav, setActiveNav] = useState('Overview')
  const [filter, setFilter] = useState('All')
  const [search, setSearch] = useState('')
  const [selected, setSelected] = useState(null)
  const [notice, setNotice] = useState('')

  const counts = useMemo(() => ({
    Total: applications.length,
    Pending: applications.filter(a => a.status === 'Pending').length,
    Approved: applications.filter(a => a.status === 'Approved').length,
    Rejected: applications.filter(a => a.status === 'Rejected').length,
  }), [applications])

  const filtered = applications.filter(app => {
    const matchesFilter = filter === 'All' || app.status === filter
    const query = search.toLowerCase()
    const matchesSearch =
      app.name.toLowerCase().includes(query) ||
      app.id.toLowerCase().includes(query) ||
      app.course.toLowerCase().includes(query)

    return matchesFilter && matchesSearch
  })

  function updateStatus(id, status) {
    setApplications(current =>
      current.map(app => app.id === id ? { ...app, status } : app)
    )
    setSelected(null)
    setNotice(`Application ${id} marked ${status.toLowerCase()}. Demo data only.`)
  }

  return (
    <div className="admin-layout">
      <aside className="admin-sidebar">
        <div className="admin-brand">
          <div className="admin-logo">C</div>
          <div>
            <strong>College ERP</strong>
            <span>Administration</span>
          </div>
        </div>

        <p className="nav-heading">WORKSPACE</p>
        <nav className="admin-nav">
          {navItems.map(item => (
            <button
              key={item.label}
              className={activeNav === item.label ? 'nav-item active' : 'nav-item'}
              onClick={() => {
                setActiveNav(item.label)
                setNotice('')
              }}
            >
              <span className="nav-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="staff-profile">
            <div className="staff-avatar">AS</div>
            <div>
              <strong>Admission Staff</strong>
              <span>Staff account</span>
            </div>
          </div>
          <button className="logout-button" onClick={onLogout}>
            ← Sign out
          </button>
        </div>
      </aside>

      <main className="admin-main">
        <header className="admin-topbar">
          <div>
            <span className="breadcrumb">Workspace / {activeNav}</span>
            <h1>{activeNav === 'Overview' ? 'Admission Overview' : activeNav}</h1>
          </div>
          <div className="topbar-right">
            <span className="today-label">Admissions Portal</span>
            <div className="top-avatar">AS</div>
          </div>
        </header>

        {notice && <div className="admin-notice" role="status">{notice}</div>}

        {activeNav === 'Reports' ? (
          <section className="content-section">
            <div className="section-heading">
              <div>
                <h2>Application Reports</h2>
                <p>Current summary based on demo applications.</p>
              </div>
            </div>
            <div className="stats-grid">
              {Object.entries(counts).map(([label, value]) => (
                <div className="stat-card" key={label}>
                  <span>{label} applications</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
          </section>
        ) : (
          <>
            <section className="stats-grid">
              {[
                { label: 'Total Applications', value: counts.Total, mark: '▤', tone: 'blue' },
                { label: 'Pending Review', value: counts.Pending, mark: '◷', tone: 'amber' },
                { label: 'Approved', value: counts.Approved, mark: '✓', tone: 'green' },
                { label: 'Rejected', value: counts.Rejected, mark: '×', tone: 'red' },
              ].map(stat => (
                <div className="stat-card" key={stat.label}>
                  <div className="stat-top">
                    <span>{stat.label}</span>
                    <span className={`stat-mark ${stat.tone}`}>{stat.mark}</span>
                  </div>
                  <strong>{stat.value}</strong>
                  <small>Demo data overview</small>
                </div>
              ))}
            </section>

            <section className="content-section">
              <div className="section-heading">
                <div>
                  <h2>Applications</h2>
                  <p>Review and manage submitted admission applications.</p>
                </div>
                <span className="record-count">{filtered.length} records</span>
              </div>

              <div className="table-toolbar">
                <input
                  className="search-input"
                  value={search}
                  onChange={event => setSearch(event.target.value)}
                  placeholder="Search name, ID or course..."
                  aria-label="Search applications"
                />
                <select
                  value={filter}
                  onChange={event => setFilter(event.target.value)}
                  aria-label="Filter application status"
                >
                  <option>All</option>
                  <option>Pending</option>
                  <option>Approved</option>
                  <option>Rejected</option>
                </select>
              </div>

              {activeNav === 'Applications' && (
                <p className="view-note">Applications view selected. Use search and status filters to find a record.</p>
              )}

              <div className="table-wrap">
                <table className="applications-table">
                  <thead>
                    <tr>
                      <th>Applicant</th>
                      <th>Course</th>
                      <th>Applied on</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map(app => (
                      <tr key={app.id}>
                        <td>
                          <div className="applicant-cell">
                            <div className="applicant-avatar">{app.name.split(' ').map(n => n[0]).join('')}</div>
                            <div>
                              <strong>{app.name}</strong>
                              <span>{app.id} · {app.email}</span>
                            </div>
                          </div>
                        </td>
                        <td>{app.course}</td>
                        <td>{app.date}</td>
                        <td><span className={`status-pill ${app.status.toLowerCase()}`}>{app.status}</span></td>
                        <td>
                          <button className="view-button" onClick={() => setSelected(app)}>Review</button>
                        </td>
                      </tr>
                    ))}
                    {filtered.length === 0 && (
                      <tr><td colSpan="5" className="empty-state">No applications match your search.</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}

        <footer className="admin-footer">
          College ERP · Admission Management <span>Frontend demo · Not connected to backend</span>
        </footer>
      </main>

      {selected && (
        <div className="modal-backdrop" onClick={() => setSelected(null)}>
          <section
            className="review-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="review-title"
            onClick={event => event.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelected(null)} aria-label="Close review">×</button>
            <span className="breadcrumb">APPLICATION REVIEW · {selected.id}</span>
            <h2 id="review-title">{selected.name}</h2>
            <p className="modal-email">{selected.email}</p>
            <div className="review-detail"><span>Course</span><strong>{selected.course}</strong></div>
            <div className="review-detail"><span>Application date</span><strong>{selected.date}</strong></div>
            <div className="review-detail"><span>Current status</span><strong>{selected.status}</strong></div>
            <p className="demo-warning">Demo only: changes stay in this page and are not saved to a server.</p>
            <div className="modal-actions">
              <button className="reject-action" onClick={() => updateStatus(selected.id, 'Rejected')}>Reject</button>
              <button className="approve-action" onClick={() => updateStatus(selected.id, 'Approved')}>Approve</button>
            </div>
          </section>
        </div>
      )}
    </div>
  )
}

export default AdmissionDashboard
