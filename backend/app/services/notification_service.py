from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.services.communication_service import send_email, send_whatsapp


def create_notification(db: Session, user_id: int, message: str):
    notif = Notification(
        user_id=user_id,
        message=message
    )

    db.add(notif)
    db.commit()

    # ✅ FETCH USER
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # ✅ EMAIL
        send_email(
            user.email,
            "Notification",
            message
        )

        # ✅ WHATSAPP (if phone exists)
        if user.phone:
            send_whatsapp(user.phone, message)


def get_user_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(
        Notification.user_id == user_id
    ).order_by(Notification.created_at.desc()).all()


def mark_as_read(db: Session, notification_id: int, user_id: int):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()

    if not notif:
        return False

    notif.is_read = True
    db.commit()

    return True