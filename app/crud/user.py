from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserSchema
from app.main.security import hash_password, validate_password, encode_jwt
from app.main.utils import get_user_by_username


class CRUDUser:
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 100

    def register_user(self, db: Session, user: UserCreate) -> dict:
        if not (self.MIN_USERNAME_LENGTH <= len(user.username) <= self.MAX_USERNAME_LENGTH):
            raise HTTPException(
                status_code=400,
                detail=f"Username length must be between {self.MIN_USERNAME_LENGTH} and {self.MAX_USERNAME_LENGTH} characters"
            )

        if not (self.MIN_NAME_LENGTH <= len(user.name) <= self.MAX_NAME_LENGTH):
            raise HTTPException(
                status_code=400,
                detail=f"Name length must be between {self.MIN_NAME_LENGTH} and {self.MAX_NAME_LENGTH} characters"
            )

        if not (self.MIN_PASSWORD_LENGTH <= len(user.password) <= self.MAX_PASSWORD_LENGTH):
            raise HTTPException(
                status_code=400,
                detail=f"Password length must be between {self.MIN_PASSWORD_LENGTH} and {self.MAX_PASSWORD_LENGTH} characters"
            )

        db_user = get_user_by_username(db, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = hash_password(user.password)
        new_user = User(username=user.username, name=user.name, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"username": new_user.username, "name": new_user.name}

    def login(self, db: Session, user: UserLogin) -> dict:
        db_user = get_user_by_username(db, user.username)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password"
            )
        if not validate_password(user.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password"
            )

        token = encode_jwt({"sub": db_user.username, "username": db_user.username})

        return {"access_token": token, "token_type": "bearer"}

    def get_me(self, user: UserSchema) -> dict:
        return {
            "username": user.username,
            "name": user.name
        }


crud_user = CRUDUser()
