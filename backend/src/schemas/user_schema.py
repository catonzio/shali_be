from pydantic import BaseModel
from typing import List
from models.user import User
from schemas.item_schema import ItemSchema


class UserBase(BaseModel):
    username: str
    email: str
    # password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserSchema(UserBase):
    id: int
    # lists: List[List] = []

    class Config:
        orm_mode = True

    def from_model(user: User):
        return UserSchema(username=user.username, email=user.email, id=user.id)
