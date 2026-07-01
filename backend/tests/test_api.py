import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_create_driver_and_trip_and_stats():
    driver = client.post(
        "/api/drivers",
        json={"phone_number": "+380978600618", "name": "Driver One"},
    )
    assert driver.status_code == 201
    driver_id = driver.json()["id"]

    trip = client.post(
        "/api/trips",
        json={
            "driver_id": driver_id,
            "action_type": "departure",
            "time": "08:15:00",
            "odometer_km": 125000,
            "route": "Kyiv - Lviv",
        },
    )
    assert trip.status_code == 201

    stats = client.get("/api/drivers/stats/overview")
    assert stats.status_code == 200
    assert stats.json() == {"total_drivers": 1, "total_trips": 1}
