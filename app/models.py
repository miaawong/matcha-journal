from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db.base_class import Base

# SQLAlchemy
# SQLAlchemy is a library for interacting with databases using Python

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    # Relationship: One user has many entries
    entries = relationship("MatchaEntry", back_populates="owner")


class Brand(Base):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True) # e.g., "Ippodo"

# link the brand to the matcha entries
    entries = relationship("MatchaEntry", back_populates="brand")

    # This is what the Admin uses to display the brand name in the UI
    def __str__(self):
        return self.name  # This tells the Admin: "Represent this object as the brand name"
    
    # Optional: __repr__ is what developers see in the console/logs
    def __repr__(self):
        return f"<Brand(name='{self.name}')>"

class MatchaEntry(Base):
    __tablename__ = "matcha_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # The Foreign Key + The Index
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    
    product_name: Mapped[str] = mapped_column() # e.g., "Sayaka"
    rating: Mapped[float] = mapped_column(Float)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    # link the matcha entry to the brand
    brand = relationship("Brand", back_populates="entries")
    # The "Back Link" to the user
    owner = relationship("User", back_populates="entries")