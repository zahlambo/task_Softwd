from fastapi import FastAPI
from core.db import get_database
from models import *
from routers import allocar, historical_reports,hrm

app = FastAPI(title="Allocar",description="This is a api for allocating vehicles to employees.")
db=get_database()
app.include_router(allocar.router)
app.include_router(historical_reports.router)
app.include_router(hrm.router)


#db.employees.createIndex({ email: 1 }, { unique: true })
