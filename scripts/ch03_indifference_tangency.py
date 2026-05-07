"""3단원 Figure: 효용 무차별 곡선과 효율 프론티어의 접점.

다양한 γ(위험회피계수)를 가진 투자자의 무차별 곡선이
효율 프론티어와 만나는 접점이 그 투자자의 최적 포트폴리오.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 효율 프론티어 (간단한 모형: σ에 대한 mu의 위쪽 곡선)
sig = np.linspace(0.06, 0.30, 200)
# 프론티어: μ = a + b*sqrt(σ - σ_mvp) (포물선 비슷)
sigma_mvp = 0.08
mu_mvp = 0.05
mu_front = mu_mvp + 0.30 * np.sqrt(np.maximum(sig - sigma_mvp, 0))

fig, ax = plt.subplots(figsize=(9, 6))
ax.plot(sig * 100, mu_front * 100, color="#1f6feb", linewidth=2.4,
        label="효율적 프론티어 (위쪽)")
ax.scatter(sigma_mvp * 100, mu_mvp * 100, c="#d62728", s=120,
           edgecolors="white", linewidths=1.5, zorder=5, label="MVP")

# 무차별 곡선 — U = μ - (γ/2) σ²
def indif(gamma, U, sig_arr):
    return U + 0.5 * gamma * sig_arr ** 2

gammas = [2.0, 4.0, 8.0]
colors = ["#9467bd", "#e7298a", "#1b9e77"]
labels = ["γ=2 (공격적)", "γ=4 (균형)", "γ=8 (보수적)"]

# 각 γ에 대해 접점 찾기
for gamma, color, label in zip(gammas, colors, labels):
    # 접점: dμ/dσ = γσ → 0.30 / (2 sqrt(σ - σ_mvp)) = γσ
    sigs = np.linspace(0.085, 0.30, 1000)
    dmu_dsigma = 0.30 / (2 * np.sqrt(sigs - sigma_mvp))
    target = gamma * sigs
    diff = np.abs(dmu_dsigma - target)
    idx = np.argmin(diff)
    sig_opt = sigs[idx]
    mu_opt = mu_mvp + 0.30 * np.sqrt(sig_opt - sigma_mvp)

    # 무차별 곡선 (그 투자자가 도달한 효용 수준)
    U_star = mu_opt - 0.5 * gamma * sig_opt ** 2
    sig_grid = np.linspace(0, 0.32, 200)
    mu_grid = indif(gamma, U_star, sig_grid)
    ax.plot(sig_grid * 100, mu_grid * 100, "--", color=color, linewidth=1.5,
            alpha=0.7, label=label + f" → σ={sig_opt*100:.1f}%")
    ax.scatter(sig_opt * 100, mu_opt * 100, c=color, s=120, zorder=6,
               edgecolors="white", linewidths=1.2)

ax.set_xlabel("표준편차 σ (%)")
ax.set_ylabel("기대수익률 μ (%)")
ax.set_title("무차별 곡선과 효율 프론티어의 접점 = 그 투자자의 최적 포트폴리오\n"
             "γ가 작을수록 (공격적) 더 오른쪽 (위험-수익 큰 점)을 선택")
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim(0, 32)
ax.set_ylim(2, 22)

plt.tight_layout()
save(fig, "ch03_indifference_tangency")
