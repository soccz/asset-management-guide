"""B2단원 보강: 그래프 라플라시안 고유값 + Fiedler 벡터.

스펙트럴 클러스터링의 핵심:
- 작은 고유값들의 개수 = 자연스러운 클러스터 수 (eigengap)
- 두 번째 작은 고유값의 고유벡터(Fiedler)가 첫 분할 신호
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(99)
N = 30  # 자산 수, 3개 클러스터

# 3개 클러스터 가정 (10개씩)
cluster_size = 10
labels_true = np.array([0]*cluster_size + [1]*cluster_size + [2]*cluster_size)

# 유사도 행렬: 같은 클러스터는 강한 연결, 다른 클러스터는 약한 연결
W = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        if i == j:
            W[i, j] = 0
        elif labels_true[i] == labels_true[j]:
            W[i, j] = 0.7 + 0.2 * rng.random()
        else:
            W[i, j] = 0.05 + 0.1 * rng.random()

# Degree matrix
D = np.diag(W.sum(axis=1))
# Unnormalized Laplacian
L = D - W

# 고유값 / 고유벡터
eigvals, eigvecs = np.linalg.eigh(L)
# 정렬 (작은 것부터)
idx = np.argsort(eigvals)
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

# Fiedler 벡터 = 두 번째 작은 고유벡터
fiedler = eigvecs[:, 1]
# 세 번째 작은 고유벡터 (3개 클러스터 분리에 추가)
v3 = eigvecs[:, 2]

fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.5),
                         gridspec_kw={"width_ratios": [1, 1, 1.1], "wspace": 0.32})

# (a) 고유값 spectrum + eigengap
ax = axes[0]
k = 8
ax.scatter(range(k), eigvals[:k], s=110, color="#1f6feb",
           edgecolor="white", linewidth=1.5, zorder=5)
ax.plot(range(k), eigvals[:k], color="#1f6feb", linewidth=1.4, alpha=0.5)

# eigengap 강조
ax.fill_between([2, 3], 0, max(eigvals[:k]) * 1.1,
                alpha=0.18, color="#d62728")
ax.text(2.5, eigvals[3] * 0.5, "eigengap\n(클러스터 3개 신호)",
        ha="center", fontsize=10, color="#a31515", fontweight="bold")

ax.set_xlabel("고유값 인덱스 (작은 순)", fontsize=11)
ax.set_ylabel("고유값 λ", fontsize=11)
ax.set_title("(a) 라플라시안 고유값 spectrum\n작은 고유값 3개 → 클러스터 3개",
             fontsize=12, pad=10)
ax.set_xticks(range(k))

# (b) Fiedler 벡터 (정렬됨)
ax = axes[1]
sort_idx = np.argsort(fiedler)
colors_true = ["#d62728", "#1f6feb", "#2ca02c"]
for i in range(N):
    ax.bar(i, fiedler[sort_idx][i],
           color=colors_true[labels_true[sort_idx][i]],
           edgecolor="white", linewidth=0.4, width=0.85)

ax.axhline(0, color="#1c1917", linewidth=0.7)
ax.set_xlabel("자산 (Fiedler 값으로 정렬)", fontsize=11)
ax.set_ylabel("Fiedler 벡터 v₂[i]", fontsize=11)
ax.set_title("(b) Fiedler 벡터 v₂ (두 번째 작은 고유벡터)\n부호로 첫 클러스터 분할",
             fontsize=12, pad=10)

# (c) v2 vs v3 산점도 — 3 클러스터 분리
ax = axes[2]
for k in range(3):
    mask = labels_true == k
    ax.scatter(eigvecs[mask, 1], eigvecs[mask, 2],
               color=colors_true[k], s=110,
               edgecolor="white", linewidth=1.5,
               label=f"클러스터 {k+1}")

ax.axhline(0, color="#888", linestyle=":", linewidth=0.8)
ax.axvline(0, color="#888", linestyle=":", linewidth=0.8)
ax.set_xlabel("Fiedler 벡터 v₂", fontsize=11)
ax.set_ylabel("세 번째 고유벡터 v₃", fontsize=11)
ax.set_title("(c) (v₂, v₃) 평면 — 3 클러스터 명확 분리\n→ k-means가 이 평면에서 군집화",
             fontsize=12, pad=10)
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

fig.suptitle("스펙트럴 클러스터링의 핵심 — 라플라시안 고유 분해",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "chB2_laplacian_eigen")
