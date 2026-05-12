from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)) -> schemas.TaskResponse:
    student = crud.get_student(db, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {payload.student_id} was not found")
    return crud.create_task(db, payload)


@router.get("", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)) -> list[schemas.TaskResponse]:
    return crud.get_tasks(db)


@router.get("/student/{student_id}", response_model=list[schemas.TaskResponse])
def get_tasks_by_student(student_id: int, db: Session = Depends(get_db)) -> list[schemas.TaskResponse]:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")
    return crud.get_tasks_by_student(db, student_id)


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> schemas.TaskResponse:
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} was not found")
    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)) -> schemas.TaskResponse:
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} was not found")
    return crud.update_task(db, task, payload)


@router.patch("/{task_id}/status", response_model=schemas.TaskResponse)
def update_task_status(
    task_id: int,
    payload: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db),
) -> schemas.TaskResponse:
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} was not found")
    return crud.update_task_status(db, task, payload.status)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} was not found")

    crud.delete_task(db, task)
    return {"message": f"Task {task_id} deleted successfully"}
