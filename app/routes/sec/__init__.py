# app/routes/sec/__init__.py
from fastapi import APIRouter
from app.routes.sec import company, filing, utils

# Create a parent router for all SEC-related endpoints
router = APIRouter(prefix="/sec", tags=["SEC"])

# Include all SEC-related routers
router.include_router(company.router)
router.include_router(filing.router)
router.include_router(utils.router)
