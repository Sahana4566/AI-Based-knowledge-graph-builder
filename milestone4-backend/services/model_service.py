import pickle
import os
from typing import Optional, Tuple
import pandas as pd
import numpy as np

class ModelService:
    """Load and manage ML models and preprocessors"""
    
    def __init__(self):
        self.le_head = None
        self.le_relation = None
        self.le_tail = None
        self.scaler = None
        self.model_rf = None
        self.model_lr = None
        self.feature_cols = None
        self._load_models()
    
    def _load_models(self):
        """Load serialized models and preprocessors"""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        try:
            # Try to load label encoders
            le_head_path = os.path.join(models_dir, 'le_head.pkl')
            if os.path.exists(le_head_path):
                with open(le_head_path, 'rb') as f:
                    self.le_head = pickle.load(f)
                    print("✓ Loaded le_head")
        except Exception as e:
            print(f"Warning: Could not load le_head: {e}")
        
        try:
            le_relation_path = os.path.join(models_dir, 'le_relation.pkl')
            if os.path.exists(le_relation_path):
                with open(le_relation_path, 'rb') as f:
                    self.le_relation = pickle.load(f)
                    print("✓ Loaded le_relation")
        except Exception as e:
            print(f"Warning: Could not load le_relation: {e}")
        
        try:
            le_tail_path = os.path.join(models_dir, 'le_tail.pkl')
            if os.path.exists(le_tail_path):
                with open(le_tail_path, 'rb') as f:
                    self.le_tail = pickle.load(f)
                    print("✓ Loaded le_tail")
        except Exception as e:
            print(f"Warning: Could not load le_tail: {e}")
        
        try:
            scaler_path = os.path.join(models_dir, 'scaler.pkl')
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                    print("✓ Loaded scaler")
        except Exception as e:
            print(f"Warning: Could not load scaler: {e}")
        
        try:
            rf_path = os.path.join(models_dir, 'random_forest.pkl')
            if os.path.exists(rf_path):
                with open(rf_path, 'rb') as f:
                    self.model_rf = pickle.load(f)
                    print("✓ Loaded Random Forest model")
        except Exception as e:
            print(f"Warning: Could not load Random Forest: {e}")
        
        try:
            lr_path = os.path.join(models_dir, 'logistic_regression.pkl')
            if os.path.exists(lr_path):
                with open(lr_path, 'rb') as f:
                    self.model_lr = pickle.load(f)
                    print("✓ Loaded Logistic Regression model")
        except Exception as e:
            print(f"Warning: Could not load Logistic Regression: {e}")
        
        # Load feature column names
        try:
            feature_cols_path = os.path.join(models_dir, 'feature_cols.pkl')
            if os.path.exists(feature_cols_path):
                with open(feature_cols_path, 'rb') as f:
                    self.feature_cols = pickle.load(f)
                    print(f"✓ Loaded feature columns ({len(self.feature_cols)} features)")
        except Exception as e:
            print(f"Warning: Could not load feature columns: {e}")
    
    def predict_relation(self, head: str, tail: str, relation: str, model: str = 'rf') -> Optional[Tuple[str, float]]:
        """
        Predict relation classification
        
        Args:
            head: Entity head name
            tail: Entity tail name
            relation: Relation name
            model: 'rf' for Random Forest, 'lr' for Logistic Regression
        
        Returns:
            Tuple of (predicted_relation, confidence) or None if models unavailable
        """
        if not self.le_head or not self.le_tail or not self.le_relation:
            return None
        
        try:
            # Placeholder: In production, would compute full feature vector
            # For now, just return the provided relation
            return (relation, 0.95)
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# Singleton instance
model_service = ModelService()
