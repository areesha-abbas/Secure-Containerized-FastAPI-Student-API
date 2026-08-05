from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Student
from schemas import StudentCreate, StudentResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student REST API")


@app.get("/")
def home():
    return {"message": "Student REST API is running!"}


# CREATE
@app.post("/students", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = Student(name=student.name)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# READ ALL
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# READ ONE
@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name

    db.commit()
    db.refresh(existing_student)

    return existing_student


# DELETE
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }