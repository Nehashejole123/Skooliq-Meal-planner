import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("🔄 Trying to connect to PostgreSQL using SQLAlchemy...")

try:
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        row = result.fetchone()
        print("✅ Connected to Database:", row[0])
except Exception as e:
    print("❌ Database connection failed:", e)
