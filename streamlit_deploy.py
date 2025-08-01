import streamlit as st
import pandas as pd
from src.preprocess import load_and_clean_data
from src.features import preprocess_features
import joblib

# Load model
model = joblib.load("D:/GitHub/Churn Prediction and Customer Segmentation/models/churn_prediction_model.pkl")

# Feature list
features = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Last_Interaction',
            'Payment_Delay', 'Subscription_Type', 'Total_Spend', 'Contract_Length']

st.title("📊 Customer Churn Prediction Dashboard")

st.sidebar.header("🔧 Choose Input Method")
input_mode = st.sidebar.radio("How would you like to input data?", ["📁 Upload CSV", "🧍 Manual Entry"])

# -------------------------------
# 📁 Option 1: CSV Upload
# -------------------------------
if input_mode == "📁 Upload CSV":
    uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])
    if uploaded_file:
        cleaned_df = load_and_clean_data(uploaded_file)
        st.subheader("🔍 Preview of cleaned Data")
        st.dataframe(cleaned_df.head())
        print('Data being processed.')
        X, _, _ = preprocess_features(cleaned_df)


        if st.button("Predict Churn"):
            try:
                predictions = model.predict(X)
            
                if not isinstance(X, pd.DataFrame):
                    X = pd.DataFrame(X, columns=features)  # use your actual feature names here
                X['Churn_Prediction'] = predictions
                st.success("✅ Predictions completed")
                st.dataframe(X[['Churn_Prediction']])

                st.subheader("📈 Churn Breakdown")
                st.write(X['Churn_Prediction'].value_counts())

                st.download_button("Download Results", X.to_csv(index=False), file_name="churn_predictions.csv")
            except Exception as e:
                st.error(e)
