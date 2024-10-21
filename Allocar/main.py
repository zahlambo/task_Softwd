from fastapi import FastAPI, HTTPException
from db import get_database
from models import *
from datetime import date,datetime

app = FastAPI()
db=get_database()


@app.post("/allocate_vehicle/", response_model=allocation)
async def allocate_vehicle(request: AllocationRequest):

    employee = await db["employees"].find_one({"id": request.employee_id})
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

   
    last_allocation = await db["allocations"].find_one(sort=[("id", -1)]) 
    if last_allocation:
        new_id = last_allocation["id"] + 1
    else:
        new_id = 1 

    allocation_doc = allocation(
        id=new_id, 
        employee_id=request.employee_id,
        vehicle_id=request.vehicle_id,
        allocation_date=request.allocation_date
    )


    await db["allocations"].insert_one(allocation_doc.model_dump())

    return allocation_doc


@app.put("/update_allocation/{allocation_id}", response_model=allocation)
async def update_allocation(allocation_id: int, request: AllocationRequest):

    existing_allocation = await db["allocations"].find_one({"id": allocation_id})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")


    allocation_date =(existing_allocation["allocation_date"])

    today = date.today()
    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot update past or ongoing allocation")

    new_allocation_date = request.allocation_date
    allocation_exists = await db["allocations"].find_one({
        "vehicle_id": request.vehicle_id,
        "allocation_date": new_allocation_date
    })
    if allocation_exists and allocation_exists["id"] != allocation_id:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for this date")

    update_result = await db["allocations"].update_one(
        {"id": allocation_id},
        {"$set": {
            "vehicle_id": request.vehicle_id,
            "allocation_date": new_allocation_date 
        }}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Allocation update failed")

    updated_allocation = await db["allocations"].find_one({"id": allocation_id})
    return allocation(**updated_allocation)


@app.delete("/delete_allocation/{allocation_id}")
async def delete_allocation(allocation_id: int):

    allocation = await db["allocations"].find_one({"id": allocation_id})
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    allocation_date =(allocation["allocation_date"])

    today = date.today()
    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot update past or ongoing allocation")

    await db["allocations"].delete_one({"id": allocation_id})

    return {"message": "Allocation deleted successfully"}