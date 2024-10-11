import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

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
def save_new_listing(listing_data):
    # TODO: Make DB for this

    # Save the new listing to a CSV or database for retraining
    new_data = pd.DataFrame([listing_data])
    new_data.to_csv("data/new_listings.csv", mode='a', header=False, index=False)

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