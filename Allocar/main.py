from fastapi import FastAPI
from core.db import get_database
from models import *
from routers import allocar, hrm,reports,default

app = FastAPI(title="Allocar",description="This is a api for allocating vehicles to employees.")
db=get_database()
app.include_router(allocar.router)
app.include_router(reports.router)
app.include_router(hrm.router)
app.include_router(default.router)