from fastapi import APIRouter, Depends
from app.schemas.user import UserSchema
from app.main.utils import get_current_auth_user
from app.crud.user import crud_user


router = APIRouter()


@router.get("/me/")
def get_me(user: UserSchema = Depends(get_current_auth_user)):
    return crud_user.get_me(user)
