from datetime import date, timedelta

from app import crud, schemas
from app.database import Base, SessionLocal, engine


Base.metadata.create_all(bind=engine)


def seed() -> None:
    db = SessionLocal()
    try:
        student = crud.get_student_by_email(db, "demo@student.com")
        if not student:
            student = crud.create_student(
                db,
                schemas.StudentCreate(
                    name="Demo Student",
                    email="demo@student.com",
                    study_hours_per_day=4,
                    preferred_start_time="09:00",
                    preferred_end_time="18:00",
                ),
            )

        tasks = crud.get_tasks_by_student(db, student.id)
        if not tasks:
            examples = [
                schemas.TaskCreate(
                    student_id=student.id,
                    title="Prepare Distributed Programming REST API",
                    description="Design endpoints and validate request payloads",
                    course_name="Distributed Programming",
                    deadline=date.today() + timedelta(days=3),
                    difficulty=5,
                    estimated_hours=8,
                    is_exam_related=True,
                ),
                schemas.TaskCreate(
                    student_id=student.id,
                    title="Write project report",
                    description="Document architecture and testing",
                    course_name="Distributed Programming",
                    deadline=date.today() + timedelta(days=7),
                    difficulty=4,
                    estimated_hours=6,
                    is_exam_related=False,
                ),
            ]
            for task in examples:
                crud.create_task(db, task)

        exams = crud.get_exams_by_student(db, student.id)
        if not exams:
            crud.create_exam(
                db,
                schemas.ExamCreate(
                    student_id=student.id,
                    subject="Distributed Programming",
                    course_name="Distributed Programming",
                    exam_date=date.today() + timedelta(days=10),
                    importance=5,
                    estimated_revision_hours=6,
                ),
            )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed completed")
