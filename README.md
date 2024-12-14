# Snare: Apartment Listing Anomaly Detector

Snare is an anomaly detection tool designed to identify fraudulent apartment listings on platforms such as Craigslist, Zillow, and Apartments.com. By leveraging machine learning techniques and a combination of supervised and unsupervised models, Snare flags suspicious listings to protect users from scams.

---

## Features

### 1. **Data Collection**
- Scrapes data from platforms like Craigslist, Zillow, and Apartments.com.
- Two scraping functions:
  - Scrape individual listings provided by the user.
  - Scrape multiple listings and add them to the database for model analysis.

### 2. **Anomaly Detection**
- **Techniques Used:**
  - Isolation Forest
  - DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **Analyzed Features:**
  - Price metrics (e.g., price per bedroom, price per square foot).
  - Presence of suspicious words in descriptions.
  - Phone number patterns (e.g., multiple agent associations).
  - Proximity to important locations like universities and military bases.

### 3. **Database Integration**
- Powered by **PostgreSQL** via Supabase for efficient data storage and retrieval.

### 4. **API**
- Built with **FastAPI** to serve anomaly detection results.

### 5. **Web Interface**
- User-friendly interface for submitting URLs and receiving detailed anomaly detection insights.

### 6. **Model Retraining**
- Logic implemented for retraining the model when new data is added, ensuring continuous improvement.

---

## Technical Details

### Architecture
1. **Web Scraping**
   - Extracts key features such as price, address, bedrooms, bathrooms, time posted, and more.
   - Ensures robust handling of incomplete data (e.g., missing phone numbers).

2. **Machine Learning**
   - Combines supervised and unsupervised techniques for robust anomaly detection.
   - Key features include:
     - Distance Suspiciousness: Calculates suspiciousness based on proximity to high-population areas.
     - Contains Suspicious Diction: Flags listings with scammy keywords.
     - Phone Number Patterns: Detects anomalies in phone number usage.

3. **Database**
   - PostgreSQL stores listing data, model outputs, and retraining logs.

4. **Deployment**
   - Target platforms: Heroku, AWS.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/svnsvnsvn/snare.git
   cd snare
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database via Supabase:
   - Follow Supabase setup instructions [here](https://supabase.com/).
   - Add your database credentials to `.env`.

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Usage

1. **Scraping Listings**
   - Use the web interface to submit URLs or batch scrape listings.

2. **View Results**
   - Analyze flagged listings through the web interface.

3. **API Integration**
   - Use the provided FastAPI endpoints for custom integrations.

---

## Future Enhancements

- Improve scraping functionality for additional platforms.
- Add advanced fraud detection metrics (e.g., image analysis).

---
