from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)) -> schemas.StudentResponse:
    if crud.get_student_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail=f"Student with email {payload.email} already exists")

    try:
        student = crud.create_student(db, payload)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create student due to a data integrity issue") from exc
    return student


@router.get("", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)) -> list[schemas.StudentResponse]:
    return crud.get_students(db)


@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)) -> schemas.StudentResponse:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")
    return student


@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    payload: schemas.StudentUpdate,
    db: Session = Depends(get_db),
) -> schemas.StudentResponse:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")

    if payload.email and payload.email.lower() != student.email.lower() and crud.get_student_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail=f"Student with email {payload.email} already exists")

    return crud.update_student(db, student, payload)


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")

    crud.delete_student(db, student)
    return {"message": f"Student {student_id} deleted successfully"}
