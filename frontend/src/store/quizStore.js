import { create } from 'zustand'

export const useQuizStore = create((set, get) => ({
  sessionId: null,
  currentQuestion: null,
  currentIndex: 0,
  totalQuestions: 0,
  chapterName: '',
  answers: [],
  questionShownAt: null,
  phase: 'home',

  selectedExam: null,
  selectedSubject: null,
  selectedChapter: null,

  setExam:    (exam) => set({ selectedExam: exam }),
  setSubject: (sub)  => set({ selectedSubject: sub }),
  setChapter: (ch)   => set({ selectedChapter: ch }),

  startSession: (sessionId, question, chapterName, total) => set({
    sessionId,
    currentQuestion: question,
    chapterName,
    totalQuestions: total || 10,
    currentIndex: 0,
    answers: [],
    questionShownAt: Date.now(),
    phase: 'quiz',
  }),

  markShown: () => set({ questionShownAt: Date.now() }),

  recordAnswer: (questionId, selectedOption, correct, nextQuestion) => {
    const elapsed = Date.now() - (get().questionShownAt || Date.now())
    set(s => ({
      answers: [...s.answers, { questionId, selectedOption, correct, responseTimeMs: elapsed }],
      currentQuestion: nextQuestion || null,
      currentIndex: s.currentIndex + 1,
      questionShownAt: Date.now(),
    }))
  },

  finishQuiz: () => set({ phase: 'result' }),

  reset: () => set({
    sessionId: null, currentQuestion: null, currentIndex: 0,
    totalQuestions: 0, chapterName: '', answers: [],
    questionShownAt: null, phase: 'home',
    selectedExam: null, selectedSubject: null, selectedChapter: null,
  }),
}))