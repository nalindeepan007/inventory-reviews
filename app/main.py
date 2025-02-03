from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import createDbSchema, shutdownDatabase

from app.routers import reviews
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespanPlan(app: FastAPI):
    # Startup: Create database schema
    await createDbSchema()
    yield
    # Shutdown: Close database connections
    await shutdownDatabase()

app = FastAPI(title="inventory reviews Service", lifespan=lifespanPlan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(reviews.router, prefix="/reviews", tags=["Reviews, trends"])

@app.get("/")
def read_root():
    return {"message": "🚀 inventory-reviews ⚙  Nalin Deepan"}
