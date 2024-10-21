from fastapi import FastAPI, HTTPException
from typing import List
from db import get_database
from models import *
import datetime

app = FastAPI()
db=get_database()

@app.post("/allocate_vehicle/", response_model=allocation)
async def allocate_vehicle(request: AllocationRequest):

    employee = await db["employees"].find_one({"id": request.employee_id})
    print(employee)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")


    vehicle = await db["vehicles"].find_one({"id": request.vehicle_id})
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")


    allocation_exists = await db["allocations"].find_one({
        "vehicle_id": request.vehicle_id,
        "allocation_date": request.allocation_date
    })
    if allocation_exists:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date")


    allocation_doc = allocation(
        id=1, 
        employee_id=request.employee_id,
        vehicle_id=request.vehicle_id,
        allocation_date=request.allocation_date
    )


    await db["allocations"].insert_one(allocation_doc.model_dump())

    return allocation_doc