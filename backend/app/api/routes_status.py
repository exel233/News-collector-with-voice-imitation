from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Briefing, NewsEvent, SourceArticle, User


router = APIRouter(prefix="/status", tags=["status"])


@router.get("")
def status(db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "articles": db.query(SourceArticle).count(),
        "events": db.query(NewsEvent).count(),
        "briefings": db.query(Briefing).count(),
        "mode": "mock-friendly-mvp",
    }
