from sqlalchemy.orm import Session
from schemas.item_schema import ItemCreate
from models.item import Item


class ItemRepo:
    async def create(db: Session, item: ItemCreate):
        db_item = Item(
            name=item.name,
            description=item.description,
            list_id=item.list_id,
            index=item.index,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, _id):
        return db.query(Item).filter(Item.id == _id).first()

    def fetch_by_name(db: Session, name):
        return db.query(Item).filter(Item.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Item).offset(skip).limit(limit).all()

    async def delete(db: Session, item_id):
        db_item = db.query(Item).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item


if __name__ == "__main__":
    print("Hello")
