from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database import Base, engine
from app.routers import analytics, exams, health, notifications, schedules, students, tasks


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Study Planner API",
    description="Distributed Student Planning System backend API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(students.router)
app.include_router(tasks.router)
app.include_router(exams.router)
app.include_router(schedules.router)
app.include_router(notifications.router)
app.include_router(analytics.router)


@app.get("/swagger", include_in_schema=False)
def swagger_alias() -> RedirectResponse:
    return RedirectResponse(url="/docs")
