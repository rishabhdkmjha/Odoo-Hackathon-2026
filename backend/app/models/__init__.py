"""
Import every model here so that Base.metadata is fully populated
before Base.metadata.create_all(engine) is called in main.py.
"""
from app.models.user import User
from app.models.department import Department
from app.models.category import AssetCategory
from app.models.asset import Asset
from app.models.allocation import AssetAllocation, TransferRequest
from app.models.booking import Booking
from app.models.maintenance import MaintenanceRequest
from app.models.notification import Notification, AuditLog

__all__ = [
    "User",
    "Department",
    "AssetCategory",
    "Asset",
    "AssetAllocation",
    "TransferRequest",
    "Booking",
    "MaintenanceRequest",
    "Notification",
    "AuditLog",
]
