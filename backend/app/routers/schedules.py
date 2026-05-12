from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.schedule_service import generate_schedule_for_student, get_schedule_for_student

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.post("/generate/{student_id}", response_model=schemas.ScheduleGenerateResponse)
def generate_schedule(student_id: int, db: Session = Depends(get_db)) -> schemas.ScheduleGenerateResponse:
    try:
        return generate_schedule_for_student(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/student/{student_id}", response_model=list[schemas.StudySessionResponse])
def get_schedule(student_id: int, db: Session = Depends(get_db)) -> list[schemas.StudySessionResponse]:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")
    return get_schedule_for_student(db, student_id)


@router.patch("/{session_id}/complete", response_model=schemas.StudySessionResponse)
def complete_session(session_id: int, db: Session = Depends(get_db)) -> schemas.StudySessionResponse:
    session = crud.get_study_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Study session with id {session_id} was not found")
    return crud.mark_session_completed(db, session)


@router.delete("/student/{student_id}")
def delete_schedule(student_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")

    deleted_rows = crud.delete_schedule_by_student(db, student_id)
    return {"message": f"Deleted {deleted_rows} session(s) for student {student_id}"}
