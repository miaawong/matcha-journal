from sqlalchemy import create_engine  # Removed create_all
from sqlalchemy.orm import sessionmaker

# 1. The Connection String 
SQLALCHEMY_DATABASE_URL = "postgresql://matcha_user:matcha_password@localhost:5432/matcha_journal"

# 2. The Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. The Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The Helper (Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()