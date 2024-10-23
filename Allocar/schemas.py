from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,date
from typing import Optional

class employee(BaseModel):
    employee_id: Optional[int] = Field(None, gt=0,description="Unique identifier for the employee, must be a positive integer.")
    name: str = Field(min_length=3, max_length=30,description="Name of the employee, must be between 3 and 30 characters.")
    email: EmailStr = Field(min_length=7, max_length=50,description="Valid email address of the employee, unique and between 7 and 50 characters.")
    department: str = Field(min_length=2, max_length=30,description="Department the employee belongs to, must be between 2 and 30 characters.")
    date_joined: datetime = Field(description="Date the employee joined the company.")
class add_employee(employee):
    pass



class vehicle(BaseModel):
    vehicle_id: Optional[int] = Field(None, gt=0,description="Unique identifier for the vehicle, must be a positive integer.")
    driver_name: str = Field(min_length=3, max_length=30,description="Name of the driver assigned to the vehicle, must be between 3 and 30 characters.")
    vehicle_model: str = Field(min_length=2, max_length=30,description="Model of the vehicle, must be between 2 and 30 characters.")
    license_plate: str = Field(min_length=10, max_length=30,description="License plate of the vehicle, must be between 10 and 30 characters.")

class allocation(BaseModel):
    allocation_id: int = Field(gt=0,description="Unique identifier for the allocation, must be a positive integer.")
    employee_id: int = Field(gt=0,description="Unique identifier for the employee, must be a positive integer.")
    vehicle_id: int = Field(gt=0,description="Unique identifier for the vehicle, must be a positive integer.")
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

class allocation_request(BaseModel):
    employee_id: int = Field(gt=0,description="Unique identifier for the employee, must be a positive integer.")
    vehicle_id: int = Field(gt=0,description="Unique identifier for the vehicle, must be a positive integer.")
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format, including time if applicable")

class allocation_history_filters(BaseModel):
    allocation_id: Optional[int] = Field(None, description="Filter by Allocation ID")
    employee_id: Optional[int] = Field(None, description="Filter by Employee ID")
    vehicle_id: Optional[int] = Field(None, description="Filter by Vehicle ID")
    allocation_date: Optional[datetime] = Field(None, description="Date in YYYY-MM-DD format, including time if applicable")
