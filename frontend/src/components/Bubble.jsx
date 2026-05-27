import './Bubble.css'

export default function Bubble({ children, side = 'left', delay = 0, className = '' }) {
  return (
    <div
      className={`bubble bubble--${side} ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      {side === 'left' && (
        <span className="bubble__avatar">🤖</span>
      )}
      <div className="bubble__body">
        {children}
      </div>
    </div>
  )
}