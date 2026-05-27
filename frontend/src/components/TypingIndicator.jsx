import './TypingIndicator.css'

export default function TypingIndicator() {
  return (
    <div className="typing">
      <span className="typing__avatar">🤖</span>
      <div className="typing__dots">
        <span /><span /><span />
      </div>
    </div>
  )
}