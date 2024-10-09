# Functions for scraping Zillow, Craigslist

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_listing(url):
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

# #Features we need: Listing Number, Price, Address, Agent Name, Agent Number, NumBedrooms, NumBathrooms, Stories, DatePosted, SqFT, Latitude, Longitude, Description and Title, ImageSrc
# # Currently working to get Title, Price and Location. Will need to do more to get all features. 
# url = 'https://staugustine.craigslist.org/search/apa#search=1~gallery~0~1'

# response = requests.get(url)

# # Check if request was successful (status code 200)
# if response.status_code == 200:
#     print("Request successful!")
# else:
#     print(f"Request failed with status code: {response.status_code}")

# soup = BeautifulSoup(response.content,'html.parser')

# # Can use prettify to see the raw html structure that is being pulled. 
# #print(soup.prettify()[:1000])  # Print the first 1000 characters

# # Find all listing containers using <li> with class 'cl-static-search-result'
# listings = soup.find_all('li', class_='cl-static-search-result')

# # Create empty lists to store the data
# titles = []
# prices = []
# locations = []

# # Loop through each listing and extract the title, price, and location
# for listing in listings:
#     # Extract the title
#     title_div = listing.find('div', class_='title')
#     title = title_div.text.strip() if title_div else 'No title'
    
#     # Extract the price
#     price_div = listing.find('div', class_='price')
#     price = price_div.text.strip() if price_div else 'No price'
    
#     # Extract the location
#     location_div = listing.find('div', class_='location')
#     location = location_div.text.strip() if location_div else 'No location'
    
#     # Append the data to the respective lists
#     titles.append(title)
#     prices.append(price)
#     locations.append(location)

# # Create a DataFrame from the collected data
# df = pd.DataFrame({
#     'Title': titles,
#     'Price': prices,
#     'Location': locations
# })

# # Print the DataFrame to see the results
# print(df)
