from sqlalchemy.orm import Session
from db.models.user import User 


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_id(id: int, db: Session):
    user = db.query(User).filter(User.userId == id).first()
    return user

