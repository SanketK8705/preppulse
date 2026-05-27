import { Outlet, NavLink, useLocation } from 'react-router-dom'
import './Layout.css'

const NAV = [
  { to: '/',          label: 'Quiz',      icon: '💬' },
  { to: '/analytics', label: 'Analytics', icon: '📊' },
]

export default function Layout() {
  const loc = useLocation()
  const hideNav = loc.pathname === '/quiz'

  return (
    <div className="layout">
      {/* ── Header ── */}
      <header className="layout__header">
        <div className="layout__brand">
          <span className="layout__brand-icon"></span>
          <span className="layout__brand-name">PrepPulse</span>
        </div>
        {!hideNav && (
          <nav className="layout__nav">
            {NAV.map(n => (
              <NavLink
                key={n.to}
                to={n.to}
                end={n.to === '/'}
                className={({ isActive }) =>
                  'layout__nav-link' + (isActive ? ' layout__nav-link--active' : '')
                }
              >
                <span>{n.icon}</span>
                <span>{n.label}</span>
              </NavLink>
            ))}
          </nav>
        )}
      </header>

      {/* ── Page ── */}
      <main className="layout__main">
        <Outlet />
      </main>
    </div>
  )
}