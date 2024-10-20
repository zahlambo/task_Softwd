import random
import motor.motor_asyncio
import asyncio

#initialize the MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["Allocar" ]
emp_collection = db["employees"]
veh_collection = db["vehicles"]
#alloc_collection = db["allocations"]

async def generate_random_name():
    first_name = random.choice(["John", "Jane", "Michael", "Emily", "Robert", "Maria", "David", "Linda", "Thomas", "Patricia","Shadman","James"])
    last_name = random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson","Saif","Khan"])

    return f"{first_name} {last_name}"

async def generate_random_email(name):
    email_parts = name.replace(" ", ".").lower().split(".")
    username = ".".join(email_parts[:2]) + str(random.randint(100, 999))
    domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])

    return f"{username}@{domain}"

async def generate_employee_data(num_employees):
    for i in range(num_employees):
        id = i + 1
        name = await generate_random_name()
        email = await generate_random_email(name)

        # Create a document to insert
        employee_doc = {
            "id": id,
            "name": name,
            "email": email
        }

        # Insert the document into the collection
        await emp_collection.insert_one(employee_doc)

async def generate_vehicle(num_vehicles):
    for i in range(num_vehicles):
        id = i + 1
        driver_name = await generate_random_name()
        vehicle_model = random.choice(["Toyota", "Nissan", "Ford", "Chevrolet", "Kia", "Hyundai", "Honda", "BMW", "Mercedes-Benz", "Audi"])
        
        # Create a document to insert
        vehicle_doc = {
            "id": id,
            "driver_name": driver_name,
            "vehicle_model": vehicle_model
        }

        # Insert the document into the collection
        await veh_collection.insert_one(vehicle_doc)

# Run the async function
async def main():
    await generate_employee_data(1000)
    print("Inserted 1000 employee records.")
    await generate_vehicle(1000)
    print("Inserted 1000 vehicle records.")

# Start the async event loop
if __name__ == "__main__":
    asyncio.run(main())
