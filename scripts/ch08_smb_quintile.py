"""8단원 보강: 사이즈 5분위 평균 수익률 — Banz 1981 사이즈 효과.

시가총액으로 5분위(Q1=대형, Q5=소형) 정렬.
역사적으로 소형주가 대형주보다 약 3~5%/년 높은 수익 → SMB 팩터.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

quintiles = ["Q1\n(대형)", "Q2", "Q3", "Q4", "Q5\n(소형)"]
returns_pct = [9.5, 10.4, 11.6, 12.8, 14.2]      # 평균 연수익률
volatility_pct = [16.5, 17.8, 19.2, 21.5, 24.8]  # 변동성 (소형일수록 ↑)

colors = ["#1f6feb", "#5e9af2", "#9bc4f5", "#cccccc", "#d62728"]

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"wspace": 0.28})

# (a) 평균 수익률 막대
ax = axes[0]
bars = ax.bar(quintiles, returns_pct, color=colors, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, returns_pct):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.25,
            f"{val:.1f}%", ha="center", fontsize=11, fontweight="bold")

# SMB = Q5 - Q1 강조
smb = returns_pct[-1] - returns_pct[0]
ax.annotate("", xy=(4, returns_pct[-1]), xytext=(0, returns_pct[0]),
            arrowprops=dict(arrowstyle="->", color="#1f6feb", lw=2.4))
ax.text(2, 17, f"SMB = Q5 - Q1\n= {smb:.1f}%p / 년",
        ha="center", fontsize=11, color="#1f6feb", fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="#1f6feb", boxstyle="round,pad=0.5"))

ax.set_ylabel("평균 연수익률 (%)", fontsize=11)
ax.set_title("(a) 사이즈 5분위 평균 수익률\n소형주(Q5) > 대형주(Q1) 일관성",
             fontsize=12, pad=10)
ax.set_ylim(0, 19)

# (b) 평균 vs 변동성 (위험 조정)
ax = axes[1]
sharpe = [(r - 4) / s for r, s in zip(returns_pct, volatility_pct)]  # R_f=4%

x = np.arange(len(quintiles))
width = 0.35

ax.bar(x - width/2, returns_pct, width=width, color="#1f6feb",
       edgecolor="white", linewidth=0.8, label="평균 수익률 (%)")
ax.bar(x + width/2, volatility_pct, width=width, color="#ff9900",
       edgecolor="white", linewidth=0.8, label="변동성 σ (%)")

ax.set_xticks(x)
ax.set_xticklabels(quintiles, fontsize=10.5)

# 샤프비율 텍스트
for i, sh in enumerate(sharpe):
    ax.text(i, max(returns_pct[i], volatility_pct[i]) + 1.0,
            f"Sharpe {sh:.2f}",
            ha="center", fontsize=9, color="#444", fontweight="bold")

ax.set_ylabel("값 (%)", fontsize=11)
ax.set_title("(b) 평균 vs 변동성 — 소형주는 수익도 변동성도 높음\n샤프비율(R_f=4%)로 위험 조정",
             fontsize=12, pad=10)
ax.legend(loc="upper left", fontsize=10.5)
ax.set_ylim(0, 32)

fig.suptitle("사이즈 효과(Banz 1981) — 소형주의 추가 수익과 추가 위험",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch08_smb_quintile")
