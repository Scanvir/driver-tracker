from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=schemas.TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(payload: schemas.TripCreate, db: Session = Depends(get_db)):
    driver = db.get(models.Driver, payload.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    trip = models.Trip(**payload.model_dump(), source="manual")
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.get("", response_model=list[schemas.TripResponse])
def list_trips(db: Session = Depends(get_db)):
    return db.query(models.Trip).order_by(models.Trip.created_at.desc()).all()


@router.get("/{trip_id}", response_model=schemas.TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.get(models.Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.put("/{trip_id}", response_model=schemas.TripResponse)
def update_trip(trip_id: int, payload: schemas.TripUpdate, db: Session = Depends(get_db)):
    trip = db.get(models.Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(trip, field, value)

    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.get(models.Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return None
