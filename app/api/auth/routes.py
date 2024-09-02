from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.db.session import get_db
from app.crud.auth import crud_auth


router = APIRouter()


@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_auth.register_user(db, user)


@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return crud_auth.login(db, user)
