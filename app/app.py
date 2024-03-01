
from fastapi import FastAPI

app = FastAPI(
    title="spot_gab_api",
    description="API for spot_gab_app",
    verion="0.1.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]
)