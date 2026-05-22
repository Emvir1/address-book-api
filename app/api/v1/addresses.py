from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressResponse, AddressUpdate
from app.services.address_service import (
    create_address,
    delete_address,
    get_address,
    get_addresses_within_distance,
    list_addresses,
    update_address,
)

router = APIRouter(prefix="/addresses", tags=["Addresses"])
logger = get_logger(__name__)


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create(payload: AddressCreate, db: Session = Depends(get_db)) -> AddressResponse:
    logger.info("POST /addresses name=%r", payload.name)
    return create_address(db, payload)


@router.get("/", response_model=list[AddressResponse])
def list_all(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    logger.info("GET /addresses skip=%d limit=%d", skip, limit)
    return list_addresses(db, skip=skip, limit=limit)


@router.get("/nearby", response_model=list[AddressResponse])
def nearby(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Center latitude"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Center longitude"),
    distance_km: float = Query(..., gt=0, le=20_000, description="Search radius in kilometres"),
    db: Session = Depends(get_db),
) -> list[AddressResponse]:
    logger.info("GET /addresses/nearby lat=%.4f lon=%.4f radius=%.1fkm", latitude, longitude, distance_km)
    return get_addresses_within_distance(db, latitude, longitude, distance_km)


@router.get("/{address_id}", response_model=AddressResponse)
def get_one(address_id: int, db: Session = Depends(get_db)) -> AddressResponse:
    logger.info("GET /addresses/%d", address_id)
    address = get_address(db, address_id)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address {address_id} not found")
    return address


@router.patch("/{address_id}", response_model=AddressResponse)
def update(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)) -> AddressResponse:
    logger.info("PATCH /addresses/%d", address_id)
    address = update_address(db, address_id, payload)
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address {address_id} not found")
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(address_id: int, db: Session = Depends(get_db)) -> None:
    logger.info("DELETE /addresses/%d", address_id)
    deleted = delete_address(db, address_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address {address_id} not found")
