import csv
import io
import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..utils import parse_hhmm

router = APIRouter(prefix="/google-forms", tags=["google-forms"])


def _get_or_create_driver(db: Session, phone: str):
    driver = db.query(models.Driver).filter(models.Driver.phone_number == phone).first()
    if not driver:
        driver = models.Driver(phone_number=phone, name=f"Driver {phone[-4:]}")
        db.add(driver)
        db.flush()
    return driver


@router.post("/sync", response_model=schemas.GoogleSyncResponse)
def sync_google_forms(db: Session = Depends(get_db)):
    sheet_csv_url = os.getenv("GOOGLE_SHEETS_CSV_URL")
    default_phone = os.getenv("DEFAULT_DRIVER_PHONE", "+380978600618")

    if not sheet_csv_url:
        raise HTTPException(status_code=400, detail="GOOGLE_SHEETS_CSV_URL is not configured")

    with httpx.Client(timeout=20) as client:
        response = client.get(sheet_csv_url)
        response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))

    imported = 0
    skipped = 0

    for row in reader:
        try:
            action_raw = (row.get("action") or row.get("Тип дій") or "").strip().lower()
            if action_raw not in {"departure", "arrival", "transfer", "виїзд", "заїзд", "переміщення"}:
                skipped += 1
                continue

            action_map = {
                "departure": models.ActionType.departure,
                "виїзд": models.ActionType.departure,
                "arrival": models.ActionType.arrival,
                "заїзд": models.ActionType.arrival,
                "transfer": models.ActionType.transfer,
                "переміщення": models.ActionType.transfer,
            }

            phone = (row.get("phone") or row.get("Номер") or default_phone).strip()
            route = (row.get("route") or row.get("Маршрут") or "").strip()
            time_value = (row.get("time") or row.get("Час") or "").strip()
            odometer_raw = (row.get("odometer") or row.get("Одометр") or "").strip()

            if not route or not time_value or not odometer_raw:
                skipped += 1
                continue

            odometer_km = int(float(odometer_raw.replace(",", ".")))
            trip_time = parse_hhmm(time_value)
            driver = _get_or_create_driver(db, phone)

            exists = (
                db.query(models.Trip)
                .filter(
                    models.Trip.driver_id == driver.id,
                    models.Trip.action_type == action_map[action_raw],
                    models.Trip.time == trip_time,
                    models.Trip.odometer_km == odometer_km,
                    models.Trip.route == route,
                )
                .first()
            )
            if exists:
                skipped += 1
                continue

            trip = models.Trip(
                driver_id=driver.id,
                action_type=action_map[action_raw],
                time=trip_time,
                odometer_km=odometer_km,
                route=route,
                source="google_forms",
            )
            db.add(trip)
            imported += 1
        except Exception:
            skipped += 1

    db.commit()
    return schemas.GoogleSyncResponse(imported_rows=imported, skipped_rows=skipped)
