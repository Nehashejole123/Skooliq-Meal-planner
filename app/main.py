from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import db, crud, schemas, models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Skooliq Meal Planner API 🚀"}

# ---------------- Database Dependency ----------------
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# ---------------- Students ----------------
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student.name)

@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ---------------- Health Profile ----------------
@app.post("/students/{student_id}/health_profile", response_model=schemas.HealthProfile)
def create_health_profile(student_id: int, profile: schemas.HealthProfileCreate, db: Session = Depends(get_db)):
    return crud.create_health_profile(db, student_id, profile)

# ---------------- Meal Plan ----------------
@app.post("/students/{student_id}/meal_plan", response_model=schemas.MealPlan)
def create_meal_plan(student_id: int, db: Session = Depends(get_db)):
    return crud.create_meal_plan(db, student_id)

# ✅ NEW: Get all meal plans for a student
@app.get("/students/{student_id}/meal_plans", response_model=List[schemas.MealPlan])
def get_meal_plans(student_id: int, db: Session = Depends(get_db)):
    plans = db.query(models.MealPlan).filter(models.MealPlan.student_id == student_id).all()
    if not plans:
        raise HTTPException(status_code=404, detail="No meal plans found for this student")
    return plans

# ✅ Auto-create tables if not exist
models.Base.metadata.create_all(bind=db.engine)
