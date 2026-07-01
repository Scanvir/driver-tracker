from datetime import datetime, time as dt_time
from typing import Optional
from pydantic import BaseModel, Field
from .models import ActionType


class DriverBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=20)
    name: str = Field(default="Driver", min_length=1, max_length=120)


class DriverCreate(DriverBase):
    pass


class DriverResponse(DriverBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TripBase(BaseModel):
    action_type: ActionType
    time: dt_time
    odometer_km: int = Field(..., ge=0)
    route: str = Field(..., min_length=2, max_length=255)


class TripCreate(TripBase):
    driver_id: int


class TripUpdate(BaseModel):
    action_type: ActionType | None = None
    time: Optional[dt_time] = None
    odometer_km: int | None = Field(default=None, ge=0)
    route: str | None = Field(default=None, min_length=2, max_length=255)


class TripResponse(TripBase):
    id: int
    driver_id: int
    source: str
    created_at: datetime

    class Config:
        from_attributes = True


class DriverWithTrips(DriverResponse):
    trips: list[TripResponse] = []


class StatsResponse(BaseModel):
    total_drivers: int
    total_trips: int


class GoogleSyncResponse(BaseModel):
    imported_rows: int
    skipped_rows: int
