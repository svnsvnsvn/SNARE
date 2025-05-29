# API endpoints (routers)
# The logic for scraping, detecting, etc.
from fastapi import APIRouter, HTTPException
from app.models.listing import ListingRequest
from app.scrapers.scrapeData import scrape_listing, save_scraped_data
from app.scrapers.extractFeatures import extractFeatures

router = APIRouter()
print("Starting...")

@router.post("/check_listing")
async def check_listing(request: ListingRequest):  
    print("Checking listing...")
    try:
        # Step 1: Scrape the listing data from the URL
        listing_list, source = scrape_listing(request.url)
        listing_data = listing_list[0] if listing_list else {}
        
        save_scraped_data(listing_list, source)
        print("\nScraped data saved to database")
        
        '''
        print("\nDone scraping. Now Detecting anomalies.")

        # Step 2: Detect anomalies in the scraped data
        anomalies = detect_anomalies(listing_data)

        # Step 3: Call retrain_if_needed to check if it's time to retrain the model
        retrain_if_needed()
        '''
                
        # For now, just return the scraped data
        is_suspicious = False  # Placeholder
                
        return {
    "url": request.url, 
    "is_suspicious": is_suspicious,
    "name": listing_data.get("listing_name", "Unknown") if listing_data else "Unknown",
    "scraped_data": listing_data
}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

