from fastapi import FastAPI
from app.routes.listings import router as listings_router

app = FastAPI()

# Include listings routes
app.include_router(listings_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to SNARE WEB API: Scam Network Anomaly Recognition Engine - Web-based Evaluation Bot"}
