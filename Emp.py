from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Emp(BaseModel):
    id: int
    Name: str
    Job: str
    salary: int
    deptno: int
    email: str
    phone: int

Emp_details = [
    {
        "id": 1,
        "Name": "Shubham",
        "Job": "Software",
        "salary": 2000,
        "deptno": 10,
        "email": "shubham@gmail.com",
        "phone": 1234567890
    }
]


@app.get("/employee")
def get_all_employees():
    return Emp_details


@app.get("/employee/{emp_id}")
def get_employee_by_id(emp_id: int):
    for emp in Emp_details:
        if emp["id"] == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Invalid Employee ID")


@app.post("/add_employee")
def add_employee(employee: Emp):
    new_emp={"id": employee.id,
        "Name": employee.Name,
        "Job": employee.Job,
        "salary": employee.salary,
        "deptno": employee.deptno,
        "email": employee.email,
        "phone": employee.phone}
    for i in Emp_details:
        if i["id"] == new_emp['id']:
            return 'Id Already Used'
        if i["email"] == new_emp['email']:
            return 'Email Already Used'
        if i["phone"] == new_emp['phone']:
            return 'Phone Already Used'
    # Add employee as dict
    Emp_details.append(new_emp)

    return {
        "message": "Employee added successfully",
        "employee": new_emp
    }
