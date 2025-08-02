from src.data_cleaning import load_and_clean_data
from src.data_preparation import preprocess_features
from src.model_prediction import train_churn_model
from src.model_cluster import run_customer_segmentation
import time

def main():
    start = time.time()
    print("🚀 Starting DS Pipeline...")

    cleaned_df = load_and_clean_data('data/raw/telcom_behavior.csv')
    X, y = preprocess_features(cleaned_df)

    train_churn_model(X, y)
    print('Churn Prediction Done !')
    run_customer_segmentation(X, y)
    print('Customer Segmentation Done !')

    print("✅ Pipeline Complete.")
    print(f'⏱️ pipeline took {(time.time() - start)/60:.2f} minutes')

if __name__ == "__main__":
    main()
