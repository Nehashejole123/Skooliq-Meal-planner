from app.db import engine, Base
from app import models

def create_all_tables():
    print("🚀 Creating all tables in skooldb...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_all_tables()
