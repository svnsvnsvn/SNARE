"""
SNARE Feature Engineering Pipeline
=================================

Production-ready feature engineering pipeline that transforms raw apartment listing data
into the features expected by our trained anomaly detection models.

This module bridges the gap between scraped listing data and model input requirements.
"""

import pandas as pd
import numpy as np
import json
import os
import joblib
from datetime import datetime
from typing import Dict, Any, List, Optional
import re
from sklearn.cluster import DBSCAN


class SNAREFeaturePipeline:
    """
    Feature engineering pipeline for SNARE anomaly detection.
    
    Transforms raw listing data into the 23 features used by our trained models:
    - Temporal patterns (posting time analysis)
    - Linguistic patterns (scam phrases, caps, exclamations)  
    - Geographic patterns (distance from city centers, location clustering)
    - Pricing patterns (price per sqft, duplicates)
    - Metadata patterns (missing info, duplicates)
    """
    
    def __init__(self, models_dir: str = "ml/"):
        """Initialize the feature pipeline with saved model artifacts."""
        self.models_dir = models_dir
        self.scaler = None
        self.feature_config = None
        self.city_centers = None
        self.scam_words = None
        self.load_artifacts()
    
    def load_artifacts(self):
        """Load saved model artifacts needed for feature engineering."""
        try:
            # Load feature scaler
            scaler_path = os.path.join(self.models_dir, "feature_scaler.pkl")
            self.scaler = joblib.load(scaler_path)
            
            # Load feature configuration
            with open(os.path.join(self.models_dir, "feature_config.json"), 'r') as f:
                self.feature_config = json.load(f)
            
            # Load city centers for distance calculations
            with open(os.path.join(self.models_dir, "city_centers.json"), 'r') as f:
                city_centers_data = json.load(f)
                
                # Handle the nested structure: {latitude: {city: lat}, longitude: {city: lon}}
                if 'latitude' in city_centers_data and 'longitude' in city_centers_data:
                    lats = city_centers_data['latitude']
                    lons = city_centers_data['longitude']
                    
                    self.city_centers = {}
                    for city in lats.keys():
                        if city in lons:
                            self.city_centers[city] = {
                                'latitude': lats[city],
                                'longitude': lons[city]
                            }
                else:
                    # Handle flat structure: {city: {latitude: lat, longitude: lon}}
                    self.city_centers = city_centers_data
            
            # Load scam words list
            with open(os.path.join(self.models_dir, "scam_words.json"), 'r') as f:
                scam_config = json.load(f)
                self.scam_words = scam_config['scam_words']
            
            print(f"Feature pipeline artifacts loaded successfully from {self.models_dir}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load feature pipeline artifacts: {str(e)}")
    
    def transform_listing(self, listing_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Transform a single raw listing into engineered features.
        
        Args:
            listing_data: Raw listing data from scraper
            
        Returns:
            DataFrame with single row containing 23 engineered features
        """
        # Convert to DataFrame for consistent processing
        df = pd.DataFrame([listing_data])
        
        # Apply all feature engineering steps
        df = self._engineer_temporal_features(df)
        df = self._engineer_linguistic_features(df)
        df = self._engineer_geographic_features(df)
        df = self._engineer_pricing_features(df)
        df = self._engineer_metadata_features(df)
        df = self._engineer_duplicate_features(df)
        
        # Select only the features expected by the model
        feature_cols = self.feature_config['features']
        df_features = df[feature_cols].copy()
        
        # Handle missing values
        df_features = self._handle_missing_values(df_features)
        
        return df_features
    
    def _engineer_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer temporal pattern features."""
        df = df.copy()
        
        # Parse posting time (handle various formats)
        if 'time_posted' in df.columns:
            try:
                df['time_posted'] = pd.to_datetime(df['time_posted'], utc=True, errors='coerce')
            except:
                df['time_posted'] = pd.NaT
        else:
            # If no time provided, use current time as fallback
            df['time_posted'] = datetime.now()
        
        # Extract temporal features
        df['post_hour'] = df['time_posted'].dt.hour if not df['time_posted'].isna().all() else 12
        df['posted_at_night'] = df['post_hour'].apply(lambda x: x >= 0 and x <= 5 if pd.notna(x) else False)
        
        return df
    
    def _engineer_linguistic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer linguistic pattern features from description text."""
        df = df.copy()
        
        # Ensure description exists
        if 'description' not in df.columns:
            df['description'] = ""
        df['description'] = df['description'].fillna("").astype(str)
        
        # Basic text features
        df['description_length'] = df['description'].str.len()
        df['has_contact_info'] = df['description'].str.contains(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', regex=True, case=False)
        df['num_exclamations'] = df['description'].str.count(r'!+')
        df['num_all_caps'] = df['description'].str.findall(r'\b[A-Z]{2,}\b').str.len()
        
        # Scam phrase detection
        desc_clean = df['description'].str.lower().str.strip()
        
        # Individual scam word flags
        for word in self.scam_words:
            col_name = f'has_{word.replace(" ", "_")}'
            df[col_name] = desc_clean.str.contains(word, regex=False, case=False)
        
        # Aggregate scam metrics
        df['num_scam_phrases'] = sum(
            df[f'has_{word.replace(" ", "_")}'] for word in self.scam_words
        )
        df['scam_phrase_density'] = df['num_scam_phrases'] / np.maximum(df['description_length'], 1)
        
        return df
    
    def _engineer_geographic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer geographic pattern features."""
        df = df.copy()
        
        # Ensure geographic coordinates exist
        if 'latitude' not in df.columns:
            df['latitude'] = np.nan
        if 'longitude' not in df.columns:
            df['longitude'] = np.nan
        if 'city' not in df.columns:
            df['city'] = "Unknown"
        
        # Distance from city center calculation
        df['distance_from_city_center'] = df.apply(self._calculate_city_distance, axis=1)
        
        # Location clustering (simplified for single listing)
        # For production, you might want to cluster against existing database
        df['location_cluster'] = 0  # Default cluster
        df['location_is_noise'] = False  # Default not noise
        
        return df
    
    def _calculate_city_distance(self, row) -> float:
        """Calculate distance from listing to city center."""
        try:
            lat, lon = row['latitude'], row['longitude']
            city = row['city']
            
            if pd.isna(lat) or pd.isna(lon) or city not in self.city_centers:
                return 50.0  # Default distance for unknown locations
            
            city_lat = self.city_centers[city]['latitude']
            city_lon = self.city_centers[city]['longitude']
            
            return self._haversine_distance(lat, lon, city_lat, city_lon)
            
        except Exception:
            return 50.0  # Fallback distance
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate haversine distance between two points in kilometers."""
        R = 6371  # Earth radius in km
        
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        return R * c
    
    def _engineer_pricing_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer pricing pattern features."""
        df = df.copy()
        
        # Ensure price and square footage exist (but don't override with defaults)
        if 'price' not in df.columns:
            df['price'] = np.nan  # Don't default to 0, let it be NaN if missing
        if 'square_footage' not in df.columns:
            df['square_footage'] = np.nan
        
        df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Remove .fillna(0)
        df['square_footage'] = pd.to_numeric(df['square_footage'], errors='coerce')
        
        # Price per square foot
        df['price_per_sqft'] = df['price'] / df['square_footage']
        df['price_per_sqft'] = df['price_per_sqft'].replace([np.inf, -np.inf], np.nan)
        df['price_per_sqft_missing'] = df['price_per_sqft'].isna()
        
        # Bedroom to bathroom ratio
        if 'bedrooms' not in df.columns:
            df['bedrooms'] = 0
        if 'bathrooms' not in df.columns:
            df['bathrooms'] = 1
            
        df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce').fillna(0)
        df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce').fillna(1)
        
        df['bed_bath_ratio'] = df['bedrooms'] / df['bathrooms'].replace(0, np.nan)
        
        return df
    
    def _engineer_metadata_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer metadata pattern features."""
        df = df.copy()
        
        # Missing address information flags
        df['address_missing'] = df.get('address', '').isna() | (df.get('address', '') == '') | df.get('address', '').str.strip().eq('')
        df['city_missing'] = df.get('city', '').isna() | (df.get('city', '') == '') | df.get('city', '').str.strip().eq('')
        df['state_missing'] = df.get('state', '').isna() | (df.get('state', '') == '') | df.get('state', '').str.strip().eq('')
        df['postal_code_missing'] = df.get('postal_code', '').isna() | (df.get('postal_code', '') == '') | df.get('postal_code', '').str.strip().eq('')
        df['square_footage_missing'] = df.get('square_footage', np.nan).isna()
        
        return df
    
    def _engineer_duplicate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer duplicate pattern features (simplified for single listing)."""
        df = df.copy()
        
        # For single listing, these are defaults (would be calculated against database in production)
        df['name_dup_count'] = 1
        df['desc_dup_count'] = 1
        df['price_std_in_desc'] = 0
        df['sqft_std_in_desc'] = 0
        df['desc_mismatch_flag'] = False
        df['desc_grouped'] = False
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in engineered features."""
        df = df.copy()
        
        # Fill numeric features with appropriate defaults
        numeric_defaults = {
            'latitude': 27.7663,  # Florida center
            'longitude': -82.6404,
            'bedrooms': 1,
            'bathrooms': 1,
            'square_footage': 800,
            'post_hour': 12,
            'name_dup_count': 1,
            'num_exclamations': 0,
            'num_all_caps': 0,
            'price_per_sqft': 2.0,
            'location_cluster': 0,
            'desc_dup_count': 1,
            'description_length': 100,
            'num_scam_phrases': 0,
            'scam_phrase_density': 0.0,
            'distance_from_city_center': 10.0,
            'bed_bath_ratio': 1.0
        }
        
        for col, default_val in numeric_defaults.items():
            if col in df.columns:
                df[col] = df[col].fillna(default_val)
        
        # Fill boolean features with False
        boolean_cols = [col for col in df.columns if col.endswith('_missing') or col.startswith('posted_at_') or col.startswith('has_') or col.endswith('_flag') or col.endswith('_grouped') or col.endswith('_noise')]
        for col in boolean_cols:
            if col in df.columns:
                df[col] = df[col].fillna(False)
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get the list of feature names expected by the model."""
        return self.feature_config['features']
    
    def transform_and_scale(self, listing_data: Dict[str, Any]) -> np.ndarray:
        """
        Transform listing and apply scaling for model input.
        
        Args:
            listing_data: Raw listing data
            
        Returns:
            Scaled feature array ready for model prediction
        """
        # Transform to features
        df_features = self.transform_listing(listing_data)
        
        # Apply scaling
        X_scaled = self.scaler.transform(df_features)
        
        return X_scaled
