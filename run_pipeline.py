from src.preprocess import load_and_clean_data
from src.features import preprocess_features
from src.model import train_churn_model
from src.cluster import run_customer_segmentation
import time

def main():
    start = time.time()
    print("🚀 Starting DS Pipeline...")

    cleaned_df = load_and_clean_data('data/raw/telcom_behavior.csv')
    X, y, df_scaled = preprocess_features(cleaned_df)

    train_churn_model(X, y)
    run_customer_segmentation(df_scaled)

    print("✅ Pipeline Complete.")
    print(f'⏱️ pipeline took {(time.time() - start)/60:.2f} minutes')

if __name__ == "__main__":
    main()
