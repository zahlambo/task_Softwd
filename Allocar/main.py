from fastapi import FastAPI, HTTPException,Query, Depends
#from typing import List
from db import get_database
from models import *
from datetime import date,datetime
from typing import List
from routers import allocar

app = FastAPI()
db=get_database()
app.include_router(allocar.router)

