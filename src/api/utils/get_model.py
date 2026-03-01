import joblib


def load_ml_model(model_path):
    """Load the pre-trained model from the specified path."""
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None