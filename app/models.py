from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Index, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from .db.base_class import Base

# SQLAlchemy
# SQLAlchemy is a library for interacting with databases using Python

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    # Relationship: One user has many entries
    journal_entries = relationship("JournalEntry", back_populates="owner")


class Brand(Base):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True) # e.g., "Ippodo"
    
    # link the brand to the Journal entries
    products = relationship("Product", back_populates="brand")

    # This is what the Admin uses to display the brand name in the UI
    def __str__(self):
        return self.name  # This tells the Admin: "Represent this object as the brand name"
    
    # Optional: __repr__ is what developers see in the console/logs
    def __repr__(self):
        return f"<Brand(name='{self.name}')>"


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    brand_id:  Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    grade: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    date_purchased: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(Text, index=True) 
    # back_populates is the attr name in the other class
    brand = relationship("Brand", back_populates="products")
    journal_entries = relationship("JournalEntry", back_populates='product')


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)
    # Denormalized brand_id for faster filtering (derived from product.brand_id)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    rating: Mapped[float] = mapped_column(Float)
    # The Foreign Key + The Index
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[date] = mapped_column(Date)
    method: Mapped[str] = mapped_column(String, nullable=True)

    # The "Back Link" to the user
    owner = relationship("User", back_populates="journal_entries")
    # Back lint to product
    product = relationship("Product", back_populates="journal_entries")
