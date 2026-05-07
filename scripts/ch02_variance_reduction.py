"""2단원 보강: 분산투자의 정량적 한계.

자산 수 N이 늘어날수록 포트폴리오 분산은 줄지만 평균 공분산(체계적 위험)으로 수렴.
σ²_p = (1/N)·σ²_indiv + ((N-1)/N)·cov_avg
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 가정: 개별 자산 표준편차 30%, 평균 상관계수 0.3
sigma_indiv = 0.30
rho_avg = 0.30
cov_avg = rho_avg * sigma_indiv ** 2  # 평균 공분산

Ns = np.arange(1, 51)
var_p = (1 / Ns) * sigma_indiv ** 2 + ((Ns - 1) / Ns) * cov_avg
sd_p = np.sqrt(var_p)

systematic = np.sqrt(cov_avg)  # 체계적 위험 (수렴값)

fig, ax = plt.subplots(figsize=(11, 6))

ax.plot(Ns, sd_p * 100, color="#1f6feb", linewidth=2.4,
        label="포트폴리오 표준편차 σ_p")
ax.fill_between(Ns, systematic * 100, sd_p * 100,
                alpha=0.18, color="#1f6feb", label="비체계적 위험 (분산으로 제거 가능)")
ax.axhline(systematic * 100, color="#d62728", linestyle="--", linewidth=1.6,
           label=f"체계적 위험 (σ → {systematic*100:.1f}%)")
ax.fill_between(Ns, 0, systematic * 100,
                alpha=0.10, color="#d62728")

# 핵심 포인트 강조
for n_mark in [1, 5, 20]:
    sd = sd_p[n_mark - 1] * 100
    ax.scatter([n_mark], [sd], s=80, color="#1c1917", zorder=5)
    ax.annotate(f"N={n_mark}\nσ={sd:.1f}%",
                xy=(n_mark, sd), xytext=(n_mark + 2, sd + 1.5),
                fontsize=10.5, fontweight="bold")

ax.set_xlabel("포트폴리오에 포함된 자산 수 N", fontsize=12)
ax.set_ylabel("포트폴리오 표준편차 σ_p (%)", fontsize=12)
ax.set_title("분산투자의 한계 — 자산을 늘려도 체계적 위험은 사라지지 않는다\n"
             f"(개별 자산 σ={sigma_indiv*100:.0f}%, 평균 상관계수 ρ={rho_avg:.2f} 가정)",
             fontsize=13, pad=14)
ax.legend(loc="upper right", fontsize=11, framealpha=0.95)
ax.set_xlim(0, 51)
ax.set_ylim(0, 32)

# 메시지 박스
ax.text(35, 22,
        "N이 클수록 σ_p는\n체계적 위험에 수렴한다.\n→ 분산투자만으론 못 없애는 위험",
        fontsize=10.5, color="#a31515",
        bbox=dict(facecolor="white", edgecolor="#d62728", boxstyle="round,pad=0.6"))

save(fig, "ch02_variance_reduction")
