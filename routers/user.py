from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends

from entities import User
from routers.auth import get_current_user
from services import UserService

router = APIRouter()
user_service = UserService()


@router.get("/users", response_model=List[User])
def get_users(first_name: Optional[str] = "", last_name: Optional[str] = "", current_user: str = Depends(get_current_user)):
    if first_name or last_name:
        return user_service.find_by_first_name_and_last_name(first_name, last_name)
    return user_service.find_all()


@router.post("/users", response_model=User)
def create_user(user: User, current_user: str = Depends(get_current_user)):
    if user_service.find_by_username(user.username):
        raise HTTPException(status_code=400, detail="User with such username already exists")
    return user_service.save(user)


@router.get("/users/{username}", response_model=User)
def get_user(username: str, current_user: str = Depends(get_current_user)):
    user = user_service.find_by_username(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User with such username does not exist")

