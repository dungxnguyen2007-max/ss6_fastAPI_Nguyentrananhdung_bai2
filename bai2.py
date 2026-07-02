from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class add_student(BaseModel):
    id : int = Field(...,gt=1)
    code: str = Field(...,min_length=1,max_length=10)
    name: str = Field(...)
    email: str = Field(...)
    age: int = Field(...,gt = 0)

@app.post("/students")
def add_student(more_student: add_student):
    for i in students:
        if i["id"] == more_student.id:
            raise HTTPException(
                status_code= 400,detail="ID đã tồn tại"
            )
    for c in students:
        if c["code"] == more_student.code:
            raise HTTPException (
                status_code= 400, detail="Code đã tồn tại"
            )
    students.append(more_student.model_dump())
    return{
        "message":"Thêm thành công sinh viên",
        "Data": more_student
    }

@app.get("/students/{student_id}")
def get_student(student_id:int):
    for student in students:
        if student["id"] == student_id:
            return student
        
    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy sinh viên"
    )

@app.get("/student")
def show_student(keyword: str |None = None,
                 min_age : int | None = None,
                 max_age: int | None= None):
    student_list =[]
    for student in students:
        if keyword is not None:
            if keyword.lower() not in student["name"].lower() and keyword.lower() not in student["code"]:
                continue
        if max_age is not None:
            if student["age"] > max_age:
                continue
        if min_age is not None:
            if student["age"] < min_age:
                continue
        student_list.append(student)
    return{
        "message":"Lấy thông tin sinh viên thành công",
        "Data":student_list
    }

@app.put("/students/{student_id}")
def update_student(student_id: int , new : add_student):
    for s in students:
        if s["id"] != student_id and s["code"] == new.code:
            raise HTTPException(
            status_code=400,
            detail="Code đã tồn tại"
        )
    for student in students:
        if student["id"] == student_id:
            student.update(new.model_dump())
            return{
                "message":"Cập nhật thành công",
                "Data": student
            }
    raise HTTPException(
        status_code= 404,
        detail="Không tìm thấy sinh viên"
    )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return{
                "message": "Xóa thành công",
                "Data": student
            }
    raise HTTPException(
        status_code= 404,
        detail="Không tìm thấy sinh viên"
    )