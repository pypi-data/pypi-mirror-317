import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Base class for creating models
Base = declarative_base()


# User model
class User(Base):
    """
    Represents an example user model.

    Attributes:
        id (UUID): Unique identifier for the user.
        username (str): Unique username for the user, used for login and identification.
        products (list[Product]): List of products listed by the user as the seller.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)

    # Relationships
    products = relationship("Product", back_populates="seller")

    # IMPORTANT
    # Method to convert the user object to an event object
    def to_event_object(self):
        return {
            "user_id": str(self.id),
            "username": self.username,
        }


# Product model
class Product(Base):
    """
    Represents an example product model.

    Attributes:
        id (UUID): Unique identifier for the product.
        title (str): Name of the product.
        description (str): Description of the product.
        price (float): Price of the product.
        seller_id (UUID): Foreign key linking to the user who listed the product.
        seller (User): The user who listed the product.
    """

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    seller = relationship("User", back_populates="products")

    # IMPORTANT
    # Method to convert the product object to an event object
    def to_event_object(self):
        return {
            "product_id": str(self.id),
            "title": self.title,
            "price": str(self.price),
        }
