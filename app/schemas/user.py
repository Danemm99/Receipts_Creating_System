from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: str


class UserCreate(UserSchema):
    name: str


class UserLogin(UserSchema):
    pass
