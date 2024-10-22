from fastapi import FastAPI
from core.db import get_database
from models import *
from routers import allocar

app = FastAPI(title="Allocar",description="This is a api for allocating vehicles to employees.")
db=get_database()
app.include_router(allocar.router)
