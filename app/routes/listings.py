# API endpoints (routers)
# The logic for scraping, detecting, etc.
from fastapi import APIRouter, HTTPException
from app.models.listing import ListingRequest
from app.scrapers.scrapeData import scrape_listing, save_scraped_data
from app.scrapers.extractFeatures import extractFeatures
from ml.anomaly_detector import SNAREAnomalyDetector

router = APIRouter()
print("Starting...")

# Initialize the anomaly detector once when the module loads
try:
    anomaly_detector = SNAREAnomalyDetector()
    print("SNARE anomaly detector initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize anomaly detector: {e}")
    anomaly_detector = None

@router.post("/check_listing")
async def check_listing(request: ListingRequest):  
    print("Checking listing...")
    try:
        # Step 1: Scrape the listing data from the URL
        listing_list, source = scrape_listing(request.url)
        listing_data = listing_list[0] if listing_list else {}
        
        save_scraped_data(listing_list, source)
        print("\nScraped data saved to database")
        
        # Step 2: Detect anomalies in the scraped data using trained models
        anomaly_results = {}
        if anomaly_detector and listing_data:
            print("Analyzing listing for anomalies...")
            anomaly_results = anomaly_detector.detect_anomaly(listing_data)
            is_suspicious = anomaly_results.get("is_suspicious", False)
            print(f"Anomaly detection complete. Is suspicious: {is_suspicious}")
        else:
            # Fallback if detector not available
            is_suspicious = False
            anomaly_results = {
                "is_suspicious": False,
                "confidence_score": 0.0,
                "anomaly_score": 0.0,
                "note": "Anomaly detector not available"
            }
                
        return {
            "url": request.url, 
            "is_suspicious": is_suspicious,
            "name": listing_data.get("listing_name", "Unknown") if listing_data else "Unknown",
            "confidence_score": anomaly_results.get("confidence_score", 0.0),
            "anomaly_score": anomaly_results.get("anomaly_score", 0.0),
            "analysis": anomaly_results.get("feature_analysis", {}),
            "model_predictions": anomaly_results.get("model_predictions", {}),
            "scraped_data": listing_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check_manual_listing")
async def check_manual_listing(listing_data: dict):
    """Analyze manually entered listing data for anomalies."""
    print("Checking manually entered listing...")
    try:
        # Step 1: Process the manual listing data
        print(f"Received manual listing: {listing_data.get('listing_name', 'Unknown')}")
        
        # Save to database if desired (optional)
        # save_manual_listing(listing_data)
        
        # Step 2: Detect anomalies in the manual data using trained models
        anomaly_results = {}
        if anomaly_detector and listing_data:
            print("Analyzing manual listing for anomalies...")
            anomaly_results = anomaly_detector.detect_anomaly(listing_data)
            is_suspicious = anomaly_results.get("is_suspicious", False)
            print(f"Manual anomaly detection complete. Is suspicious: {is_suspicious}")
        else:
            # Fallback if detector not available
            is_suspicious = False
            anomaly_results = {
                "is_suspicious": False,
                "confidence_score": 0.0,
                "anomaly_score": 0.0,
                "note": "Anomaly detector not available"
            }
                
        return {
            "url": "manual_entry", 
            "is_suspicious": is_suspicious,
            "name": listing_data.get("listing_name", "Unknown"),
            "confidence_score": anomaly_results.get("confidence_score", 0.0),
            "anomaly_score": anomaly_results.get("anomaly_score", 0.0),
            "analysis": anomaly_results.get("feature_analysis", {}),
            "model_predictions": anomaly_results.get("model_predictions", {}),
            "scraped_data": listing_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model_info")
async def get_model_info():
    """Get information about the loaded anomaly detection models."""
    try:
        if anomaly_detector:
            return anomaly_detector.get_model_info()
        else:
            return {
                "error": "Anomaly detector not available",
                "models_loaded": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

