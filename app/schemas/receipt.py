from pydantic import BaseModel, ConfigDict, validator
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductSchema
from fastapi import HTTPException


class ReceiptCreate(BaseModel):
    model_config = ConfigDict(strict=True)

    products: List[ProductSchema]
    payment_type: str
    payment_amount: float


class ReceiptCreatingResponse(BaseModel):
    id: int
    products: List[ProductSchema]
    payment_type: str
    payment_amount: float
    total: float
    rest: float
    created_at: datetime


class ReceiptResponse(BaseModel):
    id: int
    created_at: datetime
    total: float
    payment_type: str
    payment_amount: float
    rest: float
    products: List[ProductSchema]

    class Config:
        orm_mode = True


class ReceiptFilterParams(BaseModel):
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
    min_total: Optional[float] = None
    max_total: Optional[float] = None
    payment_type: Optional[str] = None

    @validator('min_total', 'max_total')
    def validate_positive_amount(cls, value):
        if value is not None and value <= 0:
            raise HTTPException(
                status_code=400, detail="'min_total' and 'max_total' must be greater than 0")
        return value

    @validator('max_total')
    def validate_max_total(cls, value, values):
        min_total = values.get('min_total')
        if min_total is not None and value is not None and value < min_total:
            raise HTTPException(
                status_code=400, detail="'max_total' must be greater than or equal to 'min_total'")
        return value

    @validator('created_to')
    def validate_date(cls, value, values):
        created_from = values.get('created_from')
        if created_from is not None and value is not None and value <= created_from:
            raise HTTPException(
                status_code=400, detail="'created_to' must be greater than 'created_from'")
        return value

    @validator('payment_type')
    def validate_payment_type(cls, value):
        if value and value not in ["cash", "cashless"]:
            raise HTTPException(
                status_code=400, detail="Payment type must be 'cash' or 'cashless'")
        return value


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10

    @validator('page', 'page_size')
    def validate_positive(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=400, detail="'page' and 'page_size' must be greater than 0")
        return value
