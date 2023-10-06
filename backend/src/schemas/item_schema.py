from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    list_id: int
    description: Optional[str] = None
    is_checked: Optional[bool] = False
    index: Optional[int] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_checked: Optional[bool] = None
    index: Optional[int] = None


class ItemSchema(ItemBase):
    id: int

    class Config:
        orm_mode = True
