"""8단원 보강: 가치 프리미엄(HML)의 시각적 증거.

(a) HML 누적수익 — 80년 시뮬레이션 (Fama-French 1963~ 정성적 재현)
(b) B/M 5분위 평균 연수익률 — 가치(High B/M) > 성장(Low B/M)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(2025)

# (a) HML 80년 누적수익 — 평균 연 4.5% 프리미엄, 변동성 12%
years = np.arange(1940, 2020)
T = len(years)
hml_returns = rng.normal(0.045, 0.12, T)
# 두 차례 반전기 (1990s 닷컴, 2010s 가치 부진)
hml_returns[55:60] = rng.normal(-0.05, 0.12, 5)
hml_returns[68:78] = rng.normal(-0.02, 0.10, 10)
cum_hml = np.cumprod(1 + hml_returns)

# 시장 비교
mkt_returns = rng.normal(0.10, 0.18, T)
cum_mkt = np.cumprod(1 + mkt_returns)

# (b) B/M 5분위 평균 연수익률
bm_quintiles = ["Q1\n(저 B/M\n성장주)", "Q2", "Q3", "Q4", "Q5\n(고 B/M\n가치주)"]
bm_returns_pct = [8.5, 10.2, 11.4, 13.0, 15.8]
colors_q = ["#d62728", "#e57b76", "#cccccc", "#7faedf", "#1f6feb"]

fig, axes = plt.subplots(1, 2, figsize=(15, 6.5),
                         gridspec_kw={"width_ratios": [1.4, 1], "wspace": 0.28})

# (a)
ax = axes[0]
ax.plot(years, cum_hml, color="#1f6feb", linewidth=2.4,
        label="HML (가치 - 성장)")
ax.plot(years, cum_mkt / cum_mkt[0] * cum_hml[0],
        color="#999", linewidth=1.4, linestyle="--",
        label="시장 (참고용 정규화)", alpha=0.7)
ax.axhline(1.0, color="#bbb", linestyle=":", linewidth=1)
ax.fill_between(years[55:60], 0, 50, alpha=0.15, color="#d62728")
ax.fill_between(years[68:78], 0, 50, alpha=0.15, color="#d62728")
ax.text(1995, 18, "닷컴\n(가치 부진)", fontsize=9.5, color="#a31515",
        ha="center", fontweight="bold")
ax.text(2013, 12, "2010년대\n(가치 부진 재현)", fontsize=9.5, color="#a31515",
        ha="center", fontweight="bold")

ax.set_yscale("log")
ax.set_title("(a) HML 80년 누적수익 — 가치 프리미엄의 장기 일관성\n"
             f"평균 연 +4.5% (시뮬레이션, $1 → ${cum_hml[-1]:.1f})",
             fontsize=12, pad=10)
ax.set_xlabel("연도", fontsize=11)
ax.set_ylabel("누적수익 ($1 시작, 로그 스케일)", fontsize=11)
ax.legend(loc="upper left", fontsize=10.5)

# (b)
ax = axes[1]
bars = ax.bar(bm_quintiles, bm_returns_pct, color=colors_q, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, bm_returns_pct):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3,
            f"{val:.1f}%", ha="center", fontsize=11, fontweight="bold")

# Q5 - Q1 = HML
hml_pct = bm_returns_pct[-1] - bm_returns_pct[0]
ax.annotate("", xy=(4, 15.8), xytext=(0, 8.5),
            arrowprops=dict(arrowstyle="->", color="#1f6feb", lw=2.4))
ax.text(2, 17, f"HML = Q5 - Q1\n= {hml_pct:.1f}%p / 년",
        ha="center", fontsize=11, color="#1f6feb", fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="#1f6feb", boxstyle="round,pad=0.5"))

ax.set_title("(b) B/M 5분위 평균 연수익률\n가치주(Q5) > 성장주(Q1) 일관성",
             fontsize=12, pad=10)
ax.set_ylabel("연 평균 수익률 (%)", fontsize=11)
ax.set_ylim(0, 20)

fig.suptitle("가치 프리미엄(HML) — Fama-French 1992 핵심 발견의 시각화",
             fontsize=14, y=1.02, fontweight="bold")

save(fig, "ch08_hml_value_premium")
