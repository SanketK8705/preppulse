from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


# ── Users ────────────────────────────────────────────────
class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    device_id: str
    nickname: str
    last_active: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# ── Exams ────────────────────────────────────────────────
class Exam(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    icon: str
    color: str
    description: str

    class Config:
        populate_by_name = True


# ── Subjects ─────────────────────────────────────────────
class Subject(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    exam_id: str
    name: str
    icon: str

    class Config:
        populate_by_name = True


# ── Chapters ─────────────────────────────────────────────
class Chapter(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    subject_id: str
    name: str
    question_count: int = 10

    class Config:
        populate_by_name = True


# ── Questions ────────────────────────────────────────────
class Question(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    chapter_id: str
    text: str
    options: List[str]          # exactly 4
    correct_index: int          # 0-3
    difficulty: str             # easy | medium | hard
    explanation: str

    class Config:
        populate_by_name = True


# ── Quiz Sessions ────────────────────────────────────────
class QuizSession(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    chapter_id: str
    question_ids: List[str]
    current_index: int = 0
    score: int = 0
    status: str = "active"      # active | completed | abandoned
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


# ── Quiz Responses ───────────────────────────────────────
class QuizResponse(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    session_id: str
    question_id: str
    selected_index: int
    is_correct: bool
    shown_at: datetime
    answered_at: datetime = Field(default_factory=datetime.utcnow)
    response_duration_ms: int

    class Config:
        populate_by_name = True


# ── API Request/Response schemas ─────────────────────────
class StartQuizRequest(BaseModel):
    device_id: str
    chapter_id: str
    nickname: Optional[str] = "Learner"

class AnswerRequest(BaseModel):
    session_id: str
    question_id: str
    selected_index: int
    shown_at: str               # ISO timestamp from frontend

class QuestionOut(BaseModel):
    id: str
    text: str
    options: List[str]
    difficulty: str
    question_number: int
    total_questions: int