from sqlalchemy.orm import Session
from .models import Student, HealthProfile, MealPlan
from .ai_client import generate_meal_plan
from .schemas import HealthProfileCreate
import json


# ---------------- Students ----------------
def create_student(db: Session, name: str):
    student = Student(name=name)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


# ---------------- Health Profile ----------------
def create_health_profile(db: Session, student_id: int, profile: HealthProfileCreate):
    health = HealthProfile(
        student_id=student_id,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        diseases=profile.diseases,
        allergies=profile.allergies
    )
    db.add(health)
    db.commit()
    db.refresh(health)
    return health


# ---------------- Meal Plan ----------------
def create_meal_plan(db: Session, student_id: int, plan_data=None):
    profile = db.query(HealthProfile).filter(HealthProfile.student_id == student_id).first()
    if not profile:
        raise Exception("Health profile not found")

    # Generate via Gemini or fallback
    if plan_data is None:
        try:
            raw_response = generate_meal_plan(profile)

            # ✅ Ensure it's a dictionary
            if isinstance(raw_response, str):
                try:
                    plan_data = json.loads(raw_response)   # if it’s JSON string
                except json.JSONDecodeError:
                    # fallback: wrap string into dict
                    plan_data = {"summary": raw_response}
            elif isinstance(raw_response, dict):
                plan_data = raw_response
            else:
                plan_data = {"summary": str(raw_response)}

        except Exception:
            # final fallback
            plan_data = {
                "breakfast": "Oatmeal with fruits",
                "lunch": "Rice, dal, salad",
                "dinner": "Chapati, vegetables, milk"
            }

    meal_plan = MealPlan(student_id=student_id, plan=plan_data)
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan
