import numpy as np
from sklearn.datasets import make_blobs
from scipy.spatial.distance import cdist
from sklearn.metrics import silhouette_score as sklearn_silhouette


def silhouette_score(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute the silhouette score for the given dataset and labels.

    Parameters:
    x : np.ndarray
        The dataset as a 2D NumPy array of shape (n_samples, n_features).
    y : np.ndarray
        Cluster labels for each data point as a 1D NumPy array of shape (n_samples,).

    Returns:
    float
        The average silhouette score for the dataset.
    """
    # Compute pairwise distances once
    dists = cdist(x, x)

    # Prepare result storage
    results = np.full(x.shape[0], fill_value=-1.0, dtype=np.float32)

    # Get unique cluster ids
    cluster_ids = np.unique(y)

    # Precompute intra-cluster indices for each cluster
    cluster_indices = {cluster_id: np.argwhere(y == cluster_id).flatten() for cluster_id in cluster_ids}

    for i in range(x.shape[0]):
        # Intra-cluster distances (a(i))
        intra_idx = cluster_indices[y[i]]
        if len(intra_idx) <= 1:  # Handle single-point clusters
            a_i = 0.0
        else:
            intra_distances = dists[i, intra_idx]
            a_i = np.sum(intra_distances) / (intra_distances.shape[0] - 1)

        # Nearest-cluster distances (b(i))
        b_i = np.inf
        for cluster_id in cluster_ids:
            if cluster_id != y[i]:
                inter_idx = cluster_indices[cluster_id]
                inter_distances = dists[i, inter_idx]
                b_i = min(b_i, np.mean(inter_distances))

        # Silhouette score for point i
        results[i] = (b_i - a_i) / max(a_i, b_i)

    # Return the mean silhouette score
    return np.mean(results)


# Example Usage
x, y = make_blobs(n_samples=10000, n_features=400, centers=5, cluster_std=10, center_box=(-1, 1))
score = silhouette_score(x=x, y=y)
print(f"Silhouette Score: {score}")

score_sklearn = sklearn_silhouette(x, y)
print(f"Silhouette Score: {score_sklearn}")
