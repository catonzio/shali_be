from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from controllers.access_controller import get_current_user
from db import get_db
from models.item import Item
from models.user import User
from repositories.item_repository import ItemRepo
from repositories.list_repository import ListRepo
from schemas.item_schema import ItemSchema, ItemCreate, ItemUpdate
from sqlalchemy.orm import Session
from fastapi import APIRouter

router = APIRouter(tags=["Item"])


@router.post("/", response_model=ItemSchema, status_code=201)
async def create_item(
    current_user: Annotated[User, Depends(get_current_user)],
    item_request: ItemCreate,
    db: Session = Depends(get_db),
):
    """
    Create an Item and store it in the database
    """
    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")
    if item_request.index is None:
        db_list: List[Item] = await ListRepo.fetch_by_id(
            db, item_request.list_id, current_user.id
        )
        if db_list is not None:
            db_items = db_list.items
            item_request.index = db_items[-1].index + 1 if db_items else 0
    return await ItemRepo.create(db=db, item=item_request)


@router.get("/", response_model=List[ItemSchema])
def get_all_items(
    current_user: Annotated[User, Depends(get_current_user)],
    name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all the Items stored in database
    """
    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        items.routerend(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@router.get("/{item_id}", response_model=ItemSchema)
def get_item(
    current_user: Annotated[User, Depends(get_current_user)],
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@router.delete("/{item_id}")
async def delete_item(
    current_user: Annotated[User, Depends(get_current_user)],
    item_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await ItemRepo.delete(db, item_id)
    return "Item deleted successfully!"


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(
    current_user: Annotated[User, Depends(get_current_user)],
    item_id: int,
    item_request: ItemUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an Item stored in the database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        if update_item_encoded["name"] is not None:
            db_item.name = update_item_encoded["name"]
        if update_item_encoded["description"] is not None:
            db_item.description = update_item_encoded["description"]
        if update_item_encoded["is_checked"] is not None:
            db_item.is_checked = int(update_item_encoded["is_checked"])
        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
