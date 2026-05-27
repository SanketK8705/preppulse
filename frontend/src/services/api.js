import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// ── Device fingerprint ──
export function getDeviceId() {
  let id = localStorage.getItem('sb_device_id')
  if (!id) {
    id = 'dev_' + Math.random().toString(36).slice(2) + Date.now().toString(36)
    localStorage.setItem('sb_device_id', id)
  }
  return id
}

// ── Exams / Subjects / Chapters ──
export const fetchExams = () => api.get('/exams').then(r => r.data)
export const fetchSubjects = (examId) => api.get(`/subjects?exam_id=${examId}`).then(r => r.data)
export const fetchChapters = (subjectId) => api.get(`/chapters?subject_id=${subjectId}`).then(r => r.data)

// ── Quiz ──
export const startQuiz = (chapterId) =>
  api.post('/quiz/start', { chapter_id: chapterId, device_id: getDeviceId(), nickname: 'Player' }).then(r => r.data)

export const submitAnswer = (sessionId, questionId, optionIndex, shownAt) =>
  api.post('/quiz/answer', {
    session_id: sessionId,
    question_id: questionId,
    selected_index: optionIndex,
    shown_at: new Date(shownAt).toISOString(),
    device_id: getDeviceId(),
  }).then(r => r.data)
  
export const fetchResult = (sessionId) =>
  api.get(`/quiz/${sessionId}/result`).then(r => r.data)

// ── Analytics ──
export const fetchAnalyticsSummary = () => api.get('/analytics/summary').then(r => r.data)
export const fetchPeakHours = () => api.get('/analytics/peak-hours').then(r => r.data)
export const fetchDropOff = () => api.get('/analytics/drop-off').then(r => r.data)
export const fetchDailySessions = () => api.get('/analytics/daily-sessions').then(r => r.data)

// ── Seed ──
export const seedDatabase = () => api.post('/seed').then(r => r.data)