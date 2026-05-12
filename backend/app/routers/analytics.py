from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import DashboardStatsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard/{student_id}", response_model=DashboardStatsResponse)
def get_dashboard_stats(student_id: int, db: Session = Depends(get_db)) -> DashboardStatsResponse:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} was not found")

    stats = crud.get_dashboard_stats(db, student_id)
    return DashboardStatsResponse(**stats)
