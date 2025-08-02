import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def run_customer_segmentation(X,_):
    # Standardizing predictors
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    features = ['Age', 'Gender', 'Tenure', 'Usage_Frequency', 'Support_Calls', 'Last_Interaction',
                    'Payment_Delay', 'Subscription_Type', 'Total_Spend', 'Contract_Length']
    
    # Return preprocessed + a DataFrame version for clustering
    df_scaled = pd.DataFrame(X_scaled, columns=features)


    kmeans = KMeans(n_clusters=4, random_state=42)
    df_scaled['Segment'] = kmeans.fit_predict(df_scaled)

    # Save segment chart
    df_scaled['Segment'].value_counts().plot(kind='bar', title='Segment Distribution')
    plt.savefig('output/charts/segment_distribution.png')

    # Save cluster profiles
    segment_profiles = df_scaled.groupby('Segment').mean()
    segment_profiles.to_csv('data/cluster/segment_profiles.csv')
