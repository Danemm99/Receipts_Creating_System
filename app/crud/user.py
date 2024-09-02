from app.schemas.user import UserCreate, UserLogin, UserSchema


class CRUDUser:

    def get_me(self, user: UserSchema) -> dict:
        return {
            "username": user.username,
            "name": user.name
        }


crud_user = CRUDUser()
