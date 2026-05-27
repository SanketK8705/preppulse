import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchExams, fetchSubjects, fetchChapters, startQuiz, seedDatabase } from '../services/api.js'
import { useQuizStore } from '../store/quizStore.js'
import Bubble from '../components/Bubble.jsx'
import TypingIndicator from '../components/TypingIndicator.jsx'
import './Home.css'

const STEP = { EXAM: 'exam', SUBJECT: 'subject', CHAPTER: 'chapter', STARTING: 'starting' }

export default function Home() {
  const navigate = useNavigate()
  const { setExam, setSubject, setChapter, startSession } = useQuizStore()

  const [step, setStep]         = useState(STEP.EXAM)
  const [typing, setTyping]     = useState(false)
  const [messages, setMessages] = useState([])
  const [exams, setExams]       = useState([])
  const [subjects, setSubjects] = useState([])
  const [chapters, setChapters] = useState([])
  const [selected, setSelected] = useState({ exam: null, subject: null, chapter: null })
  const [seeding, setSeeding]   = useState(false)
  const [seedDone, setSeedDone] = useState(false)
  const bottomRef = useRef(null)

  // push a bot message with typing delay
  const botSay = (content, delay = 600) => {
    setTyping(true)
    setTimeout(() => {
      setTyping(false)
      setMessages(m => [...m, { side: 'left', content }])
    }, delay)
  }

  // scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typing])

  // init: load exams
  useEffect(() => {
    botSay('Hey! Welcome to **PrepPulse**. What would you like to be tested on today?', 400)
    fetchExams()
      .then(data => {
        setExams(data)
        setTimeout(() => setStep(STEP.EXAM), 800)
      })
      .catch(() => {
        botSay("Hmm, couldn't load exams. Try seeding the database first ", 800)
      })
  }, [])

  const handleSeed = async () => {
    setSeeding(true)
    try {
      await seedDatabase()
      setSeedDone(true)
      const data = await fetchExams()
      setExams(data)
      botSay('Database seeded! Now pick an exam to get started.')
      setStep(STEP.EXAM)
    } catch {
      botSay('Seed failed. Is the backend running?')
    } finally {
      setSeeding(false)
    }
  }

  const selectExam = async (exam) => {
    setSelected(s => ({ ...s, exam }))
    setExam(exam)
    setMessages(m => [...m, { side: 'right', content: exam.name }])
    setStep(null)

    botSay(`Great choice! Which subject in **${exam.name}**?`, 700)
    const subs = await fetchSubjects(exam._id)
    setSubjects(subs)
    setTimeout(() => setStep(STEP.SUBJECT), 1000)
  }

  const selectSubject = async (subject) => {
    setSelected(s => ({ ...s, subject }))
    setSubject(subject)
    setMessages(m => [...m, { side: 'right', content: subject.name }])
    setStep(null)

    botSay(`Nice! Pick a chapter from **${subject.name}**.`, 700)
    const chs = await fetchChapters(subject._id)
    setChapters(chs)
    setTimeout(() => setStep(STEP.CHAPTER), 1000)
  }

  const selectChapter = async (chapter) => {
    setSelected(s => ({ ...s, chapter }))
    setChapter(chapter)
    setMessages(m => [...m, { side: 'right', content: chapter.name }])
    setStep(STEP.STARTING)

    botSay(`Alright! Starting quiz for **${chapter.name}**... Get ready!`, 600)

    try {
      const { session_id, question, chapter_name } = await startQuiz(chapter._id)
      startSession(session_id, question, chapter_name, question.total_questions)
      setTimeout(() => navigate('/quiz'), 1200)
    } catch {
      botSay("Couldn't start quiz. Please try again.")
      setStep(STEP.CHAPTER)
    }
  }

  return (
    <div className="home">
      <div className="home__chat">

        {/* dynamic messages */}
        {messages.map((msg, i) => (
          <Bubble key={i} side={msg.side} delay={0}>
            <span dangerouslySetInnerHTML={{ __html: msg.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
          </Bubble>
        ))}

        {typing && <TypingIndicator />}

        {/* ── Choices ── */}
        {step === STEP.EXAM && exams.length > 0 && (
          <div className="home__choices animate-slide-up">
            {exams.map((e, i) => (
              <button
                key={e._id}
                className="choice-btn"
                style={{ animationDelay: `${i * 60}ms` }}
                onClick={() => selectExam(e)}
              >
                <span className="choice-btn__icon">📚</span>
                <span>{e.name}</span>
              </button>
            ))}
          </div>
        )}

        {step === STEP.SUBJECT && subjects.length > 0 && (
          <div className="home__choices animate-slide-up">
            {subjects.map((s, i) => (
              <button
                key={s._id}
                className="choice-btn"
                style={{ animationDelay: `${i * 60}ms` }}
                onClick={() => selectSubject(s)}
              >
                <span className="choice-btn__icon">🔬</span>
                <span>{s.name}</span>
              </button>
            ))}
          </div>
        )}

        {step === STEP.CHAPTER && chapters.length > 0 && (
          <div className="home__choices animate-slide-up">
            {chapters.map((c, i) => (
              <button
                key={c._id}
                className="choice-btn"
                style={{ animationDelay: `${i * 60}ms` }}
                onClick={() => selectChapter(c)}
              >
                <span className="choice-btn__icon">📄</span>
                <span>{c.name}</span>
              </button>
            ))}
          </div>
        )}

        {step === STEP.STARTING && (
          <div className="home__loading animate-fade-in">
            <div className="home__spinner" />
            <span>Loading quiz…</span>
          </div>
        )}

        {/* seed helper */}
        {exams.length === 0 && !seeding && !seedDone && step === STEP.EXAM && (
          <div className="home__seed animate-slide-up">
            <p>No data yet. Seed the database to get started.</p>
            <button className="seed-btn" onClick={handleSeed}>
              🌱 Seed Database
            </button>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  )
}