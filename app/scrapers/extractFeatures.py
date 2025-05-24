
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import time


# Features we need: Listing Number, Price, Address, Agent Name, Agent Number, NumBedrooms, NumBathrooms, Stories, DatePosted, SqFT, Latitude, Longitude, Description and Title, ImageSrc
# Currently working to get Title, Price and Location. Will need to do more to get all features.
url1 = "https://staugustine.craigslist.org/apa/d/saint-augustine-fully-furnished/7847425449.html"
# url2 = "https://staugustine.craigslist.org/apa/d/saint-augustine-bedroom-bath-doublewide/7791918230.html"
# url3 = "https://staugustine.craigslist.org/apa/d/saint-augustine-fully-furnished-studio/7791998736.html"
# url4 = "https://jacksonville.craigslist.org/apa/d/jacksonville-one-month-free-by-hurry/7788164796.html#"
# url5 = "https://gainesville.craigslist.org/apa/d/near-uf-spacious-bedroom-bath-apt-in/7789759036.html"
# url6 = "https://orlando.craigslist.org/apa/d/casselberry-500-off-first-months-rent/7787017002.html#"

def convert_price(price_str):
    """
    Converts the price string (e.g., "$1,299") to a numerical value (int or float).
    """
    if price_str:
        # Remove dollar sign and commas, and convert to float or int
        return float(price_str.replace('$', '').replace(',', ''))
    return None  # Return None if no price is found

def convert_lat_long(lat_str, long_str):
    """
    Converts latitude and longitude strings to float values.
    """
    try:
        latitude = float(lat_str) if lat_str else None
        longitude = float(long_str) if long_str else None
        return latitude, longitude
    except ValueError:
        return None, None  # Return None if the conversion fails
    
def extract_square_footage(text):
    """
    Extracts square footage from a given text (title or description) using regex.
    Captures patterns like '675 ft²', '675 sqft', '675 sq ft', etc.
    """
    # Regular expression pattern to match square footage
    sqft_pattern = re.compile(r'(\d{3,4})\s?(sqft|sq ft|ft²)', re.IGNORECASE)
    
    # Search for the pattern in the provided text
    sqft_match = sqft_pattern.search(text)
    
    # If a match is found, return the numeric part of the square footage
    if sqft_match:
        return int(sqft_match.group(1))  # Return only the numeric part as an integer
    
    # If no match is found, return None
    return None

def extract_phone_number(soup):
    """
    Extracts phone numbers from the entire page content using regex.
    This will capture any pattern that looks like a phone number.
    """
    page_text = soup.get_text()  # Extract all text from the page
    # Regex pattern to match phone numbers (common formats with or without separators)
    phone_number_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    phone_numbers = phone_number_pattern.findall(page_text)
    
    # Return the first found phone number or None if none found
    return phone_numbers[0] if phone_numbers else None

def extractFeatures(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")

    # ------------------------------------------------------------------------------------------------------------------------------
    # Find Price
    price_tag = soup.find("span", class_="price")

    # Extract the price value from the <span> tag
    if price_tag:
        price_value = convert_price(price_tag.text.strip())  # Convert price to a number
    else:
        price_value = None
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
    # TODO: Try to find Agent Names and Phone Numbers. Does Craigslist have them? (this now works)
    # Yes. Used Selenium for clicking the "reveal phone number" button. BeautifulSoup can't handle JS-based interactions.
    # Extract the phone number using regex
    phone_number = extract_phone_number(soup)

    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO: Try to find the Stories Feature. This might be available in the description. 
    # Explore if properties mention "stories" or levels and extract that feature if available.
    #! Decided not to do this because apartments typically only have one floor anyways.

    # ------------------------------------------------------------------------------------------------------------------------------
    # TODO: Extract image source for future use (could help with image-based anomaly detection).
    # You could pull image URLs and store them for later reverse image searches or detection of reused images in scam listings.

    # ------------------------------------------------------------------------------------------------------------------------------
    # Extract additional JSON data from the <script> tag
    script_tag = soup.find("script", {"id": "ld_posting_data"})
    json_data = json.loads(script_tag.string)

    longitude_str = json_data.get("longitude")
    latitude_str = json_data.get("latitude")
    latitude, longitude = convert_lat_long(latitude_str, longitude_str)

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
    square_footage = extract_square_footage(listing_name) or extract_square_footage(description)

    # ------------------------------------------------------------------------------------------------------------------------------
    # Compile all the data into a dictionary (DataFrame ready)

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
        "square_footage": square_footage,
        "url": url
    }
    return Userdata


# Print the DataFrame example
# Uncomment the following lines to test a specific listing
# print(extractFeatures(url1))


'''

ANN when you come back: try scraping the following links for additional features.
- Try scraping a bunch of listings just to see if you can get a good amount of data.
- These links contain information about average rent prices and household income by zipcode. This could be useful for the model to determine if a listing is overpriced or underpriced based on the average price in that area.
- These are secondary datasets that can be used to enrich the primary dataset.


secondary dataset links. Want to include the average price/rent per zipcode in the model. 850$ might be normal in the an average zipcode, but would be a big red flag in the most expensive zipcode.
https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html?utm_source=chatgpt.com
https://www.unitedstateszipcodes.org/rankings/zips-in-fl/median_monthly_rent/
http://www.usa.com/rank/florida-state--median-household-income--zip-code-rank.htm
http://www.usa.com/rank/florida-state--house-median-value--zip-code-rank.htm?hl=32202&hlst=FL&yr=9000

'''