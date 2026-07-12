"""
Reports & Analytics service (Screen 9).
"""
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.asset import Asset
from app.models.department import Department
from app.models.allocation import AssetAllocation
from app.models.booking import Booking
from app.models.maintenance import MaintenanceRequest
from app.models.enums import AllocationStatusEnum


def get_reports(db: Session) -> dict:
    # Most-used vs idle assets: rank by number of allocations
    utilization = (
        db.query(Asset.id, Asset.name, Asset.asset_tag, func.count(AssetAllocation.id).label("allocation_count"))
        .outerjoin(AssetAllocation, AssetAllocation.asset_id == Asset.id)
        .group_by(Asset.id)
        .order_by(func.count(AssetAllocation.id).desc())
        .all()
    )

    maintenance_by_category = (
        db.query(Asset.category_id, func.count(MaintenanceRequest.id).label("count"))
        .join(MaintenanceRequest, MaintenanceRequest.asset_id == Asset.id)
        .group_by(Asset.category_id)
        .all()
    )

    department_allocation_summary = (
        db.query(Department.id, Department.name, func.count(AssetAllocation.id).label("active_allocations"))
        .outerjoin(
            AssetAllocation,
            (AssetAllocation.department_id == Department.id)
            & (AssetAllocation.status == AllocationStatusEnum.ACTIVE),
        )
        .group_by(Department.id)
        .all()
    )

    booking_heatmap = (
        db.query(func.strftime("%H", Booking.start_time).label("hour"), func.count(Booking.id).label("count"))
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    return {
        "asset_utilization": [
            {"asset_id": r[0], "name": r[1], "asset_tag": r[2], "allocation_count": r[3]} for r in utilization
        ],
        "maintenance_frequency_by_category": [
            {"category_id": r[0], "maintenance_count": r[1]} for r in maintenance_by_category
        ],
        "department_allocation_summary": [
            {"department_id": r[0], "department_name": r[1], "active_allocations": r[2]}
            for r in department_allocation_summary
        ],
        "booking_heatmap_by_hour": [{"hour": r[0], "bookings": r[1]} for r in booking_heatmap],
    }
