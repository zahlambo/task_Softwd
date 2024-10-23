from fastapi import APIRouter, HTTPException
from core.db import get_database
from models import *
import string
import  random
from utils.db_utils import *
from schemas import *
from pymongo.errors import DuplicateKeyError

router = APIRouter()
db=get_database()

@router.post('/add_employee/', response_model=employee, summary="Add a new employee")
async def add_employee(employee: AddEmployee):

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


@router.post('/add_vehicle/', response_model=vehicle, summary="Add a new vehicle")
async def add_vehicle(vehicle: AddVehicle):

    characters = string.ascii_letters + string.digits
    license_plate = ''.join(random.choice(characters) for _ in range(random.randint(10, 30)))

    last_vehicle = await db["vehicles"].find_one(sort=[("vehicle_id", -1)])
    new_id = last_vehicle["vehicle_id"] + 1 if last_vehicle else 1

    vehicle_doc=Vehicle(
        vehicle_id=new_id,
        driver_name=vehicle.driver_name,
        vehicle_model=vehicle.vehicle_model,
        license_plate=license_plate
    )

    try:
        await db['vehicles'].insert_one(vehicle_doc.model_dump())
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Vehicle already exists")
    return vehicle_doc