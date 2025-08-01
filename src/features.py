import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_features(df):
    features = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Last_Interaction',
                'Payment_Delay', 'Subscription_Type', 'Total_Spend', 'Contract_Length']

    X = df[features]
    if 'Churn' in df.columns:
        y = df['Churn']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Return preprocessed + a DataFrame version for clustering
    df_scaled = pd.DataFrame(X_scaled, columns=features)
    
    return X_scaled, y, df_scaled
