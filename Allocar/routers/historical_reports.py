from fastapi import APIRouter, Depends, HTTPException
from core.db import get_database
from models import *
from datetime import date
from typing import List
from utils.db_utils import *
from schemas import *

router = APIRouter()

@router.get("/allocation_history/", response_model=List[allocation],summary="Get allocation history")
async def get_allocation_history(filters: AllocationHistoryFilters = Depends()):
    query_filters = {}
    # dynamic query filters based on request parameters
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

    allocation_history = await db["allocations"].find(query_filters).to_list(length=None)
    return [allocation(**allocation_data) for allocation_data in allocation_history]


@router.post("/vehicle_availability")
async def vehicle_availability(data: check_vehicle_availability):

    if not data.end_date:
        data.end_date = data.start_date
    
    #User input is in date format, but we need to convert it to datetime format
    start_of_day = datetime.combine(data.start_date, datetime.min.time())  # 00:00:00 on the start date
    end_of_day = datetime.combine(data.end_date, datetime.max.time())      # 23:59:59 on the end date


    conflicting_allocation = await db['allocations'].find_one({
        "vehicle_id": data.vehicle_id,
        "allocation_date": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    })

    if conflicting_allocation:
        return {"available": False}

    return {"available": True}

@router.get("/employee/allocations/{employee_id}/", response_model=List[allocation], summary="Get employee allocations")
async def get_employee_allocations(employee_id: int):

    employee_allocations = await db["allocations"].find({"employee_id": employee_id}).to_list(length=None)

    if not employee_allocations:
        raise HTTPException(status_code=404, detail="No allocations found for this employee")

    return employee_allocations

@router.get("/vehicle/allocations/{vehicle_id}/", response_model=List[allocation], summary="Get vehicle allocations")   
async def get_vehicle_allocations(vehicle_id: int):

    vehicle_allocations = await db["allocations"].find({"vehicle_id": vehicle_id}).to_list(length=None)

    if not vehicle_allocations:
        raise HTTPException(status_code=404, detail="No allocations found for this vehicle")

    return vehicle_allocations

@router.get('/employee/allocation_stats')
async def get_employee_allocation_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$employee_id",
                "total_allocations": {"$sum": 1}
            }
        }
    ]

    allocation_stats = await db["allocations"].aggregate(pipeline).to_list(None)
    return allocation_stats

