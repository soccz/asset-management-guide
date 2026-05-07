"""13단원 Figure: Momentum Smile.

x축 = 시장 수익률, y축 = TSMOM 수익률. 시장이 극단일 때 TSMOM이 빛난다.
출처: Moskowitz, Ooi & Pedersen (2012), Fig.4 개념적 재현.
정성적 패턴(U자/스마일)을 보여주는 데 목적이며, 수치 자체는 시뮬레이션이다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(42)
n = 400
mkt = rng.normal(0.005, 0.045, n)
tsmom = 8.0 * mkt**2 + 0.005 + rng.normal(0, 0.025, n)

fig, ax = plt.subplots(figsize=(8.5, 5.5))
ax.scatter(mkt * 100, tsmom * 100, s=24, alpha=0.55,
           c="#1f6feb", edgecolors="white", linewidths=0.4,
           label="월별 관측치 (시뮬레이션)")
xs = np.linspace(mkt.min(), mkt.max(), 200)
ax.plot(xs * 100, (8.0 * xs**2 + 0.005) * 100, color="#d62728", linewidth=2.2,
        label="평균 추세 (Momentum Smile)")
ax.axhline(0, color="grey", linewidth=0.6, linestyle="--")
ax.axvline(0, color="grey", linewidth=0.6, linestyle="--")
ax.set_xlabel("시장 수익률 (%) — S&P 500 월별")
ax.set_ylabel("TSMOM 포트폴리오 수익률 (%)")
ax.set_title("Momentum Smile — 시장이 극단일 때 TSMOM이 더 빛난다\n"
             "[Moskowitz, Ooi & Pedersen 2012, Fig.4 재현]")
ax.legend(loc="upper center", fontsize=9, frameon=True)

ax.annotate("시장 폭락 시기:\n모든 자산 short → 시장↓ → +수익",
            xy=(-9, 6.4), xytext=(-12, 9),
            fontsize=8.5, ha="left", color="#444",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
ax.annotate("강세장:\n모든 자산 long → 시장↑ → +수익",
            xy=(9, 6.4), xytext=(2.5, 9.2),
            fontsize=8.5, ha="left", color="#444",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
ax.annotate("횡보장:\n신호 섞임 → 수익 ≈ 0",
            xy=(0, 0.5), xytext=(-5, -3.0),
            fontsize=8.5, ha="left", color="#444",
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))

plt.tight_layout()
save(fig, "ch13_momentum_smile")
