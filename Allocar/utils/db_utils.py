from datetime import datetime
from core.db import get_database
from fastapi import HTTPException

db = get_database()

async def get_employee(employee_id: int):
    return await db["employees"].find_one({"id": employee_id})

async def get_vehicle(vehicle_id: int):
    return await db["vehicles"].find_one({"id": vehicle_id})

# async def is_vehicle_allocated(vehicle_id: int, allocation_date: datetime):
#     return await db["allocations"].find_one({
#         "vehicle_id": vehicle_id,
#         "allocation_date": allocation_date
#     })

async def get_allocation_by_id(allocation_id: int):
    allocation = await db["allocations"].find_one({"id": allocation_id})
    if not allocation:
        raise HTTPException(status_code=404, detail=f"Allocation with ID {allocation_id} not found.")
    return allocation

async def is_vehicle_allocated(vehicle_id: int, allocation_date: datetime, exclude_allocation_id: int = None):
    query = {
        "vehicle_id": vehicle_id,
        "allocation_date": allocation_date
    }
    if exclude_allocation_id:
        query["id"] = {"$ne": exclude_allocation_id}
    return await db["allocations"].find_one(query)

async def delete_allocation_by_id(allocation_id: int):
    await db["allocations"].delete_one({"id": allocation_id})


async def update_allocation_by_id(allocation_id: int, update_data: dict):
    return await db["allocations"].update_one(
        {"id": allocation_id},
        {"$set": update_data}
    )