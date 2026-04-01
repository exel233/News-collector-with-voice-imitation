from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.models import Briefing, NewsEvent, SourceArticle, User


router = APIRouter(prefix="/status", tags=["status"])


@router.get("")
def status(admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return {
        "admin_email": admin.email,
        "users": db.query(User).count(),
        "articles": db.query(SourceArticle).count(),
        "events": db.query(NewsEvent).count(),
        "briefings": db.query(Briefing).count(),
        "mode": "mock-friendly-mvp",
    }
