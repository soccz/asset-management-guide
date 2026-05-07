"""4단원 보강: 자산별 샤프비율 비교 — 왜 접점 포트폴리오가 최선인가.

각 자산의 (μ - R_f) / σ 가 샤프비율. 접점 포트폴리오가 모든 단일 자산보다
높은 샤프비율을 갖는다는 것이 평균분산 최적화의 핵심 결과.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

Rf = 0.03

# 가상 자산 6개 + 접점 포트폴리오
names = ["국채", "회사채", "원자재", "REITs", "주식\n(US)", "주식\n(EM)", "접점\n포트폴리오"]
mu = np.array([0.045, 0.060, 0.085, 0.090, 0.105, 0.130, 0.115])
sigma = np.array([0.05, 0.08, 0.20, 0.16, 0.18, 0.28, 0.13])
sharpe = (mu - Rf) / sigma

is_tan = [False] * 6 + [True]
colors = ["#1f6feb"] * 6 + ["#d62728"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"width_ratios": [1.3, 1], "wspace": 0.3})

# (a) 위험-수익 평면
ax = axes[0]
for i, (n, m, s, c) in enumerate(zip(names, mu, sigma, colors)):
    marker = "*" if is_tan[i] else "o"
    size = 380 if is_tan[i] else 180
    ax.scatter(s * 100, m * 100, color=c, s=size, marker=marker,
               edgecolor="white", linewidth=2, zorder=5)
    offset_y = 1.0 if not is_tan[i] else -2.5
    ax.annotate(n, xy=(s * 100, m * 100), xytext=(s * 100 + 0.3, m * 100 + offset_y),
                fontsize=10, fontweight="bold" if is_tan[i] else "normal",
                color="#a31515" if is_tan[i] else "#1c1917")

# CAL through tangency
tan_s, tan_m = sigma[-1], mu[-1]
slope = (tan_m - Rf) / tan_s
xs = np.linspace(0, 35, 100)
ys = (Rf + slope * xs / 100) * 100
ax.plot(xs, ys, color="#d62728", linewidth=2.0, linestyle="--", alpha=0.7,
        label=f"CAL (slope = 샤프비율 = {slope:.2f})")

ax.scatter(0, Rf * 100, color="#1c1917", s=120, marker="D", zorder=5)
ax.annotate(f"R_f = {Rf*100:.0f}%", xy=(0, Rf*100), xytext=(0.5, Rf*100 - 0.8),
            fontsize=10)

ax.set_xlim(-1, 32)
ax.set_ylim(2, 16)
ax.set_xlabel("표준편차 σ (%)", fontsize=12)
ax.set_ylabel("기대 수익률 E[R] (%)", fontsize=12)
ax.set_title("(a) 자산별 위험-수익 + 접점 포트폴리오\nCAL의 기울기 = 샤프비율 (가장 가파른 직선)",
             fontsize=11.5, pad=10)
ax.legend(loc="upper left", fontsize=10.5)

# (b) 샤프비율 막대
ax = axes[1]
bars = ax.bar(names, sharpe, color=colors, edgecolor="#1c1917", linewidth=0.8, width=0.7)
for bar, val, tan in zip(bars, sharpe, is_tan):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.02,
            f"{val:.2f}", ha="center",
            fontsize=10.5, fontweight="bold" if tan else "normal",
            color="#a31515" if tan else "#1c1917")

# 접점 라인
ax.axhline(sharpe[-1], color="#d62728", linestyle="--", linewidth=1.4, alpha=0.6)
ax.text(0, sharpe[-1] + 0.04, "접점 포트폴리오의 샤프비율 — 모든 단일 자산보다 높음",
        fontsize=10, color="#a31515", fontweight="bold")

ax.set_ylim(0, max(sharpe) + 0.25)
ax.set_ylabel("샤프비율  (μ - R_f) / σ", fontsize=11)
ax.set_title("(b) 자산별 샤프비율\n접점 포트폴리오 > 모든 단일 자산",
             fontsize=11.5, pad=10)
ax.tick_params(axis="x", labelsize=9)

fig.suptitle(f"왜 접점 포트폴리오가 최선인가 — 샤프비율의 시각적 증거 (R_f = {Rf*100:.0f}%)",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch04_sharpe_comparison")
