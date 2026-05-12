from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.services.priority_service import calculate_task_priority


def create_student(db: Session, payload: schemas.StudentCreate) -> models.Student:
    student = models.Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_students(db: Session) -> list[models.Student]:
    return db.query(models.Student).order_by(models.Student.created_at.desc()).all()


def get_student(db: Session, student_id: int) -> models.Student | None:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_email(db: Session, email: str) -> models.Student | None:
    return db.query(models.Student).filter(func.lower(models.Student.email) == email.lower()).first()


def update_student(db: Session, student: models.Student, payload: schemas.StudentUpdate) -> models.Student:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: models.Student) -> None:
    db.delete(student)
    db.commit()


def create_task(db: Session, payload: schemas.TaskCreate) -> models.Task:
    task_data = payload.model_dump()
    task_data["priority_score"] = calculate_task_priority(
        deadline=payload.deadline,
        difficulty=payload.difficulty,
        is_exam_related=payload.is_exam_related,
        estimated_hours=payload.estimated_hours,
    )
    task = models.Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session) -> list[models.Task]:
    return db.query(models.Task).order_by(models.Task.deadline.asc()).all()


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks_by_student(db: Session, student_id: int) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.student_id == student_id)
        .order_by(models.Task.deadline.asc(), models.Task.priority_score.desc())
        .all()
    )


def get_active_tasks_by_student(db: Session, student_id: int) -> list[models.Task]:
    return (
        db.query(models.Task)
        .filter(
            models.Task.student_id == student_id,
            models.Task.status.in_(["pending", "in_progress"]),
        )
        .all()
    )


def update_task(db: Session, task: models.Task, payload: schemas.TaskUpdate) -> models.Task:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    task.priority_score = calculate_task_priority(
        deadline=task.deadline,
        difficulty=task.difficulty,
        is_exam_related=task.is_exam_related,
        estimated_hours=task.estimated_hours,
    )

    db.commit()
    db.refresh(task)
    return task


def update_task_status(db: Session, task: models.Task, status: str) -> models.Task:
    task.status = status
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()


def create_exam(db: Session, payload: schemas.ExamCreate) -> models.Exam:
    exam = models.Exam(**payload.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def get_exams(db: Session) -> list[models.Exam]:
    return db.query(models.Exam).order_by(models.Exam.exam_date.asc()).all()


def get_exam(db: Session, exam_id: int) -> models.Exam | None:
    return db.query(models.Exam).filter(models.Exam.id == exam_id).first()


def get_exams_by_student(db: Session, student_id: int) -> list[models.Exam]:
    return (
        db.query(models.Exam)
        .filter(models.Exam.student_id == student_id)
        .order_by(models.Exam.exam_date.asc())
        .all()
    )


def get_upcoming_exams_by_student(db: Session, student_id: int, from_date: date) -> list[models.Exam]:
    return (
        db.query(models.Exam)
        .filter(models.Exam.student_id == student_id, models.Exam.exam_date >= from_date)
        .order_by(models.Exam.exam_date.asc())
        .all()
    )


def update_exam(db: Session, exam: models.Exam, payload: schemas.ExamUpdate) -> models.Exam:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(exam, key, value)
    db.commit()
    db.refresh(exam)
    return exam


def delete_exam(db: Session, exam: models.Exam) -> None:
    db.delete(exam)
    db.commit()


def create_study_session(db: Session, payload: schemas.StudySessionCreate) -> models.StudySession:
    session = models.StudySession(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def create_study_sessions_bulk(db: Session, payloads: list[schemas.StudySessionCreate]) -> list[models.StudySession]:
    sessions = [models.StudySession(**payload.model_dump()) for payload in payloads]
    db.add_all(sessions)
    db.commit()
    for session in sessions:
        db.refresh(session)
    return sessions


def get_study_session(db: Session, session_id: int) -> models.StudySession | None:
    return db.query(models.StudySession).filter(models.StudySession.id == session_id).first()


def get_schedule_by_student(db: Session, student_id: int) -> list[models.StudySession]:
    return (
        db.query(models.StudySession)
        .filter(models.StudySession.student_id == student_id)
        .order_by(models.StudySession.session_date.asc(), models.StudySession.priority_score.desc())
        .all()
    )


def delete_schedule_by_student(db: Session, student_id: int) -> int:
    deleted_rows = db.query(models.StudySession).filter(models.StudySession.student_id == student_id).delete()
    db.commit()
    return deleted_rows


def mark_session_completed(db: Session, session: models.StudySession) -> models.StudySession:
    session.completed = True
    db.commit()
    db.refresh(session)
    return session


def get_dashboard_stats(db: Session, student_id: int) -> dict:
    total_tasks = db.query(models.Task).filter(models.Task.student_id == student_id).count()
    pending_tasks = (
        db.query(models.Task)
        .filter(models.Task.student_id == student_id, models.Task.status.in_(["pending", "in_progress"]))
        .count()
    )
    completed_tasks = (
        db.query(models.Task)
        .filter(models.Task.student_id == student_id, models.Task.status == "completed")
        .count()
    )
    high_priority_tasks = (
        db.query(models.Task)
        .filter(models.Task.student_id == student_id, models.Task.priority_score >= 8)
        .count()
    )
    upcoming_exams = (
        db.query(models.Exam)
        .filter(models.Exam.student_id == student_id, models.Exam.exam_date >= date.today())
        .count()
    )
    generated_sessions = db.query(models.StudySession).filter(models.StudySession.student_id == student_id).count()
    total_scheduled_hours = (
        db.query(func.coalesce(func.sum(models.StudySession.duration_hours), 0.0))
        .filter(models.StudySession.student_id == student_id)
        .scalar()
        or 0.0
    )

    completion_rate = 0.0
    if total_tasks > 0:
        completion_rate = round((completed_tasks / total_tasks) * 100, 2)

    return {
        "student_id": student_id,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "high_priority_tasks": high_priority_tasks,
        "upcoming_exams": upcoming_exams,
        "generated_sessions": generated_sessions,
        "total_scheduled_hours": round(float(total_scheduled_hours), 2),
        "completion_rate": completion_rate,
    }
