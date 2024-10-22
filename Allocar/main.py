from fastapi import FastAPI
from Allocar.core.db import get_database
from models import *
from routers import allocar

app = FastAPI()
db=get_database()
app.include_router(allocar.router)

