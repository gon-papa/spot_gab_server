
from fastapi import FastAPI

app = FastAPI(
    title="now_go_api",
    description="API for now_go_api",
    verion="0.1.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]
)