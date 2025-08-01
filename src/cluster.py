from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def run_customer_segmentation(df_scaled):
    kmeans = KMeans(n_clusters=4, random_state=42)
    df_scaled['Segment'] = kmeans.fit_predict(df_scaled)

    # Save segment chart
    df_scaled['Segment'].value_counts().plot(kind='bar', title='Segment Distribution')
    plt.savefig('output/charts/segment_distribution.png')

    # Save cluster profiles
    segment_profiles = df_scaled.groupby('Segment').mean()
    segment_profiles.to_csv('data/cluster/segment_profiles.csv')
    