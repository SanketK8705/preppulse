import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchResult } from '../services/api.js'
import { useQuizStore } from '../store/quizStore.js'
import './Result.css'

function ScoreRing({ score, total }) {
  const pct   = total ? Math.round((score / total) * 100) : 0
  const r     = 52
  const circ  = 2 * Math.PI * r
  const dash  = circ - (pct / 100) * circ

  const grade =
    pct >= 90 ? { label: 'Excellent!',  color: '#3ecf8e', emoji: '🏆' } :
    pct >= 70 ? { label: 'Good job!',   color: '#25d366', emoji: '🎉' } :
    pct >= 50 ? { label: 'Not bad.',    color: '#f5a623', emoji: '📚' } :
                { label: 'Keep going!', color: '#e05c5c', emoji: '💪' }

  return (
    <div className="result__ring-wrap">
      <svg className="result__ring" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={r} fill="none" stroke="var(--bg-card)" strokeWidth="10" />
        <circle
          cx="60" cy="60" r={r}
          fill="none"
          stroke={grade.color}
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={dash}
          transform="rotate(-90 60 60)"
          style={{ transition: 'stroke-dashoffset 1s cubic-bezier(0.4,0,0.2,1)' }}
        />
      </svg>
      <div className="result__ring-center">
        <span className="result__ring-pct">{pct}%</span>
        <span className="result__ring-frac">{score}/{total}</span>
      </div>
      <div className="result__grade" style={{ color: grade.color }}>
        {grade.emoji} {grade.label}
      </div>
    </div>
  )
}

export default function Result() {
  const navigate = useNavigate()
  const { sessionId, answers, reset, selectedChapter, totalQuestions } = useQuizStore()

  const [detail, setDetail]   = useState(null)
  const [loading, setLoading] = useState(true)

  const correct = answers.filter(a => a.correct).length
  const total = totalQuestions || answers.length

  useEffect(() => {
    if (!sessionId) { navigate('/'); return }
    fetchResult(sessionId)
      .then(d => setDetail(d))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [sessionId])

  const avgTime = answers.length
    ? Math.round(answers.reduce((s, a) => s + (a.responseTimeMs || 0), 0) / answers.length / 1000)
    : 0

  return (
    <div className="result animate-fade-in">
      <div className="result__header">
        <h1 className="result__title">Quiz Complete</h1>
        {selectedChapter && (
          <p className="result__subtitle">{selectedChapter.name}</p>
        )}
      </div>

      <ScoreRing score={detail?.score ?? correct} total={detail?.total ?? total} />

      {/* stats row */}
      <div className="result__stats">
        {[
          { label: 'Correct',     value: detail?.score ?? correct, icon: '✅' },
          { label: 'Wrong',       value: (detail?.total ?? total) - (detail?.score ?? correct), icon: '❌' },
          { label: 'Avg time',    value: `${avgTime}s`, icon: '⏱' },
        ].map(s => (
          <div key={s.label} className="result__stat">
            <span className="result__stat-icon">{s.icon}</span>
            <span className="result__stat-val">{s.value}</span>
            <span className="result__stat-label">{s.label}</span>
          </div>
        ))}
      </div>

      {/* per-question breakdown */}
      {answers.length > 0 && (
        <div className="result__breakdown">
          <h3 className="result__section-title">Question Breakdown</h3>
          <div className="result__qs">
            {answers.map((a, i) => (
              <div key={i} className={`result__q result__q--${a.correct ? 'correct' : 'wrong'}`}>
                <span className="result__q-num">Q{i + 1}</span>
                <span className="result__q-icon">{a.correct ? '✅' : '❌'}</span>
                <span className="result__q-time">{Math.round((a.responseTimeMs || 0) / 1000)}s</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* actions */}
      <div className="result__actions">
        <button className="result__btn result__btn--primary" onClick={() => { reset(); navigate('/') }}>
          🔄 Try Another
        </button>
        <button className="result__btn result__btn--secondary" onClick={() => navigate('/analytics')}>
          📊 Analytics
        </button>
      </div>
    </div>
  )
}