from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from controllers.access_controller import get_current_user
from db import get_db
from models.user import User
from repositories.list_repository import ListRepo
from schemas.item_schema import ItemSchema
from schemas.list_schema import ListSchema, ListCreate, ListUpdate
from sqlalchemy.orm import Session
from fastapi import APIRouter

from schemas.user_schema import UserSchema

router = APIRouter(tags=["List"])


@router.post("/", response_model=ListSchema, status_code=201)
async def create_list(
    current_user: Annotated[User, Depends(get_current_user)],
    list_request: ListCreate,
    db: Session = Depends(get_db),
):
    """
    Create a List and save it in the database
    """
    db_list = ListRepo.fetch_by_name(
        db, name=list_request.name, user_id=current_user.id
    )

    if db_list:
        raise HTTPException(status_code=400, detail="List already exists!")
    list_request.user_id = current_user.id
    return await ListRepo.create(db=db, list=list_request)


@router.get("/", response_model=List[ListSchema])
def get_all_lists(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get all the Lists lists of the user in database
    """
    if name:
        lists = []
        db_list = ListRepo.fetch_by_name(db, name, user_id=current_user.id)
        print(db_list)
        lists.append(db_list)
        return lists
    else:
        return ListRepo.fetch_all_by_user(db, user_id=current_user.id)


@router.get("/{list_id}", response_model=ListSchema)
def get_list(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    list_id: int,
    db: Session = Depends(get_db),
):
    """
    Get the List with the given ID provided by User listd in database
    """
    db_list = ListRepo.fetch_by_id(db, list_id, user_id=current_user.id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found with the given ID")
    elif db_list == False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_list


@router.delete("/{list_id}")
async def delete_list(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    list_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete the List with the given ID provided by User listd in database
    """
    db_list = ListRepo.fetch_by_id(db, list_id, user_id=current_user.id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found with the given ID")
    elif db_list == False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await ListRepo.delete(db, db_list)


@router.put("/{list_id}")
async def update_list(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    list_id: int,
    list_request: ListUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a List stored in the database
    """
    db_list = ListRepo.fetch_by_id(db, list_id, user_id=current_user.id)
    if db_list:
        update_list_encoded = jsonable_encoder(list_request)
        if update_list_encoded["name"] is not None:
            db_list.name = update_list_encoded["name"]
        if update_list_encoded["description"] is not None:
            db_list.description = update_list_encoded["description"]
        if update_list_encoded["is_checked"] is not None:
            db_list.is_checked = int(update_list_encoded["is_checked"])
        return await ListRepo.update(db=db, list_data=db_list)
    elif db_list == False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=400, detail="List not found with the given ID")


@router.get("/{list_id}/items", response_model=List[ItemSchema])
def get_items(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
    list_id: int,
    db: Session = Depends(get_db),
):
    """
    Get the List with the given ID provided by User listd in database
    """
    db_list = ListRepo.fetch_by_id(db, list_id, user_id=current_user.id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found with the given ID")
    elif db_list == False:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db_list.items
