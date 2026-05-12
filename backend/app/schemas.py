from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


TaskStatus = Literal["pending", "in_progress", "completed", "cancelled"]
SessionType = Literal["task", "exam_revision", "general"]
NotificationSeverity = Literal["high", "medium", "low"]
NotificationType = Literal[
    "task_deadline",
    "exam_reminder",
    "high_priority_task",
    "overdue_task",
    "schedule_warning",
    "study_session_today",
]


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    study_hours_per_day: float = Field(default=4.0, ge=1, le=12)
    preferred_start_time: str = Field(default="09:00", pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    preferred_end_time: str = Field(default="18:00", pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    study_hours_per_day: float | None = Field(default=None, ge=1, le=12)
    preferred_start_time: str | None = Field(default=None, pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    preferred_end_time: str | None = Field(default=None, pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    student_id: int
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    course_name: str | None = Field(default=None, max_length=120)
    deadline: date
    difficulty: int = Field(ge=1, le=5)
    estimated_hours: float = Field(gt=0)
    is_exam_related: bool = False
    status: TaskStatus = "pending"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    course_name: str | None = Field(default=None, max_length=120)
    deadline: date | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    estimated_hours: float | None = Field(default=None, gt=0)
    is_exam_related: bool | None = None
    status: TaskStatus | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(TaskBase):
    id: int
    priority_score: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExamBase(BaseModel):
    student_id: int
    subject: str = Field(min_length=1, max_length=200)
    course_name: str | None = Field(default=None, max_length=120)
    exam_date: date
    importance: int = Field(ge=1, le=5)
    estimated_revision_hours: float = Field(default=4.0, gt=0)


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    subject: str | None = Field(default=None, min_length=1, max_length=200)
    course_name: str | None = Field(default=None, max_length=120)
    exam_date: date | None = None
    importance: int | None = Field(default=None, ge=1, le=5)
    estimated_revision_hours: float | None = Field(default=None, gt=0)


class ExamResponse(ExamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudySessionBase(BaseModel):
    student_id: int
    task_id: int | None = None
    session_date: date
    title: str = Field(min_length=1, max_length=250)
    duration_hours: float = Field(gt=0)
    priority_score: float = 0.0
    session_type: SessionType = "task"
    completed: bool = False


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionUpdate(BaseModel):
    session_date: date | None = None
    title: str | None = Field(default=None, min_length=1, max_length=250)
    duration_hours: float | None = Field(default=None, gt=0)
    priority_score: float | None = None
    session_type: SessionType | None = None
    completed: bool | None = None


class StudySessionResponse(StudySessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduleGenerateResponse(BaseModel):
    student_id: int
    total_sessions: int
    total_hours: float
    warnings: list[str]
    sessions: list[StudySessionResponse]


class NotificationResponse(BaseModel):
    type: NotificationType
    message: str
    severity: NotificationSeverity
    related_id: int | None = None


class DashboardStatsResponse(BaseModel):
    student_id: int
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    high_priority_tasks: int
    upcoming_exams: int
    generated_sessions: int
    total_scheduled_hours: float
    completion_rate: float
