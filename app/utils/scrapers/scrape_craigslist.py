from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from UserScraping import scrapeListing

def init_driver():
    driver = webdriver.Safari()
    return driver

def get_listing_links(search_url):
    """Use Selenium to load a Craigslist search page and extract individual listing URLs."""
    print(f"Fetching search page using Selenium: {search_url}")
    
    driver = init_driver()
    driver.get(search_url)  # Load the search page

    # Wait for the page to fully load (you may need to adjust this)
    time.sleep(5)  # Optional: Adjust sleep time if the page loads slower

    # Get the page source once content is fully loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Now find <a> tags within 'gallery-card' divs
    div_containers = soup.find_all('div', class_='gallery-card')
    
    # Extract the <a> tag inside each 'gallery-card' div
    listing_links = []
    for div in div_containers:
        a_tag = div.find('a', class_='cl-app-anchor text-only posting-title')
        if a_tag:
            listing_links.append(a_tag['href'])
    
    if listing_links:
        print(f"Found {len(listing_links)} listings.")
    else:
        print(f"No listings found on the page.")
    
    driver.quit()  # Close the Selenium browser session

    return listing_links

def scrape_craigslist(craigslist_search_url):
    """Scrapes a Craigslist search page and extracts listing data."""
    print(f"Scraping Craigslist URL: {craigslist_search_url}")
    
    # Step 1: Get all the listing links from the search page
    listing_links = get_listing_links(craigslist_search_url)
    
    all_listings_data = []
    for link in listing_links:
        print(f"Scraping listing URL: {link}")

        # Call UserScraping function to scrape the individual listing
        data = scrapeListing(link)

        if data:
            print(f"Successfully scraped data: {data}")
            all_listings_data.append(data)
        else:
            print(f"Failed to scrape data for listing: {link}")

    print(f"Scraped {len(all_listings_data)} listings.")
    return all_listings_data