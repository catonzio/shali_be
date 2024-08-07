from pydantic import BaseModel
from typing import List, Optional
from schemas.item_schema import ItemSchema


class ListBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_checked: Optional[bool] = False
    index: Optional[int] = None


class ListCreate(ListBase):
    user_id: Optional[int] = None
    # pass


class ListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_checked: Optional[bool] = None
    index: Optional[int] = None


class ListByUser(BaseModel):
    user_id: int


class ListSchema(ListBase):
    id: int
    user_id: int
    # items: List[ItemSchema] = []

    class Config:
        from_attributes = True


class ReorderListItems(BaseModel):
    old_index: int
    new_index: int
