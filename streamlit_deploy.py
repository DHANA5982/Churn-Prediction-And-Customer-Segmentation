import streamlit as st
import pandas as pd
import os
import joblib

# Import your custom modules
try:
    from src.data_cleaning import load_and_clean_data
    from src.data_preparation import preprocess_features
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.stop()

# Load models with error handling
@st.cache_resource
def load_models():
    """Load models with caching and error handling."""
    try:
        # Use relative paths for cloud deployment
        model_path = "models/churn_prediction_model.pkl"
        segment_path = "models/segment_model.pkl"
        
        if not os.path.exists(model_path):
            st.error(f"Model file not found: {model_path}")
            return None, None
            
        if not os.path.exists(segment_path):
            st.error(f"Segment model file not found: {segment_path}")
            return None, None
            
        model = joblib.load(model_path)
        seg_model = joblib.load(segment_path)
        
        return model, seg_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

# Load models
model, seg_model = load_models()

if model is None or seg_model is None:
    st.error("Failed to load models. Please check the deployment.")
    st.stop()

# Feature list used in both models
features = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Last_Interaction',
            'Payment_Delay', 'Subscription_Type', 'Total_Spend', 'Contract_Length']

st.title("📊 Customer Churn & Segmentation Dashboard")

st.sidebar.header("🔧 Choose Input Method")
input_mode = st.sidebar.radio("How would you like to input data?", ["📁 Upload CSV", "🧍 Manual Entry"])

# -------------------------------
# 📁 Option 1: CSV Upload
# -------------------------------
if input_mode == "📁 Upload CSV":
    st.write('Required features list with sensible datatypes:')
    st.code(features)
    uploaded_file = st.file_uploader("Upload customer CSV", type=["csv"])

    if uploaded_file:
        try:
            cleaned_df = load_and_clean_data(uploaded_file)
            st.subheader("🔍 Preview of Cleaned Data")
            st.dataframe(cleaned_df.head())

            X, _ = preprocess_features(cleaned_df)
        except Exception as e:
            st.error(f"Error while preprocessing: {e}")

        if st.button("🔮 Predict Churn & Segment"):
            try:
                churn_preds = model.predict(X)
                churn_probs = model.predict_proba(X)[:, 1]
                clusters = seg_model.predict(X)

                cleaned_df['Churn_Prediction'] = churn_preds
                cleaned_df['Churn_Probability'] = churn_probs
                cleaned_df['Customer_Segment'] = clusters

                st.success("✅ Predictions completed!")
                st.dataframe(cleaned_df[['Churn_Prediction', 'Churn_Probability', 'Customer_Segment']])

                st.subheader("📈 Churn Breakdown")
                st.bar_chart(cleaned_df['Churn_Prediction'].value_counts())

                st.subheader("🧩 Segment Distribution")
                st.bar_chart(cleaned_df['Customer_Segment'].value_counts())

                st.download_button("⬇ Download Results",
                                   cleaned_df.to_csv(index=False),
                                   file_name="churn_segment_predictions.csv")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

# -------------------------------
# 🧍 Option 2: Manual Entry
# -------------------------------
elif input_mode == "🧍 Manual Entry":
    st.subheader("🔢 Enter Customer Info")

    # Categorical selections
    gender = st.selectbox("Gender", ["Male", "Female"])
    sub_type = st.selectbox("Subscription Type", ["Basic", "Standard", "Premium"])
    con_length = st.selectbox("Contract Length", ["Monthly", "Quarterly", "Annual"])

    # Numeric inputs
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    tenure = st.slider("Tenure (months)", 0, 60, 12)
    usage = st.slider("Usage Frequency (times/month)", 0, 100, 20)
    support_calls = st.number_input("Support Calls (past 6 months)", 0, 50, 2)
    last_interaction = st.number_input("Last Interaction (days ago)", 0, 365, 30)
    payment_delay = st.slider("Payment Delay (days)", 0, 60, 5)
    total_spend = st.number_input("Total Spend ($)", 0.0, 10000.0, 500.0)

    # Mapping categorical to numerical
    gender_val = 1 if gender == "Male" else 0
    sub_val = {"Basic": 1, "Standard": 2, "Premium": 3}[sub_type]
    con_val = {"Monthly": 1, "Quarterly": 2, "Annual": 3}[con_length]

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

    if st.button("🧠 Predict"):
        try:
            churn_pred = model.predict(input_df)[0]
            churn_prob = model.predict_proba(input_df)[0][1]
            segment = seg_model.predict(input_df)[0]

            st.success(f"✅ Prediction: {'Churn' if churn_pred else 'No Churn'} (Probability: {churn_prob:.2f})")
            st.info(f"🧩 Customer Segment: {segment}")

             # Segment dictionary
            segment_info = {
                0: {
                    "label": "High-Risk Monthly Customers",
                    "risk": "🔴 HIGH RISK",
                    "desc": "Monthly contract customers with high support needs, frequent payment delays, and low spending.",
                    "plan": "📌 Action Plan: Prioritize retention efforts with loyalty offers or incentives for longer contracts."
                },
                1: {
                    "label": "Stable Value Customers",
                    "risk": "🟢 LOW RISK",
                    "desc": "Reliable, low-maintenance customers with consistent payments and long contracts.",
                    "plan": "📌 Action Plan: Consider loyalty perks or upsell premium services."
                },
                2: {
                    "label": "Premium Troubled Customers",
                    "risk": "🟡 MEDIUM-HIGH RISK",
                    "desc": "Premium subscribers experiencing high support needs and payment delays.",
                    "plan": "📌 Action Plan: Address service issues urgently to avoid losing high-value clients."
                },
                3: {
                    "label": "Premium Male Loyalists",
                    "risk": "🟢 LOW RISK",
                    "desc": "Young male premium users with high spend and minimal support needs.",
                    "plan": "📌 Action Plan: Engage with exclusive upgrades, referral programs, and premium loyalty campaigns."
                }
            }

            seg = segment_info.get(segment)
            
            if seg:
                st.subheader(f"📊 Segment Profile: {seg['label']} ({seg['risk']})")
                st.markdown(f"**Who they are:** {seg['desc']}")
                st.markdown(seg["plan"])
            else:
                st.warning("Segment not recognized.")

        except Exception as e:
            st.error(f"Prediction failed: {e}")


