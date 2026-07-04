from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import get_dashboard_summary

router = APIRouter()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
