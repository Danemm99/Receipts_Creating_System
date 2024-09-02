from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.main.utils import get_current_auth_user
from app.models.user import User
from app.schemas.receipt import (ReceiptCreate, ReceiptCreatingResponse, ReceiptResponse, ReceiptFilterParams,
                                 PaginationParams)
from app.db.session import get_db
from typing import List
from fastapi.responses import PlainTextResponse
from app.crud.receipt import crud_receipt


router = APIRouter()


@router.post("/", response_model=ReceiptCreatingResponse)
def create_receipt(
    receipt_id: ReceiptCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_auth_user)
):
    return crud_receipt.create_receipt(db, receipt_id, user.id)


@router.get("/", response_model=List[ReceiptResponse])
def get_receipts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_auth_user),
    filters: ReceiptFilterParams = Depends(),
    pagination: PaginationParams = Depends(),
):
    return crud_receipt.get_receipts(db, user.id, filters, pagination)


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt_by_id(
    receipt_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_auth_user)
):
    return crud_receipt.get_receipt_by_id(db, receipt_id, user.id)


@router.get("/public/{receipt_id}")
def get_public_receipt(receipt_id: int, line_length: int = 40, db: Session = Depends(get_db)):
    return PlainTextResponse(content=crud_receipt.get_public_receipt(db, receipt_id, line_length))
