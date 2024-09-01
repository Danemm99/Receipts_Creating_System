from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserSchema
from app.db.session import get_db
from app.main.utils import get_current_auth_user
from app.crud.user import crud_user


router = APIRouter()


@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.register_user(db, user)


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return crud_user.login(db, user)


@router.get("/me/")
def get_me(user: UserSchema = Depends(get_current_auth_user)):
    return crud_user.get_me(user)
