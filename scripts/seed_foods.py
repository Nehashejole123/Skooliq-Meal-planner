# scripts/seed_foods.py
from app.db import SessionLocal, engine
from app import models, crud
models.Base.metadata.create_all(bind=engine)

sample_foods = [
    {"name":"Oatmeal", "calories_kcal":220, "protein_g":6, "carbs_g":40, "fat_g":4,
     "allergens": {"gluten": True, "nuts": False, "milk": False}, "tags":["kid_friendly","breakfast"], "prep_time_min":10 },
    {"name":"Banana", "calories_kcal":100, "protein_g":1.2, "carbs_g":27, "fat_g":0.3, "allergens": {}, "tags":["snack"], "prep_time_min":1},
    {"name":"Rice and Dal", "calories_kcal":520, "protein_g":14, "carbs_g":80, "fat_g":6, "allergens": {}, "tags":["lunch"], "prep_time_min":30},
    {"name":"Chapati and Veg", "calories_kcal":430, "protein_g":10, "carbs_g":60, "fat_g":8, "allergens": {"gluten": True}, "tags":["dinner"], "prep_time_min":20},
    {"name":"Peanut Butter Toast", "calories_kcal":300, "protein_g":8, "carbs_g":30, "fat_g":15, "allergens": {"nuts": True}, "tags":["breakfast"], "prep_time_min":5},
    {"name":"Idli and Sambar", "calories_kcal":350, "protein_g":9, "carbs_g":60, "fat_g":6, "allergens": {}, "tags":["breakfast","south_indian"], "prep_time_min":30},
    {"name":"Vegetable Pulao", "calories_kcal":480, "protein_g":10, "carbs_g":70, "fat_g":12, "allergens": {}, "tags":["lunch"], "prep_time_min":35},
    {"name":"Steamed Veg Soup", "calories_kcal":120, "protein_g":3, "carbs_g":18, "fat_g":2, "allergens": {}, "tags":["dinner","light"], "prep_time_min":15},
    {"name":"Moong Dal Chilla", "calories_kcal":260, "protein_g":12, "carbs_g":30, "fat_g":8, "allergens": {}, "tags":["breakfast"], "prep_time_min":15},
    {"name":"Fruit Salad", "calories_kcal":150, "protein_g":2, "carbs_g":35, "fat_g":0.5, "allergens": {}, "tags":["snack"], "prep_time_min":10},
    # add up to 20-50 items for MVP
]

db = SessionLocal()
crud.create_foods_from_list(db, sample_foods)
db.close()
print("Seeded foods.")
