# db_init.py
from db.connection import engine
from db.models import Base  # Base is your declarative_base from db/models.py

# Create all tables if they do not exist
Base.metadata.create_all(engine)
print("Database and tables created successfully.")
