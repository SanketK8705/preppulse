import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_db, close_db
from app.routes import exams, subjects, chapters, quiz, analytics, seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    # Auto-seed if env var set and DB is empty
    if os.getenv("AUTO_SEED", "false").lower() == "true":
        from app.services.seed_service import seed_if_empty
        await seed_if_empty()
    yield
    await close_db()


app = FastAPI(
    title="SkillBytes API",
    description="WhatsApp-style quiz app backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exams.router, prefix="/api")
app.include_router(subjects.router, prefix="/api")
app.include_router(chapters.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(seed.router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "app": "SkillBytes"}


@app.get("/health")
async def health():
    return {"status": "healthy"}