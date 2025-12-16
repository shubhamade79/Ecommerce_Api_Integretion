from sqlalchemy import Column, Integer, String, Float, Boolean,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    isInsured = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    password = Column(String(100),nullable=False)
    confirm_password = Column(String(100),nullable=False)
    debit_card = relationship(
        "DebitCard",
        back_populates="user",
        uselist=False
    )

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    address = Column(String(100), nullable=False)
    pincode = Column(String(15), nullable=False)
    state = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

class Card(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, nullable=False)

class DebitCard(Base):
    __tablename__ = "debit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String(16), unique=True, index=True)
    cvv = Column(String(3))
    expiry = Column(String(5))  # MM/YY
    balance = Column(Float, default=500000.0)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="debit_card")


from datetime import datetime
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    heading = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    rating = Column(Float, nullable=False)
    user_name = Column(String(100), nullable=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("debit_cards.id"))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="PLACED")

class WishList(Base):
    __tablename__= "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"),)
    product_id = Column(Integer, ForeignKey("product.id"),)


