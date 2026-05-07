"""7단원 보강: 팩터 로딩(β) 분포 — 횡단면에서 자산이 어떻게 분포하는가.

자산 30개의 (β_market, β_SMB, β_HML) 3차원 로딩을 산점도로 표시.
같은 산업/스타일 자산이 군집 형태로 보임 → 다중팩터 모형의 직관.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(7)
N = 30

# 3개 군집 (성장주, 가치주, 소형주)
def cluster(center, n, scale=0.18):
    return center + rng.normal(0, scale, (n, 3))

growth = cluster(np.array([1.05, -0.3, -0.5]), 10)   # large growth
value = cluster(np.array([0.95, -0.1, +0.7]), 10)    # large value
small = cluster(np.array([1.20, +0.8, +0.2]), 10)    # small mixed

loadings = np.vstack([growth, value, small])
groups = ["성장주 (large growth)"] * 10 + ["가치주 (large value)"] * 10 + ["소형주 (small)"] * 10
colors_map = {"성장주 (large growth)": "#d62728",
              "가치주 (large value)": "#1f6feb",
              "소형주 (small)":         "#2ca02c"}
colors_list = [colors_map[g] for g in groups]

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"wspace": 0.28})

# (a) β_market vs β_HML
ax = axes[0]
for g in colors_map:
    mask = [gr == g for gr in groups]
    pts = loadings[mask]
    ax.scatter(pts[:, 0], pts[:, 2], color=colors_map[g], s=110,
               edgecolor="white", linewidth=1.5, label=g)

ax.axhline(0, color="#888", linestyle=":", linewidth=0.8)
ax.axvline(1, color="#888", linestyle=":", linewidth=0.8)
ax.set_xlabel("β_market (시장 노출)", fontsize=12)
ax.set_ylabel("β_HML (가치 노출)", fontsize=12)
ax.set_title("(a) 시장 vs 가치 로딩 — 성장/가치 분리",
             fontsize=12, pad=10)
ax.legend(loc="lower right", fontsize=10, framealpha=0.95)

# (b) β_SMB vs β_HML
ax = axes[1]
for g in colors_map:
    mask = [gr == g for gr in groups]
    pts = loadings[mask]
    ax.scatter(pts[:, 1], pts[:, 2], color=colors_map[g], s=110,
               edgecolor="white", linewidth=1.5, label=g)

ax.axhline(0, color="#888", linestyle=":", linewidth=0.8)
ax.axvline(0, color="#888", linestyle=":", linewidth=0.8)
ax.set_xlabel("β_SMB (사이즈 노출)", fontsize=12)
ax.set_ylabel("β_HML (가치 노출)", fontsize=12)
ax.set_title("(b) 사이즈 vs 가치 로딩 — 소형주 분리\n3팩터 공간에서 자산 군집",
             fontsize=12, pad=10)
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

# 메시지 박스
ax.text(-0.5, -0.85,
        "핵심: 같은 스타일 자산이\nβ 공간에서 군집을 이룸\n→ 팩터가 횡단면 차이를 설명",
        fontsize=10, color="#1c1917",
        bbox=dict(facecolor="white", edgecolor="#888",
                  boxstyle="round,pad=0.5"))

fig.suptitle("FF3 팩터 로딩(β)의 횡단면 분포 — 같은 스타일은 비슷한 β를 갖는다",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch07_factor_loadings")
