from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def linear_regression(X, y):
    """Performs linear regression."""
    model = LinearRegression()
    model.fit(X, y)
    return model

def kmeans_clustering(X, n_clusters=3):
    """Applies KMeans clustering."""
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    return kmeans

def pca_analysis(X):
    """Applies PCA (Principal Component Analysis)."""
    pca = PCA(n_components=2)
    transformed_data = pca.fit_transform(X)
    return transformed_data
