
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from typing import Optional
from app import models, schemas



# Inside app/crud.py
# Journal entry has denormalized brand_id for fast filtering (derived from product.brand_id)
def get_all_journal_entries(db: Session, brand_id: Optional[int] = None):
    query = db.query(models.JournalEntry).options(
        joinedload(models.JournalEntry.product).joinedload(models.Product.brand)
    )
    if brand_id is not None:
        # Fast direct filter using denormalized brand_id (no JOIN needed!)
        query = query.filter(models.JournalEntry.brand_id == brand_id)
    return query.all()

def create_journal_entry(db: Session, entry: schemas.JournalEntryCreate, user_id: int):
    # Lookup product to get brand_id for denormalization
    product = db.query(models.Product).filter(models.Product.id == entry.product_id).first()
    if not product:
        raise ValueError(f"Product with id {entry.product_id} not found")
    
    # Create entry with brand_id populated from product
    entry_data = entry.model_dump()
    entry_data['brand_id'] = product.brand_id
    entry_data['user_id'] = user_id
    
    db_entry = models.JournalEntry(**entry_data)
    db.add(db_entry)
    db.commit()
    return db.query(models.JournalEntry).options(
        joinedload(models.JournalEntry.product).joinedload(models.Product.brand)
    ).filter(models.JournalEntry.id == db_entry.id).first()

def sync_journal_entry_brand_ids(db: Session, product_id: Optional[int] = None):
    """
    Sync brand_id in journal entries when a product's brand changes.
    If product_id is None, syncs all entries (use with caution on large datasets).
    """
    if product_id is not None:
        # Sync entries for a specific product
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if product:
            db.query(models.JournalEntry).filter(
                models.JournalEntry.product_id == product_id
            ).update({models.JournalEntry.brand_id: product.brand_id})
    else:
        # Sync all entries (slower but ensures consistency)
        # This uses a subquery to update brand_id from product.brand_id
        db.execute(
            text("""
                UPDATE journal_entries 
                SET brand_id = (
                    SELECT brand_id FROM products 
                    WHERE products.id = journal_entries.product_id
                )
            """)
        )
    db.commit()

def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def get_brands(db: Session, include_products: bool = False):
    query = db.query(models.Brand)
    if include_products:
        # Load products but not their nested brand to avoid circular references
        query = query.options(joinedload(models.Brand.products))
    return query.all()