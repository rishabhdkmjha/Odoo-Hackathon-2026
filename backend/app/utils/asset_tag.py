"""
Auto-generates sequential, zero-padded asset tags like AF-0001.
"""
from sqlalchemy.orm import Session

from app.models.asset import Asset


def generate_asset_tag(db: Session) -> str:
    last_asset = db.query(Asset).order_by(Asset.id.desc()).first()
    next_id = (last_asset.id + 1) if last_asset else 1
    return f"AF-{next_id:04d}"
