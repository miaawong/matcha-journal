
from sqlalchemy.orm import Session, joinedload
from app import models, schemas



# Inside app/crud.py
# SQLAlchemy Query: Get all matcha entries with their brands
def get_all_matcha_entries(db: Session):

    return db.query(models.MatchaEntry).options(joinedload(models.MatchaEntry.brand)).all()

def create_matcha_entry(db: Session, entry: schemas.MatchaEntryCreate, user_id: int):
    db_entry = models.MatchaEntry(**entry.model_dump(), user_id=user_id)
    db.add(db_entry)
    db.commit()
    
    # The trick: Refresh AND Load the relationship
    # This ensures the 'brand' object is attached before returning to the API
    return db.query(models.MatchaEntry).options(
        joinedload(models.MatchaEntry.brand)
    ).filter(models.MatchaEntry.id == db_entry.id).first()

def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def get_brands(db: Session):
    return db.query(models.Brand).all()