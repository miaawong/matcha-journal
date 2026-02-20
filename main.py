from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, schemas, models
from app.db.base_class import Base
from app.db.session import engine, get_db


# admin imports
from sqladmin import Admin, ModelView
from app.models import User, Brand, JournalEntry

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/", response_model=List[schemas.JournalEntryResponse])
def read_all_entries(
    db: Session = Depends(get_db),
    brand_id: Optional[int] = Query(None, description="Filter entries by brand ID")
):
    return crud.get_all_journal_entries(db, brand_id=brand_id)

@app.post("/entries/", response_model=schemas.JournalEntryResponse)
def create_new_entry(entry: schemas.JournalEntryCreate, db: Session = Depends(get_db)):
    return crud.create_journal_entry(db=db, entry=entry, user_id=1)


@app.post("/brands/", response_model=schemas.BrandResponse)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db=db, brand=brand)

@app.get("/brands/", response_model=List[schemas.BrandResponse])
def read_brands(db: Session = Depends(get_db)):
    return crud.get_brands(db)



# put 
# delete 



# Create the Admin interface
admin = Admin(app, engine)

# Tell the admin which tables to show
class JournalEntryView(ModelView, model=JournalEntry):
    column_list = [JournalEntry.id, JournalEntry.product_name, JournalEntry.rating, "brand"]

admin.add_view(JournalEntryView)