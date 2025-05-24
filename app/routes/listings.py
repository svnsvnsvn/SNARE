# API endpoints (routers)
# The logic for scraping, detecting, etc.
from fastapi import APIRouter, HTTPException
from models.listing import ListingRequest
# from anomaly_detection import detect_anomalies  # Import anomaly detection logic
from scrapers.extractFeatures import extractFeatures 
# from app.utils.scrapeData import save_scraped_data
# from db.database import insert_listing
# from ml.retrain import retrain_if_needed

router = APIRouter()
print("Starting...")

@router.post("/check_listing")
async def check_listing(request: ListingRequest):  # Expecting the body to be parsed into a ListingRequest object
    print("Checking...")
    try:
        # Step 1: Scrape the listing data from the URL
        listing_data = extractFeatures(request.url)

        '''print(listing_data)
        
        print("\nDone scraping. Now Detecting anomalies.")

        # Step 2: Detect anomalies in the scraped data
        anomalies = detect_anomalies(listing_data)

        # Step 3: Save the listing for retraining purposes
        save_scraped_data(listing_data)

        # Step 4: Call retrain_if_needed to check if it's time to retrain the model
        retrain_if_needed()

        # Step 5: Return whether the listing is suspicious
        is_suspicious = len(anomalies) > 0  # True if anomalies were found
        
        return {"url": request.url, "is_suspicious": is_suspicious}'''
                
        # For now, just return the scraped data
        # TODO: Add anomaly detection later
        is_suspicious = False  # Placeholder
                
        return {
    "url": request.url, 
    "is_suspicious": is_suspicious,
    "name": listing_data.get("listing_name", "Unknown") if listing_data else "Unknown",
    "scraped_data": listing_data
}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrape")
async def scrape_url(url: str):
    try:
        # Step 1: Scrape the listing data from the given URL
        data = extractFeatures(url)

        print(data)
        
        if not data:
            raise HTTPException(status_code=400, detail="Could not scrape the listing")
        
        # Step 2: Save the scraped data to the database using the raw SQLite method
        try:
            # insert_listing(data)
            #TODO: FIX THIS LOGIC bc now you need the source
            return {"message": f"Listing {data.get('listing_id')} saved to the database."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Note: I feel like the second function is redundant, but I left it in for now. Why allow users to scrape a URL if they can just use the first function?
    # Maybe the first function is for checking if a listing is suspicious, while the second one is for scraping and saving to the database?
    # I think its better to keep the first for checking and scraping as well as saving to the database and the second one should be deleted. 
    # This makes sense because the first one is for checking if a listing is suspicious and the second one is for scraping and saving to the database.