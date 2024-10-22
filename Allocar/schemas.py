from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class employee_response(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3,max_length=30)
    email: str = Field(min_length=7,max_length=50)

class vehicle_response(BaseModel):
    id: int = Field(gt=0)
    driver_name: str = Field(min_length=3,max_length=30)
    vehicle_model: str = Field(min_length=2,max_length=30)
    
class allocation_response(BaseModel):
    id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: datetime = Field(description="Date in YYYY-MM-DD format")

