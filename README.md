# Allocar - Car Allocation

This project is a FastAPI-based vehicle allocation system for a company's employees. Employees can allocate vehicles for specific days, provided the vehicle is not already allocated for that day. The system is built with FastAPI and MongoDB, providing features such as allocation, updating, deleting, and viewing a history of allocations.

## Installation

To set up this project, you need Python 3.8+ installed on your machine, as well as MongoDB. Follow the instructions below:

### Clone the repository

```bash
git clone https://github.com/zahlambo/task_Softwd
cd allocar
```

## Install dependencies

```bash
python -m venv env
env\Scripts\activate   # On Linux:source env/bin/activate
pip install -r requirements.txt
```
## Set up the environment

Create a .env file in the project root directory. This file should contain the environment variables needed for database connections. For example:

```
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=Allocar
```
## Running the Project
To run the FastAPI application, use the following command:

```
fastapi run main
or 
uvicorn main:app --reload
```
## Generating Data
To populate your MongoDB database with sample employee and vehicle data, use the gendata.py script. 
This will generate employees, vehicles, and allocation
```
python gendata.py
```

## API Endpoints

**POST /allocate_vehicle/:** Allocate a vehicle to an employee for a specific date.

**PUT /update_allocation/{allocation_id}:** Update an existing vehicle allocation before the allocation date.

**DELETE /delete_allocation/{allocation_id}:** Delete a vehicle allocation, but only if the allocation date is in the future.

**GET /allocation_history/:** View the history of vehicle allocations with filters such as employee ID, vehicle ID, or allocation date.

## Swagger Documentation

FastAPI automatically generates Swagger documentation for your API, which can be accessed at:

```
http://127.0.0.1:8000/docs

```
## Deployment and Maintenance

**1. Containerization**
Use Docker to ensure consistency across different environments. Here’s a basic Dockerfile:
```
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

```
**2. Cloud Deployment**
You can deploy the Dockerized app to cloud platforms like AWS, Google Cloud, or Azure. Alternatively, use services like Heroku or DigitalOcean, which are simple to configure for FastAPI.

**3. Database Setup**
Ensure MongoDB is available in the cloud (e.g., MongoDB Atlas). Update the .env file with the production database URL.

### Maintenance
**1. Monitoring**
Use tools like Prometheus and Grafana for performance metrics, or ELK stack (Elasticsearch, Logstash, Kibana) for logging.

**2. Database Maintenance**
Utilize MongoDB’s features like replication and sharding for scalability. Monitor performance using MongoDB Atlas Monitoring tools.

**3. Unit Testing & CI/CD**
Create unit tests for key features and automate them with CI/CD pipelines (e.g., GitHub Actions, GitLab CI). Add integration tests for critical functionalities like vehicle allocation.

**4. Scalability**
As usage grows, scale the app horizontally by adding more containers/pods. Use a load balancer to evenly distribute traffic.

**5. Security**

* Manage sensitive data like credentials with environment variables.
* Add rate-limiting to prevent DoS attacks.
* Ensure secure communication with HTTPS and enable authentication for exposed APIs.

