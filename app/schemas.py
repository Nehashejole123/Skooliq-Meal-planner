from pydantic import BaseModel
from typing import Optional, Dict, Any

# ---------------- Students ----------------
class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        orm_mode = True


# ---------------- Health Profile ----------------
class HealthProfileBase(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    diseases: Optional[Dict[str, Any]] = None
    allergies: Optional[Dict[str, Any]] = None

class HealthProfileCreate(HealthProfileBase):
    pass

class HealthProfile(HealthProfileBase):
    id: int
    student_id: int
    class Config:
        orm_mode = True


# ---------------- Meal Plan ----------------
class MealPlanBase(BaseModel):
    plan: Dict[str, Any]   # ✅ JSON dictionary

class MealPlanCreate(MealPlanBase):
    pass

class MealPlan(MealPlanBase):
    id: int
    student_id: int
    class Config:
        orm_mode = True

