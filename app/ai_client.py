# app/ai_client.py
from typing import List, Dict
from app import schemas
from app import crud
import math

def calc_daily_calorie_target(profile: schemas.HealthProfile, goal: str = "maintain"):
    # Simple Mifflin-St Jeor (male default). Without gender, use average offset.
    bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    activity_factor = 1.3  # conservative for school students; you can add field later
    target = bmr * activity_factor
    if goal == "lose":
        target -= 300
    elif goal == "gain":
        target += 300
    return int(max(1000, target))

def pick_item_for_slot(candidates: List[dict], target_kcal: float, used_ids: set):
    # simple: pick item closest to target_kcal and not used yet
    best = None
    best_diff = 1e9
    for c in candidates:
        if c.id in used_ids:
            continue
        diff = abs(c.calories_kcal - target_kcal)
        if diff < best_diff:
            best_diff = diff
            best = c
    if best:
        used_ids.add(best.id)
    return best

def generate_meal_plan(db, profile: schemas.HealthProfile):
    """
    Returns a dict:
    {
      "week_plan": {"Day 1": {"breakfast": {...}, "lunch": {...}, "dinner": {...}}, ...},
      "summary": {"daily_calories": X, "avg_protein": Y},
      "note": "..."
    }
    """
    # 1) compute target
    daily_target = calc_daily_calorie_target(profile)

    # 2) get candidate foods from DB excluding allergens/disease constraints
    candidates = crud.get_candidate_foods(db=db,
                                         allergies=profile.allergies or {},
                                         diseases=profile.diseases or {},
                                         tags=["kid_friendly"] if True else None,
                                         cuisine=None,
                                         max_prep=45)
    if not candidates:
        # fallback: return simple default plan (safe)
        return {
            "week_plan": {f"Day {i+1}": {
                "breakfast": {"name": "Oatmeal", "calories_kcal": 200},
                "lunch": {"name": "Rice and dal", "calories_kcal": 500},
                "dinner": {"name": "Chapati and veg", "calories_kcal": 400}
            } for i in range(7)},
            "summary": {"daily_calories": daily_target},
            "note": "Fallback plan (no dataset candidates matched)."
        }

    # convert SQLAlchemy objects to simple objects for ease of use
    # but we can use fields directly assuming attributes exist
    # Build 7-day plan using greedy picks
    week_plan = {}
    used_ids = set()
    # per-slot calorie distribution
    breakfast_pct, lunch_pct, dinner_pct = 0.25, 0.40, 0.30

    for i in range(7):
        b_target = daily_target * breakfast_pct
        l_target = daily_target * lunch_pct
        d_target = daily_target * dinner_pct

        breakfast = pick_item_for_slot(candidates, b_target, used_ids)
        lunch = pick_item_for_slot(candidates, l_target, used_ids)
        dinner = pick_item_for_slot(candidates, d_target, used_ids)

        # fallback if some slot None -> allow reuse
        if not breakfast:
            breakfast = pick_item_for_slot(candidates, b_target, set())
        if not lunch:
            lunch = pick_item_for_slot(candidates, l_target, set())
        if not dinner:
            dinner = pick_item_for_slot(candidates, d_target, set())

        def food_to_dict(f):
            if f is None:
                return {"name": "Snack", "calories_kcal": 150}
            return {
                "id": f.id,
                "name": f.name,
                "calories_kcal": float(f.calories_kcal),
                "protein_g": float(f.protein_g or 0),
                "carbs_g": float(f.carbs_g or 0),
                "fat_g": float(f.fat_g or 0),
                "allergens": f.allergens or {}
            }

        week_plan[f"Day {i+1}"] = {
            "breakfast": food_to_dict(breakfast),
            "lunch": food_to_dict(lunch),
            "dinner": food_to_dict(dinner)
        }

    # summary
    avg_protein = sum((fp.get('protein_g', 0) for day in week_plan.values() for fp in [day['breakfast'], day['lunch'], day['dinner']])) / (7*3)

    note = f"7-day plan generated using dataset. Daily calorie target ≈ {daily_target} kcal."

    return {
        "week_plan": week_plan,
        "summary": {"daily_calories": daily_target, "avg_protein_g": round(avg_protein, 1)},
        "note": note
    }
