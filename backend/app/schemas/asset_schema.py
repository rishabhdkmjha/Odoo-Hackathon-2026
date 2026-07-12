from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import AssetStatusEnum, AssetConditionEnum


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    category_id: int
    department_id: Optional[int] = None
    serial_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[float] = None
    condition: AssetConditionEnum = AssetConditionEnum.NEW
    location: Optional[str] = None
    is_bookable: bool = False
    photo_url: Optional[str] = None
    document_url: Optional[str] = None


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    department_id: Optional[int] = None
    serial_number: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[float] = None
    condition: Optional[AssetConditionEnum] = None
    location: Optional[str] = None
    is_bookable: Optional[bool] = None
    status: Optional[AssetStatusEnum] = None
    photo_url: Optional[str] = None
    document_url: Optional[str] = None


class AssetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    asset_tag: str
    serial_number: Optional[str] = None
    qr_code: Optional[str] = None
    category_id: int
    department_id: Optional[int] = None
    acquisition_date: Optional[date] = None
    acquisition_cost: Optional[float] = None
    condition: AssetConditionEnum
    location: Optional[str] = None
    status: AssetStatusEnum
    is_bookable: bool
    photo_url: Optional[str] = None
    document_url: Optional[str] = None
    created_at: datetime
