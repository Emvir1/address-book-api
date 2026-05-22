import math

from geopy.distance import geodesic
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

logger = get_logger(__name__)


def create_address(db: Session, payload: AddressCreate) -> Address:
    address = Address(**payload.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    logger.info("Created address id=%d name=%r city=%r country=%r", address.id, address.name, address.city, address.country)
    return address


def get_address(db: Session, address_id: int) -> Address | None:
    address = db.get(Address, address_id)
    if address is None:
        logger.warning("Address id=%d not found", address_id)
    return address


def list_addresses(db: Session, skip: int = 0, limit: int = 100) -> list[Address]:
    addresses = db.query(Address).offset(skip).limit(limit).all()
    logger.debug("Listed %d addresses (skip=%d limit=%d)", len(addresses), skip, limit)
    return addresses


def update_address(db: Session, address_id: int, payload: AddressUpdate) -> Address | None:
    address = db.get(Address, address_id)
    if address is None:
        logger.warning("Update failed — address id=%d not found", address_id)
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    logger.info("Updated address id=%d fields=%s", address_id, list(update_data.keys()))
    return address


def delete_address(db: Session, address_id: int) -> bool:
    address = db.get(Address, address_id)
    if address is None:
        logger.warning("Delete failed — address id=%d not found", address_id)
        return False

    db.delete(address)
    db.commit()
    logger.info("Deleted address id=%d", address_id)
    return True


def get_addresses_within_distance(
    db: Session,
    center_lat: float,
    center_lon: float,
    distance_km: float,
) -> list[Address]:
    lat_delta = distance_km / 111.0
    lon_delta = distance_km / (111.0 * math.cos(math.radians(center_lat))) if abs(center_lat) < 90 else distance_km

    candidates = (
        db.query(Address)
        .filter(
            Address.latitude.between(center_lat - lat_delta, center_lat + lat_delta),
            Address.longitude.between(center_lon - lon_delta, center_lon + lon_delta),
        )
        .all()
    )

    center = (center_lat, center_lon)
    results = [
        addr for addr in candidates
        if geodesic(center, (addr.latitude, addr.longitude)).km <= distance_km
    ]

    logger.info(
        "Nearby search center=(%.4f, %.4f) radius=%.1fkm — %d/%d candidates matched",
        center_lat, center_lon, distance_km, len(results), len(candidates),
    )
    return results
