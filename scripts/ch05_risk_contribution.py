"""5단원 보강: 자산별 리스크 기여도 — 가중치와 위험은 다르다.

60/40 포트폴리오는 자본 비중은 균형이지만 위험의 90% 이상을 주식이 책임진다.
리스크 패리티만 자산별 위험 기여를 동등화한다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 자산: 주식, 채권, 원자재, 부동산
assets = ["주식", "채권", "원자재", "부동산"]
sigmas = np.array([0.18, 0.05, 0.20, 0.15])  # 표준편차
# 단순화: 상관 0 (실제론 다른데, 메시지 명확화 위해)
cov = np.diag(sigmas ** 2)

def risk_contrib(weights, cov):
    """각 자산이 포트폴리오 분산에 기여하는 비중 (퍼센트)."""
    var_p = weights @ cov @ weights
    mrc = cov @ weights              # marginal risk contribution
    rc = weights * mrc               # risk contribution
    return rc / var_p

strategies = {
    "60/40\n(주식·채권)": np.array([0.60, 0.40, 0.0, 0.0]),
    "25/25/25/25\n(동일가중)": np.array([0.25, 0.25, 0.25, 0.25]),
    "리스크 패리티\n(위험 동등)": None,  # 계산
    "최소분산\n(MV)":           None,
}

# 리스크 패리티 — 1/σ 가중 (대각 공분산일 때 정확)
rp_w = (1 / sigmas) / (1 / sigmas).sum()
strategies["리스크 패리티\n(위험 동등)"] = rp_w

# 최소분산 — 1/σ² 가중
mv_w = (1 / sigmas ** 2) / (1 / sigmas ** 2).sum()
strategies["최소분산\n(MV)"] = mv_w

names = list(strategies.keys())
weights_mat = np.array([strategies[n] for n in names])
rc_mat = np.array([risk_contrib(strategies[n], cov) * 100 for n in names])

colors = ["#d62728", "#1f6feb", "#ff9900", "#2ca02c"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6.5),
                         gridspec_kw={"width_ratios": [1, 1], "wspace": 0.28})

# (a) 자본 비중
ax = axes[0]
bottom = np.zeros(len(names))
for i, asset in enumerate(assets):
    vals = weights_mat[:, i] * 100
    ax.bar(names, vals, bottom=bottom, color=colors[i], edgecolor="white",
           linewidth=1.2, label=asset, width=0.65)
    for j, v in enumerate(vals):
        if v > 4:
            ax.text(j, bottom[j] + v / 2, f"{v:.0f}%",
                    ha="center", va="center", fontsize=10,
                    color="white", fontweight="bold")
    bottom += vals
ax.set_title("(a) 자본 비중 (Allocation)\n— 4전략의 자본 배분", fontsize=12, pad=10)
ax.set_ylabel("비중 (%)", fontsize=11)
ax.set_ylim(0, 105)
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

# (b) 리스크 기여도
ax = axes[1]
bottom = np.zeros(len(names))
for i, asset in enumerate(assets):
    vals = rc_mat[:, i]
    ax.bar(names, vals, bottom=bottom, color=colors[i], edgecolor="white",
           linewidth=1.2, label=asset, width=0.65)
    for j, v in enumerate(vals):
        if v > 4:
            ax.text(j, bottom[j] + v / 2, f"{v:.0f}%",
                    ha="center", va="center", fontsize=10,
                    color="white", fontweight="bold")
    bottom += vals

# 60/40 강조
ax.annotate("주식이 위험의 90%+\n→ '균형'이라는 착각",
            xy=(0, 70), xytext=(0.7, 78),
            fontsize=10.5, color="#a31515", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="#d62728", boxstyle="round,pad=0.5"),
            arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.4))
# RP 강조
ax.annotate("리스크 패리티만\n자산별 위험 동등",
            xy=(2, 25), xytext=(2.3, 50),
            fontsize=10.5, color="#1f6feb", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="#1f6feb", boxstyle="round,pad=0.5"),
            arrowprops=dict(arrowstyle="->", color="#1f6feb", lw=1.4))

ax.set_title("(b) 리스크 기여도 (Risk Contribution)\n— 같은 비중도 위험 분담은 천차만별",
             fontsize=12, pad=10)
ax.set_ylabel("리스크 기여 (%)", fontsize=11)
ax.set_ylim(0, 105)

fig.suptitle("자본 비중 ≠ 위험 기여 — 60/40의 진실과 리스크 패리티의 직관",
             fontsize=14, y=1.02, fontweight="bold")

save(fig, "ch05_risk_contribution")
