from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from models.user import User
from schemas.user_schema import UserCreate, UserSchema, UserLogin
from db import get_db
from repositories.user_repository import UserRepo
from controllers.access_controller import get_password_hash
from controllers.access_controller import get_current_user


router = APIRouter(tags=["User"])


@router.post("/register", response_model=UserSchema, status_code=201)
async def create_user(user_request: UserCreate, db: Session = Depends(get_db)):
    """
    Create a List and save it in the database
    """
    db_user = UserRepo.fetch_by_email_pwd(db, user_request.email, user_request.password)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists!")
    user_request.password = get_password_hash(user_request.password)
    return await UserRepo.create(db=db, user=user_request)


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    return UserSchema(
        id=current_user.id, username=current_user.username, email=current_user.email
    )


@router.get("/all", response_model=List[UserSchema])
async def get_all_users(db: Session = Depends(get_db)):
    users_db = await UserRepo.fetch_all(db)
    return [UserSchema.from_model(u) for u in users_db]
