import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Features we need: Listing Number, Price, Address, Agent Name, Agent Number, NumBedrooms, NumBathrooms, Stories, DatePosted, SqFT, Latitude, Longitude, Description and Title, ImageSrc
# Currently working to get Title, Price and Location. Will need to do more to get all features.
url1 = "https://staugustine.craigslist.org/apa/d/saint-augustine-modern-bed-townhouse-in/7791808730.html"
url2 = "https://staugustine.craigslist.org/apa/d/saint-augustine-bedroom-bath-doublewide/7791918230.html"
url3 = "https://staugustine.craigslist.org/apa/d/saint-augustine-fully-furnished-studio/7791998736.html"
url4 = "https://jacksonville.craigslist.org/apa/d/jacksonville-one-month-free-by-hurry/7788164796.html#"
url5 = "https://gainesville.craigslist.org/apa/d/near-uf-spacious-bedroom-bath-apt-in/7789759036.html"
url6 = "https://orlando.craigslist.org/apa/d/casselberry-500-off-first-months-rent/7787017002.html#"


# Initialize Selenium WebDriver
def init_driver():
    """_summary_

    Returns:
        _type_: _description_
    """
    driver = webdriver.Safari()
    return driver


# Use Selenium to interact with the page and reveal the phone number
def get_phone_number(driver):
    """_summary_

    Args:
        driver (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Locate the <a> tag with the class 'show-contact' and click it
    try:
        show_contact_button = driver.find_element(
            By.XPATH, "//a[contains(@class, 'show-contact')]"
        )
        driver.execute_script(
            "arguments[0].scrollIntoView();", show_contact_button
        )  # Scroll into view
        show_contact_button.click()  # Click the link to reveal contact info
    except Exception as e:
        print(f"Failed to click the show contact button: {e}")
        # print(driver.page_source)  # Print the page source for debugging
        return None

    # After clicking, retrieve the 'data-href' attribute, which contains the link to the contact info
    try:
        data_href = show_contact_button.get_attribute("data-href")
        if data_href:
            # Construct the full URL for the contact info
            contact_info_url = f"https://jacksonville.craigslist.org{data_href}"

            # Load the new page that contains the contact info
            driver.get(contact_info_url)

            # Wait for the phone number to appear on this new page
            phone_number = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//b[contains(text(),'Call:')]")
                )
            )
            return phone_number.text.strip()
        else:
            print("No 'data-href' found in the show contact button")
            return None
    except Exception as e:
        print(f"Failed to retrieve phone number from 'data-href': {e}")
        return None


def scrapeListing(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    driver = init_driver()
    driver.get(url)
    time.sleep(3)  # Adjust time based on page load time
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # print(soup.prettify()[:1000])  # Print the first 1000 characters

    # ------------------------------------------------------------------------------------------------------------------------------
    # Find Price
    price_tag = soup.find("span", class_="price")
    # Extract the price value from the <span> tag
    if price_tag:
        price_value = price_tag.text.strip()  # Use .strip() to remove extra spaces
    else:
        print("Price tag not found")

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # This finds the script tag containing the Listing ID (different script tag)
    script_tag = soup.find("script", string=re.compile("window.cl.init"))

    # Use regular expression to extract the pID
    pID_match = re.search(r"'pID':\s*(\d+)", script_tag.string)

    # If the pID is found, extract it
    if pID_match:
        pID = pID_match.group(1)
    else:
        print("pID not found")

    # -----------------------------------------------------------------------------------------------------------------------------------------
    # Find and extract the time posted feature
    time_tag = soup.find("time", class_="date timeago")
    if time_tag:
        datetime_value = time_tag["datetime"]
    else:
        print("Time tag not found")

    # -------------------------------------------------------------------------------------------------------------------------------
    # Extract property description (this now works)
    description_tag = soup.find_all("section", {"id": "postingbody"})
    description = (
        description_tag[0].text.strip() if description_tag else "Description not found"
    )

    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO: Try to find Agent Names and Phone Numbers. Does Craigslist have them?
    # Yes. Used Selenium for clicking the "reveal phone number" button. BeautifulSoup can't handle JS-based interactions.
    # Extract the phone number if possible (using Selenium)
    phone_number = None
    if driver:
        phone_number = get_phone_number(driver)
        driver.quit()
    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO: Try to find the Stories Feature. This might be available in the description.
    # Explore if properties mention "stories" or levels and extract that feature if available.

    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO: Extract image source for future use (could help with image-based anomaly detection).
    # You could pull image URLs and store them for later reverse image searches or detection of reused images in scam listings.

    # ------------------------------------------------------------------------------------------------------------------------------
    # Extract additional JSON data from the <script> tag
    script_tag = soup.find("script", {"id": "ld_posting_data"})
    json_data = json.loads(script_tag.string)

    longitude = json_data.get("longitude")
    latitude = json_data.get("latitude")
    number_of_bedrooms = json_data.get("numberOfBedrooms")
    number_of_bathrooms = json_data.get("numberOfBathroomsTotal")
    address = json_data.get("address", {})
    street_address = address.get("streetAddress")
    city = address.get("addressLocality")
    state = address.get("addressRegion")
    postal_code = address.get("postalCode")
    listing_name = json_data.get("name")

    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO Try to find where Square Footage is mentioned (possibly in the title or description).
    # This can be tricky because square footage might be mentioned differently in various listings (e.g., "ft²").
    # You could use regex to scan for patterns like "675ft²" or "675 sq ft" and extract that value.

    # ------------------------------------------------------------------------------------------------------------------------------
    # Compile all the data into a dictionary (DataFrame ready)
    # TODO CONVERT PRICE, LONG, LAT INTO NUMERICAL VALUE
    Userdata = {
        "listing_id": pID,
        "listing_name": listing_name,
        "price": price_value,
        "address": street_address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "latitude": latitude,
        "longitude": longitude,
        "bedrooms": number_of_bedrooms,
        "bathrooms": number_of_bathrooms,
        "time_posted": datetime_value,
        "description": description,
        "phone_number": phone_number,
        # TODO Add square footage here once we find it
        # 'square_footage': square_footage,
    }
    return Userdata


# Print the DataFrame example
# Uncomment the following lines to test a specific listing
# print(scrapeListing(url6))
