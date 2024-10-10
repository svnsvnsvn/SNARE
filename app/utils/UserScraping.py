import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re


# Features we need: Listing Number, Price, Address, Agent Name, Agent Number, NumBedrooms, NumBathrooms, Stories, DatePosted, SqFT, Latitude, Longitude, Description and Title, ImageSrc
# Currently working to get Title, Price and Location. Will need to do more to get all features. 
url1 = 'https://staugustine.craigslist.org/apa/d/saint-augustine-modern-bed-townhouse-in/7791808730.html'
url2 = 'https://staugustine.craigslist.org/apa/d/saint-augustine-bedroom-bath-doublewide/7791918230.html'
url3 = 'https://staugustine.craigslist.org/apa/d/saint-augustine-fully-furnished-studio/7791998736.html'
url4 = 'https://jacksonville.craigslist.org/apa/d/jacksonville-one-month-free-by-hurry/7788164796.html#'
url5 = 'https://gainesville.craigslist.org/apa/d/near-uf-spacious-bedroom-bath-apt-in/7789759036.html'
url6 = 'https://orlando.craigslist.org/apa/d/casselberry-500-off-first-months-rent/7787017002.html#'


def ScrapeListing(url):
    response = requests.get(url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful!")
    else:
        print(f"Request failed with status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify()[:1000])  # Print the first 1000 characters

    # ------------------------------------------------------------------------------------------------------------------------------
    # Find Price
    price_tag = soup.find('span', class_='price')
    # Extract the price value from the <span> tag
    if price_tag:
        price_value = price_tag.text.strip()  # Use .strip() to remove extra spaces
    else:
        print("Price tag not found")


    # ------------------------------------------------------------------------------------------------------------------------------------------------

    # This finds the script tag containing the Listing ID (different script tag)
    script_tag = soup.find('script', string=re.compile('window.cl.init'))

    # Use regular expression to extract the pID
    pID_match = re.search(r"'pID':\s*(\d+)", script_tag.string)

    # If the pID is found, extract it
    if pID_match:
        pID = pID_match.group(1)
    else:
        print("pID not found")


    # -----------------------------------------------------------------------------------------------------------------------------------------

    # Find and extract the time posted feature

    time_tag = soup.find('time', class_='date timeago')
    if time_tag:
        datetime_value = time_tag['datetime']
    else:
        print("Time tag not found")


    # -------------------------------------------------------------------------------------------------------------------------------
    # PROPERTY DESCRIPTION HAS NO TAGS OR CLASS NAMES,  NOTHING!!!
    # Could count down the amount of <p> tags to get it, but it might be different from page to page. will have to go back to this,
    # because decription is needed for scammy word search.  

    # ---------------------------------------------------------------------------------------------------------------------------------------

    # Try to find where Square Footage is found


    # ---------------------------------------------------------------------------------------------------------------------------------------

    # Try to Find Agent Names and Phone Numbers? do they have them on craigslist??


    # ---------------------------------------------------------------------------------------------------------------------------------------

    # Try to find Stories Feature

    # --------------------------------------------------------------------------------------------------------------------------------------


    # Maybe try to extract image source to reverse look it up in the future. could be useful to just scrape it now instead of later


    # -----------------------------------------------------------------------------------------------------------------------------------


    # This finds the script tag containing the JSON data
    script_tag = soup.find('script', {'id': 'ld_posting_data'})
    json_data = json.loads(script_tag.string)

    longitude = json_data.get('longitude')
    latitude = json_data.get('latitude')
    number_of_bedrooms = json_data.get('numberOfBedrooms')
    number_of_bathrooms = json_data.get('numberOfBathroomsTotal')
    address = json_data.get('address', {})
    street_address = address.get('streetAddress')
    city = address.get('addressLocality')
    state = address.get('addressRegion')
    postal_code = address.get('postalCode')
    listing_name = json_data.get('name')


    # -------------------------------------------------------------------------------------------------------------------------------------------
    # Create the dataframe

    Userdata = {
        'Listing_ID': pID,
        'Price': price_value,
        'Listing Name': listing_name,
        'Street Address': street_address,
        'City': city,
        'State': state,
        'Postal Code': postal_code,
        'Latitude': latitude,
        'Longitude': longitude,
        'Bedrooms': number_of_bedrooms,
        'Bathrooms': number_of_bathrooms,
        'Time Posted': datetime_value
    }
    return Userdata


# Print the DataFrame
# print(df)
print(ScrapeData(url6))

