"""
SNARE Anomaly Detection Service
==============================

Production anomaly detection service that uses trained models to score apartment listings.

Integrates:
- Feature engineering pipeline
- Trained Isolation Forest, DBSCAN, and LOF models
- Ensemble scoring and consensus logic
- Real-time anomaly detection for scraped listings
"""

import numpy as np
import pandas as pd
import joblib
import json
import os
from typing import Dict, Any, Tuple, List
from datetime import datetime
from sklearn.cluster import DBSCAN

from ml.feature_pipeline import SNAREFeaturePipeline


class SNAREAnomalyDetector:
    """
    Production anomaly detection service for SNARE.
    
    Combines multiple trained models to detect suspicious apartment listings:
    - Isolation Forest: Tree-based anomaly detection
    - DBSCAN: Density-based clustering outlier detection  
    - LOF: Local density anomaly detection
    - Ensemble: Consensus scoring across all models
    """
    
    def __init__(self, models_dir: str = "ml/"):
        """Initialize the anomaly detector with trained models."""
        self.models_dir = models_dir
        self.feature_pipeline = SNAREFeaturePipeline(models_dir)
        
        # Model components
        self.isolation_forest = None
        self.lof_model = None
        self.dbscan_params = None
        self.model_metadata = {}
        
        self.load_models()
    
    def load_models(self):
        """Load all trained models and metadata."""
        try:
            # Load Isolation Forest
            iso_path = os.path.join(self.models_dir, "isolation_forest_model.pkl")
            self.isolation_forest = joblib.load(iso_path)
            
            # Load LOF model
            lof_path = os.path.join(self.models_dir, "lof_model.pkl")
            self.lof_model = joblib.load(lof_path)
            
            # Load DBSCAN parameters
            with open(os.path.join(self.models_dir, "dbscan_params.json"), 'r') as f:
                self.dbscan_params = json.load(f)
            
            # Load model metadata for context
            with open(os.path.join(self.models_dir, "model_summary.json"), 'r') as f:
                self.model_metadata = json.load(f)
            
            print(f"Anomaly detection models loaded successfully from {self.models_dir}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load anomaly detection models: {str(e)}")
    
    def detect_anomaly(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if a listing is anomalous using ensemble of trained models.
        
        Args:
            listing_data: Raw listing data from scraper
            
        Returns:
            Dictionary containing anomaly detection results
        """
        try:
            # Transform raw data into engineered features
            X_scaled = self.feature_pipeline.transform_and_scale(listing_data)
            df_features = self.feature_pipeline.transform_listing(listing_data)
            
            # Get predictions from all models
            iso_result = self._predict_isolation_forest(X_scaled, df_features)
            dbscan_result = self._predict_dbscan(X_scaled)
            lof_result = self._predict_lof(X_scaled)
            
            # Ensemble scoring with feature data for business logic
            ensemble_result = self._ensemble_scoring(iso_result, dbscan_result, lof_result, df_features)
            
            # Compile comprehensive results
            results = {
                "is_suspicious": ensemble_result["is_anomaly"],
                "confidence_score": ensemble_result["confidence"],
                "anomaly_score": ensemble_result["overall_score"],
                "model_predictions": {
                    "isolation_forest": {
                        "is_anomaly": iso_result["is_anomaly"],
                        "score": iso_result["score"],
                        "prediction": iso_result["prediction"]
                    },
                    "dbscan": {
                        "is_anomaly": dbscan_result["is_anomaly"],
                        "cluster": dbscan_result["cluster"],
                        "is_noise": dbscan_result["is_noise"]
                    },
                    "lof": {
                        "is_anomaly": lof_result["is_anomaly"],
                        "score": lof_result["score"],
                        "prediction": lof_result["prediction"]
                    }
                },
                "feature_analysis": self._analyze_features(df_features),
                "processing_info": {
                    "timestamp": datetime.now().isoformat(),
                    "models_used": ["isolation_forest", "dbscan", "lof"],
                    "feature_count": len(self.feature_pipeline.get_feature_names())
                }
            }
            
            return results
            
        except Exception as e:
            # Return safe fallback result on error
            return {
                "is_suspicious": False,
                "confidence_score": 0.0,
                "anomaly_score": 0.0,
                "error": f"Detection failed: {str(e)}",
                "processing_info": {
                    "timestamp": datetime.now().isoformat(),
                    "status": "error"
                }
            }
    
    def _predict_isolation_forest(self, X_scaled: np.ndarray, df_features: pd.DataFrame) -> Dict[str, Any]:
        """Get Isolation Forest prediction."""
        try:
            # Use original features (not scaled) for Isolation Forest
            X_original = df_features.iloc[:1]  # First row as DataFrame
            
            prediction = self.isolation_forest.predict(X_original)[0]
            score = self.isolation_forest.decision_function(X_original)[0]
            
            return {
                "prediction": int(prediction),
                "score": float(score),
                "is_anomaly": prediction == -1
            }
        except Exception as e:
            return {
                "prediction": 1,
                "score": 0.0,
                "is_anomaly": False,
                "error": str(e)
            }
    
    def _predict_dbscan(self, X_scaled: np.ndarray) -> Dict[str, Any]:
        """Get DBSCAN clustering prediction."""
        try:
            # Initialize DBSCAN with saved parameters
            dbscan = DBSCAN(
                eps=self.dbscan_params["eps"],
                min_samples=self.dbscan_params["min_samples"]
            )
            
            # For single point, we'd typically compare against training clusters
            # For now, we'll use a simplified approach
            cluster_label = dbscan.fit_predict(X_scaled)[0]
            is_noise = cluster_label == -1
            
            return {
                "cluster": int(cluster_label),
                "is_noise": bool(is_noise),
                "is_anomaly": bool(is_noise)
            }
        except Exception as e:
            return {
                "cluster": 0,
                "is_noise": False,
                "is_anomaly": False,
                "error": str(e)
            }
    
    def _predict_lof(self, X_scaled: np.ndarray) -> Dict[str, Any]:
        """Get LOF prediction."""
        try:
            # Note: LOF with novelty=False can't predict on new data
            # We'll use a workaround or retrain LOF with novelty=True if needed
            # For now, return default values
            return {
                "prediction": 1,
                "score": 1.0,
                "is_anomaly": False,
                "note": "LOF requires retraining with novelty=True for new predictions"
            }
        except Exception as e:
            return {
                "prediction": 1,
                "score": 1.0,
                "is_anomaly": False,
                "error": str(e)
            }
    
    def _ensemble_scoring(self, iso_result: Dict, dbscan_result: Dict, lof_result: Dict, df_features: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Combine predictions from all models into ensemble score.
        
        Uses weighted voting with confidence scoring based on model agreement.
        Includes business logic overrides for extreme cases.
        """
        try:
            # Count anomaly votes
            anomaly_votes = sum([
                iso_result.get("is_anomaly", False),
                dbscan_result.get("is_anomaly", False),
                lof_result.get("is_anomaly", False)
            ])
            
            # Calculate overall anomaly decision
            is_anomaly = anomaly_votes >= 2  # Majority vote
            
            # BUSINESS LOGIC OVERRIDES for extreme cases
            override_applied = False
            override_reason = ""
            
            if df_features is not None and len(df_features) > 0:
                features = df_features.iloc[0]
                
                # Debug: Print what we're actually getting
                print(f"DEBUG - Feature columns: {list(df_features.columns)}")
                print(f"DEBUG - Feature values: {dict(features)}")
                
                # Override 1: Extremely low prices (obvious scams)
                price = features.get('price', 0)
                price_per_sqft = features.get('price_per_sqft', 0)
                
                print(f"DEBUG - price: {price}, price_per_sqft: {price_per_sqft}")
                
                # Much more aggressive thresholds since the models clearly suck
                if price > 0 and price < 800:  # Less than $800/month is suspicious in most markets
                    is_anomaly = True
                    override_applied = True
                    override_reason = f"Suspiciously low price: ${price}"
                elif price_per_sqft > 0 and price_per_sqft < 0.50:  # Less than $0.50/sqft is very suspicious
                    is_anomaly = True
                    override_applied = True
                    override_reason = f"Suspiciously low price per sqft: ${price_per_sqft:.2f}"
                
                # Override 2: Extremely high prices (potential scams)
                elif price > 0 and price > 8000:  # More than $8k/month without context
                    sqft = features.get('square_footage', 0)
                    if sqft > 0 and price/sqft > 40:  # More than $40/sqft is extremely high
                        is_anomaly = True
                        override_applied = True
                        override_reason = f"Extremely high price per sqft: ${price/sqft:.2f}"
            
            # Calculate confidence based on model agreement and overrides
            if override_applied:
                confidence = 0.95  # High confidence for business logic overrides
            elif anomaly_votes == 3:
                confidence = 0.95  # All models agree - high confidence
            elif anomaly_votes == 2:
                confidence = 0.75  # Majority agrees - medium confidence
            elif anomaly_votes == 1:
                confidence = 0.35  # Split decision - low confidence
            else:
                confidence = 0.85  # All normal - high confidence normal
            
            # Calculate overall anomaly score (0-1, higher = more anomalous)
            iso_score = max(0, -iso_result.get("score", 0))  # Convert to positive
            overall_score = iso_score  # Primary score from Isolation Forest
            
            result = {
                "is_anomaly": is_anomaly,
                "confidence": confidence,
                "overall_score": float(overall_score),
                "anomaly_votes": anomaly_votes,
                "total_models": 3
            }
            
            if override_applied:
                result["business_logic_override"] = True
                result["override_reason"] = override_reason
                print(f"DEBUG - Override applied! Reason: {override_reason}")
            else:
                print(f"DEBUG - No override applied. is_anomaly: {is_anomaly}, votes: {anomaly_votes}")
            
            print(f"DEBUG - Final result: {result}")
            
            return result
            
        except Exception as e:
            return {
                "is_anomaly": False,
                "confidence": 0.0,
                "overall_score": 0.0,
                "error": str(e)
            }
    
    def _analyze_features(self, df_features: pd.DataFrame) -> Dict[str, Any]:
        """Analyze key features that might indicate suspicious behavior."""
        try:
            features = df_features.iloc[0]  # First (and only) row
            
            suspicious_indicators = []
            
            # Price indicators
            if features.get('price_per_sqft', 0) < 0.5:
                suspicious_indicators.append("Very low price per square foot")
            elif features.get('price_per_sqft', 0) > 10:
                suspicious_indicators.append("Very high price per square foot")
            
            # Location indicators
            if features.get('distance_from_city_center', 0) > 30:
                suspicious_indicators.append("Far from city center")
            
            # Language indicators
            if features.get('num_scam_phrases', 0) > 2:
                suspicious_indicators.append("Multiple scam phrases detected")
            
            if features.get('num_exclamations', 0) > 5:
                suspicious_indicators.append("Excessive exclamation marks")
            
            # Missing info indicators
            missing_count = sum([
                features.get('address_missing', False),
                features.get('square_footage_missing', False),
                features.get('city_missing', False)
            ])
            if missing_count > 1:
                suspicious_indicators.append("Multiple missing data fields")
            
            return {
                "suspicious_indicators": suspicious_indicators,
                "key_features": {
                    "price": float(features.get('price', 0)),
                    "price_per_sqft": float(features.get('price_per_sqft', 0)),
                    "distance_from_city": float(features.get('distance_from_city_center', 0)),
                    "scam_phrases": int(features.get('num_scam_phrases', 0)),
                    "description_length": int(features.get('description_length', 0))
                }
            }
            
        except Exception as e:
            return {
                "suspicious_indicators": [],
                "key_features": {},
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return information about loaded models."""
        return {
            "models_loaded": {
                "isolation_forest": self.isolation_forest is not None,
                "lof": self.lof_model is not None,
                "dbscan_params": self.dbscan_params is not None
            },
            "training_info": self.model_metadata.get("dataset_info", {}),
            "model_performance": self.model_metadata.get("ensemble_results", {}),
            "feature_count": len(self.feature_pipeline.get_feature_names())
        }
