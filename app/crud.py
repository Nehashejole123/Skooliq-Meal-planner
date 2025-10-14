from sqlalchemy.orm import Session
from .models import Food, MealPlan, HealthProfile
from .ai_client import generate_meal_plan

# ---------------- Foods ---------------- #
def create_foods_from_list(db: Session, food_list: list):
    created = []
    for f in food_list:
        obj = Food(
            name=f["name"],
            calories_kcal=f.get("calories_kcal", 0),
            protein_g=f.get("protein_g"),
            carbs_g=f.get("carbs_g"),
            fat_g=f.get("fat_g"),
            allergens=f.get("allergens", {}),
            tags=f.get("tags", []),
            cuisine=f.get("cuisine"),
            prep_time_min=f.get("prep_time_min"),
            cost_index=f.get("cost_index", 1),
            is_school_friendly=f.get("is_school_friendly", True)
        )
        db.add(obj)
        created.append(obj)
    db.commit()
    for c in created:
        db.refresh(c)
    return created


def get_all_foods(db: Session, limit: int = 100):
    return db.query(Food).limit(limit).all()


def get_candidate_foods(
    db: Session,
    allergies: dict = None,
    diseases: dict = None,
    tags: list = None,
    cuisine: str = None,
    max_prep: int = None
):
    q = db.query(Food)

    # filter by allergies: exclude foods where any allergen key is true
    if allergies:
        for a, val in allergies.items():
            if val:
                q = q.filter(~Food.allergens.contains({a: True}))

    # tags filter
    if tags:
        for t in tags:
            q = q.filter(Food.tags.contains([t]))

    if cuisine:
        q = q.filter(Food.cuisine == cuisine)

    if max_prep is not None:
        q = q.filter(Food.prep_time_min <= max_prep)

    return q.all()

# ---------------- Meal Plan ---------------- #
def create_meal_plan(db: Session, student_id: int, plan_data=None):
    profile = db.query(HealthProfile).filter(HealthProfile.student_id == student_id).first()
    if not profile:
        raise Exception("Health profile not found")

    # generate plan from dataset + AI client if not provided
    if plan_data is None:
        plan_data = generate_meal_plan(db, profile)   # ✅ pass db

    meal_plan = MealPlan(student_id=student_id, plan=plan_data)
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan
