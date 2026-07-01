from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import drivers, google_forms, trips

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Driver Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(trips.router, prefix="/api")
app.include_router(drivers.router, prefix="/api")
app.include_router(google_forms.router, prefix="/api")
