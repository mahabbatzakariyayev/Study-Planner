from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("", response_model=schemas.ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(payload: schemas.ExamCreate, db: Session = Depends(get_db)) -> schemas.ExamResponse:
    student = crud.get_student(db, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {payload.student_id} was not found")
    return crud.create_exam(db, payload)


@router.get("", response_model=list[schemas.ExamResponse])
def get_exams(db: Session = Depends(get_db)) -> list[schemas.ExamResponse]:
    return crud.get_exams(db)


@router.get("/student/{student_id}", response_model=list[schemas.ExamResponse])
def get_exams_by_student(student_id: int, db: Session = Depends(get_db)) -> list[schemas.ExamResponse]:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")
    return crud.get_exams_by_student(db, student_id)


@router.get("/{exam_id}", response_model=schemas.ExamResponse)
def get_exam(exam_id: int, db: Session = Depends(get_db)) -> schemas.ExamResponse:
    exam = crud.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} was not found")
    return exam


@router.put("/{exam_id}", response_model=schemas.ExamResponse)
def update_exam(exam_id: int, payload: schemas.ExamUpdate, db: Session = Depends(get_db)) -> schemas.ExamResponse:
    exam = crud.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} was not found")
    return crud.update_exam(db, exam, payload)


@router.delete("/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    exam = crud.get_exam(db, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail=f"Exam with id {exam_id} was not found")

    crud.delete_exam(db, exam)
    return {"message": f"Exam {exam_id} deleted successfully"}
