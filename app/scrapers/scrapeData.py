# This file handles the logic for determining which scraper to use based on the URL (Craigslist, Zillow, Apartments.com).

import argparse
import json
from pathlib import Path

from spiders.spider_craigslist import scrape_craigslist
from spiders.spider_zillow import scrape_zillow_search
from app.scrapers.extractFeatures import extractFeatures

# Import database functionality
from db.database_setup import ListingsDatabase, migrate_from_json

DB = ListingsDatabase("data/listings.db")
JSON_FILE = Path("data/listings.json")  # Kept for backward compatibility


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
        print(f"Scraped {len(scraped_data)} listings from {url}")
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
        
def save_scraped_data(scraped_data, src):
    """
    Insert the scraped data into the database
    """
    if scraped_data:
        print(f"\nSaving {len(scraped_data)} listings to database...")
        
        # Ensure all listings have the correct source
        for listing in scraped_data:
            listing['source'] = src.replace('_listings', '')
        
        # Insert into database
        successful = DB.insert_multiple_listings(scraped_data)
        
        if successful > 0:
            print(f"Successfully saved {successful} listings")
            
            # Show updated stats
            stats = DB.get_stats()
            print(f"Database now has {stats['total_listings']} total listings")
        else:
            print("No listings were saved")

def show_database_summary():
    """Display database statistics"""
    stats = DB.get_stats()
    
    print("\n" + "="*50)
    print("APARTMENT LISTINGS DATABASE SUMMARY")
    print("="*50)
    
    print(f"Total Listings: {stats['total_listings']}")
    
    print(f"\nBy Source:")
    for source in stats['by_source']:
        print(f"  {source['source'].title()}: {source['count']} listings")
    
    if stats['price_stats']['price_count'] > 0:
        print(f"\nPrice Statistics:")
        print(f"  Range: ${stats['price_stats']['min_price']:,.0f} - ${stats['price_stats']['max_price']:,.0f}")
        print(f"  Average: ${stats['price_stats']['avg_price']:,.0f}")
        print(f"  Listings with prices: {stats['price_stats']['price_count']}")
    
    print(f"\nTop Cities:")
    for city in stats['top_cities'][:5]:
        print(f"  {city['city']}, {city['state']}: {city['count']} listings")
    
    print(f"\nBedroom Distribution:")
    for bedroom in stats['bedroom_distribution']:
        bed_label = "Studio" if bedroom['bedrooms'] == 0 else f"{bedroom['bedrooms']} bed"
        print(f"  {bed_label}: {bedroom['count']} listings")

def search_listings(**kwargs):
    """
    Search listings with various filters
    
    Examples:
    search_listings(city="Jacksonville", max_price=2000)
    search_listings(bedrooms=2, source="zillow")
    """
    return DB.get_listings(**kwargs)

def main():
    print("Welcome to the SNARE Scraper (Database Edition)")

    parser = argparse.ArgumentParser(
        prog="scrapeData",
        description="This program scrapes apartment listing information from Craigslist, Zillow, and Apartments.com and stores relevant listing data in a database for model training.",
    )

    parser.add_argument(
        "--aptURL",
        type=str,
        help="The URL to be scraped from. Should be from either Zillow, Apartments.com, or Craigslist.",
    )
    
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Migrate existing JSON data to database"
    )
    
    parser.add_argument(
        "--stats",
        action="store_true", 
        help="Show database statistics"
    )
    
    parser.add_argument(
        "--search",
        type=str,
        help="Search listings (e.g., 'city=Jacksonville&bedrooms=2')"
    )

    args = parser.parse_args()
    
    # Handle migration
    if args.migrate:
        json_path = "data/listings.json"
        if Path(json_path).exists():
            print("Starting migration from JSON to database...")
            success = migrate_from_json(json_path)
            if success:
                print("Migration completed successfully!")
                show_database_summary()
            else:
                print("Migration failed!")
        else:
            print("JSON file not found at data/listings.json")
        return
    
    # Handle stats
    if args.stats:
        show_database_summary()
        return
    
    # Handle search
    if args.search:
        search_params = {}
        for param in args.search.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # Try to convert to appropriate type
                if key in ['bedrooms', 'limit']:
                    search_params[key] = int(value)
                elif key in ['min_price', 'max_price']:
                    search_params[key] = float(value)
                else:
                    search_params[key] = value
        
        results = search_listings(**search_params)
        print(f"\n🔍 Found {len(results)} listings:")
        for listing in results[:10]:  # Show first 10
            price_str = f"${listing['price']:,.0f}" if listing['price'] else "No price"
            bed_str = f"{listing['bedrooms']}BR" if listing['bedrooms'] else "?BR"
            print(f"  {listing['listing_name']} - {bed_str} - {price_str} ({listing['source']})")
        
        if len(results) > 10:
            print(f"  ... and {len(results) - 10} more")
        return
    
    # Handle URL scraping (original functionality)
    if args.aptURL:
        result = scrape_listing(args.aptURL)
        
        if result:  
            scraped_data, src = result  
            save_scraped_data(scraped_data, src)
            print("\nScraped data saved to database")
            show_database_summary()
        else:
            print("No data scraped")
    else:
        # Show help and current stats if no arguments
        parser.print_help()
        print("\n" + "="*50)
        show_database_summary()

if __name__ == "__main__":
    main()

