import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # may need to add this to other files to ensure that theyre treated as packages which is important because we are using relative imports and that means that the __init__.py files are not being recognized becaue they are not in the same directory as the file that is being run. 
# the this in question is the __init__.py file in the app directory. it is used to mark a directory as a package because it contains the __init__.py file. otherwise, the directory is not treated as a package and the __init__.py file is not executed.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from extractFeatures import extractFeatures
from tqdm import tqdm  

def init_driver():
    """
    Initialize the Safari WebDriver and ensure it closes properly.
    """
    driver = None
    try:
        driver = webdriver.Safari()
        print("Safari WebDriver initialized.")
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
    
    print(f"Found {len(div_containers)} listing containers on the page.")
    
    
    # Extract the <a> tag inside each 'gallery-card' div
    listing_links = []
    for div in div_containers:
        # a_tag = div.find('a', class_='cl-app-anchor text-only posting-title') # need a better way to find this and identify the listing
        # instead of using the class name, we can use the href attribute to find the link
        a_tag = div.find('a', href=True)  # find the first <a> tag with an href attribute
        if a_tag:
            listing_links.append(a_tag['href'])
            
    print(f"Extracted {len(listing_links)} listing links.")
    
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

                # Call extract features function to scrape the individual listing
                data = extractFeatures(link)

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


# i noticed that craigslist does this thing where it tells you the posoiton of where you are in the list of listings i.e.,: https://jacksonville.craigslist.org/search/apa#search=2~gallery~198 
# i wonder if that can be stored in the json file as well to possibly help with scraping the data so that we can know how many listings there are in total and how many we have scraped so far.