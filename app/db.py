# app/db.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()  # loads .env from project root

# Ensure this matches your .env (fallback provided)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:Neha@localhost:5432/skooliq"
)

# SQLAlchemy 2.0 style
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# correct (non-deprecated) import
Base = declarative_base()

# DO NOT import models at module top-level here (avoids circular import).
# When you want to create tables manually, run this module as a script:
if __name__ == "__main__":
    # import models only when explicitly running this file
    import importlib
    importlib.import_module("app.models")   # registers models with Base
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created (if not existing).")
