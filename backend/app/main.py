"""
AssetFlow Backend - FastAPI entrypoint.
Wires up routers, CORS, DB table creation, and centralized exception handling
so every response - success or error - follows the standard envelope:
{ "success": bool, "message": str, "data": Any }
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.database import Base, engine
from app import models  # noqa: F401 - ensures all models are registered on Base.metadata
from app.routers import (
    auth_router,
    dashboard_router,
    employee_router,
    department_router,
    category_router,
    asset_router,
    allocation_router,
    transfer_router,
    booking_router,
    maintenance_router,
    notification_router,
    report_router,
)
from app.utils.response import error_response

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# --- Centralized exception handling: every error still returns the standard envelope ---

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content=error_response(str(exc.detail)))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response("Validation error", data=exc.errors()),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content=error_response("Internal server error"))


# --- Routers ---
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(employee_router.router)
app.include_router(department_router.router)
app.include_router(category_router.router)
app.include_router(asset_router.router)
app.include_router(allocation_router.router)
app.include_router(transfer_router.router)
app.include_router(booking_router.router)
app.include_router(maintenance_router.router)
app.include_router(notification_router.router)
app.include_router(report_router.router)


@app.get("/")
def health_check():
    return {"success": True, "message": "AssetFlow API is running", "data": {"status": "ok"}}
