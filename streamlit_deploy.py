import streamlit as st
import pandas as pd
from data_cleaning import load_and_clean_data
from data_preparation import preprocess_features
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
    st.write('Required features list with sensible datatypes:')
    st.write(f'{features}')
    uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])
    if uploaded_file:
        try:
            cleaned_df = load_and_clean_data(uploaded_file)
            st.subheader("🔍 Preview of cleaned Data")
            st.dataframe(cleaned_df.head())
            X, _, _ = preprocess_features(cleaned_df)
        except Exception as e:
            st.error(e)

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

# -------------------------------
# 🧍 Option 2: Manual Entry
# -------------------------------
elif input_mode == "🧍 Manual Entry":
    st.subheader("🔢 Enter Customer Info")

    gender = st.selectbox("Gender", ["Male", "Female"])
    sub_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
    con_length = st.selectbox("Contract Length (months)", ['Monthly', 'Quarterly', 'Annual'])
    
    # Input fields
    age = st.number_input("Age", min_value=18, max_value=90, value=30)
    tenure = st.slider("Tenure (months)", 0, 60, 12)
    usage = st.slider("Usage Frequency (times/month)", 0, 100, 20)
    support_calls = st.number_input("Support Calls (past 6 months)", 0, 50, 2)
    last_interaction = st.number_input("Last Interaction (days ago)", 0, 365, 30)
    payment_delay = st.slider("Payment Delay (days)", 0, 60, 5)
    total_spend = st.number_input("Total Spend ($)", 0.0, 10000.0, 500.0)

    # Map categorical values if needed
    gender_val = 1 if gender == "Male" else 0
    sub_map = {"Basic": 1, "Standard": 2, "Premium": 3}
    sub_val = sub_map[sub_type]
    con_map = {'Monthly': 1, 'Quarterly': 2, 'Annual': 3}
    con_val = con_map[con_length]


    input_df = pd.DataFrame([{
        'Age': age,
        'Gender': gender_val,
        'Tenure': tenure,
        'Usage_Frequency': usage,
        'Support_Calls': support_calls,
        'Last_Interaction': last_interaction,
        'Payment_Delay': payment_delay,
        'Subscription_Type': sub_val,
        'Total_Spend': total_spend,
        'Contract_Length': con_val
    }])

    st.write("📋 Input Preview")
    st.dataframe(input_df)

    if st.button("🧠 Predict Churn"):
        prediction = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]
        st.success(f"✅ Prediction: {'Churn' if prediction else 'No Churn'} (Probability: {prob:.2f})")

