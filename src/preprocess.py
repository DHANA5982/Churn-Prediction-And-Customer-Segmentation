import pandas as pd

def load_and_clean_data(path):
    try:
        df = pd.read_csv(path)
        
        # Drop rows with critical nulls
        df.dropna(inplace=True)
    
    except Exception as e:
        print(e)

    return df