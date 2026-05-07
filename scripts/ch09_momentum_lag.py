"""9단원 Figure: 시차별 모멘텀과 반전.

x축: 시차 h (개월)
y축: 회귀계수 β_h (자기상관 강도)
1~12개월: 양수 (모멘텀) / 13개월~: 음수 (장기 반전) / 1개월: 단기 반전 → 음수
출처: Moskowitz 2012, Fig.1; Lewellen 2002 정성적 패턴.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 시차별 회귀계수 (정성적 패턴)
rng = np.random.default_rng(3)
h = np.arange(1, 61)

# 1개월: 단기 반전 (-0.04 부근)
# 2~12개월: 모멘텀 (양수, 0.05~0.10)
# 13~36개월: 장기 반전 (음수, -0.04~-0.02)
# 37~60개월: 약하게 0 부근
beta = np.zeros_like(h, dtype=float)
beta[0] = -0.04
beta[1:12] = np.linspace(0.10, 0.04, 11) + rng.normal(0, 0.005, 11)
beta[12:36] = np.linspace(-0.02, -0.05, 24) + rng.normal(0, 0.005, 24)
beta[36:] = rng.normal(0, 0.012, 60 - 36)

fig, ax = plt.subplots(figsize=(11, 5.5))

colors = []
for b in beta:
    if b > 0.02:
        colors.append("#2ca02c")  # 모멘텀
    elif b < -0.02:
        colors.append("#d62728")  # 반전
    else:
        colors.append("#bbbbbb")  # 비유의

ax.bar(h, beta, color=colors, edgecolor="white", linewidth=0.5)
ax.axhline(0, color="black", linewidth=0.7)
ax.axhline(0.02, color="grey", linewidth=0.5, linestyle=":", alpha=0.6)
ax.axhline(-0.02, color="grey", linewidth=0.5, linestyle=":", alpha=0.6)

# 영역 구분
ax.axvspan(0.5, 1.5, alpha=0.10, color="#d62728")
ax.text(1, 0.135, "단기\n반전", fontsize=9, ha="center", color="#a31515")

ax.axvspan(1.5, 12.5, alpha=0.10, color="#2ca02c")
ax.text(7, 0.135, "모멘텀 (1~12개월)", fontsize=10, ha="center", color="#1a5e1a",
        fontweight="bold")

ax.axvspan(12.5, 36.5, alpha=0.10, color="#d62728")
ax.text(24.5, 0.135, "장기 반전 (13~36개월)", fontsize=10, ha="center",
        color="#a31515", fontweight="bold")

ax.axvspan(36.5, 60.5, alpha=0.10, color="#bbbbbb")
ax.text(48.5, 0.135, "비유의 (~5년 너머)", fontsize=10, ha="center", color="#666")

ax.set_xlabel("시차 h (개월)")
ax.set_ylabel(r"회귀계수 $\beta_h$  (양수 → 모멘텀, 음수 → 반전)")
ax.set_title("시차별 자기상관 — 모멘텀은 \"중기\" 현상이다\n"
             "1개월 단기 반전 → 2~12개월 모멘텀 → 13~36개월 장기 반전\n"
             "[Moskowitz et al. 2012 Fig.1, Lewellen 2002 정성적 재현]")
ax.set_ylim(-0.08, 0.16)
ax.set_xlim(0, 61)

plt.tight_layout()
save(fig, "ch09_momentum_lag")
