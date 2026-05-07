"""1단원 Figure: 분산투자가 위험을 줄이는 효과.

가로축 = 포트폴리오에 담은 종목 수 N.
세로축 = 포트폴리오 표준편차 (위험).
종목 수가 늘수록 비체계적 위험은 감소하지만 체계적 위험은 남는다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(2)
N_max = 60
sims = 800

# 모든 종목의 변동성 = 30%, 평균 상관계수 = 0.3
sigma_i = 0.30
rho = 0.3

# 종목 수 N에 따른 포트폴리오 분산:
# Var(rp) = (1/N)*sigma^2 + (1-1/N)*rho*sigma^2
Ns = np.arange(1, N_max + 1)
var_p = (1 / Ns) * sigma_i ** 2 + (1 - 1 / Ns) * rho * sigma_i ** 2
sigma_p = np.sqrt(var_p)

# 시스템 위험 한계
limit = sigma_i * np.sqrt(rho)

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(Ns, sigma_p * 100, color="#1f6feb", linewidth=2.4,
        label="포트폴리오 표준편차")
ax.axhline(limit * 100, color="#d62728", linestyle="--", linewidth=1.5,
           label=f"체계적 위험 한계 ≈ {limit*100:.1f}%")
ax.fill_between(Ns, limit * 100, sigma_p * 100, alpha=0.18, color="#1f6feb",
                label="비체계적 위험 (분산 가능)")
ax.fill_between(Ns, 0, limit * 100, alpha=0.18, color="#d62728",
                label="체계적 위험 (분산 불가)")

ax.annotate("종목 1개:\n변동성 30%",
            xy=(1, sigma_i * 100), xytext=(7, 28),
            fontsize=10, arrowprops=dict(arrowstyle="->", color="#444"))
ax.annotate("30개 정도면\n체계적 위험에\n근접 (∼17%)",
            xy=(30, sigma_p[29] * 100), xytext=(36, 22),
            fontsize=10, arrowprops=dict(arrowstyle="->", color="#444"))

ax.set_xlabel("포트폴리오 종목 수 N")
ax.set_ylabel("포트폴리오 표준편차 (%)")
ax.set_title("분산투자 효과 — 종목 수가 늘수록 위험은 줄지만 0이 되지는 않는다\n"
             "(σ_i = 30%, 평균 상관계수 ρ = 0.3 가정)")
ax.legend(loc="upper right", fontsize=9.5)
ax.set_ylim(0, 32)

plt.tight_layout()
save(fig, "ch01_diversification")
