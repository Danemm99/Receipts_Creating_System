from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.user import User
from app.models.receipt import Receipt
from app.models.product import Product
from app.schemas.receipt import ReceiptResponse, ReceiptCreate, ReceiptFilterParams, PaginationParams
from app.main.utils import validate_receipt_data, wrap_text
from typing import List


class CRUDReceipt:
    MIN_LINE_LENGTH = 30

    def create_receipt(self, db: Session, receipt_in: ReceiptCreate, user_id: int) -> Receipt:
        total = sum(product.price * product.quantity for product in receipt_in.products)
        rest = receipt_in.payment_amount - total

        validate_receipt_data(receipt_in, rest)

        db_receipt = Receipt(
            user_id=user_id,
            total=total,
            payment_type=receipt_in.payment_type,
            payment_amount=receipt_in.payment_amount,
            rest=rest
        )

        db.add(db_receipt)
        db.commit()
        db.refresh(db_receipt)

        for product_data in receipt_in.products:
            db_product = Product(
                name=product_data.name,
                price=product_data.price,
                quantity=product_data.quantity,
                receipt_id=db_receipt.id
            )
            db.add(db_product)

        db.commit()
        db.refresh(db_receipt)

        return db_receipt

    def get_receipts(
        self, db: Session, user_id: int, filters: ReceiptFilterParams, pagination: PaginationParams
    ) -> List[ReceiptResponse]:
        query = db.query(Receipt).filter(Receipt.user_id == user_id)

        if filters.created_from:
            query = query.filter(Receipt.created_at >= filters.created_from)
        if filters.created_to:
            query = query.filter(Receipt.created_at <= filters.created_to)
        if filters.min_total:
            query = query.filter(Receipt.total >= filters.min_total)
        if filters.max_total:
            query = query.filter(Receipt.total <= filters.max_total)
        if filters.payment_type:
            query = query.filter(Receipt.payment_type == filters.payment_type)

        receipts = query.options(joinedload(Receipt.products)) \
            .offset((pagination.page - 1) * pagination.page_size) \
            .limit(pagination.page_size) \
            .all()

        return receipts

    def get_receipt_by_id(
        self, db: Session, receipt_id: int, user_id: int
    ) -> ReceiptResponse:
        receipt = db.query(Receipt).filter(
            Receipt.id == receipt_id,
            Receipt.user_id == user_id
        ).options(joinedload(Receipt.products)).first()

        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")

        return receipt

    def get_public_receipt(self, db: Session, receipt_id: int, line_length: int) -> str:
        if line_length < self.MIN_LINE_LENGTH:
            raise HTTPException(status_code=404, detail=f"Line length should be at least {self.MIN_LINE_LENGTH} characters")

        receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")

        user = db.query(User).filter(User.id == receipt.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        receipts_products = receipt.products

        username = user.name
        username_padding = (line_length - len(username)) // 2
        receipt_text = " " * username_padding + username + "\n"
        receipt_text += "=" * line_length + "\n"

        for i, product in enumerate(receipts_products):
            total = product.quantity * product.price
            name = product.name

            receipt_text += f"{product.quantity:.2f} x {product.price:.2f}\n"

            if len(name) > line_length // 2:
                name_lines = wrap_text(name, line_length // 2)
            else:
                name_lines = [name]

            for j, name_line in enumerate(name_lines):
                if j == len(name_lines) - 1:
                    line = f"{name_line}" + " " * (line_length - len(name_line) - len(f"{total:.2f}")) + f"{total:.2f}"
                else:
                    line = f"{name_line}" + " " * (line_length - len(name_line))

                receipt_text += line + "\n"

            if i != len(receipts_products) - 1:
                receipt_text += "-" * line_length + "\n"
        receipt_text += "=" * line_length + "\n"
        receipt_text += "Total:" + (line_length - 6 - len(f"{receipt.total:.2f}")) * " " + f"{receipt.total:.2f}\n"
        receipt_text += "Payment type:" + (line_length - 13 - len(f"{receipt.payment_type}")) * " " + f"{receipt.payment_type}\n"
        receipt_text += "Payment amount:" + (line_length - 15 - len(f"{receipt.payment_amount}")) * " " + f"{receipt.payment_amount}\n"
        receipt_text += "Rest:" + (line_length - 5 - len(f"{receipt.rest:.2f}")) * " " + f"{receipt.rest:.2f}\n"
        receipt_text += "=" * line_length + "\n"

        date_str = receipt.created_at.strftime('%d.%m.%Y %H:%M')
        date_padding = (line_length - len(date_str)) // 2
        receipt_text += " " * date_padding + date_str + "\n"

        thank_you_message = "Thank you for your purchase!"
        thank_you_padding = (line_length - len(thank_you_message)) // 2
        receipt_text += " " * thank_you_padding + thank_you_message + "\n"

        return receipt_text


crud_receipt = CRUDReceipt()
