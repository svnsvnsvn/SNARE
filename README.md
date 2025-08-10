# SNARE: Rental Listing Anomaly Detection Research Platform

**SNARE (Scam Network Anomaly Recognition Engine)** is a research platform for experimenting with machine learning approaches to detect anomalous rental listings. This project explores anomaly detection techniques applied to real estate data collected primarily from Florida markets.

---

## Research Context

This project began as a hackathon experiment and has evolved into a comprehensive study of anomaly detection in rental listing data. The platform demonstrates data collection, feature engineering, and machine learning implementation rather than serving as a production tool.

---

## Features

### Advanced Anomaly Detection
- **Machine Learning Ensemble:**
  - Isolation Forest for outlier detection
  - DBSCAN for clustering-based anomaly identification  
  - Local Outlier Factor (LOF) for density-based detection
- **Analyzed Features:**
  - Price metrics (price per bedroom, price per square foot)
  - Suspicious keywords in listing descriptions
  - Phone number and contact patterns
  - Geographic proximity to population centers

### Web Scraping Implementation
- Data collection from Craigslist and other rental platforms
- Two scraping modes:
  1. Individual listing analysis for real-time evaluation
  2. Batch data collection for model training and research

### Feature Engineering Pipeline
- Automated feature extraction from raw listing data
- Price ratio calculations and statistical analysis
- Keyword frequency and sentiment analysis
- Geographic and temporal feature generation

### Data Storage and Management
- SQLite database for local development and research
- Listing storage, model predictions, and retraining logs
- Data export capabilities for further analysis

### Web Interface
- React-based frontend with Vite development server
- FastAPI backend for ML model integration
- Interactive form for listing URL submission and analysis

### Model Retraining Infrastructure
- Automated retraining pipeline for model updates
- Performance tracking and model versioning
- Data drift detection and model validation

---

## Technical Stack

| Component         | Technology                     |
|-------------------|--------------------------------|
| **Frontend**      | React, Vite, Tailwind CSS     |
| **Backend**       | FastAPI, Python               |
| **Database**      | SQLite                         |
| **Machine Learning** | Scikit-learn, NumPy, Pandas   |
| **Web Scraping**  | BeautifulSoup, Selenium        |

---

## Installation

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

## Usage

### 1. Data Collection
- Use the web interface to submit individual listing URLs for analysis
- Batch scraping capabilities for research data collection

### 2. Analysis Results
- View anomaly scores and model predictions through the web interface
- Export results for further analysis and research

### 3. API Integration
- RESTful API endpoints for programmatic access to the anomaly detection service
- FastAPI documentation available at http://localhost:8000/docs

---

## Research Applications

- **Academic Study:** Analyzing patterns in rental listing anomalies
- **Data Science Portfolio:** Demonstrating end-to-end ML pipeline implementation  
- **Algorithm Research:** Comparing ensemble anomaly detection approaches
- **Feature Engineering:** Exploring real estate data characteristics

---

## Development Notes

This platform represents a learning exercise and research tool rather than a production system. The models demonstrate interesting patterns in the data but require significant additional validation and refinement for practical deployment.

Key technical achievements:
- End-to-end ML pipeline from data collection to web interface
- Ensemble anomaly detection with multiple algorithms
- Feature engineering for real estate domain
- Full-stack implementation with modern web technologies

---
