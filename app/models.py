from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship
from .db import Base

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
    height_cm = Column(Integer)
    weight_kg = Column(Integer)
    diseases = Column(JSON)     # ✅ real JSON
    allergies = Column(JSON)    # ✅ real JSON
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="health_profile")


class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    plan = Column(JSON, nullable=False)   # ✅ JSON column
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="meal_plans")
