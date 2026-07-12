"""
Centralized enums for the whole application.
Kept in one place so models, schemas, and services never drift out of sync.
"""
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    ASSET_MANAGER = "asset_manager"
    DEPARTMENT_HEAD = "department_head"
    EMPLOYEE = "employee"


class UserStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class DepartmentStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class AssetStatusEnum(str, enum.Enum):
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"
    LOST = "lost"
    DISPOSED = "disposed"


class AssetConditionEnum(str, enum.Enum):
    NEW = "new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    DAMAGED = "damaged"


class AllocationStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    TRANSFER_REQUESTED = "transfer_requested"


class TransferStatusEnum(str, enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class BookingStatusEnum(str, enum.Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MaintenanceStatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TECHNICIAN_ASSIGNED = "technician_assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class MaintenancePriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationTypeEnum(str, enum.Enum):
    ASSET_ASSIGNED = "asset_assigned"
    MAINTENANCE_APPROVED = "maintenance_approved"
    MAINTENANCE_REJECTED = "maintenance_rejected"
    BOOKING_CONFIRMED = "booking_confirmed"
    BOOKING_CANCELLED = "booking_cancelled"
    BOOKING_REMINDER = "booking_reminder"
    TRANSFER_APPROVED = "transfer_approved"
    TRANSFER_REQUESTED = "transfer_requested"
    OVERDUE_RETURN = "overdue_return"
    AUDIT_DISCREPANCY = "audit_discrepancy"
