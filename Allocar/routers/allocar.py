from fastapi import HTTPException, Depends,APIRouter
from core.db import get_database
from models import *
from datetime import date
from typing import List
from utils.db_utils import *
from schemas import *

router = APIRouter()
db=get_database()


@router.post("/allocate_vehicle/", response_model=allocation,summary="Allocate a vehicle to an employee")
async def allocate_vehicle(request: AllocationRequest = Depends()):

    employee = await get_employee(request.employee_id)
    if request.allocation_date.date()<date.today():
        raise HTTPException(status_code=400, detail=f"You can not set a previous date.")

    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {request.employee_id} not found.")

    vehicle = await get_vehicle(request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {request.vehicle_id} not found.")

    allocation_exists = await is_vehicle_allocated(request.vehicle_id, request.allocation_date)
    if allocation_exists:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for the selected date.")

    last_allocation = await db["allocations"].find_one(sort=[("allocation_id", -1)])
    new_id = last_allocation["allocation_id"] + 1 if last_allocation else 1

    allocation_doc = allocation(
        allocation_id=new_id,
        employee_id=request.employee_id,
        vehicle_id=request.vehicle_id,
        allocation_date=request.allocation_date
    )

    await db["allocations"].insert_one(allocation_doc.model_dump())

    return allocation_doc


@router.put("/update_allocation/{allocation_id}", response_model=allocation,summary="Update an existing vehicle allocation")
async def update_allocation(allocation_id: int, request: AllocationRequest = Depends()):

    existing_allocation = await get_allocation_by_id(allocation_id)
    if not existing_allocation:
        raise HTTPException(status_code=404, detail=f"Allocation with ID {allocation_id} not found.")

    allocation_date = existing_allocation["allocation_date"]
    today = date.today()
    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot update past or ongoing allocations.")

    allocation_exists = await is_vehicle_allocated(request.vehicle_id, request.allocation_date, exclude_allocation_id=allocation_id)
    if allocation_exists:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for the new date.")

    update_result = await update_allocation_by_id(allocation_id, {
        "vehicle_id": request.vehicle_id,
        "allocation_date": request.allocation_date
    })

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update allocation.")

    updated_allocation = await get_allocation_by_id(allocation_id)
    return allocation(**updated_allocation)



@router.delete("/delete_allocation/{allocation_id}",summary="Delete a vehicle allocation")
async def delete_allocation(allocation_id: int):

    allocation = await get_allocation_by_id(allocation_id)

    allocation_date = allocation["allocation_date"]
    today = date.today()

    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot delete past or ongoing allocation.")

    await delete_allocation_by_id(allocation_id)
    return {"message": f"Allocation with ID {allocation_id} deleted successfully"}
