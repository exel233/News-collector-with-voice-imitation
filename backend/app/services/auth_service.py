from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.models import Topic, User, UserSettings
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


DEFAULT_TOPICS = [
    ("computer-science", "Computer Science", "AI, software engineering, chips, research, and open source."),
    ("politics", "Politics", "Government, elections, policy, and regulation."),
    ("business", "Business", "Markets, companies, startups, and macro trends."),
    ("science", "Science", "Research, space, climate, medicine, and physics."),
    ("world", "World News", "Conflicts, diplomacy, public safety, and global affairs."),
]


def seed_topics(db: Session) -> None:
    if db.query(Topic).count():
        return
    for slug, label, description in DEFAULT_TOPICS:
        db.add(Topic(slug=slug, label=label, description=description))
    db.commit()


def register_user(db: Session, payload: RegisterRequest) -> TokenResponse:
    seed_topics(db)
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name,
        timezone=payload.timezone,
    )
    db.add(user)
    db.flush()
    db.add(UserSettings(user_id=user.id))
    db.commit()
    return TokenResponse(access_token=create_access_token(user.email))


def login_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))
