# Snare: Apartment Listing Anomaly Detector

**Snare (Scam Network Anomaly Recognition Engine)** is an anomaly detection tool designed to protect users from fraudulent apartment listings on platforms such as Craigslist, Zillow, and Apartments.com. By combining machine learning techniques with robust data collection, Snare helps users identify scams and make informed decisions.

---

## Why Snare?

Apartment rental scams cost individuals thousands of dollars each year. **Snare** aims to solve this problem by leveraging anomaly detection algorithms and domain-specific insights to flag suspicious listings before users fall victim.

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

2. Set up environment variables:
   ```bash
   # Copy the example environment file and configure it
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install frontend dependencies:
   ```bash
   cd snare-web-frontend
   npm install
   cd ..
   ```

5. Run the application:

   **Development Mode (recommended):**
   ```bash
   # Terminal 1: Start backend server
   python run_server.py
   
   # Terminal 2: Start frontend development server
   cd snare-web-frontend
   npm run dev
   ```

   **Alternative backend start:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the application:
   - **Frontend:** http://localhost:3000
   - **Backend API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs

### Quick Setup Script
For automated setup, run:
```bash
chmod +x setup_dev.sh
./setup_dev.sh
```

### Environment Configuration

The application supports flexible configuration through environment variables:

**Backend (.env):**
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 127.0.0.1)
- `CORS_ALLOW_ORIGINS`: Allowed frontend origins
- API keys and database credentials

**Frontend (snare-web-frontend/.env):**
- `VITE_API_BASE_URL`: Backend API URL (default: http://127.0.0.1:8000)
- Environment-specific configurations available

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
