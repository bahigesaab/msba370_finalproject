from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def elbow_function(df):
    distorsions = []
    for k in range(2, 20):
        kmeans = KMeans(n_clusters=k, init="k-means++")
        kmeans.fit(df)
        distorsions.append(kmeans.inertia_)

    fig = plt.figure(figsize=(15, 5))
    plt.plot(range(2, 20), distorsions, marker ="8", color="red")
    plt.grid(True)
    plt.xlabel("K Value")
    plt.xticks(np.arange(1,20,1))
    plt.ylabel("WCSS")
    plt.title('Elbow curve')
    return fig


def plot_cluster(df, nr_clusters):
    kmeans = KMeans(n_clusters=nr_clusters, init="k-means++")
    clusters = kmeans.fit_predict(df)
    df["label"] = clusters
    fig = px.scatter_3d(df, x='Discount', y='Sales', z='Profit', color='label', size_max=18)
    fig.update_layout(width=1000, height=700)
    return fig

def clusters_centroid_dataframe(df, nr_clusters):
    kmeans = KMeans(n_clusters=nr_clusters, init="k-means++")
    clusters = kmeans.fit_predict(df)
    df["label"] = clusters
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=['Discount', 'Sales', 'Profit'])
    return centroids
