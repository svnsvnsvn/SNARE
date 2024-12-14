# Snare: Apartment Listing Anomaly Detector

**Snare** is a cutting-edge anomaly detection tool designed to protect users from fraudulent apartment listings on platforms such as Craigslist, Zillow, and Apartments.com. By combining state-of-the-art machine learning techniques with robust data collection, Snare helps users identify scams and make informed decisions.

---

## Why Snare?

Apartment rental scams cost individuals thousands of dollars each year. **Snare** aims to solve this problem by leveraging advanced anomaly detection algorithms and domain-specific insights to flag suspicious listings before users fall victim.

---

## Features 🚀

### 🔍 Advanced Anomaly Detection
- **Machine Learning Techniques:**
  - Isolation Forest for identifying outliers.
  - DBSCAN for clustering and density-based anomaly detection.
- **Analyzed Features:**
  - Price metrics (e.g., price per bedroom, price per square foot).
  - Presence of suspicious words in descriptions.
  - Phone number patterns (e.g., multiple agent associations).
  - Proximity to high-population areas and points of interest.

### 🌐 Comprehensive Web Scraping
- Scrapes data from Craigslist, Zillow, and Apartments.com.
- Two scraping functions:
  1. Scrape individual listings based on user input.
  2. Batch scrape listings for database analysis and model training.

### 📊 Intelligent Feature Engineering
- Flags anomalies based on:
  - Price ratios.
  - Keyword analysis (e.g., scammy language).
  - Phone number and contact patterns.
  - Time on market and proximity to key locations.

### 💾 Robust Database Integration
- Powered by **PostgreSQL** via Supabase for scalable and efficient data storage.
- Tracks listings, model results, and retraining logs.

### 🌟 User-Friendly Web Interface
- Built with **FastAPI** for streamlined API interactions.
- Intuitive web interface for submitting URLs and receiving detection insights.

### 🔄 Continuous Model Improvement
- Implements logic for retraining anomaly detection models based on new data, ensuring continuous refinement and accuracy.

---

## Technical Stack 💻

| Stack Component   | Technology Used                |
|-------------------|--------------------------------|
| **Frontend**      | HTML, CSS, JavaScript          |
| **Backend**       | FastAPI, Python                |
| **Database**      | PostgreSQL, Supabase           |
| **Machine Learning** | Scikit-learn, NumPy, Pandas     |
| **Web Scraping**  | BeautifulSoup, Selenium        |

---

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/svnsvnsvn/snare.git
   cd snare
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database via Supabase:
   - Follow Supabase setup instructions [here](https://supabase.com/).
   - Add your database credentials to `.env`.

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the web interface at `http://localhost:8000`.

---

## Usage 📚

### 1. Scraping Listings
- Use the web interface to submit URLs for analysis or batch scrape listings into the database.

### 2. View Results
- Analyze flagged listings directly from the web interface.

### 3. API Integration
- Integrate Snare with your existing tools via its FastAPI-powered API endpoints.

---

## Real-World Applications 🌍

- **Individual Renters:** Identify fraudulent listings before engaging.
- **Real Estate Platforms:** Enhance user trust by integrating Snare's detection engine.
- **Market Analysts:** Study patterns of fraudulent activity in the housing market.

---

## Future Roadmap 🛤️

- **Image Analysis:** Integrate AI to detect anomalies in listing photos.
- **Enhanced Scalability:** Add multi-threaded scraping and caching for high-performance data collection.
- **Community Integration:** Allow users to report and share flagged listings.

---
