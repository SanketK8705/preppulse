from fastapi import APIRouter
from datetime import datetime, timedelta
from app.database import get_db

router = APIRouter()


@router.get("/analytics/summary")
async def get_summary():
    db = get_db()
    now = datetime.utcnow()

    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # DAU - unique users with sessions in last 24h
    dau_pipeline = [
        {"$match": {"started_at": {"$gte": day_ago}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    dau_res = await db.quiz_sessions.aggregate(dau_pipeline).to_list(1)
    dau = dau_res[0]["count"] if dau_res else 0

    # WAU
    wau_pipeline = [
        {"$match": {"started_at": {"$gte": week_ago}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    wau_res = await db.quiz_sessions.aggregate(wau_pipeline).to_list(1)
    wau = wau_res[0]["count"] if wau_res else 0

    # MAU
    mau_pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "count"}
    ]
    mau_res = await db.quiz_sessions.aggregate(mau_pipeline).to_list(1)
    mau = mau_res[0]["count"] if mau_res else 0

    # Total sessions (last 30d)
    total_sessions = await db.quiz_sessions.count_documents(
        {"started_at": {"$gte": month_ago}}
    )

    # Questions served (last 30d)
    qs_pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$project": {"count": {"$size": "$question_ids"}}},
        {"$group": {"_id": None, "total": {"$sum": "$count"}}}
    ]
    qs_res = await db.quiz_sessions.aggregate(qs_pipeline).to_list(1)
    questions_served = qs_res[0]["total"] if qs_res else 0

    # Questions answered (last 30d)
    qa_pipeline = [
        {"$match": {"answered_at": {"$gte": month_ago}}},
        {"$count": "count"}
    ]
    qa_res = await db.quiz_responses.aggregate(qa_pipeline).to_list(1)
    questions_answered = qa_res[0]["count"] if qa_res else 0

    # Avg response time (ms)
    art_pipeline = [
        {"$match": {"answered_at": {"$gte": month_ago}}},
        {"$group": {"_id": None, "avg_ms": {"$avg": "$response_duration_ms"}}}
    ]
    art_res = await db.quiz_responses.aggregate(art_pipeline).to_list(1)
    avg_response_ms = round(art_res[0]["avg_ms"]) if art_res else 0

    # Completion rate
    completed = await db.quiz_sessions.count_documents(
        {"started_at": {"$gte": month_ago}, "status": "completed"}
    )
    completion_rate = round((completed / total_sessions * 100), 1) if total_sessions else 0

    # Avg questions per session
    avg_q_per_session = round(questions_answered / total_sessions, 1) if total_sessions else 0

    # Top chapters by sessions
    top_chapters_pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$group": {"_id": "$chapter_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_chapters_raw = await db.quiz_sessions.aggregate(top_chapters_pipeline).to_list(5)

    top_chapters = []
    for tc in top_chapters_raw:
        from bson import ObjectId
        if ObjectId.is_valid(tc["_id"]):
            chap = await db.chapters.find_one({"_id": ObjectId(tc["_id"])})
            top_chapters.append({
                "chapter": chap["name"] if chap else tc["_id"],
                "sessions": tc["count"]
            })

    return {
        "dau": dau,
        "wau": wau,
        "mau": mau,
        "total_sessions": total_sessions,
        "questions_served": questions_served,
        "questions_answered": questions_answered,
        "avg_response_ms": avg_response_ms,
        "completion_rate": completion_rate,
        "avg_questions_per_session": avg_q_per_session,
        "completed_sessions": completed,
        "top_chapters": top_chapters,
    }


@router.get("/analytics/peak-hours")
async def get_peak_hours():
    db = get_db()
    month_ago = datetime.utcnow() - timedelta(days=30)

    pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$project": {"hour": {"$hour": "$started_at"}}},
        {"$group": {"_id": "$hour", "sessions": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    results = await db.quiz_sessions.aggregate(pipeline).to_list(24)

    # Fill all 24 hours
    hour_map = {r["_id"]: r["sessions"] for r in results}
    return [
        {"hour": h, "sessions": hour_map.get(h, 0), "label": f"{h:02d}:00"}
        for h in range(24)
    ]


@router.get("/analytics/drop-off")
async def get_drop_off():
    db = get_db()
    month_ago = datetime.utcnow() - timedelta(days=30)

    # For each question position (1-10), count how many sessions reached it
    pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$project": {
            "question_ids": 1,
            "current_index": 1,
            "status": 1,
            "total": {"$size": "$question_ids"}
        }},
    ]
    sessions = await db.quiz_sessions.aggregate(pipeline).to_list(10000)

    max_q = 10
    reached = [0] * max_q
    for s in sessions:
        answered = s["current_index"]
        for i in range(min(answered, max_q)):
            reached[i] += 1

    total_started = len(sessions)
    return [
        {
            "question_number": i + 1,
            "users_reached": reached[i],
            "drop_off_pct": round((1 - reached[i] / total_started) * 100, 1) if total_started else 0
        }
        for i in range(max_q)
    ]


@router.get("/analytics/daily-sessions")
async def get_daily_sessions():
    db = get_db()
    month_ago = datetime.utcnow() - timedelta(days=30)

    pipeline = [
        {"$match": {"started_at": {"$gte": month_ago}}},
        {"$project": {
            "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$started_at"}},
            "status": 1,
        }},
        {"$group": {
            "_id": "$date",
            "total": {"$sum": 1},
            "completed": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}}
        }},
        {"$sort": {"_id": 1}}
    ]
    results = await db.quiz_sessions.aggregate(pipeline).to_list(31)

    return [
        {"date": r["_id"], "sessions": r["total"], "completed": r["completed"]}
        for r in results
    ]