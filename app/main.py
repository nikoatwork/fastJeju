from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from app.routes import api, sec  # Added the sec router
from app.routes.sec import router as sec_router


# Create FastAPI app
app = FastAPI(
    title="FastJeju API",
    description="A FastAPI example with pydantic and pandas",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api.router)
app.include_router(sec_router)  # Added the SEC router

@app.get("/")
async def root():
    return {"message": "Welcome to FastJeju API. Go to /docs for documentation."}
