# models.py
from pydantic import BaseModel,Field

class employee(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3,max_digits=30)
    email: str = Field(min_length=7,max_digits=50)

class vehicle(BaseModel):
    id: int = Field(gt=0)
    driver_name: str = Field(min_length=3,max_digits=30)
    vehicle_model: str = Field(min_length=2,max_digits=30)
    
class allocation(BaseModel):
    id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    allocation_date: str = Field(min_length=10,max_digits=10)


