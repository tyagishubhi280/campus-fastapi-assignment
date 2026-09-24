from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import events, items


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Campus Management APIs",
    description=(
        "Task 1: Campus Lost & Found API. "
        "Task 2: Campus Event Seat Reservation API."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items.router)
app.include_router(events.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Campus Management APIs are running.",
        "docs": "/docs",
    }
