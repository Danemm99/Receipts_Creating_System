from app.main.security import hash_password
from app.models.user import User
from app.test_api.conftest import client, test_db, db
from app.crud.auth import crud_auth


MIN_USERNAME_LENGTH = crud_auth.MIN_USERNAME_LENGTH
MAX_USERNAME_LENGTH = crud_auth.MAX_USERNAME_LENGTH
MIN_NAME_LENGTH = crud_auth.MIN_NAME_LENGTH
MAX_NAME_LENGTH = crud_auth.MAX_NAME_LENGTH
MIN_PASSWORD_LENGTH = crud_auth.MIN_PASSWORD_LENGTH
MAX_PASSWORD_LENGTH = crud_auth.MAX_PASSWORD_LENGTH


def test_register_successful(test_db, db):
    response_post_register = client.post("/api/auth/register", json={
        "username": "User 1",
        "password": "password",
        "name": "Test User"
    })

    response = response_post_register.json()

    assert response["username"] == "User 1"
    assert response["name"] == "Test User"


def test_register_invalid_username(test_db, db):
    response_post_register = client.post("/api/auth/register", json={
        "username": "",
        "password": "password",
        "name": "name"
    })

    response = response_post_register.json()

    assert response["detail"] == f"Username length must be between {MIN_USERNAME_LENGTH} and {MAX_USERNAME_LENGTH} characters"


def test_register_invalid_password(test_db, db):
    response_post_register = client.post("/api/auth/register", json={
        "username": "username",
        "password": "",
        "name": "name"
    })

    response = response_post_register.json()

    assert response["detail"] == f"Password length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH} characters"


def test_register_invalid_name(test_db, db):
    response_post_register = client.post("/api/auth/register", json={
        "username": "username",
        "password": "password",
        "name": ""
    })

    response = response_post_register.json()

    assert response["detail"] == f"Name length must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters"


def test_register_existing_user(test_db, db):
    client.post("/api/auth/register", json={
        "username": "User 1",
        "password": "password",
        "name": "Test User"
    })

    response_post_register = client.post("/api/auth/register", json={
        "username": "User 1",
        "password": "password",
        "name": "Test User"
    })

    response = response_post_register.json()

    assert response["detail"] == "Username already registered"


def test_login_successful(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    tokens_response = response_post_login.json()

    assert "access_token" in tokens_response
    assert "token_type" in tokens_response


def test_login_invalid_username(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 2",
        "password": "password"
    })

    response = response_post_login.json()

    assert response["detail"] == "Invalid username or password"


def test_login_invalid_password(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password12"
    })

    response = response_post_login.json()

    assert response["detail"] == "Invalid username or password"


