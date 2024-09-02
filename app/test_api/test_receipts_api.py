from app.main.security import hash_password
from app.models.user import User
from app.models.receipt import Receipt
from app.models.product import Product
from app.test_api.conftest import client, test_db, db
from datetime import datetime, timedelta


def test_create_receipt_not_authenticated(test_db, db):
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

    response_post_create = client.post("/api/receipts/", json=receipt_valid_data)
    response = response_post_create.json()

    assert response["detail"] == "Not authenticated"


def test_create_receipt_insufficient_payment(test_db, db):
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

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == "Insufficient payment amount"


def test_create_receipt_invalid_product_list(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

    receipt_invalid_data = {
        "products": [],
        "payment_type": "cash",
        "payment_amount": 5.0
    }

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == "Product list must contain at least one item"


def test_create_receipt_invalid_payment_type(test_db, db):
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
        "payment_type": "some string",
        "payment_amount": 10.0
    }

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == "Payment type must be 'cash' or 'cashless'"


def test_create_receipt_invalid_payment_amount(test_db, db):
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
        "payment_amount": 0
    }

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == "Payment amount must be greater than 0"


def test_create_receipt_invalid_price_product(test_db, db):
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
                "price": 0,
                "quantity": 2
            }
        ],
        "payment_type": "cash",
        "payment_amount": 10
    }

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == f"Price for product '{receipt_invalid_data['products'][0]['name']}' must be greater than 0"


def test_create_receipt_invalid_quantity_product(test_db, db):
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
                "price": 5,
                "quantity": 0
            }
        ],
        "payment_type": "cash",
        "payment_amount": 10
    }

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_invalid_data, headers=headers)
    response = response_post_create.json()

    assert response["detail"] == f"Quantity for product '{receipt_invalid_data['products'][0]['name']}' must be greater than 0"


def test_create_receipt_successful(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
    db.commit()

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

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_post_create = client.post("/api/receipts/", json=receipt_valid_data, headers=headers)
    response = response_post_create.json()

    assert response["total"] == 10.0
    assert response["payment_type"] == "cash"
    assert response["rest"] == 0


def test_get_receipt_not_authenticated(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
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

    response_get = client.get(f"/api/receipts/{receipt.id}/")
    response = response_get.json()

    assert response["detail"] == "Not authenticated"


def test_get_receipt_authenticated_success(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
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

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get(f"/api/receipts/{receipt.id}/", headers=headers)
    response = response_get.json()

    assert response["total"] == 10.0
    assert response["payment_type"] == "cash"
    assert response["rest"] == 0


def test_get_receipt_for_different_user(test_db, db):
    user1 = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user1)
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
        user_id=user1.id,
        total=10.0,
        payment_type="cash",
        payment_amount=10.0,
        rest=0.0
    )

    db.add(receipt)
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 2",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get(f"/api/receipts/{receipt.id}/", headers=headers)
    response = response_get.json()

    assert response["detail"] == "Receipt not found"


def test_get_not_existing_receipt(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )

    db.add(user)
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

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get(f"/api/receipts/2/", headers=headers)
    response = response_get.json()

    assert response["detail"] == "Receipt not found"


def test_get_receipts_not_authenticated(test_db, db):
    response_get = client.get("/api/receipts/")
    response = response_get.json()

    assert response["detail"] == "Not authenticated"


def test_get_receipts_authenticated_success(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
    db.commit()

    receipt1 = Receipt(
        id=1,
        user_id=user.id,
        total=10.0,
        payment_type="cash",
        payment_amount=10.0,
        rest=0.0
    )

    receipt2 = Receipt(
        id=2,
        user_id=user.id,
        total=20.0,
        payment_type="cashless",
        payment_amount=20.0,
        rest=0.0
    )

    db.add_all([receipt1, receipt2])
    db.commit()

    product1 = Product(
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get("/api/receipts/", headers=headers)
    response = response_get.json()

    assert len(response) == 2
    assert response[0]["total"] == 10.0
    assert response[0]["payment_type"] == "cash"
    assert response[0]["rest"] == 0
    assert response[1]["total"] == 20.0
    assert response[1]["payment_type"] == "cashless"
    assert response[1]["rest"] == 0


def test_get_receipts_filter_by_payment_type(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_filter = {"payment_type": "cash"}
    response_get = client.get("/api/receipts/", params=params_filter, headers=headers)
    response = response_get.json()

    assert len(response) == 1
    assert response[0]["payment_type"] == "cash"


def test_get_receipts_invalid_filter_by_payment_type(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_filter = {"payment_type": "some string"}
    response_get = client.get("/api/receipts/", params=params_filter, headers=headers)
    response = response_get.json()

    assert response["detail"] == "Payment type must be 'cash' or 'cashless'"


def test_get_receipts_filter_by_min_total(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_filter = {"min_total": 15.0}
    response_get = client.get("/api/receipts/", params=params_filter, headers=headers)
    response = response_get.json()

    assert len(response) == 1
    assert response[0]["total"] == 20.0


def test_get_receipts_filter_by_max_total(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_filter = {"max_total": 15.0}
    response_get = client.get("/api/receipts/", params=params_filter, headers=headers)
    response = response_get.json()

    assert len(response) == 1
    assert response[0]["total"] == 10.0


def test_get_receipts_invalid_total_filter(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_invalid_filter = {"min_total": 15.0, "max_total": 10.0}
    response_get = client.get("/api/receipts/", params=params_invalid_filter, headers=headers)
    response = response_get.json()

    assert response["detail"] == "'max_total' must be greater than or equal to 'min_total'"

    params_invalid_filter = {"min_total": 0, "max_total": 0}
    response_get = client.get("/api/receipts/", params=params_invalid_filter, headers=headers)
    response = response_get.json()

    assert response["detail"] == "'min_total' and 'max_total' must be greater than 0"


def test_get_receipts_pagination(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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
        name="Product 1",
        price=5.0,
        quantity=2,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_pagination = {"page": 1, "page_size": 2}
    response_get = client.get("/api/receipts/", params=params_pagination, headers=headers)
    response = response_get.json()

    assert len(response) == 2


def test_get_receipts_invalid_pagination(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
    db.commit()

    receipt1 = Receipt(
        id=1,
        user_id=user.id,
        total=15.0,
        payment_type="cash",
        payment_amount=15.0,
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
        name="Product 1",
        price=5.0,
        quantity=3,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    db.add_all([product1, product2])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    params_invalid_pagination = {"page": 0, "page_size": 0}
    response_get = client.get("/api/receipts/", params=params_invalid_pagination, headers=headers)
    response = response_get.json()

    assert response["detail"] == "'page' and 'page_size' must be greater than 0"


def test_get_receipts_filter_by_date(test_db, db):
    now = datetime.utcnow()
    two_days_ago = now - timedelta(days=2)
    one_day_ago = now - timedelta(days=1)

    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
    db.commit()

    receipt1 = Receipt(
        id=1,
        user_id=user.id,
        created_at=two_days_ago,  # 2 days ago
        total=15.0,
        payment_type="cash",
        payment_amount=15.0,
        rest=0.0
    )

    receipt2 = Receipt(
        id=2,
        user_id=user.id,
        created_at=one_day_ago,  # 1 day ago
        total=20.0,
        payment_type="cashless",
        payment_amount=20.0,
        rest=0.0
    )

    receipt3 = Receipt(
        id=3,
        user_id=user.id,
        created_at=now,  # today
        total=45.0,
        payment_type="cash",
        payment_amount=45.0,
        rest=0.0
    )

    db.add_all([receipt1, receipt2, receipt3])
    db.commit()

    product1 = Product(
        name="Product 1",
        price=5.0,
        quantity=3,
        receipt_id=receipt1.id
    )

    product2 = Product(
        name="Product 2",
        price=10.0,
        quantity=2,
        receipt_id=receipt2.id
    )

    product3 = Product(
        name="Product 3",
        price=15.0,
        quantity=3,
        receipt_id=receipt3.id
    )

    db.add_all([product1, product2, product3])
    db.commit()

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 1",
        "password": "password"
    })

    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}


    start_date = one_day_ago.isoformat()
    end_date = now.isoformat()

    print(start_date, end_date)
    print(receipt1.created_at, receipt2.created_at, receipt3.created_at)

    params_date_filter = {"created_from": start_date, "created_to": end_date}
    response_get = client.get("/api/receipts/", params=params_date_filter, headers=headers)
    response = response_get.json()

    assert len(response) == 2
    assert response[0]["total"] == 20.0
    assert response[1]["total"] == 45.0


def test_get_public_receipt_without_auth(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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

    response_get = client.get(f"/api/receipts/public/{receipt.id}/")
    assert response_get.status_code == 200


def test_get_public_receipt_by_different_user(test_db, db):
    user1 = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user1)
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
        user_id=user1.id,
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

    response_post_login = client.post("/api/auth/login", json={
        "username": "User 2",
        "password": "password"
    })
    access_token = response_post_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response_get = client.get(f"/api/receipts/public/{receipt.id}/", headers=headers)
    assert response_get.status_code == 200


def test_get_public_receipt_invalid_line_length(test_db, db):
    user = User(
        id=1,
        username="User 1",
        name="Test User",
        hashed_password=hash_password('password'),
    )
    db.add(user)
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

    response_get = client.get(f"/api/receipts/public/{receipt.id}/", params=params)
    response = response_get.json()
    assert response["detail"] == "Line length should be at least 30 characters"
