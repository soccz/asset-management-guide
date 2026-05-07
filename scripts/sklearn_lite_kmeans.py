"""아주 가벼운 k-means 구현 — sklearn 의존성 회피용.
"""
import numpy as np


def simple_kmeans(X: np.ndarray, k: int, seed: int = 0,
                  max_iter: int = 100, tol: float = 1e-6) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    idx = rng.choice(n, size=k, replace=False)
    centers = X[idx].copy()
    for _ in range(max_iter):
        dists = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        labels = dists.argmin(axis=1)
        new_centers = np.array([
            X[labels == j].mean(axis=0) if (labels == j).any() else centers[j]
            for j in range(k)
        ])
        if np.linalg.norm(new_centers - centers) < tol:
            break
        centers = new_centers
    return labels
