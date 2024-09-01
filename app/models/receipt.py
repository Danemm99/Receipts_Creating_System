from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)
    payment_type = Column(String)
    payment_amount = Column(Float)
    rest = Column(Float)

    products = relationship("Product", backref="receipts")
    user = relationship("User", backref="receipts")
