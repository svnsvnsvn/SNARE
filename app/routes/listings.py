# API endpoints (routers)
# The logic for scraping, detecting, etc.

from fastapi import APIRouter, HTTPException
from app.models.listing import ListingRequest
from ml.anomaly_detection import detect_anomalies, save_new_listing  # Import anomaly detection logic
from app.utils.UserScraping import scrapeListing
from ml.retrain import retrain_if_needed

router = APIRouter()
print("Starting...")

@router.post("/check_listing")
async def check_listing(request: ListingRequest):  # Expecting the body to be parsed into a ListingRequest object
    print("Checking...")
    try:
        # Step 1: Scrape the listing data from the URL
        listing_data = scrapeListing(request.url)

        print("\nDone scraping. Now Detecting anomalies.")

        # Step 2: Detect anomalies in the scraped data
        anomalies = detect_anomalies(listing_data)

        # Step 3: Save the listing for retraining purposes
        save_new_listing(listing_data)

        # Step 4: Call retrain_if_needed to check if it's time to retrain the model
        retrain_if_needed()

        # Step 5: Return whether the listing is suspicious
        is_suspicious = len(anomalies) > 0  # True if anomalies were found
        
        return {"url": request.url, "is_suspicious": is_suspicious}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

