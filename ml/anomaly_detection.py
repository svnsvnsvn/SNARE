import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

"""
TODO List for Dataset Enrichment:

1. Convert Price to Numeric:
   - Convert the 'price' field (e.g., '$1,349') to a floating-point number for easier manipulation.
   - This will allow the creation of derived features like 'price per bedroom' and 'price per bathroom'.

2. Derived Features:
   - Price per Bedroom: Calculate the price per bedroom by dividing the total price by the number of bedrooms.
   - Price per Bathroom: Similarly, calculate price per bathroom.
   - Price per Square Foot: If square footage is available, compute price per square foot for better comparisons across listings.

3. Latitude and Longitude as Numeric:
   - Ensure that latitude and longitude are stored as floating-point numbers so they can be used for geospatial calculations, such as distances to points of interest.

4. Listing Age:
   - Calculate how many days the listing has been live by subtracting 'time_posted' from the current date.
   - Older listings without activity might indicate suspicious or fraudulent behavior.

5. Suspicious Keywords:
   - Implement a search for specific keywords that could indicate scams or fraudulent behavior. For example, "wire money," "Western Union," or "cash only."
   - Create a binary flag (0 or 1) based on whether these keywords are present in the description.

6. Description Length:
   - Calculate the length of the listing's description (number of characters). 
   - Short or overly vague descriptions might be an indicator of scams.

7. Amenities Count:
   - Count the number of amenities mentioned in the description. 
   - Listings with a very high or very low number of amenities may be suspicious. 
   - Examples include 'Dishwasher', 'Walk-In Closet', 'Ceiling Fan', etc. 
   - Create binary flags for the presence of important amenities, e.g., 'has_dishwasher', 'has_in_unit_laundry', etc.

8. Image Extraction:
   - Extract the URLs of the listing's images for potential use in reverse image searches, which can help detect reused or stock images, a common scam tactic.
   - You could also count the number of images as a potential feature (listings with few or no images may be more suspicious).

9. Geospatial Features:
   - Calculate distances between the listing and key locations (e.g., universities, city centers, military bases).
   - Listings that are geographically far from points of interest but have high prices could be flagged for further investigation.

10. Phone Number Extraction:
   - If the phone number is available in the description, extract it and store it. 
   - Use it to identify duplicate listings that share the same contact information.

11. Duplicate Listings:
   - Track listings with similar or identical attributes (e.g., price, address, or phone number).
   - Repeated listings in multiple locations may indicate fraudulent behavior.

12. Clustering and Anomaly Detection (Future Step):
   - Once the dataset is enriched, use clustering techniques like DBSCAN or Isolation Forest to group similar listings and detect outliers.
   - Listings that deviate significantly from their clusters in terms of price, amenities, or other features could be considered suspicious.

13. Testing:
   - After enriching the dataset, test the scraping functions on multiple listings to ensure robustness.
   - Handle edge cases where certain fields (like price or address) might be missing or formatted inconsistently.
   - Verify that all derived features are calculated correctly and ensure that numeric and categorical data are properly formatted for model training.

14. Expanding to Other Platforms:
   - After refining the Craigslist scraper, extend similar scraping and enrichment logic to other platforms like Zillow and Apartments.com.
   - Be mindful of differences in HTML structure and the availability of different features on these sites.

REMINDER:
- * Before proceeding to model training, ensure all scraped data is consistent, and any missing values are handled appropriately. *
- Consider whether additional features (e.g., temporal patterns or property types) would help improve your fraud detection model.
"""


# -----------------------------------------
# Data Preprocessing
# -----------------------------------------
def preprocess_data(listing_data):
    '''
    Preprocesses a single listing by scaling its features.

    Args:
        listing_data: the single listing to be pre-processed.

    Returns:
        tuple: Scaled feature values, original DataFrame.

    '''
    print("First attempting to preprocess the data...")

    # Convert the scraped data (dictionary) into a DataFrame with a single row
    df = pd.DataFrame([listing_data])

    print(df.head())

    # List of features that you want to scale (must match model's feature set)
    # TODO: Should be the columns of the df because price per ratios and all the engineered features will have to be remade.
    features = ['Price per Bedroom', 'Price per Full Bathroom', 'Price per Total Bathroom',
                'Price per Story', 'Price per Garage Space', 'Price per Living Area',
                'Price per Lot Size Acre', 'Price per Year Built', 'Under_30_Days_Flag',
                'Distance Suspiciousness', 'is_phone_suspicious', 'contains_suspicious_diction']
    
    # Standardize the features using StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    
    return X_scaled, df

# -----------------------------------------
# Isolation Forest Anomaly Detection
# -----------------------------------------
def isolation_forest_anomaly_detection(df, contamination=0.05):
    '''
    Applies isolation forest for anomaly detection.

    Args:
        df (DataFrame): DataFrame containing the features to be analyzed.
        contamination (float): The proportion of anomalies in the data.

    Returns:
        DataFrame: DataFrame with 'is_anomaly_iso' flag (1 for anomaly, 0 for normal).
    '''
    X_scaled, _ = preprocess_data(df)
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    anomaly_flags = iso_forest.fit_predict(X_scaled)  # Fit and predict anomalies
    df['is_anomaly_iso'] = (anomaly_flags == -1).astype(int)  # Flag anomalies as 1
    return df

# -----------------------------------------
# DBSCAN Anomaly Detection
# -----------------------------------------

def dbscan_anomaly_detection(df, eps=0.5, min_samples=5):
    '''
    Applies DBSCAN for anomaly detection.
        
        Args:
            df (DataFrame): DataFrame containing the features to be analyzed.
            eps (float): Maximum distance between two samples for them to be considered as in the same cluster.
            min_samples (int): Minimum number of samples to form a cluster.
        
        Returns:
            DataFrame: DataFrame with 'is_anomaly_dbscan' flag (1 for anomaly, 0 for normal).
    '''
    X_scaled, _ = preprocess_data(df)
    dbscan = DBSCAN(eps=eps, min_samples = min_samples)
    dbscan_labels = dbscan.fit_predict(X_scaled) # DBSCAN clusters
    df['is_anomaly_dbscan'] = np.where(dbscan_labels == -1,1,0) # Flag anomalies
    return df

def combined_anomaly_detection(df):
    '''
    Applies both Isolation Forest and DBSCAN and combines their results.
    
    Args:
        listing_data (dict): A dictionary of listing features.
    
    Returns:
        DataFrame: DataFrame with combined anomaly detection results ('is_anomaly_combined').
    '''
    df = isolation_forest_anomaly_detection(df)
    df = dbscan_anomaly_detection(df)
    
    # If either model flags an anomaly, we flag it as suspicious
    df['is_anomaly_combined'] = np.where((df['is_anomaly_iso'] == 1) | (df['is_anomaly_dbscan'] == 1), 1, 0)
    return df

# -----------------------------------------
# Continuous Learning / Retraining the Model
# -----------------------------------------
def retrain_model(initial_df, new_listings_df):
    """
    Retrains the model using new listings data combined with the initial training data.
    
    Args:
        initial_df (DataFrame): The original dataset used to train the model.
        new_listings_df (DataFrame): New listings to be added to the training set.
    
    Returns:
        tuple: Retrained Isolation Forest and DBSCAN models.
    """
    # Combine the initial dataset with new listings
    combined_df = pd.concat([initial_df, new_listings_df], ignore_index=True)
    
    # Re-preprocess the data
    X_scaled, _ = preprocess_data(combined_df)
    
    # Retrain Isolation Forest
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    iso_forest.fit(X_scaled)
    
    # Retrain DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan.fit(X_scaled)
    
    return iso_forest, dbscan  # Return the updated models

# -----------------------------------------
# Example for Detection in Production
# -----------------------------------------
def detect_anomalies(listing_data):
    """
    Detects anomalies for a given listing data using the combined anomaly detection method.
    
    Args:
        listing_data (dict): A dictionary of listing features.
    
    Returns:
        DataFrame: Listings flagged as anomalies.
    """
    df_with_anomalies = combined_anomaly_detection(listing_data)
    
    # Return only the rows flagged as anomalies
    return df_with_anomalies[df_with_anomalies['is_anomaly_combined'] == 1]