from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.listings import router as listings_router
from app.config import get_settings, get_cors_config, get_api_config

# Load settings
settings = get_settings()
api_config = get_api_config()
cors_config = get_cors_config()

# Create FastAPI app with configuration
app = FastAPI(
    title=api_config["title"],
    description=api_config["description"],
    version=api_config["version"]
)

# Add CORS middleware with configuration
app.add_middleware(
    CORSMiddleware,
    **cors_config
)

# Include listings routes
app.include_router(listings_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to SNARE WEB API: Scam Network Anomaly Recognition Engine - Web-based Evaluation Bot"}

