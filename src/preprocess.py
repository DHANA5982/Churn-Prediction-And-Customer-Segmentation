import pandas as pd

def load_and_clean_data(path):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(e)

    # Strip whitespace
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    # Drop rows with critical nulls
    df.dropna(inplace=True)

    # Float to integer datatypes to necessary columns
    cols = ['CustomerID', 'Age', 'Tenure', 'Usage_Frequency', 'Support_Calls', 
        'Payment_Delay', 'Last_Interaction']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    if 'Churn' in df.columns:
        df['Churn'] = pd.to_numeric(df['Churn'], errors='coerce').fillna(0).astype(int)

    sub = {'Basic':1, 'Standard': 2, 'Premium': 3}
    df['Subscription_Type'] = df['Subscription_Type'].map(sub)

    con = {'Monthly': 1, 'Quarterly': 2, 'Annual': 3}
    df['Contract_Length'] = df['Contract_Length'].map(con)

    gen = {'Female': 0, 'Male': 1}
    df['Gender'] = df['Gender'].map(gen)

    return df