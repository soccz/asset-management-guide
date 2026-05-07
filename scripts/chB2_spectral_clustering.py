"""B2단원 Figure: 스펙트럴 클러스터링 시각화.

3개의 패널로 알고리즘 흐름을 보여준다:
(a) 원본 데이터 — 보기에 어떤 클러스터가 있는지
(b) 라플라시안의 두 번째 작은 고유벡터 (Fiedler vector) — 한 차원에서 그룹이 분리됨
(c) 그 벡터를 부호로 자르거나 k-means하면 클러스터 발견
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(7)

# 3개 클러스터 데이터 생성
n_per = 30
centers = np.array([[-2.5, 0.0], [0.0, 2.0], [2.5, -0.5]])
points = []
labels_true = []
for i, c in enumerate(centers):
    pts = c + rng.normal(0, 0.5, size=(n_per, 2))
    points.append(pts)
    labels_true.extend([i] * n_per)
X = np.vstack(points)
n = X.shape[0]

# 가우시안 유사도 행렬
sigma = 1.2
W = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        if i != j:
            d2 = np.sum((X[i] - X[j]) ** 2)
            W[i, j] = np.exp(-d2 / (2 * sigma ** 2))

# 가까운 점만 연결 (k-NN 식 sparsification)
# 여기서는 단순히 W 그대로 사용

D = np.diag(W.sum(axis=1))
L = D - W

# 고유값 분해
eigvals, eigvecs = np.linalg.eigh(L)
# 가장 작은 k=3 고유벡터
U = eigvecs[:, :3]

# k-means로 U의 행을 묶음
from sklearn_lite_kmeans import simple_kmeans  # noqa: E402
labels_pred = simple_kmeans(U, k=3, seed=0)

# 그림
fig, axes = plt.subplots(1, 3, figsize=(18, 6.2))

# (a) 원본 데이터 + 그래프 간선
ax = axes[0]
# 강한 연결만 그림
edge_threshold = 0.15
for i in range(n):
    for j in range(i + 1, n):
        if W[i, j] > edge_threshold:
            ax.plot([X[i, 0], X[j, 0]], [X[i, 1], X[j, 1]],
                    color="grey", alpha=0.18, linewidth=0.5, zorder=1)
ax.scatter(X[:, 0], X[:, 1], c="#1f6feb", s=50,
           edgecolors="white", linewidths=1.0, zorder=3)
ax.set_title("(a) 원본 자산과 유사도 그래프\n"
             "정점 = 자산, 간선 = 유사도 w_ij (강할수록 진하게)", fontsize=11)
ax.set_xlabel("특성 1"); ax.set_ylabel("특성 2")
ax.set_aspect("equal")

# (b) Fiedler vector (두 번째 고유벡터) 시각화
ax = axes[1]
fiedler = eigvecs[:, 1]  # 두 번째로 작은 고유값의 고유벡터
# 정점 위치를 (Fiedler, third eigvec)로 사상
third = eigvecs[:, 2]
sc = ax.scatter(fiedler, third, c=fiedler, cmap="coolwarm", s=70,
                edgecolors="white", linewidths=1.0)
ax.axvline(0, color="grey", linewidth=0.6, linestyle="--")
ax.set_title("(b) 라플라시안 고유벡터로 자산을 사상\n"
             "(x = 둘째 고유벡터 u2, y = 셋째 고유벡터 u3)", fontsize=11)
ax.set_xlabel("u2 (Fiedler vector)"); ax.set_ylabel("u3")
plt.colorbar(sc, ax=ax, fraction=0.04, pad=0.02, label="u2 값")

# (c) 클러스터링 결과
ax = axes[2]
colors_c = ["#d62728", "#2ca02c", "#9467bd"]
# 라벨 매칭: 예측 라벨을 진짜 클러스터에 맞춰 색 사용
for k in range(3):
    mask = labels_pred == k
    ax.scatter(X[mask, 0], X[mask, 1], c=colors_c[k], s=70,
               edgecolors="white", linewidths=1.0,
               label=f"클러스터 {k + 1}")
ax.set_title("(c) k-means로 묶은 결과\n"
             "스펙트럴 사상 → 정통 k-means", fontsize=11)
ax.set_xlabel("특성 1"); ax.set_ylabel("특성 2")
ax.legend(loc="upper left", fontsize=9)
ax.set_aspect("equal")

fig.suptitle("스펙트럴 클러스터링의 흐름 — 그래프 → 고유벡터 → 클러스터",
             fontsize=13, y=1.0)
plt.tight_layout()
save(fig, "chB2_spectral_clustering")
