import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home.jsx'
import Quiz from './pages/Quiz.jsx'
import Result from './pages/Result.jsx'
import Analytics from './pages/Analytics.jsx'
import Layout from './components/Layout.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/"          element={<Home />} />
          <Route path="/quiz"      element={<Quiz />} />
          <Route path="/result"    element={<Result />} />
          <Route path="/analytics" element={<Analytics />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}