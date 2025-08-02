import pandas as pd

def preprocess_features(df):
    try:
        # Strip whitespace
        df.columns = df.columns.str.strip().str.replace(' ', '_')

        # Float to integer datatypes to necessary columns
        cols = ['Age', 'Tenure', 'Usage_Frequency', 'Support_Calls', 
            'Payment_Delay', 'Last_Interaction']
        
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
        # Float to int
        if 'Churn' in df.columns:
            df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce').fillna(0).astype(int)

        # Feature encoding mannual
        if df['Subscription_Type'].dtype == 'object':
            sub = {'Basic':1, 'Standard': 2, 'Premium': 3}
            df['Subscription_Type'] = df['Subscription_Type'].map(sub)

        if df['Contract_Length'].dtype == 'object':
            con = {'Monthly': 1, 'Quarterly': 2, 'Annual': 3}
            df['Contract_Length'] = df['Contract_Length'].map(con)

        if df['Gender'].dtype == 'object':
            gen = {'Female': 0, 'Male': 1}
            df['Gender'] = df['Gender'].map(gen)

        features = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Last_Interaction',
                    'Payment_Delay', 'Subscription_Type', 'Total_Spend', 'Contract_Length']

        # Predictors
        X = df[features]

        # Response
        if 'Churn' not in df.columns:
            df['Churn'] = None
            y = df['Churn']
        else:
            y = df['Churn']

    except Exception as e:
        print(e)

    return X, y
