from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for request validation

class ListingRequest(BaseModel):
    url: str
    address: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to SNARE WEB: Scam Network Anomaly Recognition Engine - Web-based Evaluation Bot"}

@app.post("/check_listing")
async def check_listing(request: ListingRequest):

    is_suspicious = False # This will be updated when scraping is integrated
    return {"address": request.address, "is_suspicious": is_suspicious}