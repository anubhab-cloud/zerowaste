import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .database import connect_to_mongo, close_mongo_connection
from .routers import (
    auth_router,
    listings_router,
    requests_router,
    donations_router,
    contact_router,
    stats_router,
    uploads_router
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zerowaste")

# Lifespan context manager for database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up ZeroWasteByte Backend...")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    try:
        await connect_to_mongo()
    except Exception as e:
        logger.error("Error connecting to MongoDB: %s", e)
    yield
    # Shutdown
    logger.info("Shutting down ZeroWasteByte Backend...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.APP_NAME,
    description="Full-stack FastAPI backend with MongoDB for ZeroWasteByte surplus food rescue platform.",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(listings_router)
app.include_router(requests_router)
app.include_router(donations_router)
app.include_router(contact_router)
app.include_router(stats_router)
app.include_router(uploads_router)

# Mount uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Root directory for serving images and index.html
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "database": "MongoDB connected"
    }

# Serve root index.html
@app.get("/")
async def serve_index():
    index_file = os.path.join(ROOT_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "ZeroWasteByte API running."}

# Mount static files in root (images like 11.jpg, 12.jpeg, etc.)
app.mount("/", StaticFiles(directory=ROOT_DIR, html=True), name="root_static")
