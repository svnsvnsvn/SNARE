import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))  # Adjust the path to your project structure

from fastapi import FastAPI
from routes.listings import router as listings_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify domains here
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include listings routes
app.include_router(listings_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to SNARE WEB API: Scam Network Anomaly Recognition Engine - Web-based Evaluation Bot"}

