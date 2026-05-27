import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { submitAnswer } from '../services/api.js'
import { useQuizStore } from '../store/quizStore.js'
import Bubble from '../components/Bubble.jsx'
import TypingIndicator from '../components/TypingIndicator.jsx'
import './Quiz.css'

const OPTION_LABELS = ['A', 'B', 'C', 'D']

export default function Quiz() {
  const navigate = useNavigate()
  const {
    sessionId, currentQuestion, currentIndex, totalQuestions,
    chapterName, answers, markShown, recordAnswer, finishQuiz, phase, reset
  } = useQuizStore()

  const [showOptions, setShowOptions]  = useState(false)
  const [selectedOpt, setSelectedOpt]  = useState(null)
  const [feedback, setFeedback]        = useState(null)
  const [typing, setTyping]            = useState(false)
  const [submitting, setSubmitting]    = useState(false)
  const [questionVisible, setQVisible] = useState(false)
  const bottomRef = useRef(null)

  const question = currentQuestion
  const progress = totalQuestions ? (currentIndex / totalQuestions) * 100 : 0

  // redirect if no session
  useEffect(() => {
    if (!sessionId) navigate('/', { replace: true })
  }, [sessionId])

  // redirect when phase becomes result
  useEffect(() => {
    if (phase === 'result') navigate('/result', { replace: true })
  }, [phase])

  // show question with typing delay
  useEffect(() => {
    if (!question) return
    setShowOptions(false)
    setSelectedOpt(null)
    setFeedback(null)
    setQVisible(false)

    setTyping(true)
    const t1 = setTimeout(() => {
      setTyping(false)
      setQVisible(true)
      markShown()
      const t2 = setTimeout(() => setShowOptions(true), 300)
      return () => clearTimeout(t2)
    }, 700)
    return () => clearTimeout(t1)
  }, [currentIndex, question?.id])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [showOptions, feedback, typing, questionVisible])

  const handleSelect = async (optIndex) => {
    if (selectedOpt !== null || submitting) return
    setSelectedOpt(optIndex)
    setSubmitting(true)

    try {
      const res = await submitAnswer(
        sessionId,
        question.id,
        optIndex,
        useQuizStore.getState().questionShownAt
      )
      recordAnswer(question.id, optIndex, res.is_correct, res.next_question)
      setFeedback({ correct: res.is_correct, explanation: res.explanation, correctIndex: res.correct_index })
      if (res.is_last) finishQuiz()
    } catch {
      setFeedback({ correct: false, explanation: null, correctIndex: 0 })
    } finally {
      setSubmitting(false)
    }
  }

  const handleNext = () => {
    // question already advanced in store via recordAnswer
    // just reset local UI state
    setSelectedOpt(null)
    setFeedback(null)
    setQVisible(false)
    setShowOptions(false)
  }

  if (!question) return null

  const answered = selectedOpt !== null

  return (
    <div className="quiz">
      {/* progress bar */}
      <div className="quiz__progress">
        <div className="quiz__progress-bar" style={{ width: `${progress}%` }} />
      </div>
      <div className="quiz__counter">
        <span>{currentIndex + 1} / {totalQuestions}</span>
        <span className="quiz__chapter-label">{chapterName || ''}</span>
      </div>

      {/* chat area */}
      <div className="quiz__chat">

        {questionVisible && (
          <Bubble side="left" delay={0}>
            <p className="quiz__q-num">Q{currentIndex + 1}</p>
            <p className="quiz__q-text">{question.text}</p>
          </Bubble>
        )}

        {typing && <TypingIndicator />}

        {showOptions && !answered && (
          <div className="quiz__options animate-slide-up">
            {question.options.map((opt, i) => (
              <button
                key={i}
                className="quiz__option"
                style={{ animationDelay: `${i * 50}ms` }}
                onClick={() => handleSelect(i)}
                disabled={submitting}
              >
                <span className="quiz__option-label">{OPTION_LABELS[i]}</span>
                <span className="quiz__option-text">{opt}</span>
              </button>
            ))}
          </div>
        )}

        {answered && (
          <Bubble side="right" delay={0}>
            <span className="quiz__chosen-label">{OPTION_LABELS[selectedOpt]}</span>
            {' '}{question.options[selectedOpt]}
          </Bubble>
        )}

        {feedback && (
          <Bubble side="left" delay={0}>
            <div className={`quiz__feedback quiz__feedback--${feedback.correct ? 'correct' : 'wrong'}`}>
              <span className="quiz__feedback-icon">{feedback.correct ? '✅' : '❌'}</span>
              <span>{feedback.correct ? 'Correct!' : `Wrong! Correct: ${OPTION_LABELS[feedback.correctIndex]}`}</span>
            </div>
            {feedback.explanation && (
              <p className="quiz__explanation">{feedback.explanation}</p>
            )}
          </Bubble>
        )}

        {feedback && (
          <div className="quiz__next-wrap animate-fade-in">
            <button className="quiz__next-btn" onClick={handleNext}>
              {currentIndex + 1 === totalQuestions ? 'See Results 🏆' : 'Next →'}
            </button>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <button className="quiz__quit" onClick={() => { reset(); navigate('/') }}>
        ✕ Quit
      </button>
    </div>
  )
}