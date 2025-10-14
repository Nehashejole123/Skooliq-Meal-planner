# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    health_profile = relationship("HealthProfile", back_populates="student", uselist=False)
    meal_plans = relationship("MealPlan", back_populates="student")

class HealthProfile(Base):
    __tablename__ = "health_profiles"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    diseases = Column(JSON)     # dict: {"diabetes": True}
    allergies = Column(JSON)    # dict: {"nuts": True}
    created_at = Column(DateTime, server_default=func.now())
    student = relationship("Student", back_populates="health_profile")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    plan = Column(JSON, nullable=False)   # store final week plan JSON
    created_at = Column(DateTime, server_default=func.now())
    student = relationship("Student", back_populates="meal_plans")

# ---------- New tables ----------
class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    calories_kcal = Column(Float, nullable=False, default=0.0)
    protein_g = Column(Float, nullable=True, default=0.0)
    carbs_g = Column(Float, nullable=True, default=0.0)
    fat_g = Column(Float, nullable=True, default=0.0)
    allergens = Column(JSON, nullable=True)   # e.g. {"nuts": True, "milk": False}
    tags = Column(JSON, nullable=True)        # e.g. ["vegetarian", "kid_friendly"]
    cuisine = Column(String, nullable=True)
    prep_time_min = Column(Integer, nullable=True)
    cost_index = Column(Integer, nullable=True)  # relative cost
    is_school_friendly = Column(Boolean, default=True)

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ingredients = Column(JSON, nullable=False)   # list of {food_id, qty}
    steps = Column(String, nullable=True)
    nutrition = Column(JSON, nullable=True)      # totals
