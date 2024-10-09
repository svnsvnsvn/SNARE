import os
import pandas as pd
from ml.anomaly_detection import retrain_model

def retrain_if_needed():
    """
    Retrains the model if enough new listings have been processed.
    """
    # TODO: Make DB for this
    # Load initial dataset and new listings
    initial_df = pd.read_csv("data/final_training_set.csv")
    if os.path.exists("data/new_listings.csv"):
        new_df = pd.read_csv("data/new_listings.csv")
    else:
        new_df = pd.DataFrame()  # Empty DataFrame if no new listings

    # If we have enough new listings, retrain the model
    if len(new_df) >= 100:  # Retrain after every 100 new listings
        iso_forest, dbscan = retrain_model(initial_df, new_df)
        print("Model retrained successfully.")
        
        # Optionally, remove the new listings file after retraining
        os.remove("data/new_listings.csv")
