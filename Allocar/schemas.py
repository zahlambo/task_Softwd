from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,date
from typing import Optional

# Employee Schema
class employee(BaseModel):
    employee_id: Optional[int] = Field(None, gt=0)
    name: str = Field(min_length=3, max_length=30)
    email: EmailStr = Field(min_length=7, max_length=50)
    department: str = Field(min_length=2, max_length=30)

# Vehicle Schema
class vehicle(BaseModel):
    vehicle_id: Optional[int] = Field(None, gt=0)
    driver_name: str = Field(min_length=3, max_length=30)
    vehicle_model: str = Field(min_length=2, max_length=30)

# Allocation Schema
class allocation(BaseModel):
    allocation_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

# Allocation Request Schema
class allocation_request(BaseModel):
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

# Allocation History Filters Schema
class allocation_history_filters(BaseModel):
    allocation_id: Optional[int] = Field(None, description="Filter by Allocation ID")
    employee_id: Optional[int] = Field(None, description="Filter by Employee ID")
    vehicle_id: Optional[int] = Field(None, description="Filter by Vehicle ID")
    allocation_date: Optional[datetime] = Field(None, description="Date in YYYY-MM-DD format, including time if applicable")
