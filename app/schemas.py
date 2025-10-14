# app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, List

class StudentBase(BaseModel):
    name: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        orm_mode = True

class HealthProfileBase(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    diseases: Optional[Dict[str, bool]] = None
    allergies: Optional[Dict[str, bool]] = None

class HealthProfileCreate(HealthProfileBase):
    pass

class HealthProfile(HealthProfileBase):
    id: int
    student_id: int
    class Config:
        orm_mode = True

# Food
class FoodBase(BaseModel):
    name: str
    calories_kcal: float
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    allergens: Optional[Dict[str, bool]] = None
    tags: Optional[List[str]] = None
    cuisine: Optional[str] = None
    prep_time_min: Optional[int] = None
    cost_index: Optional[int] = None

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    id: int
    class Config:
        orm_mode = True

class MealPlanBase(BaseModel):
    plan: Dict

class MealPlanCreate(MealPlanBase):
    pass

class MealPlan(MealPlanBase):
    id: int
    student_id: int
    class Config:
        orm_mode = True
