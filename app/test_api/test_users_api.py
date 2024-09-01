from app.main.security import hash_password
from app.models.user import User
from app.test_api.conftest import client, test_db, db


def test_register(test_db, db):

    response_post_register = client.post("/api/users/register", json={
        "username": "User 1",
        "password": "password",
        "name": "Test User"
    })

    response = response_post_register.json()

    assert response["username"] == "User 1"
    assert response["name"] == "Test User"

    response_post_register = client.post("/api/users/register", json={
        "username": "",
        "password": "",
        "name": ""
    })

    response = response_post_register.json()

    assert response["detail"] == "Username length must be between 3 and 20 characters"

    response_post_register = client.post("/api/users/register", json={
        "username": "User 1",
        "password": "password",
        "name": "Test User"
    })

    response = response_post_register.json()

    assert response["detail"] == "Username already registered"


def test_login(test_db, db):

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    response_post_login = client.post("/api/users/login", json={
        "username": "User 1",
        "password": "password"
    })

    tokens_response = response_post_login.json()

    assert "access_token" in tokens_response
    assert "token_type" in tokens_response

    response_post_login = client.post("/api/users/login", json={
        "username": "User 2",
        "password": "password"
    })

    response = response_post_login.json()

    assert response["detail"] == "Invalid username or password"

