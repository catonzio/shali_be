from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from db import Base


class ListModel(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, index=True)
    description = Column(String(200))
    is_checked = Column(Integer, default=0)
    # store_id = Column(Integer,ForeignKey('stores.id'),nullable=False)
    items = relationship(
        "Item", primaryjoin="ListModel.id == Item.list_id", cascade="all, delete-orphan"
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    index = Column(Integer, nullable=False)
    
    def __repr__(self):
        return "ListModel(name=%s, description=%s, items=%s)" % (
            self.name,
            self.description,
            self.items,
        )
