from datetime import datetime, time
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from .database import Base


class ActionType(str, enum.Enum):
    departure = "departure"
    arrival = "arrival"
    transfer = "transfer"


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), default="Driver")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="driver", cascade="all,delete")


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), index=True)
    action_type: Mapped[ActionType] = mapped_column(Enum(ActionType), index=True)
    time: Mapped[time] = mapped_column(Time)
    odometer_km: Mapped[int] = mapped_column(Integer)
    route: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(40), default="manual")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    driver: Mapped[Driver] = relationship("Driver", back_populates="trips")
