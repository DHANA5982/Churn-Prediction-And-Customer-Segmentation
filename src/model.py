from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
import numpy as np
import joblib
import time

def train_churn_model(X, y):
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42
    )

    print(f"🔹 Split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

    # Baseline Model
    baseline = LogisticRegression(max_iter=500)
    baseline.fit(X_train, y_train)
    y_pred_base = baseline.predict(X_val)
    print("\n📊 Baseline (Logistic Regression) on Validation Set:")
    print(f'Classification Report: {classification_report(y_val, y_pred_base)}')
    print(f'Accuracy Score: {accuracy_score(y_val, y_pred_base):.2f}')
    print(f'f1 Score: {f1_score(y_val, y_pred_base):.2f}')

    # Combine train + val for tuning
    X_trainval = np.vstack([X_train, X_val])
    y_trainval = np.concatenate([y_train, y_val])

    rf = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [1, 5, 10],
        'min_samples_leaf': [1, 2, 5],
        'max_features': ['sqrt', 'log2']
    }

    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    grid = GridSearchCV(
        rf,
        param_grid,
        scoring='f1',
        cv=skf,
        n_jobs=-1,
        verbose=1
    )

    start = time.time()

    grid.fit(X_trainval, y_trainval)

    print(f'⏱️ Grid Search took {(time.time() - start)/60:.2f} minutes')

    best_model = grid.best_estimator_

    print("\n✅ Best Hyperparameters:")
    for k, v in grid.best_params_.items():
        print(f"  {k}: {v}")

    y_pred_test = best_model.predict(X_test)
    print("\n📊 Final Test Evaluation:")
    print(classification_report(y_test, y_pred_test))
    print(f"Accuracy: {accuracy_score(y_test, y_pred_test):.2f}")
    print(f"F1 Score: {f1_score(y_test, y_pred_test):.2f}")

    joblib.dump(best_model, 'models/churn_prediction_model.pkl', compress=3)
    print("✅ Model saved to: models/churn_model.pkl")
