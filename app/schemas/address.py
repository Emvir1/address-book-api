from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Label or contact name for this address")
    street: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=255)
    state: str | None = Field(None, max_length=255)
    country: str = Field(..., min_length=1, max_length=255)
    postal_code: str | None = Field(None, max_length=20)
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")

    @field_validator("name", "street", "city", "country", mode="before")
    @classmethod
    def strip_and_reject_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field must not be blank or whitespace only")
        return stripped


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    street: str | None = Field(None, min_length=1, max_length=500)
    city: str | None = Field(None, min_length=1, max_length=255)
    state: str | None = Field(None, max_length=255)
    country: str | None = Field(None, min_length=1, max_length=255)
    postal_code: str | None = Field(None, max_length=20)
    latitude: float | None = Field(None, ge=-90.0, le=90.0)
    longitude: float | None = Field(None, ge=-180.0, le=180.0)

    @field_validator("name", "street", "city", "country", mode="before")
    @classmethod
    def strip_and_reject_blank(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field must not be blank or whitespace only")
        return stripped


class AddressResponse(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NearbyQuery(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Center point latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Center point longitude")
    distance_km: float = Field(..., gt=0, le=20_000, description="Search radius in kilometres")
