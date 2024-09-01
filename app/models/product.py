from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    def total_price(self):
        return self.price * self.quantity
