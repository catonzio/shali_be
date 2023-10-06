from typing import List
from sqlalchemy.orm import Session

from schemas.user_schema import UserCreate
from models.user import User


class UserRepo:
    async def create(db: Session, user: UserCreate) -> User:
        db_user = User(username=user.username, password=user.password, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def fetch_all(db: Session) -> List[User]:
        return db.query(User).all()

    def fetch_by_email_pwd(db: Session, email: str, password: str) -> User:
        return (
            db.query(User)
            .filter(User.email == email and User.password == password)
            .first()
        )

    def fetch_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def fetch_by_id(db: Session, id: int) -> User:
        return db.query(User).filter(User.id == id).first()

    async def update(db: Session, user_data: User):
        db.merge(user_data)
        db.commit()
