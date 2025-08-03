import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib

def run_customer_segmentation(X,_):
    # Pipeline for scaling and cluster modeling
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=4, random_state=42))
    ])

    X['Cluster'] = pipeline.fit_predict(X)
    joblib.dump(pipeline, 'models/segment_model.pkl')
    
    print(X['Cluster'].value_counts())