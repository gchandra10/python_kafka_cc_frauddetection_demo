from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

def train_initial_model():
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate legitimate transactions
    legitimate_samples = int(n_samples * 0.9)
    legitimate_amounts = np.random.uniform(10, 1000, legitimate_samples)
    legitimate_distances = np.random.uniform(0, 50, legitimate_samples)
    legitimate_times = np.random.uniform(5, 60, legitimate_samples)
    
    # Generate fraudulent transactions
    fraud_samples = n_samples - legitimate_samples
    fraud_amounts = np.random.uniform(800, 5000, fraud_samples)
    fraud_distances = np.random.uniform(50, 1000, fraud_samples)
    fraud_times = np.random.uniform(0, 5, fraud_samples)
    
    # Combine features
    X = np.vstack([
        np.column_stack([legitimate_amounts, legitimate_distances, legitimate_times]),
        np.column_stack([fraud_amounts, fraud_distances, fraud_times])
    ])
    
    # Create labels
    y = np.hstack([
        np.zeros(legitimate_samples),
        np.ones(fraud_samples)
    ])
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model
    joblib.dump(model, 'fraud_detection_model.joblib')
    return model