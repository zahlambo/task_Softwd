from fastapi import APIRouter, Depends, HTTPException
from core.db import get_database
from models import *
from datetime import date
from typing import List
from utils.db_utils import *
from schemas import *
from pymongo.errors import DuplicateKeyError


router = APIRouter()

@router.post('/add_employee/', response_model=employee, summary="Add a new employee")
async def add_employee(employee: Employee):

    last_employee = await db["employees"].find_one(sort=[("employee_id", -1)])
    new_id = last_employee["employee_id"] + 1 if last_employee else 1

    employee_doc=Employee(
        employee_id=new_id,
        name=employee.name,
        email=employee.email,
        department=employee.department
    )

    try:
        await db['employees'].insert_one(employee_doc.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Email already exists")
    return employee_doc