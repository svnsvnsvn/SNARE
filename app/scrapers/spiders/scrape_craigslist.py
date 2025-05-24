from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from UserScraping import scrapeListing
from tqdm import tqdm  # Import tqdm for progress tracking

def init_driver():
    """
    Initialize the Safari WebDriver and ensure it closes properly.
    """
    driver = None
    try:
        driver = webdriver.Safari()
    except Exception as e:
        print(f"Error initializing Safari WebDriver: {e}")
    return driver

def get_listing_links(driver):
    """
    Extract individual listing URLs from the current page.
    """
    time.sleep(5)  # Optional: Adjust sleep time if the page loads slower

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the <a> tags within 'gallery-card' divs
    div_containers = soup.find_all('div', class_='gallery-card')
    
    # Extract the <a> tag inside each 'gallery-card' div
    listing_links = []
    for div in div_containers:
        a_tag = div.find('a', class_='cl-app-anchor text-only posting-title')
        if a_tag:
            listing_links.append(a_tag['href'])
    
    return listing_links

def click_next_page(driver):
    """
    Click the 'next' button to go to the next page. 
    Returns True if there is a next page, False if no next page is found.
    """
    try:
        # Wait for the next button to become clickable and click it
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "bd-button cl-next-page icon-only"))
        )
        next_button.click()
        print("Next Button Found.")
        return True
    except Exception as e:
        print("No more pages found or error clicking next:", e)
        return False

def scrape_craigslist(craigslist_search_url, max_listings=5000, save_interval=500):
    """
    Scrapes a Craigslist search page and follows pagination links to collect up to `max_listings` listings.
    Periodically saves progress every `save_interval` listings.
    """
    print(f"Scraping Craigslist URL: {craigslist_search_url}")

    driver = init_driver()  # Initialize the WebDriver once at the start
    driver.get(craigslist_search_url)  # Load the first search page

    all_listings_data = []
    total_scraped = 0  # Counter to track total scraped listings

    # Create a tqdm progress bar with a target of max_listings
    with tqdm(total=max_listings, desc="Scraping Progress", unit="listing") as pbar:

        # Start scraping and handle multi-page navigation
        while total_scraped < max_listings:
            # Step 1: Get all the listing links from the current page
            listing_links = get_listing_links(driver)
            
            if not listing_links:
                print("No listings found on the page.")
                break
            
            for link in listing_links:
                # Stop if we reach the max_listings limit
                if total_scraped >= max_listings:
                    break

                print(f"Scraping listing URL: {link}")

                # Call UserScraping function to scrape the individual listing
                data = scrapeListing(link)

                if data:
                    print(f"Successfully scraped data: {data}")
                    all_listings_data.append(data)
                    total_scraped += 1  # Increment the count of total listings scraped

                    # Update the tqdm progress bar
                    pbar.update(1)
                else:
                    print(f"Failed to scrape data for listing: {link}")
            
            # Step 2: Attempt to go to the next page, break if there is no next page
            if not click_next_page(driver):
                print("No more pages to scrape.")
                break

            # Optionally: Wait a bit before scraping the next page to avoid being flagged as a bot
            time.sleep(3)

    driver.quit()  # Close the Selenium browser session when done

    print(f"Scraped {len(all_listings_data)} listings.")
    return all_listings_data
