import numpy as np
import pandas as pd
import time
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score

def train_churn_model(X, y):
    # Train-Test Split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print(f"🔹 Split: Train={len(X_train)}, Test={len(X_test)}")

    # Pipeline: Standardization + Random Forest
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(random_state=42))
    ])

    # Hyperparameter grid for the RF step
    param_grid = {
        'rf__n_estimators': [50, 100, 200, 300],
        'rf__max_depth': [5, 10, 20, None],
        'rf__min_samples_split': [2, 5, 7, 9],
        'rf__min_samples_leaf': [1, 2, 5, 10],
        'rf__max_features': ['sqrt', 'log2']
    }

    # Stratified K-Fold
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # Grid Search with cross-validation
    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring='f1',
        cv=skf,
        n_jobs=-1,
        verbose=1
    )

    # Train with timing
    start = time.time()
    grid.fit(X_train, y_train)
    duration = (time.time() - start) / 60
    print(f'⏱️ Grid Search took {duration:.2f} minutes')

    # Best model from GridSearchCV
    best_model = grid.best_estimator_

    # Print best hyperparameters
    print("\n✅ Best Hyperparameters:")
    for k, v in grid.best_params_.items():
        print(f"  {k}: {v}")

    # Evaluate on test set
    y_pred_test = best_model.predict(X_test)
    print("\n📊 Final Test Evaluation:")
    print(classification_report(y_test, y_pred_test))
    print(f"Accuracy: {accuracy_score(y_test, y_pred_test):.2f}")
    print(f"F1 Score: {f1_score(y_test, y_pred_test):.2f}")

    # Save the full pipeline (includes both scaler + model)
    joblib.dump(best_model, 'models/churn_prediction_model.pkl', compress=3)
    print("✅ Model saved to: models/churn_prediction_model.pkl")
