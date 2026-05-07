"""2단원 Figure: 효율적 프론티어.

μ-σ 평면에서:
- 회색 점: 무작위 포트폴리오 (가능한 모든 조합)
- 파란 곡선: 효율적 프론티어 (위쪽 절반)
- 빨간 점: 최소분산 포트폴리오 (MVP)
- 초록 별: 개별 자산
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(11)

# 4개 자산의 평균/공분산 (예시)
mu = np.array([0.06, 0.10, 0.14, 0.08])
vol = np.array([0.10, 0.18, 0.24, 0.14])
corr = np.array([
    [1.0, 0.3, 0.2, 0.4],
    [0.3, 1.0, 0.5, 0.3],
    [0.2, 0.5, 1.0, 0.2],
    [0.4, 0.3, 0.2, 1.0],
])
Sigma = corr * np.outer(vol, vol)

# 무작위 포트폴리오 5000개
n_assets = 4
n_random = 5000
weights = rng.dirichlet(np.ones(n_assets), n_random)  # 합 = 1, 모두 양수
port_mu = weights @ mu
port_vol = np.sqrt(np.einsum("ij,jk,ik->i", weights, Sigma, weights))

# 효율적 프론티어: 단순화 — 각 sigma 구간에서 최대 mu
bins = np.linspace(port_vol.min(), port_vol.max(), 80)
front_mu = []
front_sig = []
for lo, hi in zip(bins[:-1], bins[1:]):
    mask = (port_vol >= lo) & (port_vol < hi)
    if mask.any():
        front_mu.append(port_mu[mask].max())
        front_sig.append((lo + hi) / 2)
front_mu = np.array(front_mu)
front_sig = np.array(front_sig)

# 최소분산 포트폴리오 위치
mvp_idx = np.argmin(port_vol)

fig, ax = plt.subplots(figsize=(9, 6))
sc = ax.scatter(port_vol * 100, port_mu * 100, c=port_mu / port_vol,
                cmap="viridis", s=10, alpha=0.45, label="무작위 포트폴리오 (5000개)")

# 효율 프론티어 (상반부만)
mask_top = front_mu > port_mu[mvp_idx]
ax.plot(front_sig[mask_top] * 100, front_mu[mask_top] * 100,
        color="#1f6feb", linewidth=2.6, label="효율적 프론티어 (위쪽)")

# MVP
ax.scatter(port_vol[mvp_idx] * 100, port_mu[mvp_idx] * 100,
           c="#d62728", s=180, marker="o", edgecolors="white", linewidths=2,
           zorder=5, label="최소분산 포트폴리오 (MVP)")

# 개별 자산
ax.scatter(vol * 100, mu * 100, c="#2ca02c", s=180, marker="*",
           edgecolors="white", linewidths=1.5, zorder=5,
           label="개별 자산 (4개)")
for i, (v, m) in enumerate(zip(vol, mu)):
    ax.text(v * 100 + 0.4, m * 100 + 0.15, f"자산 {i+1}",
            fontsize=9, color="#1a5e1a")

cbar = plt.colorbar(sc, ax=ax, fraction=0.04, pad=0.02)
cbar.set_label("샤프 유사 비율 (μ/σ)")

ax.set_xlabel("표준편차 σ (%)")
ax.set_ylabel("기대수익률 μ (%)")
ax.set_title("효율적 프론티어 — μ-σ 평면 위 모든 가능한 조합\n"
             "(개별 자산 4개를 가중치 무작위로 5000번 결합)")
ax.legend(loc="lower right", fontsize=9)

plt.tight_layout()
save(fig, "ch02_efficient_frontier")
