from app.schemas.receipt import ReceiptCreate
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserSchema
from app.db.session import get_db
from app.main.security import decode_jwt
from jwt.exceptions import InvalidTokenError


http_bearer = HTTPBearer()


def validate_receipt_data(receipt_in: ReceiptCreate, rest: float):

    if len(receipt_in.products) == 0:
        raise HTTPException(
            status_code=400, detail="Product list must contain at least one item"
        )

    if receipt_in.payment_type not in ["cash", "cashless"]:
        raise HTTPException(
            status_code=400, detail="Payment type must be 'cash' or 'cashless'"
        )

    if receipt_in.payment_amount <= 0:
        raise HTTPException(
            status_code=400, detail="Payment amount must be greater than 0"
        )

    for product in receipt_in.products:
        if product.price <= 0:
            raise HTTPException(
                status_code=400, detail=f"Price for product '{product.name}' must be greater than 0"
            )
        if product.quantity <= 0:
            raise HTTPException(
                status_code=400, detail=f"Quantity for product '{product.name}' must be greater than 0"
            )

    if rest < 0:
        raise HTTPException(
            status_code=400, detail="Insufficient payment amount")


def wrap_text(text, max_length):
    wrapped_lines = []
    while len(text) > max_length:
        split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        wrapped_lines.append(text[:split_point])
        text = text[split_point:].lstrip()
    wrapped_lines.append(text)
    return wrapped_lines


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: Session = Depends(get_db)
) -> UserSchema:
    username: str | None = payload.get("sub")
    user = get_user_by_username(db, username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )
