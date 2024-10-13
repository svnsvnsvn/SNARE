# This file handles the logic for determining which scraper to use based on the URL (Craigslist, Zillow, Apartments.com).
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from spiders.scrape_craigslist import scrape_craigslist
from spiders.scrape_zillow import scrape_zillow
from spiders.scrape_apartmentscom import scrape_apartments

# Add the project root (two directories up) to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from db.database import insert_listing

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


def save_scraped_data(scraped_data, src):
    """Insert the scraped data into the database."""
    if scraped_data:
        for listing in scraped_data:
            insert_listing(listing, src)


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
