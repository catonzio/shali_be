from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(String(200))
    is_checked = Column(Integer, default=0)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    index = Column(Integer, nullable=False)

    def __repr__(self):
        return "ItemModel(name=%s, description=%s, list_id=%s)" % (
            self.name,
            self.description,
            self.list_id,
        )
