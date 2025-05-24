# This file handles the logic for determining which scraper to use based on the URL (Craigslist, Zillow, Apartments.com).
# in order to gather listings to be scraped, you must run this file to commence the scraping process.

# this file is responsible for scraping apartment listings from various websites (Craigslist, Zillow, Apartments.com) and storing the relevant data in a database. It uses argparse to handle command-line arguments and provides a clear structure for scraping and saving data.
# The script is designed to be run from the command line, and it requires a URL to be passed as an argument. It then determines which website the URL belongs to and calls the appropriate scraping function. The scraped data is then inserted into a database for further processing or analysis.
# The script is modular, allowing for easy addition of new scraping functions for other websites in the future. It also includes error handling and progress tracking during the scraping process.

import argparse
import sys
import os
import json
from pathlib import Path


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from spiders.scrape_craigslist import scrape_craigslist
from spiders.scrape_zillow import scrape_zillow
from spiders.scrape_apartmentscom import scrape_apartments

# Add the project root (two directories up) to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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
