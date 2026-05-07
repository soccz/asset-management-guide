"""7단원 Figure: PCA의 시각적 의미.

상관관계 있는 두 변수의 산점도에 첫·둘째 주성분 화살표를 그린다.
주성분 1: 데이터의 분산이 가장 큰 방향. 주성분 2: 그에 직교.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(13)
n = 400
mean = [0, 0]
cov = [[3.0, 2.0], [2.0, 1.5]]
X = rng.multivariate_normal(mean, cov, n)

# PCA
Xc = X - X.mean(axis=0)
S = (Xc.T @ Xc) / (n - 1)
eigvals, eigvecs = np.linalg.eigh(S)
order = np.argsort(eigvals)[::-1]
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]

fig, ax = plt.subplots(figsize=(8.5, 7))
ax.scatter(X[:, 0], X[:, 1], s=18, alpha=0.5, c="#1f6feb",
           edgecolors="white", linewidths=0.3, label="데이터 (자산 수익률)")

# 주성분 화살표
colors = ["#d62728", "#2ca02c"]
for i in range(2):
    v = eigvecs[:, i] * np.sqrt(eigvals[i]) * 2.2
    ax.arrow(0, 0, v[0], v[1], head_width=0.20, head_length=0.25,
             fc=colors[i], ec=colors[i], linewidth=2.4,
             length_includes_head=True, zorder=5)
    ax.arrow(0, 0, -v[0], -v[1], head_width=0.20, head_length=0.25,
             fc=colors[i], ec=colors[i], linewidth=2.4, alpha=0.6,
             length_includes_head=True, zorder=5)
    ax.text(v[0] * 1.1, v[1] * 1.1, f"PC{i+1}\n(λ={eigvals[i]:.2f})",
            color=colors[i], fontsize=11, fontweight="bold")

ax.set_xlabel("자산 1 수익률")
ax.set_ylabel("자산 2 수익률")
ax.set_title("PCA — 데이터 분산이 가장 큰 방향이 첫 주성분(PC1)\n"
             "둘째 주성분(PC2)은 PC1에 직교. 두 PC의 비율 = 고유값 비율")
ax.set_aspect("equal")
ax.axhline(0, color="grey", linewidth=0.4)
ax.axvline(0, color="grey", linewidth=0.4)
ax.legend(loc="upper left", fontsize=10)

# 분산 설명력 박스
total = eigvals.sum()
ax.text(0.97, 0.02,
        f"PC1 분산 설명력: {eigvals[0]/total*100:.1f}%\n"
        f"PC2 분산 설명력: {eigvals[1]/total*100:.1f}%",
        transform=ax.transAxes, fontsize=10, ha="right", va="bottom",
        bbox=dict(boxstyle="round,pad=0.4", fc="#fffde7", ec="#888"))

plt.tight_layout()
save(fig, "ch07_pca")
