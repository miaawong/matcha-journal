from pydantic import BaseModel
from typing import Optional
# Pydantic 
# Pydantic is a library for data validation and serialization

class BrandResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class MatchaEntryResponse(BaseModel):
    id: int
    product_name: str
    brand_id: int
    rating: float
    notes: Optional[str] = None
    user_id: int
    # This MUST match the name in models.py
    brand: Optional[BrandResponse] = None

    class Config:
        from_attributes = True

class BrandCreate(BaseModel):
    name: str

class BrandResponse(BrandCreate):
    id: int

    class Config:
        from_attributes = True
# What the user sends us when they want to record a new tea
class MatchaEntryCreate(BaseModel):
    product_name: str
    brand_id: int
    rating: float
    notes: Optional[str] = None

