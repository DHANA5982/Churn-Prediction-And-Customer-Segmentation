import pytest
from src.model_prediction import train_churn_model
import os
import joblib

def generate_dummy_data():
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=500, n_features=10, 
                               n_informative=5, n_redundant=2,
                               n_classes=2, random_state=42)
    return X, y

def test_model_training():
    """Test that the model training function works and saves a model."""
    X, y = generate_dummy_data()
    train_churn_model(X, y)
    assert os.path.exists("models/churn_prediction_model.pkl"), "Model not saved"

def test_model_file_not_empty():
    """Test that the saved model file exists and is not empty."""
    assert os.path.exists("models/churn_prediction_model.pkl"), "Model file doesn't exist"
    assert os.path.getsize("models/churn_prediction_model.pkl") > 1000, "Saved model file too small"

def test_model_can_be_loaded():
    """Test that the saved model can be loaded successfully."""
    assert os.path.exists("models/churn_prediction_model.pkl"), "Model file doesn't exist"
    try:
        model = joblib.load("models/churn_prediction_model.pkl")
        assert model is not None, "Model is None after loading"
        assert hasattr(model, 'predict'), "Model doesn't have predict method"
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")

def test_model_prediction():
    """Test that the loaded model can make predictions."""
    X, _ = generate_dummy_data()
    model = joblib.load("models/churn_prediction_model.pkl")
    
    # Test prediction on a small sample
    predictions = model.predict(X[:5])
    assert len(predictions) == 5, "Prediction count mismatch"
    assert all(pred in [0, 1] for pred in predictions), "Invalid prediction values"

def test_clustering_model_exists():
    """Test that the clustering model file exists."""
    assert os.path.exists("models/segment_model.pkl"), "Clustering model file doesn't exist"
    assert os.path.getsize("models/segment_model.pkl") > 100, "Clustering model file too small"
