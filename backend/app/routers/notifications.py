from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import NotificationResponse
from app.services.notification_service import get_notifications_for_student

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/student/{student_id}", response_model=list[NotificationResponse])
def get_notifications(student_id: int, db: Session = Depends(get_db)) -> list[NotificationResponse]:
    try:
        return get_notifications_for_student(db, student_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
