import { useEffect, useState } from 'react'
import {
  AreaChart, Area, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'
import {
  fetchAnalyticsSummary, fetchPeakHours,
  fetchDropOff, fetchDailySessions
} from '../services/api.js'
import './Analytics.css'

const TOOLTIP_STYLE = {
  backgroundColor: 'var(--bg-card)',
  border: '1px solid var(--border)',
  borderRadius: 10,
  color: 'var(--text-primary)',
  fontSize: 12,
  fontFamily: 'DM Sans, sans-serif',
}

function StatCard({ icon, label, value, sub, color = 'var(--accent-green)' }) {
  return (
    <div className="analytics__stat animate-slide-up">
      <div className="analytics__stat-icon" style={{ color }}>{icon}</div>
      <div className="analytics__stat-val" style={{ color }}>{value ?? '–'}</div>
      <div className="analytics__stat-label">{label}</div>
      {sub && <div className="analytics__stat-sub">{sub}</div>}
    </div>
  )
}

export default function Analytics() {
  const [summary, setSummary]   = useState(null)
  const [peak, setPeak]         = useState([])
  const [dropoff, setDropoff]   = useState([])
  const [daily, setDaily]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)

  useEffect(() => {
    Promise.all([
      fetchAnalyticsSummary(),
      fetchPeakHours(),
      fetchDropOff(),
      fetchDailySessions(),
    ])
      .then(([s, p, d, ds]) => {
        setSummary(s)
        setPeak(p.map(h => ({ hour: `${h.hour}:00`, sessions: h.count })))
        setDropoff(d.map(q => ({ question: `Q${q.question_number}`, remaining: q.remaining_pct ?? q.count })))
        setDaily(ds.map(d => ({ date: d.date?.slice(5) ?? d.date, sessions: d.sessions ?? d.count })))
      })
      .catch(() => setError('Could not load analytics. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="analytics__loading">
      <div className="analytics__spinner" />
      <span>Loading analytics…</span>
    </div>
  )

  if (error) return (
    <div className="analytics__error">
      <span>⚠️ {error}</span>
    </div>
  )

  return (
    <div className="analytics">
      <div className="analytics__hero">
        <h1 className="analytics__title">Analytics</h1>
        <p className="analytics__desc">Platform usage at a glance</p>
      </div>

      {/* ── Summary stats ── */}
      <div className="analytics__stats-grid">
        <StatCard icon="👥" label="DAU"              value={summary?.dau}             color="var(--accent-green)" />
        <StatCard icon="📅" label="WAU"              value={summary?.wau}             color="var(--accent-teal)" />
        <StatCard icon="🌍" label="MAU"              value={summary?.mau}             color="var(--accent-lime)" />
        <StatCard icon="❓" label="Qs Served"        value={summary?.questions_served} color="var(--accent-green)" />
        <StatCard icon="✍️" label="Qs Answered"      value={summary?.questions_answered} color="var(--accent-teal)" />
        <StatCard icon="⏱" label="Avg Response"     value={summary?.avg_response_ms ? `${Math.round(summary.avg_response_ms / 1000)}s` : '–'} color="var(--accent-lime)" />
        <StatCard icon="🏁" label="Completion Rate"  value={summary?.completion_rate ? `${summary.completion_rate}%` : '–'} color="var(--accent-green)" />
        <StatCard icon="📈" label="Avg Qs/Session"   value={summary?.avg_questions_per_session} color="var(--accent-teal)" />
      </div>

      {/* ── Daily sessions ── */}
      {daily.length > 0 && (
        <div className="analytics__chart-card animate-slide-up">
          <h3 className="analytics__chart-title">Daily Sessions (last 30d)</h3>
          <ResponsiveContainer width="100%" height={160}>
            <AreaChart data={daily} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
              <defs>
                <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#25d366" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#25d366" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--border-subtle)" vertical={false} />
              <XAxis dataKey="date" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} interval={4} />
              <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={TOOLTIP_STYLE} cursor={{ stroke: 'var(--accent-green)', strokeWidth: 1, strokeDasharray: '4 4' }} />
              <Area type="monotone" dataKey="sessions" stroke="#25d366" strokeWidth={2} fill="url(#grad1)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ── Peak hours ── */}
      {peak.length > 0 && (
        <div className="analytics__chart-card animate-slide-up">
          <h3 className="analytics__chart-title">Peak Activity Hours</h3>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={peak} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
              <CartesianGrid stroke="var(--border-subtle)" vertical={false} />
              <XAxis dataKey="hour" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={TOOLTIP_STYLE} cursor={{ fill: 'rgba(37,211,102,0.05)' }} />
              <Bar dataKey="sessions" fill="#3ecf8e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ── Drop-off ── */}
      {dropoff.length > 0 && (
        <div className="analytics__chart-card animate-slide-up">
          <h3 className="analytics__chart-title">Drop-off by Question</h3>
          <p className="analytics__chart-sub">% of users still in quiz at each question</p>
          <ResponsiveContainer width="100%" height={160}>
            <LineChart data={dropoff} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
              <CartesianGrid stroke="var(--border-subtle)" vertical={false} />
              <XAxis dataKey="question" tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} />
              <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 10 }} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={TOOLTIP_STYLE} cursor={{ stroke: 'var(--accent-warn)', strokeWidth: 1, strokeDasharray: '4 4' }} />
              <Line type="monotone" dataKey="remaining" stroke="#f5a623" strokeWidth={2} dot={{ fill: '#f5a623', r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* top chapters */}
      {summary?.top_chapters?.length > 0 && (
        <div className="analytics__chart-card animate-slide-up">
          <h3 className="analytics__chart-title">Top Chapters</h3>
          <div className="analytics__chapters">
            {summary.top_chapters.map((c, i) => (
              <div key={i} className="analytics__chapter-row">
                <span className="analytics__chapter-rank">#{i + 1}</span>
                <span className="analytics__chapter-name">{c.chapter}</span>
                <span className="analytics__chapter-count">{c.sessions} sessions</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}