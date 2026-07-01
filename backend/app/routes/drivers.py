from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("", response_model=schemas.DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(payload: schemas.DriverCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Driver).filter(models.Driver.phone_number == payload.phone_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Driver with this phone number already exists")
    driver = models.Driver(**payload.model_dump())
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


@router.get("", response_model=list[schemas.DriverWithTrips])
def list_drivers(db: Session = Depends(get_db)):
    return (
        db.query(models.Driver)
        .options(selectinload(models.Driver.trips))
        .order_by(models.Driver.created_at.desc())
        .all()
    )


@router.get("/stats/overview", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    total_drivers = db.query(func.count(models.Driver.id)).scalar() or 0
    total_trips = db.query(func.count(models.Trip.id)).scalar() or 0
    return schemas.StatsResponse(total_drivers=total_drivers, total_trips=total_trips)


@router.get("/{driver_id}", response_model=schemas.DriverWithTrips)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = (
        db.query(models.Driver)
        .options(selectinload(models.Driver.trips))
        .filter(models.Driver.id == driver_id)
        .first()
    )
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
