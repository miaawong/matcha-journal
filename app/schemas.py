from datetime import date
from pydantic import BaseModel
from typing import Optional, List
# Pydantic 
# Pydantic is a library for data validation and serialization

class BrandCreate(BaseModel):
    name: str

class ProductSummary(BaseModel):
    """Simplified product schema for use in BrandResponse (no nested brand to avoid circular refs)"""
    id: int
    name: str
    brand_id: int
    grade: Optional[str] = None
    region: Optional[str] = None
    image: Optional[str] = None
    class Config: 
        from_attributes = True

class BrandResponse(BaseModel):
    id: int
    name: str
    products: Optional[List[ProductSummary]] = None
    class Config:
        # allows pydantic to read from SQLAlchemy ORM objects 
        # without it you would need to manually convert id=brand.id, name=brand.name
        from_attributes = True

class ProductCreate(BaseModel): 
    name: str
    brand_id: int 
    grade: Optional[str] = None
    region: Optional[str] = None
    date_purchased: date 
    image: str

class ProductResponse(BaseModel): 
    id: int
    name: str
    brand_id: int
    grade: Optional[str] = None
    region: Optional[str] = None
    brand: Optional[BrandResponse] = None
    image: Optional[str]= None
    class Config: 
        from_attributes = True


# What the client sends us when they want to record a new tea
class JournalEntryCreate(BaseModel):
    product_id: int
    rating: float
    notes: Optional[str] = None
    created_at: date
    method: Optional[str] = None 
    
class JournalEntryResponse(BaseModel):
    id: int
    product_id: int
    brand_id: int  # Denormalized for fast filtering
    rating: float
    notes: Optional[str] = None
    user_id: int
    # This MUST match the name in models.py
    product: Optional[ProductResponse] = None
    created_at: date
    method: Optional[str] = None

    class Config:
        from_attributes = True





