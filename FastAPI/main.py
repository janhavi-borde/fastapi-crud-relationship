# from fastapi import FastAPI
# from routes.teacher import teacher
# app = FastAPI()

# app.include_router(teacher)


from fastapi import FastAPI,HTTPException,Depends, status
from pydantic import BaseModel
from typing import List
import models
from config.db import engine,SessionLocal,Base,meta
from sqlalchemy.orm import Session

app=FastAPI()

meta.create_all(bind=engine)

class ClassBase(BaseModel):
    name:str

class TeacherBase(BaseModel):
    name:str

class TeacherCreate(BaseModel):
    name: str  

class ClassCreate(BaseModel):
    name: str
    teacher_id: int

class TeacherWithClasess(TeacherBase):
    classes: List[ClassBase] = []

class ClassUpdate(BaseModel):
    name: str

class ClassUpdateTeacher(BaseModel):
    teacher_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#get all teacher
@app.get("/teachers/")
def list_teachers(db: Session = Depends(get_db)):
    teachers = db.query(models.Teacher).all()
    return teachers

#get all classes
@app.get("/classes/")
def list_teachers(db: Session = Depends(get_db)):
    classes = db.query(models.Class).all()
    return classes

# Create a Teacher
@app.post("/teachers/", status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = models.Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

# Read a Teacher by ID
@app.get("/teachers/{teacher_id}")
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

# Create a Class for a Teacher
@app.post("/classes/")
def create_class(class_data: ClassCreate, db: Session = Depends(get_db)):
    db_class = models.Class(**class_data.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

# Retrieve all Classes for a Teacher
@app.get("/teachers/{teacher_id}/classes/")
def get_teacher_classes(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher.classes

# Update a Teacher by ID
@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, teacher: TeacherCreate, db: Session = Depends(get_db)):
    existing_teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if existing_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in teacher.dict().items():
        setattr(existing_teacher, key, value)
    db.commit()
    db.refresh(existing_teacher)
    return existing_teacher

# Update a Class by ID
@app.put("/classes/{class_id}",)
def update_class(class_id: int, class_data: ClassUpdate, db: Session = Depends(get_db)):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    for key, value in class_data.dict().items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class

# Update the Teacher Assigned to a Class
@app.put("/classes/{class_id}/teacher")
def update_class_teacher(class_id: int, class_data: ClassUpdateTeacher, db: Session = Depends(get_db)):
    db_class = db.query(models.Class).filter(models.Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    db_teacher = db.query(models.Teacher).filter(models.Teacher.id == class_data.teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db_class.teacher = db_teacher
    db.commit()
    db.refresh(db_class)
    return db_class

# Delete a Teacher by ID
@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return teacher

# read all subject from teacher id
@app.get("/teacher/{teacher_id}/allclasses", response_model=TeacherWithClasess)
def read_teacher_with_classes(*, teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.get(models.Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return teacher
