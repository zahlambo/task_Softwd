# models.py
from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class employee(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3,max_length=30)
    email: str = Field(min_length=7,max_length=50)

class vehicle(BaseModel):
    id: int = Field(gt=0)
    driver_name: str = Field(min_length=3,max_length=30)
    vehicle_model: str = Field(min_length=2,max_length=30)
    
class allocation(BaseModel):
    id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format")


class AllocationRequest(BaseModel):
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format")


class AllocationHistoryFilters(BaseModel):
    employee_id: Optional[int] = Field(None, description="Filter by Employee ID")
    vehicle_id: Optional[int] = Field(None, description="Filter by Vehicle ID")
    allocation_date: Optional[datetime] = Field(None, description="Date in YYYY-MM-DD format")

