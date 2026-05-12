from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    study_hours_per_day: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    preferred_start_time: Mapped[str] = mapped_column(String(5), default="09:00", nullable=False)
    preferred_end_time: Mapped[str] = mapped_column(String(5), default="18:00", nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="student", cascade="all, delete-orphan")
    exams: Mapped[list["Exam"]] = relationship("Exam", back_populates="student", cascade="all, delete-orphan")
    study_sessions: Mapped[list["StudySession"]] = relationship(
        "StudySession", back_populates="student", cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="ck_tasks_difficulty_range"),
        CheckConstraint("estimated_hours > 0", name="ck_tasks_estimated_hours_positive"),
        CheckConstraint(
            "status in ('pending', 'in_progress', 'completed', 'cancelled')",
            name="ck_tasks_status_values",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    course_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    deadline: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)
    is_exam_related: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student: Mapped[Student] = relationship("Student", back_populates="tasks")
    study_sessions: Mapped[list["StudySession"]] = relationship("StudySession", back_populates="task")


class Exam(Base):
    __tablename__ = "exams"
    __table_args__ = (
        CheckConstraint("importance >= 1 AND importance <= 5", name="ck_exams_importance_range"),
        CheckConstraint("estimated_revision_hours > 0", name="ck_exams_revision_hours_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    course_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    exam_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    importance: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_revision_hours: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student: Mapped[Student] = relationship("Student", back_populates="exams")


class StudySession(Base):
    __tablename__ = "study_sessions"
    __table_args__ = (
        CheckConstraint("duration_hours > 0", name="ck_sessions_duration_positive"),
        CheckConstraint(
            "session_type in ('task', 'exam_revision', 'general')",
            name="ck_sessions_type_values",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True, index=True)
    session_date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    duration_hours: Mapped[float] = mapped_column(Float, nullable=False)
    priority_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    session_type: Mapped[str] = mapped_column(String(20), default="task", nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    student: Mapped[Student] = relationship("Student", back_populates="study_sessions")
    task: Mapped[Task | None] = relationship("Task", back_populates="study_sessions")
