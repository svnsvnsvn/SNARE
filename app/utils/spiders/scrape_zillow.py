import requests
from bs4 import BeautifulSoup

def scrape_zillow(url):
    """Scrapes a Zillow listing and returns listing data."""
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        return None
    
    title = soup.find('h1', class_='ds-address-container').text.strip() if soup.find('h1', class_='ds-address-container') else 'No title'
    price_tag = soup.find('span', class_='ds-value')
    price_value = price_tag.text.strip() if price_tag else 'No price'
    address_tag = soup.find('h2', class_='ds-address-container')
    address = address_tag.text.strip() if address_tag else 'No address'

    return {
        'title': title,
        'price': price_value,
        'address': address
    }
