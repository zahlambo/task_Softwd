import random
import motor.motor_asyncio
import asyncio
from datetime import datetime, timedelta,date
from pymongo.errors import DuplicateKeyError
import string

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["Allocar"]
emp_collection = db["employees"]
veh_collection = db["vehicles"]
alloc_collection = db["allocations"]  

async def generate_random_name():
    first_name = random.choice(["John", "Jane", "Michael", "Emily", "Robert", "Maria", "David", "Linda", "Thomas", "Patricia", "Shadman", "James"])
    last_name = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Saif", "Khan"])
    return f"{first_name} {last_name}"

async def generate_random_email(name):
    email_parts = name.replace(" ", ".").lower().split(".")
    username = ".".join(email_parts[:2]) + str(random.randint(100, 999))
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
    return f"{username}@{domain}"

def generate_license_plate(length=random.randint(10, 30)):
    characters = string.ascii_letters + string.digits
    license_plate = ''.join(random.choice(characters) for _ in range(length))
    return license_plate

def generate_random_date():
    delta = datetime.now() - date(2020, 1, 1) 
    random_days = random.randint(0, delta.days)
    return date(2020, 1, 1)  + timedelta(days=random_days)

async def generate_employee_data(num_employees):
    for i in range(num_employees):
        employee_id = i + 1
        name = await generate_random_name()
        department = random.choice(["HR", "Finance", "Engineering", "Sales", "Marketing"])
        date_joined = generate_random_date()

        while True:
            try:
                email = await generate_random_email(name)

                employee_doc = {
                    "employee_id": employee_id,
                    "name": name,
                    "email": email,
                    "department": department,
                    "date_joined": date_joined
                }

                await emp_collection.insert_one(employee_doc)
                break  

            except DuplicateKeyError:
                continue

async def generate_vehicle(num_vehicles):
    for i in range(num_vehicles):
        vehicle_id = i + 1
        driver_name = await generate_random_name()
        vehicle_model = random.choice(["Toyota", "Nissan", "Ford", "Chevrolet", "Kia", "Hyundai", "Honda", "BMW", "Mercedes-Benz", "Audi"])
        license_plate = generate_license_plate()

        # Create a document to insert
        vehicle_doc = {
            "vehicle_id": vehicle_id,
            "driver_name": driver_name,
            "vehicle_model": vehicle_model,
            "license_plate":license_plate
        }

        await veh_collection.insert_one(vehicle_doc)


async def is_vehicle_allocated(vehicle_id: int, allocation_date: datetime, exclude_allocation_id: int = None):
    query = {
        "vehicle_id": vehicle_id,
        "allocation_date": allocation_date
    }
    if exclude_allocation_id:
        query["allocation_id"] = {"$ne": exclude_allocation_id}  # Ensure this matches your allocation document structure
    return await db["allocations"].find_one(query)  # Await the database call


async def generate_allocation(num_allocations):
    employees = await emp_collection.find().to_list(length=None)
    vehicles = await veh_collection.find().to_list(length=None)

    for _ in range(num_allocations):
        employee = random.choice(employees)
        vehicle = random.choice(vehicles)
        # Generate a random allocation date
        allocation_date = datetime.now() + timedelta(days=random.randint(date.today().day, 30))  # Use datetime instead of date
        


        previous_allocation = await is_vehicle_allocated(vehicle["vehicle_id"], allocation_date)
        if previous_allocation:  
            print(f"Vehicle {vehicle['vehicle_id']} already allocated on {allocation_date}")
            continue

        allocation_doc = {
            "allocation_id": _ + 1,  # Use the loop index as the allocation ID
            "employee_id": employee["employee_id"],
            "vehicle_id": vehicle["vehicle_id"],
            "allocation_date": allocation_date 
        }
        await alloc_collection.insert_one(allocation_doc)

# Run the async function
async def main():
    await emp_collection.create_index("email", unique=True)
    await generate_employee_data(1000)
    await generate_vehicle(1000)
    await generate_allocation(1000)  
    print("Inserted records.")

if __name__ == "__main__":
    
    asyncio.run(main())
