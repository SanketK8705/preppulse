# PrepPulse 

A WhatsApp-style quiz application built with React, FastAPI, and MongoDB.

---

## Tech Stack

| Layer    | Tech                          |
|----------|-------------------------------|
| Frontend | React 18 + Vite, Recharts     |
| Backend  | FastAPI + Motor (async)       |
| Database | MongoDB                       |
| Deploy   | Docker Compose                |

---

## Flow

```
Exam → Subject → Chapter → Quiz → Result
```

- No login — device fingerprint via localStorage UUID
- MCQ only, single correct answer, no negative marking
- One question at a time with Next button
- WhatsApp-style chat bubble UI, mobile-first

---

## Quick Start (Docker)

```bash
git clone https://github.com/YOUR_USERNAME/skillbytes.git
cd skillbytes
docker-compose up --build
```

Then open: http://localhost:3000

Seed the database (first time):
```bash
curl -X POST http://localhost:8000/api/seed/seed
```

This inserts:
- 3 exams (UPSC, JEE, NEET)
- 9 subjects, 27 chapters, 270 questions
- 50 simulated users
- ~1,500 quiz sessions with realistic timestamps
- ~10,000 quiz responses with `response_duration_ms` populated

---

## Local Dev (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Make sure MongoDB is running locally on port 27017.

---

## API Endpoints

### Quiz Flow
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exams/` | List all exams |
| GET | `/api/subjects/?exam_id=` | List subjects for exam |
| GET | `/api/chapters/?subject_id=` | List chapters for subject |
| POST | `/api/quiz/start` | Start quiz session |
| POST | `/api/quiz/answer` | Submit answer, get next question |
| GET | `/api/quiz/{id}/result` | Get final result |
| POST | `/api/quiz/{id}/abandon` | Abandon session |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/summary` | DAU, WAU, MAU, completion rate, avg response time |
| GET | `/api/analytics/peak-hours` | Sessions per hour (0–23) |
| GET | `/api/analytics/drop-off` | Drop-off by question number |
| GET | `/api/analytics/daily-sessions` | Sessions per day (last 14 days) |
| GET | `/api/analytics/top-chapters` | Most played chapters |
| GET | `/api/analytics/accuracy` | Correct vs incorrect counts |

Interactive docs: http://localhost:8000/docs

---

## Analytics Implemented

| Metric | How |
|--------|-----|
| Daily Active Users | Users with `last_active` within 24h |
| Weekly Active Users | Users with `last_active` within 7 days |
| Monthly Active Users | Users with `last_active` within 30 days |
| Questions Served | Sum of `total_questions` across all sessions |
| Questions Answered | Total quiz_responses documents |
| Avg Response Time | Mean of `response_duration_ms` across all responses |
| Quiz Completion Rate | `completed` sessions / total sessions × 100 |
| Drop-off Analysis | Abandoned sessions grouped by `current_index` |
| Peak Activity Hours | Sessions grouped by hour of `started_at` |
| Avg Questions per Session | Total responses / total sessions |
| Top Chapters | Sessions grouped by `chapter_id` |

---

## Data Model

```
users           device_id, nickname, last_active
exams           name, icon, color, description
subjects        exam_id, name, icon
chapters        subject_id, name, question_count
questions       chapter_id, text, options[], correct_index, difficulty, explanation
quiz_sessions   user_id, chapter_id, question_ids[], score, status, started_at, completed_at
quiz_responses  session_id, question_id, selected_index, is_correct,
                shown_at, answered_at, response_duration_ms
```

---

## Project Structure

```
skillbytes/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/routes/
│   │   │   ├── exams.py
│   │   │   ├── subjects.py
│   │   │   ├── chapters.py
│   │   │   ├── quiz.py
│   │   │   ├── analytics.py
│   │   │   └── seed.py
│   │   ├── db/database.py
│   │   ├── services/seed_service.py
│   │   └── core/config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── utils/api.js
│   │   └── styles/global.css
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## Evaluation Checklist

-  Backend architecture — FastAPI with async Motor, indexed collections
-  Database design — 7 collections, proper foreign key references, indexed queries
-  API quality — RESTful, typed, error handling, interactive docs at `/docs`
-  Analytics thinking — 11 metrics, aggregation pipelines, time-series data
-  Frontend implementation — WhatsApp UI, chat bubbles, recharts dashboard
-  Code structure — separated routes, services, utils, single responsibility
