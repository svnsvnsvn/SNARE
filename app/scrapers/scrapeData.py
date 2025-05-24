# This file handles the logic for determining which scraper to use based on the URL (Craigslist, Zillow, Apartments.com).
# in order to gather listings to be scraped, you must run this file to commence the scraping process.

import argparse
import sys
import os
import json
from pathlib import Path

from spiders.scrape_craigslist import scrape_craigslist
from spiders.scrape_zillow import scrape_zillow
from spiders.scrape_apartmentscom import scrape_apartments

# from db.database import insert_listing

JSON_FILE = Path("../../data/listings.json")


def scrape_listing(url):
    if "craigslist.org" in url:
        return (scrape_craigslist(url), "craigslist_listings")
    elif "zillow.com" in url:
        return scrape_zillow(url)
    elif "apartments.com" in url:
        return scrape_apartments(url)
    else:
        print(f"Unsupported URL: {url}")
        return None


def append_listing(listing_data, source):
    """Append listing data to the appropriate section in the JSON file."""
    with open(JSON_FILE, 'r+') as f:
        data = json.load(f)

        if source not in data:
            print(f"Source {source} not recognized.")
            data[source] = []
            return
        
        # where in this particular script would i use the data['position'] variable?

        # Check if the listing already exists in the source's list
        if any(listing['listing_id'] == listing_data['listing_id'] for listing in data[source]):
            print(f"Listing {listing_data['listing_id']} already exists in {source}. Skipping.")
            return

        data[source].append(listing_data)

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
    print("hello.")

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
    scraped_data, src = scrape_listing(args.aptURL)

    if scraped_data:
        save_scraped_data(scraped_data, src)
        print("Scraped data saved to database.")
    else:
        print("No data scraped.")


if __name__ == "__main__":
    main()
