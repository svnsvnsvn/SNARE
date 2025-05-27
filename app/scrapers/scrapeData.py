# This file handles the logic for determining which scraper to use based on the URL (Craigslist, Zillow, Apartments.com).

import argparse
import json
from pathlib import Path

from spiders.spider_craigslist import scrape_craigslist
from spiders.spider_zillow import scrape_zillow_search
from app.scrapers.extractFeatures import extractFeatures

# from db.database import insert_listing

JSON_FILE = Path("data/listings.json")


def scrape_listing(url):
    """
    Smart function that handles both individual listings and search URLs
    """
    print(f"Processing URL: {url}")
    
    # Detect URL type and scrape accordingly
    if "/search/" in url and 'gallery' in url:
        print("Detected Craigslist search URL")
        scraped_data = scrape_craigslist(url, max_listings=2000)
        
    elif "/homes/" in url or "/apartments/" in url and ("zillow.com" in url):

        print("Detected Zillow search URL") 
        scraped_data = scrape_zillow_search(url, max_listings=2000)
        
    elif "zillow.com" in url:
        print("Detected individual Zillow listing")
        data = extractFeatures(url)  # Will use ScraperAPI automatically
        scraped_data = [data] if data else None
        
    elif "craigslist.org" in url:
        print("Detected individual Craigslist listing")
        data = extractFeatures(url)
        scraped_data = [data] if data else None
        
    elif "apartments.com" in url:
        print("Detected Apartments.com listing")
        data = extractFeatures(url)
        scraped_data = [data] if data else None
        
    else:
        print(f"Unknown URL type, trying extractFeatures: {url}")
        data = extractFeatures(url)
        scraped_data = [data] if data else None
    
    # Process the scraped data
    if scraped_data and len(scraped_data) > 0:
        # Get source from first item
        first_item_source = scraped_data[0]["source"]
        
        source_map = {
            "craigslist": "craigslist_listings",
            "zillow": "zillow_listings", 
            "apartments_com": "apartments_listings"
        }
        
        return (scraped_data, source_map.get(first_item_source, "unknown"))
    
    else:
        print("No data scraped or scraping failed")
        return None
        
def append_listing(listing_data, source):
    """Append listing data to the appropriate section in the JSON file."""
    # Check if listing_id is None or empty
    if not listing_data.get('listing_id'):
        print(f"Warning: Listing has no ID. Skipping to prevent duplicates.")
        print(f"  - URL: {listing_data.get('url')}")
        print(f"  - Name: {listing_data.get('listing_name')}")
        return
    
    with open(JSON_FILE, 'r+') as f:
        data = json.load(f)

        if source not in data:
            print(f"Source {source} not recognized. Creating new category.")
            data[source] = []
        
        # Check if the listing already exists in the source's list
        if any(listing['listing_id'] == listing_data['listing_id'] for listing in data[source]):
            print(f"Listing {listing_data['listing_id']} already exists in {source}. Skipping.")
            return

        data[source].append(listing_data)
        print(f"✓ Added listing {listing_data['listing_id']} to {source}")

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def save_scraped_data(scraped_data, src):
    """Insert the scraped data into the database."""
    if scraped_data:
        for listing in scraped_data:
            # insert_listing(listing, src)
            append_listing(listing, src)
        
def main():
    print("Welcome to the SNARE Scraper.")

    parser = argparse.ArgumentParser(
        prog="scrapeData",
        description="This program scrapes apartment listing information from Craigslist, Zillow, and Appartments.com and stores relevant listing data in a database for model training.",
    )

    parser.add_argument(
        "--aptURL",
        type=str,
        required=True,
        help="The URL to be scraped from. Should be from either Zillow, Apartments.com, or Craigslist.",
    )

    args = parser.parse_args()

    result = scrape_listing(args.aptURL) 
    
    if result:  
        scraped_data, src = result  
        save_scraped_data(scraped_data, src)
        print("Scraped data saved to database.")
    else:
        print("No data scraped.")



if __name__ == "__main__":
    main()

