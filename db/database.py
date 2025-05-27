import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  

# Connection string for PostgreSQL (use your database credentials)
DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres.fxqhhoszoafxgikxbbpy',
    'password': os.getenv('DB_PWD'),
    'host': 'aws-0-us-east-1.pooler.supabase.com',  # or use your cloud hostname
    'port': '6543'
}

# Schema name (usually 'auth' in Supabase)
schema = 'public'

def create_connection():
    """Create a database connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def create_tables():
    """Create tables for Craigslist, Zillow, and Apartments.com listings if they don't already exist."""
    conn = create_connection()
    cursor = conn.cursor()

    # Create Craigslist table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.craigslist_listings (
        listing_id TEXT PRIMARY KEY,
        listing_name TEXT,
        price REAL,  -- Converted to a REAL number for better handling in database
        address TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        latitude REAL,
        longitude REAL,
        bedrooms REAL,
        bathrooms REAL,
        time_posted TEXT,
        description TEXT,
        phone_number TEXT,  -- Storing phone numbers as text since they may contain non-numeric characters (e.g., hyphens)
        square_footage REAL -- Square footage as a real number
        )
    ''')

    # TODO CONVERT PRICE, LONG, LAT INTO NUMERICAL VALUE, ADD NEW FEATURES 

    # Create Zillow table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.zillow_listings (
            listing_id TEXT PRIMARY KEY,
            listing_name TEXT,
            price TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            postal_code TEXT,
            latitude REAL,
            longitude REAL,
            bedrooms REAL,
            bathrooms REAL,
            time_posted TEXT
        )
    ''')

    # Create Apartments.com table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.apartments_listings (
            listing_id TEXT PRIMARY KEY,
            listing_name TEXT,
            price TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            postal_code TEXT,
            latitude REAL,
            longitude REAL,
            bedrooms REAL,
            bathrooms REAL,
            time_posted TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_listing(listing_data, table_name):
    """Insert listing data into the appropriate PostgreSQL table."""
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
            INSERT INTO {schema}.{table_name} (
                listing_id, listing_name, price, address, city, state, postal_code, 
                latitude, longitude, bedrooms, bathrooms, time_posted
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (listing_id) DO NOTHING
        ''', (
            listing_data['listing_id'], listing_data.get('listing_name', 'No title'), listing_data['price'], 
            listing_data['address'], listing_data['city'], listing_data['state'], listing_data['postal_code'], 
            listing_data['latitude'], listing_data['longitude'], listing_data['bedrooms'], 
            listing_data['bathrooms'], listing_data['time_posted']
        ))

        conn.commit()
        print(f"Listing {listing_data['listing_id']} inserted into {table_name}.")
    except psycopg2.Error as e:
        print(f"Error inserting listing into {table_name}: {e}")
    finally:
        conn.close()

create_tables()