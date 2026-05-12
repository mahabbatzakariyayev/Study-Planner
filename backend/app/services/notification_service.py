from datetime import date

from sqlalchemy.orm import Session

from app import crud, schemas


def get_notifications_for_student(db: Session, student_id: int) -> list[schemas.NotificationResponse]:
    student = crud.get_student(db, student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} was not found")

    notifications: list[schemas.NotificationResponse] = []
    today = date.today()

    tasks = crud.get_tasks_by_student(db, student_id)
    for task in tasks:
        if task.status in {"completed", "cancelled"}:
            continue

        days_left = (task.deadline - today).days
        if days_left < 0:
            notifications.append(
                schemas.NotificationResponse(
                    type="overdue_task",
                    message=f"Task '{task.title}' is overdue.",
                    severity="high",
                    related_id=task.id,
                )
            )
        elif days_left == 0:
            notifications.append(
                schemas.NotificationResponse(
                    type="task_deadline",
                    message=f"Task '{task.title}' is due today.",
                    severity="high",
                    related_id=task.id,
                )
            )
        elif days_left == 1:
            notifications.append(
                schemas.NotificationResponse(
                    type="task_deadline",
                    message=f"Task '{task.title}' is due tomorrow.",
                    severity="high",
                    related_id=task.id,
                )
            )
        elif 2 <= days_left <= 3:
            notifications.append(
                schemas.NotificationResponse(
                    type="task_deadline",
                    message=f"Task '{task.title}' is due in {days_left} days.",
                    severity="medium",
                    related_id=task.id,
                )
            )

        if task.priority_score >= 8:
            notifications.append(
                schemas.NotificationResponse(
                    type="high_priority_task",
                    message=f"Task '{task.title}' has high priority ({task.priority_score}).",
                    severity="high",
                    related_id=task.id,
                )
            )

    exams = crud.get_exams_by_student(db, student_id)
    for exam in exams:
        days_left = (exam.exam_date - today).days
        if days_left == 0:
            notifications.append(
                schemas.NotificationResponse(
                    type="exam_reminder",
                    message=f"Exam '{exam.subject}' is today.",
                    severity="high",
                    related_id=exam.id,
                )
            )
        elif 1 <= days_left <= 3:
            notifications.append(
                schemas.NotificationResponse(
                    type="exam_reminder",
                    message=f"Exam '{exam.subject}' is in {days_left} days.",
                    severity="high",
                    related_id=exam.id,
                )
            )
        elif 4 <= days_left <= 7:
            notifications.append(
                schemas.NotificationResponse(
                    type="exam_reminder",
                    message=f"Exam '{exam.subject}' is in {days_left} days.",
                    severity="medium",
                    related_id=exam.id,
                )
            )

    sessions = crud.get_schedule_by_student(db, student_id)
    sessions_today = [session for session in sessions if session.session_date == today and not session.completed]
    if sessions_today:
        total_hours = round(sum(session.duration_hours for session in sessions_today), 2)
        notifications.append(
            schemas.NotificationResponse(
                type="study_session_today",
                message=f"You have {len(sessions_today)} study session(s) today totaling {total_hours} hours.",
                severity="medium" if total_hours >= 3 else "low",
                related_id=sessions_today[0].id,
            )
        )

    active_tasks = [task for task in tasks if task.status in {"pending", "in_progress"}]
    if active_tasks and not sessions:
        notifications.append(
            schemas.NotificationResponse(
                type="schedule_warning",
                message="You have active tasks but no generated schedule. Generate a schedule.",
                severity="medium",
                related_id=None,
            )
        )

    return notifications
