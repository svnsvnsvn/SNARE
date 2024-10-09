# Functions for scraping Zillow, Craigslist
import requests
from bs4 import BeautifulSoup

def scrape_listing(url):

    print("Attempting to Scrape...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Example: Extract the price and bedrooms from the scraped page
    price = float(soup.find("div", class_="price").text.replace("$", "").replace(",", ""))
    bedrooms = int(soup.find("div", class_="bedrooms").text.split(" ")[0])
    
    # Return the extracted data as a dictionary
    return {
        "Price per Bedroom": price / bedrooms,
        # Add other features like bathrooms, living area, etc.
    }