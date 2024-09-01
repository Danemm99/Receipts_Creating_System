from app.main.security import hash_password
from app.models.user import User
from app.models.receipt import Receipt
from app.models.product import Product
from app.test_api.conftest import client, test_db, db


def test_create_receipt(test_db, db):

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    receipt_invalid_data = {
        "products": [
            {
              "name": "Product 1",
              "price": 5.0,
              "quantity": 2
            }
        ],
        "payment_type": "cash",
        "payment_amount": 5.0
    }

    receipt_valid_data = {
        "products": [
            {
              "name": "Product 1",
              "price": 5.0,
              "quantity": 2
            }
        ],
        "payment_type": "cash",
        "payment_amount": 10.0
    }

    response_post_login = client.post("/api/users/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/create_receipt/", json=receipt_valid_data)
    response = response_post_create.json()

    assert response["detail"] == "Not authenticated"

    response_post_create = client.post("/api/receipts/create_receipt/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == "Insufficient payment amount"

    response_post_create = client.post("/api/receipts/create_receipt/", json=receipt_valid_data, headers=headers)
    response = response_post_create.json()

    assert response["total"] == 10.0
    assert response["payment_type"] == "cash"
    assert response["rest"] == 0


def test_get_receipt_by_id(test_db, db):

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    user2 = User(
        id=2,
        username="User 2",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user2)
    db.commit()

    receipt = Receipt(
        id=1,
        user_id=user.id,
        total=10.0,
        payment_type="cash",
        payment_amount=10.0,
        rest=0.0
    )

    db.add(receipt)
    db.commit()

    product = Product(
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt.id
    )

    db.add(product)
    db.commit()

    response_post_login = client.post("/api/users/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/get_receipt/1/")
    response = response_get.json()

    assert response["detail"] == "Not authenticated"

    response_get = client.get("/api/receipts/get_receipt/1/", headers=headers)
    response = response_get.json()

    assert response["total"] == 10.0
    assert response["payment_type"] == "cash"
    assert response["rest"] == 0

    response_post_login = client.post("/api/users/login", json={
        "username": "User 2",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/get_receipt/1/", headers=headers)
    response = response_get.json()

    assert response["detail"] == "Receipt not found"


def test_get_receipts(test_db, db):

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    user2 = User(
        id=2,
        username="User 2",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user2)
    db.commit()

    receipt1 = Receipt(
        id=1,
        user_id=user.id,
        total=10.0,
        payment_type="cash",
        payment_amount=10.0,
        rest=0.0
    )

    db.add(receipt1)
    db.commit()

    receipt2 = Receipt(
        id=2,
        user_id=user.id,
        total=20.0,
        payment_type="cashless",
        payment_amount=20.0,
        rest=0.0
    )

    db.add(receipt2)
    db.commit()

    product1 = Product(
        id=1,
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    db.add(product1)
    db.commit()

    product2 = Product(
        id=2,
        name="Product 1",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add(product2)
    db.commit()

    params_filter1 = {
        "payment_type": "cash",
    }

    params_filter2 = {
        "min_total": 15.0,
    }

    params_pagination = {
        "page": 1,
        "page_size": 2
    }

    params_invalid_filter = {
        "min_total": 15.0,
        "max_total": 10.0
    }

    params_invalid_pagination = {
        "page": 0,
        "page_size": 0
    }

    response_post_login = client.post("/api/users/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/get_receipts/")
    response = response_get.json()

    assert response["detail"] == "Not authenticated"

    response_get = client.get("/api/receipts/get_receipts/", headers=headers)
    response = response_get.json()

    assert response[0]["total"] == 10.0
    assert response[0]["payment_type"] == "cash"
    assert response[0]["rest"] == 0

    assert response[1]["total"] == 20.0
    assert response[1]["payment_type"] == "cashless"
    assert response[1]["rest"] == 0

    response_get = client.get("/api/receipts/get_receipts/", params=params_filter1, headers=headers)
    response = response_get.json()

    assert len(response) == 1
    assert response[0]["payment_type"] == "cash"

    response_get = client.get("/api/receipts/get_receipts/", params=params_filter2, headers=headers)
    response = response_get.json()

    assert len(response) == 1
    assert response[0]["total"] == 20.0

    response_get = client.get("/api/receipts/get_receipts/", params=params_pagination, headers=headers)
    response = response_get.json()

    assert len(response) == 2

    response_get = client.get("/api/receipts/get_receipts/", params=params_invalid_filter, headers=headers)
    response = response_get.json()

    assert response["detail"] == "'max_total' must be greater than or equal to 'min_total'"

    response_get = client.get("/api/receipts/get_receipts/", params=params_invalid_pagination, headers=headers)
    response = response_get.json()

    assert response["detail"] == "'page' and 'page_size' must be greater than 0"

    response_post_login = client.post("/api/users/login", json={
        "username": "User 2",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/get_receipts/", headers=headers)
    response = response_get.json()

    assert len(response) == 0


def test_get_public_receipt(test_db, db):

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    user2 = User(
        id=2,
        username="User 2",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user2)
    db.commit()

    receipt = Receipt(
        id=1,
        user_id=user.id,
        total=10.0,
        payment_type="cash",
        payment_amount=10.0,
        rest=0.0
    )

    db.add(receipt)
    db.commit()

    product = Product(
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt.id
    )

    db.add(product)
    db.commit()

    params = {
        "line_length": 20,
    }

    response_get = client.get("/api/receipts/public/1/")
    assert response_get.status_code == 200

    response_post_login = client.post("/api/users/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/public/1/", headers=headers)
    assert response_get.status_code == 200

    response_post_login = client.post("/api/users/login", json={
        "username": "User 2",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/public/1/", headers=headers)
    assert response_get.status_code == 200

    response_get = client.get("/api/receipts/public/1/", params=params)
    response = response_get.json()
    assert response["detail"] == "Line length should be at least 30 characters"

