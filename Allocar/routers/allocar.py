from fastapi import FastAPI, HTTPException, Depends,APIRouter
from db import get_database
from models import *
from datetime import date,datetime
from typing import List

router = APIRouter()
db=get_database()


@router.post("/allocate_vehicle/", response_model=allocation)
async def allocate_vehicle(request: AllocationRequest = Depends()):

    # Utility function to fetch an employee by ID
    async def get_employee(employee_id: int):
        return await db["employees"].find_one({"id": employee_id})

    # Utility function to fetch a vehicle by ID
    async def get_vehicle(vehicle_id: int):
        return await db["vehicles"].find_one({"id": vehicle_id})

    # Utility function to check if vehicle is already allocated
    async def is_vehicle_allocated(vehicle_id: int, allocation_date: datetime):
        return await db["allocations"].find_one({
            "vehicle_id": vehicle_id,
            "allocation_date": allocation_date
        })

    # Validate employee
    employee = await get_employee(request.employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {request.employee_id} not found.")

    # Validate vehicle
    vehicle = await get_vehicle(request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {request.vehicle_id} not found.")

    # Check if vehicle is already allocated for the given date
    allocation_exists = await is_vehicle_allocated(request.vehicle_id, request.allocation_date)
    if allocation_exists:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for the selected date.")

    # generate the next allocation ID
    last_allocation = await db["allocations"].find_one(sort=[("id", -1)])
    new_id = last_allocation["id"] + 1 if last_allocation else 1

    # Create the allocation document
    allocation_doc = allocation(
        id=new_id,
        employee_id=request.employee_id,
        vehicle_id=request.vehicle_id,
        allocation_date=request.allocation_date
    )

    # Insert the allocation into the database
    await db["allocations"].insert_one(allocation_doc.model_dump())

    return allocation_doc



@router.put("/update_allocation/{allocation_id}", response_model=allocation)
async def update_allocation(allocation_id: int, request: AllocationRequest = Depends()):

    # Utility function to check if vehicle is already allocated for a specific date
    async def is_vehicle_allocated(vehicle_id: int, allocation_date: datetime, exclude_allocation_id: int = None):
        query = {
            "vehicle_id": vehicle_id,
            "allocation_date": allocation_date
        }
        if exclude_allocation_id:
            query["id"] = {"$ne": exclude_allocation_id}
        return await db["allocations"].find_one(query)

    # Fetch existing allocation
    existing_allocation = await db["allocations"].find_one({"id": allocation_id})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail=f"Allocation with ID {allocation_id} not found.")

    # Check if allocation can be updated (i.e., date has not passed)
    allocation_date = existing_allocation["allocation_date"]
    today = date.today()
    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot update past or ongoing allocations.")

    # Check if the new vehicle is already allocated on the requested date
    allocation_exists = await is_vehicle_allocated(request.vehicle_id, request.allocation_date, exclude_allocation_id=allocation_id)
    if allocation_exists:
        raise HTTPException(status_code=400, detail="Vehicle already allocated for the new date.")

    # Perform the update
    update_result = await db["allocations"].update_one(
        {"id": allocation_id},
        {"$set": {
            "vehicle_id": request.vehicle_id,
            "allocation_date": request.allocation_date
        }}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update allocation.")

    # Fetch and return the updated allocation
    updated_allocation = await db["allocations"].find_one({"id": allocation_id})
    return allocation(**updated_allocation)



@router.delete("/delete_allocation/{allocation_id}")
async def delete_allocation(allocation_id: int):

    # Fetch the allocation from the database
    allocation = await db["allocations"].find_one({"id": allocation_id})
    if not allocation:
        raise HTTPException(status_code=404, detail=f"Allocation with ID {allocation_id} not found.")

    # Check if the allocation can be deleted (only future allocations can be deleted)
    allocation_date = allocation["allocation_date"]
    today = date.today()
    if allocation_date.date() <= today:
        raise HTTPException(status_code=400, detail="Cannot delete past or ongoing allocation.")

    # Perform the deletion
    await db["allocations"].delete_one({"id": allocation_id})

    return {"message": f"Allocation with ID {allocation_id} deleted successfully"}



@router.get("/allocation_history/", response_model=List[allocation])
async def get_allocation_history(filters: AllocationHistoryFilters = Depends()):
    query_filters = {}

    # Build query filters dynamically
    if filters.allocation_id:
        query_filters["id"] = filters.allocation_id

    if filters.employee_id:
        query_filters["employee_id"] = filters.employee_id

    if filters.vehicle_id:
        query_filters["vehicle_id"] = filters.vehicle_id

    if filters.allocation_date:
        try:
            # Normalize the date and filter by day
            allocation_date = filters.allocation_date.replace(tzinfo=None)
            start_of_day = allocation_date.replace(hour=0, minute=0, second=0)
            end_of_day = allocation_date.replace(hour=23, minute=59, second=59)
            query_filters["allocation_date"] = {"$gte": start_of_day, "$lte": end_of_day}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid date format.")

    # Fetch allocation history based on query filters
    allocation_history = await db["allocations"].find(query_filters).to_list(length=None)

    # Return the list of allocation objects
    return [allocation(**allocation_data) for allocation_data in allocation_history]



