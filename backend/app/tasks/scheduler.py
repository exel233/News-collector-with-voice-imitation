from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.db.session import SessionLocal
from app.models.models import User, UserSettings
from app.services.briefing_service import generate_briefing_for_user


scheduler = BackgroundScheduler()


def _run_daily_generation() -> None:
    db = SessionLocal()
    try:
        now = datetime.utcnow().strftime("%H:%M")
        for user in db.query(User).all():
            settings = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
            if settings and settings.daily_schedule_time.strftime("%H:%M") == now:
                generate_briefing_for_user(db, user, mode="scheduled")
    finally:
        db.close()


def configure_scheduler() -> None:
    if scheduler.running:
        return
    scheduler.add_job(_run_daily_generation, "interval", minutes=1, id="daily-briefings", replace_existing=True)
    scheduler.start()


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
