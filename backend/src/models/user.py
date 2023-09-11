from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), nullable=False, unique=True, index=True)
    password = Column(String(80), nullable=False)
    email = Column(String(200), nullable=False)
    device_token = Column(String(200), nullable=True)
    
    lists = relationship(
        "ListModel", primaryjoin="User.id == ListModel.user_id", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "ItemModel(name=%s, email=%s)" % (
            self.username,
            self.email,
        )
