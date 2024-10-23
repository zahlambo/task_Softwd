from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Welcome to Car Allocation System</title>
        </head>
        <body>
            <h1>Welcome to the Car Allocation System API</h1>
            <p>Please go to <a href="/docs">/docs</a> to test the API.</p>
        </body>
    </html>
    """