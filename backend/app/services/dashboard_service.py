"""
Dashboard KPI aggregation (Screen 2).
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.asset import Asset
from app.models.allocation import AssetAllocation
from app.models.booking import Booking
from app.models.maintenance import MaintenanceRequest
from app.models.allocation import TransferRequest
from app.models.user import User
from app.models.enums import (
    AssetStatusEnum,
    AllocationStatusEnum,
    BookingStatusEnum,
    MaintenanceStatusEnum,
    RoleEnum,
)


def get_dashboard_data(db: Session, current_user: User) -> dict:
    today = datetime.now(timezone.utc).date()
    now = datetime.now(timezone.utc)

    assets_available = db.query(func.count(Asset.id)).filter(Asset.status == AssetStatusEnum.AVAILABLE).scalar()
    assets_allocated = db.query(func.count(Asset.id)).filter(Asset.status == AssetStatusEnum.ALLOCATED).scalar()

    maintenance_today = (
        db.query(func.count(MaintenanceRequest.id))
        .filter(func.date(MaintenanceRequest.created_at) == today)
        .scalar()
    )

    active_bookings = (
        db.query(func.count(Booking.id))
        .filter(Booking.status.in_([BookingStatusEnum.UPCOMING, BookingStatusEnum.ONGOING]))
        .scalar()
    )

    pending_transfers = (
        db.query(func.count(TransferRequest.id)).filter(TransferRequest.status == "requested").scalar()
    )

    upcoming_returns = (
        db.query(func.count(AssetAllocation.id))
        .filter(
            AssetAllocation.status == AllocationStatusEnum.ACTIVE,
            AssetAllocation.expected_return_date.isnot(None),
            AssetAllocation.expected_return_date >= today,
        )
        .scalar()
    )

    overdue_returns_q = db.query(AssetAllocation).filter(
        AssetAllocation.status == AllocationStatusEnum.ACTIVE,
        AssetAllocation.expected_return_date.isnot(None),
        AssetAllocation.expected_return_date < today,
    )
    overdue_returns = overdue_returns_q.count()

    overdue_bookings = (
        db.query(func.count(Booking.id))
        .filter(Booking.status == BookingStatusEnum.UPCOMING, Booking.end_time < now)
        .scalar()
    )

    overdue_maintenance = (
        db.query(func.count(MaintenanceRequest.id))
        .filter(
            MaintenanceRequest.status.in_(
                [MaintenanceStatusEnum.PENDING, MaintenanceStatusEnum.APPROVED,
                 MaintenanceStatusEnum.TECHNICIAN_ASSIGNED, MaintenanceStatusEnum.IN_PROGRESS]
            )
        )
        .scalar()
    )

    # Scope "my view" data for Employee / Department Head roles
    my_allocations = None
    if current_user.role == RoleEnum.EMPLOYEE:
        my_allocations = (
            db.query(func.count(AssetAllocation.id))
            .filter(
                AssetAllocation.employee_id == current_user.id,
                AssetAllocation.status == AllocationStatusEnum.ACTIVE,
            )
            .scalar()
        )

    return {
        "kpis": {
            "assets_available": assets_available or 0,
            "assets_allocated": assets_allocated or 0,
            "maintenance_today": maintenance_today or 0,
            "active_bookings": active_bookings or 0,
            "pending_transfers": pending_transfers or 0,
            "upcoming_returns": upcoming_returns or 0,
        },
        "overdue": {
            "overdue_returns_count": overdue_returns or 0,
            "overdue_returns": [
                {
                    "allocation_id": a.id,
                    "asset_id": a.asset_id,
                    "employee_id": a.employee_id,
                    "expected_return_date": a.expected_return_date,
                }
                for a in overdue_returns_q.all()
            ],
            "overdue_bookings_count": overdue_bookings or 0,
            "overdue_maintenance_count": overdue_maintenance or 0,
        },
        "my_active_allocations": my_allocations,
    }
