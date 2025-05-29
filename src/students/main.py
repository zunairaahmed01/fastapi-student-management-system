from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field , computed_field
from typing import List, Optional, Literal, Dict, Annotated
import uvicorn, json, os

# Student data model
class Student(BaseModel):
    id: str = Field(..., min_length=2, max_length=10000)
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[A-Za-z ]+$")
    age: int = Field(..., ge=0, le=150)
    gender: Literal["male", "female"]
    height: float
    weight: float
    DOB: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    email: Annotated[Optional[EmailStr], Field(default=None)] 
    linkedin: Annotated[Optional[str], Field(default=None)]
    contact: Dict[str, str]
    hobbies: Annotated[Optional[List[str]], Field(default=None)]

    @computed_field
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return bmi

# Model for updating student info
class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(min_length=3, max_length=50, default=None, pattern=r"^[A-Za-z ]+$")]
    age: Annotated[Optional[int], Field(ge=0, le=150, default=None)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]
    DOB: Annotated[Optional[str], Field(pattern=r"^\d{4}-\d{2}-\d{2}$", default=None)]
    email: Annotated[Optional[EmailStr], Field(default=None)]
    linkedin: Annotated[Optional[str], Field(default=None)]
    contact: Annotated[Optional[Dict[str, str]], Field(default=None)]
    hobbies: Annotated[Optional[List[str]], Field(default=None)]

# Load data from JSON file

def load_data():
    if not os.path.exists("Students.json"):
        with open("Students.json", "w") as f:
            json.dump({}, f, indent=4)
        return {}
    try:
        with open("Students.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open("Students.json", "w") as f:
            json.dump({}, f, indent=4)
        return {}

# Save data to JSON file
def save_data(data):
    with open("Students.json", "w") as f:
        json.dump(data, f, indent=4)

app = FastAPI(title="Students System API")

@app.get("/")
def home():
    return {"message": "Welcome to the Students API System"}

@app.get("/students")
def get_all_students():
    return load_data()

@app.get("/students/{student_id}")
def get_student_by_id(student_id: str = Path(..., example="s1")):
    data = load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student ID not found")
    return data[student_id]

@app.get("/sort_students")
def sort_students(
    sort_by: str = Query(..., description="Sort students by: height, weight, gender, age"),
    order_by: str = Query("asc", description="Order: asc or desc")
):
    data = load_data()
    valid_fields = ["height", "weight", "gender", "age"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field, choose from {valid_fields}")
    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")
    reverse = (order_by == "desc")
    sorted_list = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse)
    return sorted_list

@app.post("/students", status_code=201)
def create_student(student: Student):
    data = load_data()
    if student.id in data:
        raise HTTPException(status_code=400, detail="Student ID already exists")
    data[student.id] = student.model_dump(exclude={"id"})
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "New student created successfully"})

@app.put("/updatestuents/{student_id}")
def update_student(student_id: str, updated_data: StudentUpdate):
    data = load_data()
    if student_id not in data:
        raise HTTPException(status_code=400, detail="Student not found")

    current_data = data[student_id]
    updated_fields = updated_data.model_dump(exclude_unset=True)
    for key, value in updated_fields.items():
        current_data[key] = value

    current_data['id'] = student_id
    validated_student = Student(**current_data)
    data[student_id] = validated_student.model_dump(exclude={'id'})
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Student updated successfully"})

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    data = load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student ID not found")
    del data[student_id]
    save_data(data)
    return {"message": "Student deleted successfully"}

def start():
    uvicorn.run("students.main:app", host="127.0.0.1", port=8001, reload=True)