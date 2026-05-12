from datetime import date, timedelta

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services.priority_service import calculate_exam_revision_priority, calculate_task_priority


MAX_SESSION_HOURS = 2.0


def _iter_dates(start_date: date, end_date: date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def generate_schedule_for_student(db: Session, student_id: int) -> schemas.ScheduleGenerateResponse:
    student = crud.get_student(db, student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} was not found")

    crud.delete_schedule_by_student(db, student_id)

    warnings: list[str] = []
    study_hours_per_day = float(student.study_hours_per_day)
    today = date.today()

    day_usage: dict[date, float] = {}
    session_payloads: list[schemas.StudySessionCreate] = []

    tasks = crud.get_active_tasks_by_student(db, student_id)
    for task in tasks:
        task.priority_score = calculate_task_priority(
            deadline=task.deadline,
            difficulty=task.difficulty,
            is_exam_related=task.is_exam_related,
            estimated_hours=task.estimated_hours,
        )
    db.commit()

    sorted_tasks = sorted(tasks, key=lambda t: (-t.priority_score, t.deadline))

    def allocate_hours(
        *,
        title: str,
        total_hours: float,
        priority_score: float,
        start_date: date,
        end_date: date,
        session_type: str,
        task_id: int | None = None,
    ) -> float:
        remaining = round(float(total_hours), 2)
        if remaining <= 0:
            return 0.0

        if end_date < start_date:
            return remaining

        for current_day in _iter_dates(start_date, end_date):
            if remaining <= 0:
                break

            used = day_usage.get(current_day, 0.0)
            free_today = round(study_hours_per_day - used, 2)
            if free_today <= 0:
                continue

            while remaining > 0 and free_today > 0:
                chunk = min(MAX_SESSION_HOURS, remaining, free_today)
                if chunk <= 0:
                    break

                payload = schemas.StudySessionCreate(
                    student_id=student_id,
                    task_id=task_id,
                    session_date=current_day,
                    title=title,
                    duration_hours=round(chunk, 2),
                    priority_score=round(priority_score, 2),
                    session_type=session_type,
                    completed=False,
                )
                session_payloads.append(payload)

                day_usage[current_day] = round(day_usage.get(current_day, 0.0) + chunk, 2)
                free_today = round(study_hours_per_day - day_usage[current_day], 2)
                remaining = round(remaining - chunk, 2)

        return max(remaining, 0.0)

    for task in sorted_tasks:
        start_window = today
        end_window = task.deadline if task.deadline >= today else today

        unscheduled = allocate_hours(
            title=f"Task: {task.title}",
            total_hours=task.estimated_hours,
            priority_score=task.priority_score,
            start_date=start_window,
            end_date=end_window,
            session_type="task",
            task_id=task.id,
        )

        if unscheduled > 0:
            warnings.append(
                f"Task '{task.title}' could not be fully scheduled before deadline. Remaining {unscheduled:.2f} hours."
            )

    exams = crud.get_upcoming_exams_by_student(db, student_id, today)
    sorted_exams = sorted(exams, key=lambda exam: (exam.exam_date, -exam.importance))

    for exam in sorted_exams:
        exam_priority = calculate_exam_revision_priority(
            exam_date=exam.exam_date,
            importance=exam.importance,
            estimated_revision_hours=exam.estimated_revision_hours,
        )

        start_window = today
        end_window = exam.exam_date - timedelta(days=1)

        unscheduled = allocate_hours(
            title=f"Exam Revision: {exam.subject}",
            total_hours=exam.estimated_revision_hours,
            priority_score=exam_priority,
            start_date=start_window,
            end_date=end_window,
            session_type="exam_revision",
            task_id=None,
        )

        if unscheduled > 0:
            warnings.append(
                f"Exam revision for '{exam.subject}' could not be fully scheduled before exam date. Remaining {unscheduled:.2f} hours."
            )

    sessions = crud.create_study_sessions_bulk(db, session_payloads) if session_payloads else []

    total_hours = round(sum(session.duration_hours for session in sessions), 2)
    return schemas.ScheduleGenerateResponse(
        student_id=student_id,
        total_sessions=len(sessions),
        total_hours=total_hours,
        warnings=warnings,
        sessions=[schemas.StudySessionResponse.model_validate(session) for session in sessions],
    )


def get_schedule_for_student(db: Session, student_id: int) -> list[models.StudySession]:
    return crud.get_schedule_by_student(db, student_id)
