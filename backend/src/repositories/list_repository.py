from sqlalchemy.orm import Session

from models.list import ListModel
from schemas.list_schema import ListCreate


class ListRepo:
    async def create(db: Session, list: ListCreate):
        db_list = ListModel(
            name=list.name, description=list.description, user_id=list.user_id
        )
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
        return db_list

    def fetch_by_id(db: Session, _id: int, user_id: int):
        l = db.query(ListModel).filter(ListModel.id == _id).first()
        if l.user_id != user_id:
            return False
        return l

    def fetch_by_name(db: Session, name: str, user_id: int):
        return (
            db.query(ListModel)
            .filter(ListModel.user_id == user_id, ListModel.name == name)
            .first()
        )

    # def fetch_all(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    #     return db.query(List).offset(skip).limit(limit).all()

    def fetch_all_by_user(
        db: Session, user_id: int = None, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(ListModel)
            .filter(ListModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def delete(db: Session, list_data: ListModel):
        db.delete(list_data)
        db.commit()

    async def update(db: Session, list_data: ListModel):
        db.merge(list_data)
        db.commit()
