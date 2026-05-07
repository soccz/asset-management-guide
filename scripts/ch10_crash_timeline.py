"""10단원 보강: 모멘텀 크래시 — 역사적 사건 두 번의 월별 손실.

(a) 1932 8월: WML −78.96% (대공황 회복기)
(b) 2009 4월: WML −45.83% (글로벌 금융위기 직후 반등)

Barroso & Santa-Clara 2015, Daniel & Moskowitz 2016 보고치 기준.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"wspace": 0.28})

# (a) 1932 사건
ax = axes[0]
months_1932 = ["1932-04", "-05", "-06", "-07", "-08*", "-09", "-10", "-11"]
wml_1932 = [-5.2, -8.1, -12.4, -22.0, -78.96, +12.5, +8.3, +4.1]
colors_1932 = ["#888"] * 4 + ["#a31515"] + ["#2ca02c"] * 3
bars = ax.bar(months_1932, wml_1932, color=colors_1932, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, wml_1932):
    y = val + (1.5 if val > 0 else -3.5)
    ax.text(bar.get_x() + bar.get_width()/2, y,
            f"{val:+.1f}%", ha="center", fontsize=9.5,
            fontweight="bold" if val < -30 else "normal")

ax.axhline(0, color="#1c1917", linewidth=0.7)
ax.set_title("(a) 1932년 — 대공황 회복기 모멘텀 크래시\n8월 단월 -78.96% (역사상 최대)",
             fontsize=12, pad=10)
ax.set_ylabel("WML 월별 수익률 (%)", fontsize=11)
ax.set_ylim(-90, 25)

ax.annotate("시장 변동성 폭증 →\n공매도(과거 패자) 급반등 →\n모멘텀 long-short 동시 손실",
            xy=(4, -78.96), xytext=(5.7, -55),
            fontsize=9.8, color="#a31515",
            bbox=dict(facecolor="white", edgecolor="#d62728", boxstyle="round,pad=0.4"),
            arrowprops=dict(arrowstyle="->", color="#a31515", lw=1.4))

# (b) 2009 사건
ax = axes[1]
months_2009 = ["2009-01", "-02", "-03", "-04*", "-05", "-06", "-07", "-08"]
wml_2009 = [-3.1, -5.4, -8.2, -45.83, -3.1, +1.2, +5.4, +3.8]
colors_2009 = ["#888"] * 3 + ["#a31515"] + ["#888"] + ["#2ca02c"] * 3
bars = ax.bar(months_2009, wml_2009, color=colors_2009, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, wml_2009):
    y = val + (1.5 if val > 0 else -3.5)
    ax.text(bar.get_x() + bar.get_width()/2, y,
            f"{val:+.1f}%", ha="center", fontsize=9.5,
            fontweight="bold" if val < -30 else "normal")

ax.axhline(0, color="#1c1917", linewidth=0.7)
ax.set_title("(b) 2009년 — 금융위기 직후 모멘텀 크래시\n3월 시장 바닥 → 4월 단월 -45.83%",
             fontsize=12, pad=10)
ax.set_ylabel("WML 월별 수익률 (%)", fontsize=11)
ax.set_ylim(-55, 15)

ax.annotate("금융위기로 폭락한 은행주(과거 패자)가\n3-4월 급반등 →\n공매도한 모멘텀 전략 손실",
            xy=(3, -45.83), xytext=(4.5, -32),
            fontsize=9.8, color="#a31515",
            bbox=dict(facecolor="white", edgecolor="#d62728", boxstyle="round,pad=0.4"),
            arrowprops=dict(arrowstyle="->", color="#a31515", lw=1.4))

fig.suptitle("모멘텀 크래시의 역사적 두 사례 — 같은 메커니즘, 80년 간격\n"
             "[Barroso & Santa-Clara 2015, Daniel & Moskowitz 2016 보고치]",
             fontsize=14, y=1.02, fontweight="bold")

save(fig, "ch10_crash_timeline")
