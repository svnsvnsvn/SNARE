import sqlite3
import os

# Database file path
db_path = ('scraped_listings.db')

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    """Create a table for storing apartment listings."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS listings (
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

def insert_listing(listing_data):
    """Insert a new listing into the listings table."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO listings (
        listing_id, listing_name, price, address, city, state, postal_code,
        latitude, longitude, bedrooms, bathrooms, time_posted
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        listing_data.get('listing_id'),
        listing_data.get('listing_name'),
        listing_data.get('price'),
        listing_data.get('address'),
        listing_data.get('city'),
        listing_data.get('state'),
        listing_data.get('postal_code'),
        listing_data.get('latitude'),
        listing_data.get('longitude'),
        listing_data.get('bedrooms'),
        listing_data.get('bathrooms'),
        listing_data.get('time_posted')
    ))

    conn.commit()
    conn.close()

# Call create_table() to make sure the table is created when the script runs
create_table()
