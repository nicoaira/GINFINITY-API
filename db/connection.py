from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
