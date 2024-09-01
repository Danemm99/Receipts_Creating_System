import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent.parent

load_dotenv()


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


class Settings:
    PROJECT_NAME = "Receipts creating system"
    API_STR = "/api"
    auth_jwt = AuthJWT()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    SQLALCHEMY_TEST_DATABASE_URL: str = os.getenv("SQLALCHEMY_TEST_DATABASE_URL")


settings = Settings()
