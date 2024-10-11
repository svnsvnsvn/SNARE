import requests
from bs4 import BeautifulSoup

def scrape_apartments(url):
    """Scrapes an Apartments.com listing and returns listing data."""
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        return None
    
    title = soup.find('h1', class_='propertyName').text.strip() if soup.find('h1', class_='propertyName') else 'No title'
    price_tag = soup.find('span', class_='rentRange')
    price_value = price_tag.text.strip() if price_tag else 'No price'
    address_tag = soup.find('div', class_='propertyAddress')
    address = address_tag.text.strip() if address_tag else 'No address'

    return {
        'title': title,
        'price': price_value,
        'address': address
    }
