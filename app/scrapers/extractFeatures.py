# This file extracts features from apartment listings on various websites.

import requests
from bs4 import BeautifulSoup
import hashlib
import json
import re
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

# Features we need: Listing Number, Price, Address, Agent Name, Agent Number, NumBedrooms, NumBathrooms, Stories, DatePosted, SqFT, Latitude, Longitude, Description and Title, ImageSrc

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
    Captures patterns like '675 ft²', '675ft²', '675 sqft', '675 sq ft', etc.
    Also handles HTML entities and Unicode variations.
    """
    if not text:
        return None
        
    # Regular expression patterns to match square footage
    # Handle various formats - ordered from most specific to least specific
    sqft_patterns = [
        # Craigslist specific patterns first
        (r'\d+br\s*-\s*(\d{3,5})\s*ft²', 'Craigslist with Unicode (2br - 885ft²)'),
        (r'\d+br\s*-\s*(\d{3,5})\s*ft2', 'Craigslist with ft2 (2br - 885ft2)'),
        (r'\d+br\s*-\s*(\d{3,5})\s*ft', 'Craigslist format (2br - 885ft)'),
        (r'/\s*\d+br\s*-\s*(\d{3,5})\s*ft', 'Craigslist with slash (/ 2br - 885ft)'),
        (r'-\s*(\d{3,5})\s*ft²', 'After dash with Unicode (- 885ft²)'),
        (r'-\s*(\d{3,5})\s*ft2', 'After dash with ft2 (- 885ft2)'),
        (r'-\s*(\d{3,5})\s*ft', 'After dash (- 885ft)'),
        
        # General patterns
        (r'(\d{3,5})\s*ft²', 'Unicode superscript (ft²)'),
        (r'(\d{3,5})\s*ft\s*²', 'Unicode with spaces (ft ²)'),
        (r'(\d{3,5})\s*ft&sup2;', 'HTML entity (&sup2;)'),
        (r'(\d{3,5})\s*ft\^2', 'Caret notation (ft^2)'),
        (r'(\d{3,5})\s*ft2', 'Simple ft2'),
        (r'(\d{3,5})\s*ft\s*2', 'ft with space 2'),
        (r'(\d{3,5})\s*sqft', 'sqft format'),
        (r'(\d{3,5})\s*sq\.?\s*ft', 'sq ft or sq. ft'),
        (r'(\d{3,5})\s*square\s*feet', 'square feet'),
        (r'(\d{3,5})\s*sf', 'sf shorthand'),
        (r'(\d{3,5})\s*sq\s*feet', 'sq feet'),
        (r'(\d{3,5})\s*SqFt', 'SqFt camelCase'),
        
        # Most general patterns last
        (r'(\d{3,5})\s*ft(?:\s|$)', 'Just ft at end'),
        (r'/\s*(\d{3,5})\s*(?:ft|sf|sqft)', 'with slash prefix'),
    ]
    
    # Try each pattern
    for pattern, description in sqft_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                sqft = int(match.group(1))
                # Sanity check - reasonable apartment size
                if 100 <= sqft <= 10000:
                    return sqft
                
            except Exception as e:
                print(f"Error extracting number from match: {e}")
                continue
    
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

def extractFeatures(url, unit_listing_id=None, processed_urls=None):
    """
    Universal feature extractor - detects source and routes to appropriate function
    """
    if processed_urls is None:
        processed_urls = set()
    if url in processed_urls:
        print(f"URL already processed: {url}")
        return None
    processed_urls.add(url)  # Mark this URL as processed
    try:
        domain = urlparse(url).netloc.lower()
        
        if "craigslist.org" in domain:
            return _extract_craigslist_features(url)
        elif "zillow.com" in domain:
            return _extract_zillow_features(url, unit_listing_id=unit_listing_id, processed_urls=processed_urls)
        elif "apartments.com" in domain:
            return _extract_apartments_features(url)
        else:
            print(f"Unsupported site: {domain}")
            return None
            
    except Exception as e:
        print(f"Error extracting features from {url}: {e}")
        return None
    
    # Todo: Cache & Save Progress, So if interrupted, we don’t repeat scraped pages.
    # Ideas: # 1. Use a database or file to store already scraped URLs and their data.
    # 2. Implement a simple caching mechanism that checks if a URL has already been processed.
    # 3. Save progress periodically to avoid losing data in case of interruptions.
    # 4. Use a unique identifier for each listing (like listing ID) to avoid duplicates.

def _extract_craigslist_features(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")

    # Find Price
    price_tag = soup.find("span", class_="price")

    if price_tag:
        price_value = convert_price(price_tag.text.strip()) 
    else:
        price_value = None
        print("Price tag not found")

    # This finds the script tag containing the Listing ID (different script tag)
    script_tag = soup.find("script", string=re.compile("window.cl.init"))

    # Use regular expression to extract the pID
    pID_match = re.search(r"'pID':\s*(\d+)", script_tag.string)

    # If the pID is found, extract it
    if pID_match:
        pID = pID_match.group(1)
    else:
        print("pID not found")

    # Find and extract the time posted feature
    time_tag = soup.find("time", class_="date timeago")
    if time_tag:
        datetime_value = time_tag["datetime"]
    else:
        print("Time tag not found")

    # Extract property description (this now works)
    description_tag = soup.find_all("section", {"id": "postingbody"})
    description = (
        description_tag[0].text.strip() if description_tag else "Description not found"
    )

    phone_number = extract_phone_number(soup)

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

    # Method 1: Check the title first (most reliable)
    if listing_name:
        square_footage = extract_square_footage(listing_name)
    
    # Method 2: Check the housing info span
    if not square_footage:
        housing_span = soup.find("span", class_="housing")
        if housing_span:
            # Get text in different ways to debug
            housing_text = housing_span.get_text()
            square_footage = extract_square_footage(housing_text)
    
    # Method 3: Check the page title
    if not square_footage:
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.text
            square_footage = extract_square_footage(title_text)
    
    # Method 4: Check description as last resort
    if not square_footage and description:
        square_footage = extract_square_footage(description)

    # Compile all the data into a dictionary (DataFrame ready)

    Userdata = {
        "source": "craigslist",
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

# TODO: FIX THE ZILLOW SCRAPER AND EXTRACTOR. The issues are that it does not extract the features correctly and it does not handle the different types of Zillow pages correctly. I am unsure of the specific root issues, but I will need to debug the code and fix the issues.
SCRAPERAPI_KEY = os.getenv('SCRAPERAPI_KEY')

def _extract_zillow_features(url, unit_listing_id=None, processed_urls=None):
    """
    Handle different types of Zillow pages
    """
    print(f"Extracting Zillow data from: {url}")
    
    payload = {
        'api_key': SCRAPERAPI_KEY,
        'url': url,
        'render': 'true',
        'country_code': 'us'
    }
    
    try:
        response = requests.get('https://api.scraperapi.com/', params=payload, timeout=60)
        
        if response.status_code != 200:
            print(f"ScraperAPI error: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if this is a floor plan page with availability table
        availability_table = soup.find('table') or soup.select('[data-test="availability-table"]')
        
        if availability_table or "units available" in response.text.lower():
            print("Detected floor plan page with availability table")
            result = _extract_floor_plan_data(url, soup, response.text, unit_listing_id, processed_urls)
            # Always flatten to a list
            if isinstance(result, dict) and "floor_plan_data" in result and "units" in result:
                combined = [result["floor_plan_data"]] + result["units"]
                return combined
            elif isinstance(result, list):
                return result
            else:
                return [result] if result else []
        else:
            print("Detected complex overview page")
            result = _extract_complex_data(url, soup, response.text, unit_listing_id)
            return [result] if result else []
            
    except Exception as e:
        print(f"Error extracting Zillow features: {e}")
        return None

def _extract_floor_plan_data(url, soup, html_text, unit_listing_id=None, processed_urls=None):
    """
    Extract data from floor plan page with availability table
    """
    print("Extracting floor plan data...")
    
    if unit_listing_id:
        listing_id = unit_listing_id
    else:
        # Extract listing ID using helper function
        listing_id = extract_zillow_id(url)
        if listing_id:
            print(f"Extracted Zillow ID: {listing_id}")
    
    # Extract complex/property name
    title = None
    title_selectors = [
        'h1',
        'h2',
        '[class*="Text-"][class*="bold"]',
        '[data-test="property-title"]',
        '.property-name'
    ]
    
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            # Skip if it's just "Available units" or similar
            if title_text and 'available units' not in title_text.lower():
                title = title_text
                # Clean up title
                title = re.sub(r'\s+Apartments?$', '', title, flags=re.IGNORECASE)
                break
    
    # Extract bed/bath info - look for patterns in the table or page
    bedrooms = bathrooms = None
    
    # Method 1: Look for "X bed, Y ba" pattern in the table rows
    bed_bath_patterns = [
        r'(\d+)\s*bed[,\s]+(\d+(?:\.\d+)?)\s*ba',  # "3 bed, 2.5 ba"
        r'(\d+)\s*bd[,\s]+(\d+(?:\.\d+)?)\s*ba',   # "3 bd, 2.5 ba"
        r'(\d+)\s*bedroom[,\s]+(\d+(?:\.\d+)?)\s*bath',  # Full words
    ]
    
    for pattern in bed_bath_patterns:
        matches = re.findall(pattern, html_text, re.IGNORECASE)
        if matches:
            # Take the first match (they should all be the same for a floor plan)
            bedrooms = int(matches[0][0])
            bathrooms = float(matches[0][1])
            print(f"Found bed/bath: {bedrooms} bed, {bathrooms} bath")
            break
    
    # Method 2: Look in specific table cells
    if not bedrooms:
        # Look for unit descriptions in table
        unit_cells = soup.select('td') + soup.select('[class*="StyledTableCell"]')
        for cell in unit_cells:
            cell_text = cell.get_text(strip=True)
            for pattern in bed_bath_patterns:
                match = re.search(pattern, cell_text, re.IGNORECASE)
                if match:
                    bedrooms = int(match.group(1))
                    bathrooms = float(match.group(2))
                    break
            if bedrooms:
                break
    
    # Extract square footage
    square_footage = None
    sqft_patterns = [
        r'(\d{3,4})\s*sq\s*ft',
        r'(\d{3,4})\s*sqft',
        r'(\d{3,4})\s*square feet',
    ]
    
    for pattern in sqft_patterns:
        sqft_match = re.search(pattern, html_text, re.IGNORECASE)
        if sqft_match:
            square_footage = int(sqft_match.group(1))
            break
    
    # Extract price - look for the base rent in the table
    price = None
    
    # Method 1: Look for price patterns in table
    price_patterns = [
        r'\$([0-9,]+)\s*(?:/mo|\/month)?',  # $2,399 or $2,399/mo
        r'Base rent[:\s]*\$([0-9,]+)',      # Base rent: $2,399
        r'Starting at[:\s]*\$([0-9,]+)',    # Starting at $2,399
    ]
    
    # Find all prices and take the lowest (base rent)
    all_prices = []
    for pattern in price_patterns:
        price_matches = re.findall(pattern, html_text)
        for match in price_matches:
            try:
                price_val = float(match.replace(',', ''))
                if 500 <= price_val <= 10000:  # Reasonable rent range
                    all_prices.append(price_val)
            except:
                pass
    
    if all_prices:
        price = min(all_prices)  # Take the lowest as base rent
        print(f"Found base rent: ${price}")
    
    # Extract address
    address = city = state = postal_code = None
    
    # Look for address in various formats
    addr_pattern = re.search(
        r'(\d+\s+[^,]+),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5})',
        html_text
    )
    if addr_pattern:
        address = addr_pattern.group(1).strip()
        city = addr_pattern.group(2).strip()
        state = addr_pattern.group(3).strip()
        postal_code = addr_pattern.group(4).strip()
    
    # Extract phone number - be more specific to avoid wrong matches
    phone_number = None
    
    # Look for phone number near "Phone number" text or in contact section
    phone_section = re.search(
        r'(?:Phone number|Contact|Call)[:\s]*[\(\d][\d\s\(\)-]+\d',
        html_text,
        re.IGNORECASE
    )
    
    if phone_section:
        phone_text = phone_section.group(0)
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
        if phone_match:
            phone_number = phone_match.group(0)
    
    # If not found, look for specific patterns
    if not phone_number:
        # Pattern for (XXX) XXX-XXXX format
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}',
            r'\d{3}\.\d{3}\.\d{4}'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, html_text)
            if phone_match:
                phone_number = phone_match.group(0)
                break
    
    # Build description
    description_parts = []
    if title:
        description_parts.append(f"{title}")
    if bedrooms and bathrooms:
        description_parts.append(f"{bedrooms} bed, {bathrooms} bath units")
    if square_footage:
        description_parts.append(f"{square_footage} sq ft")
    
    # Add amenities if found
    amenities = []
    amenity_keywords = ['ATTACHED ONE-CAR GARAGE', 'POOL WITH CABANA', 'FENCED-IN BACKYARD', 
                       'SCREENED-IN LANAI', 'PLANK TILE FLOORING', 'NATURE TRAIL']
    
    for keyword in amenity_keywords:
        if keyword in html_text.upper():
            amenities.append(keyword.title())
    
    if amenities:
        description_parts.append(f"Features: {', '.join(amenities[:3])}")
    
    description = ". ".join(description_parts) if description_parts else "Apartment complex"
    
    # Extract coordinates if available
    latitude = longitude = None
    
    # Look for coordinates in JSON-LD data
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and 'geo' in data:
                latitude = data['geo'].get('latitude')
                longitude = data['geo'].get('longitude')
                break
        except:
            pass
    
    # Alternative: Look in JavaScript
    if not latitude:
        lat_match = re.search(r'latitude["\']?\s*:\s*(-?\d+\.?\d*)', html_text)
        lng_match = re.search(r'longitude["\']?\s*:\s*(-?\d+\.?\d*)', html_text)
        
        if lat_match and lng_match:
            try:
                latitude = float(lat_match.group(1))
                longitude = float(lng_match.group(1))
            except:
                pass
    
    floor_plan_data = {
        "source": "zillow",
        "listing_id": listing_id,
        "listing_name": title,
        "price": price,
        "address": address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "latitude": latitude,
        "longitude": longitude,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "time_posted": None,
        "description": description,
        "phone_number": phone_number,
        "square_footage": square_footage,
        "url": url
    }
    
    unit_urls = get_individual_unit_urls(url, listing_id=listing_id)
    unit_data_list = []
    
    for href, unit_info in unit_urls.items():
        if not unit_info.get('listing_id'):
            continue
        unit_data = extractFeatures(
            unit_info['unit_url'], unit_listing_id=unit_info.get('listing_id'), processed_urls=processed_urls)
        
        if unit_data:
            unit_data_list.append(unit_data)
            print(f"Extracted unit data: {unit_data.get('listing_name', 'No name')}")

    return {
        "floor_plan_data": floor_plan_data,
        "units": unit_data_list
    }
    
def _extract_complex_data(url, soup, html_text, unit_listing_id=None):
    """
    Extract data from apartment complex overview page
    """
    print("Extracting complex overview data...")
    
    # Extract listing ID from URL
    # Zillow IDs are typically 5-7 character alphanumeric codes at the end of the URL
    
    if unit_listing_id:
        listing_id = unit_listing_id
    else:
        listing_id = extract_zillow_id(url)
      
    # Extract complex name/title
    title = None
    title_selectors = [
        'h1[class*="Text-"]',  # Zillow uses dynamic class names
        'h1',
        '[data-test="property-title"]',
        '.property-name',
        'span[class*="Text-"][class*="bold"]'
    ]
    
    # Try multiple selectors to find the title
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            title = title_elem.get_text(strip=True)
            # Clean up title - remove "Apartments" suffix if it's redundant
            title = re.sub(r'\s+Apartments?$', '', title, flags=re.IGNORECASE)
            break
    
    # Extract price range
    price = None
    price_patterns = [
        r'\$([0-9,]+)\s*-\s*\$([0-9,]+)',  # Range like $1,200 - $2,500
        r'\$([0-9,]+)\+',  # Starting price like $1,200+
        r'From\s*\$([0-9,]+)',  # From $1,200
        r'\$([0-9,]+)',  # Simple price
    ]
    
    for pattern in price_patterns:
        price_match = re.search(pattern, html_text)
        if price_match:
            try:
                # For ranges, take the lower bound
                price = float(price_match.group(1).replace(',', ''))
                break
            except:
                pass
    
    # Extract address components
    address = city = state = postal_code = None
    
    # Method 1: Look for structured address in various formats
    address_selectors = [
        '[data-test="property-address"]',
        'address',
        'span[class*="Text-"][class*="address"]',
        'div[class*="address"]'
    ]
    
    for selector in address_selectors:
        addr_elem = soup.select_one(selector)
        if addr_elem:
            address = addr_elem.get_text(strip=True)
            break
    
    # Method 2: Regex pattern for full address
    if not address:
        # Pattern: 123 Main St, City, ST 12345
        addr_pattern = re.search(
            r'(\d+[^,]+),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5})',
            html_text
        )
        if addr_pattern:
            address = addr_pattern.group(1).strip()
            city = addr_pattern.group(2).strip()
            state = addr_pattern.group(3).strip()
            postal_code = addr_pattern.group(4).strip()
    
    # Parse address if we found it but haven't parsed components
    if address and not city:
        parts = address.split(',')
        if len(parts) >= 3:
            # Usually: street, city, state zip
            address = parts[0].strip()
            city = parts[1].strip()
            state_zip = parts[2].strip().split()
            if len(state_zip) >= 2:
                state = state_zip[0]
                postal_code = state_zip[1]
    
    # Extract bed/bath ranges
    bedrooms = bathrooms = None
    
    # Look for bed/bath info in various formats
    bed_bath_patterns = [
        r'(\d+)\s*bed[,\s]+(\d+(?:\.\d+)?)\s*ba',  # "3 bed, 2.5 ba"
        r'(\d+)\s*bd[,\s]+(\d+(?:\.\d+)?)\s*ba',   # "3 bd, 2.5 ba"
        r'(\d+)\s*bedroom[,\s]+(\d+(?:\.\d+)?)\s*bath',  # Full words
    ]
    
    for pattern in bed_bath_patterns:
        matches = re.findall(pattern, html_text, re.IGNORECASE)
        if matches:
            # Take the first match (they should all be the same for a floor plan)
            bedrooms = int(matches[0][0])
            bathrooms = float(matches[0][1])
            print(f"Found bed/bath: {bedrooms} bed, {bathrooms} bath")
            break
        
    if not bedrooms:
        # Look for unit descriptions in table
        unit_cells = soup.select('td') + soup.select('[class*="StyledTableCell"]')
        for cell in unit_cells:
            cell_text = cell.get_text(strip=True)
            for pattern in bed_bath_patterns:
                match = re.search(pattern, cell_text, re.IGNORECASE)
                if match:
                    bedrooms = int(match.group(1))
                    bathrooms = float(match.group(2))
                    break
            if bedrooms:
                break
    
    # Extract square footage range
    square_footage = None
    sqft_patterns = [
        r'(\d{3,4})\s*-\s*(\d{3,4})\s*sq\s*ft',  # Range
        r'(\d{3,4})\s*sq\s*ft',  # Single value
        r'(\d{3,4})\s*sqft',
    ]
    
    for pattern in sqft_patterns:
        sqft_match = re.search(pattern, html_text, re.IGNORECASE)
        if sqft_match:
            square_footage = int(sqft_match.group(1))  # Take lower bound
            break
    
    # Extract amenities and features for description
    amenities = []
    amenity_selectors = [
        'li[class*="amenity"]',
        'div[class*="amenity"]',
        'span[class*="feature"]'
    ]
    
    for selector in amenity_selectors:
        amenity_elems = soup.select(selector)[:5]  # Limit to first 5
        for elem in amenity_elems:
            text = elem.get_text(strip=True)
            if text and len(text) < 50:  # Reasonable length
                amenities.append(text)
    
    # Build description
    description_parts = []
    if title:
        description_parts.append(f"{title} apartment complex")
    if bedrooms is not None:
        description_parts.append(f"{bedrooms}+ bedrooms")
    if bathrooms is not None:
        description_parts.append(f"{bathrooms}+ bathrooms")
    if square_footage:
        description_parts.append(f"starting from {square_footage} sqft")
    if amenities:
        description_parts.append(f"Amenities: {', '.join(amenities[:3])}")
    
    description = ". ".join(description_parts) if description_parts else "Apartment complex"
    
    # Extract phone number
    phone_number = None
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
    ]
    
    for pattern in phone_patterns:
        phone_match = re.search(pattern, html_text)
        if phone_match:
            phone_number = phone_match.group(0)
            break
    
    # Extract lat/long if available in page data
    latitude = longitude = None
    
    # Look for coordinates in JSON-LD data
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                # Check for geo coordinates
                if 'geo' in data:
                    latitude = data['geo'].get('latitude')
                    longitude = data['geo'].get('longitude')
                elif '@graph' in data:
                    # Sometimes nested in @graph array
                    for item in data['@graph']:
                        if 'geo' in item:
                            latitude = item['geo'].get('latitude')
                            longitude = item['geo'].get('longitude')
                            break
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            continue
    
    # Alternative: Look for coordinates in JavaScript variables
    if not latitude:
        lat_match = re.search(r'latitude["\']?\s*:\s*(-?\d+\.?\d*)', html_text)
        lng_match = re.search(r'longitude["\']?\s*:\s*(-?\d+\.?\d*)', html_text)
        
        if lat_match and lng_match:
            try:
                latitude = float(lat_match.group(1))
                longitude = float(lng_match.group(1))
            except:
                pass
    
    return {
        "source": "zillow",
        "listing_id": listing_id,
        "listing_name": title,
        "price": price,
        "address": address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "latitude": latitude,
        "longitude": longitude,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "time_posted": None,  # Complex pages don't usually show posting date
        "description": description,
        "phone_number": phone_number,
        "square_footage": square_footage,
        "url": url
    }

def extract_zillow_id(url):
    """
    Extract Zillow listing ID from URL
    Zillow IDs are typically 5-7 character alphanumeric codes
    
    Examples:
    - https://www.zillow.com/b/silver-creek-saint-augustine-fl-CkCj4V/
    - https://www.zillow.com/b/the-vue-orlando-fl-5Y2Yqv/
    
    Returns:
        str: The Zillow ID or None if not found
    """
    
    print("hi", url)
    id_patterns = [
        r'-([A-Za-z0-9]{5,7})/?$',  # ID at end after hyphen (most common)
        r'/b/[^/]+-([A-Za-z0-9]{5,7})/?$',  # Specifically for /b/ URLs
        r'/([A-Za-z0-9]{5,7})_zpid/?$',  # Sometimes formatted as ID_zpid
        r'zpid=([A-Za-z0-9]{5,7})',  # In query parameters
    ]
    
    for pattern in id_patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Fallback: check last segment
    url_parts = url.rstrip('/').split('/')
    if url_parts:
        last_segment = url_parts[-1]
        # Check if last segment after last hyphen looks like an ID
        if '-' in last_segment:
            potential_id = last_segment.split('-')[-1]
            if len(potential_id) >= 5 and len(potential_id) <= 7 and potential_id.isalnum():
                print(f"Extracted Zillow ID from last segment: {potential_id}")
                return potential_id
    
    # If no ID found, generate a fallback ID
    fallback_id = generate_fallback_id(url)
    print(f"No Zillow ID found in URL, using fallback: {fallback_id}")
    return fallback_id

def get_zillow_listing_links(search_url, max_pages=1):
    """
    Extract listing URLs from Zillow search results page
    Handles both regular listings and apartment complex listings
    """
    print(f"Extracting listing links from: {search_url}")
    
    all_links = []
    
    for page in range(max_pages):
        current_url = search_url
        if page > 0:
            # Add pagination parameter
            separator = '&' if '?' in search_url else '?'
            current_url = f"{search_url}{separator}currentPage={page + 1}"
        
        payload = {
            'api_key': SCRAPERAPI_KEY,
            'url': current_url,
            'render': 'true',
            'country_code': 'us'
        }
        
        try:
            response = requests.get('https://api.scraperapi.com/', params=payload, timeout=60)
            
            if response.status_code != 200:
                print(f"Error fetching page {page + 1}: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Multiple selectors to catch different listing types
            link_selectors = [
                'a[data-test="property-card-link"]',
                'a.list-card-link',
                'article[data-test="property-card"] a',
                'div.list-card a',
                'a[href*="/b/"]', # Apartment complex links
                'a[href*="/homedetails/"]', # Regular listings

                # Additional selectors:
                'div[data-testid="property-card"] a',  # Newer Zillow grid
                'li article a',                        # Sometimes listings are in <li>
                'ul.photo-cards li a',                 # Older Zillow grid
                'div[data-testid="result-card"] a',    # Redfin and others
                'div[data-testid="home-card"] a',      # Some sites use this
                'div[data-test="search-result-card"] a',
                'div[data-test="property-card-container"] a',
                'div[data-testid="card-container"] a',
                'div[data-testid="property-card-link"] a',
                'a[data-testid="property-link"]',
                'a[data-testid="card-link"]',
            ]
            
            page_links = set()  # Use set to avoid duplicates
            
            for selector in link_selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        # Make absolute URL
                        if href.startswith('/'):
                            href = 'https://www.zillow.com' + href
                        
                        # Skip links inside a <footer>
                        if link.find_parent('footer'):
                            continue
                        
                        # Skip links inside any footer-subsection
                        if link.find_parent(attrs={"data-testid": lambda v: v and "footer-subsection" in v}):
                            continue

                        # Blacklist: Drop links if 'browse' is in the href
                        if 'browse' in href:
                            continue
                        if any(x in href for x in ['/b/', '/homedetails/', '/apartments/', '/zpid/']):
                            page_links.add(href)
            
            print(f"Found {len(page_links)} unique links on page {page + 1}")

                
            all_links.extend(list(page_links))
            
        except Exception as e:
            print(f"Error on page {page + 1}: {e}")
            continue
    
    # Remove duplicates and return
    unique_links = list(dict.fromkeys(all_links))
    print(f"Total unique listings found: {len(unique_links)}")
    
    return unique_links

def get_individual_unit_urls(floor_plan_url, listing_id=None):
    """
    Extract individual unit URLs from a floor plan page
    """
    payload = {
        'api_key': SCRAPERAPI_KEY,
        'url': floor_plan_url,
        'render': 'true',
        'country_code': 'us'
    }
    
    try:
        response = requests.get('https://api.scraperapi.com/', params=payload, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        unit_urls = {}
        
        # Look for unit links in the availability table
        unit_links = (
            soup.select('a[data-test-id="bdp-property-card"]') or
            soup.select('a[href*="/unit/"]') or
            soup.select('a[data-testid="unit-link"]') or
            soup.select('a[href*="unitId="]')
        )

        print(f"Found {len(unit_links)} unit links on floor plan page")
        if unit_links:
            print("First 3 unit links:", [link.get('href') for link in unit_links[:3]])
        
        for link in unit_links:
            href = link.get('href')
            if not href:
                continue
                
            # Extract zpid from unit URL
            unit_listing_id = None  # Initialize variable
            zpid_match = re.search(r'/(\d+)_zpid/', href)
            if zpid_match:
                zpid = zpid_match.group(1)
                if listing_id and zpid:
                    unit_listing_id = f"{listing_id}_{zpid}"
                    print(f"Created unit_listing_id: {unit_listing_id}")
                else:
                    print(f"Found zpid {zpid} but no base listing_id provided")
            else:
                print(f"No zpid found in {href}")
            
            # Make absolute URL
            if href.startswith('/'):
                href = 'https://www.zillow.com' + href
            
            # Determine final listing ID
            final_listing_id = unit_listing_id if unit_listing_id else listing_id
            
            # Only add if we have some kind of listing ID
            if final_listing_id:
                unit_urls[href] = {
                    "listing_id": final_listing_id,
                    "unit_url": href
                }
            else:
                print(f"Warning: No listing ID for unit {href}")
                # Still add the URL but with None listing_id
                unit_urls[href] = {
                    "listing_id": None,
                    "unit_url": href
                }
        
        print(f"Returning {len(unit_urls)} unit URLs")
        return unit_urls
        
    except Exception as e:
        print(f"Error extracting unit URLs: {e}")
        import traceback
        traceback.print_exc()
        return {}

def generate_fallback_id(url):
    """
    Generate a fallback ID based on URL hash when no ID can be extracted
    """
    # Create a hash of the URL to ensure uniqueness
    url_hash = hashlib.md5(url.encode()).hexdigest()
    # Take first 7 characters to match Zillow ID format
    return f"HASH{url_hash[:7]}"

def _extract_apartments_features(url):
    """
    Placeholder for Apartments.com extraction - you can improve this later
    """
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Basic Apartments.com extraction (improve this later)
    title_elem = soup.find('h1', class_='propertyName')
    title = title_elem.text.strip() if title_elem else None
    
    return {
        "source": "apartments_com",  
        "listing_id": None,
        "listing_name": title,
        "price": None,
        "address": None,
        "city": None,
        "state": None,
        "postal_code": None,
        "latitude": None,
        "longitude": None,
        "bedrooms": None,
        "bathrooms": None,
        "time_posted": None,
        "description": None,
        "phone_number": None,
        "square_footage": None,
        "url": url
    }
    