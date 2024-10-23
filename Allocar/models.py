from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,date
from typing import Optional

class Employee(BaseModel):
    employee_id: Optional[int] = Field(None, gt=0)
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=7, max_length=50)
    department: str = Field(min_length=2, max_length=30)

class AddEmployee(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=7, max_length=50)
    department: str = Field(min_length=2, max_length=30)

class Vehicle(BaseModel):
    vehicle_id: Optional[int] = Field(None, gt=0)
    driver_name: str = Field(min_length=3, max_length=30)
    vehicle_model: str = Field(min_length=2, max_length=30)

class AddVehicle(BaseModel):
    driver_name: str = Field(min_length=3, max_length=30)
    vehicle_model: str = Field(min_length=2, max_length=30)

class CheckVehicleAvailability (BaseModel):
    vehicle_id: int = Field(gt=0)
    start_date: date = Field(description="Date in YYYY-MM-DD format, including time if applicable")
    end_date: Optional[date] = Field(None, description="Date in YYYY-MM-DD format, including time if applicable")

class Allocation(BaseModel):
    allocation_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

class AllocationRequest(BaseModel):
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

class AllocationHistoryFilters(BaseModel):
    allocation_id: Optional[int] = Field(None, description="Filter by Allocation ID")
    employee_id: Optional[int] = Field(None, description="Filter by Employee ID")
    vehicle_id: Optional[int] = Field(None, description="Filter by Vehicle ID")
    allocation_date: Optional[datetime] = Field(None, description="Date in YYYY-MM-DD format, including time if applicable")

class AllocationStatsFilter(BaseModel):
    year: Optional[int] = Field(None, description="Year to filter allocations")
    month: Optional[int] = Field(None, description="Month to filter allocations (1-12)")
