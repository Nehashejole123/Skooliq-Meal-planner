from db import engine
from sqlalchemy import text

print("🔄 Trying to connect to PostgreSQL...")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        row = result.fetchone()
        if row:
            print("✅ Connected to Database:", row[0])
        else:
            print("⚠️ No result returned from database.")
except Exception as e:
    print("❌ Database connection failed:", e)
