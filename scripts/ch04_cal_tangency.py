"""4단원 Figure: 자본배분선(CAL)과 접선 포트폴리오.

무위험자산(Rf, σ=0)을 추가하면 효율 프론티어가 곡선 → 직선(CAL)이 된다.
모든 투자자가 같은 위험자산 포트폴리오(접선 포트폴리오 = MVE)를 선택.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 효율 프론티어 (위쪽)
sig = np.linspace(0.06, 0.30, 200)
sigma_mvp = 0.08
mu_mvp = 0.05
mu_front = mu_mvp + 0.30 * np.sqrt(np.maximum(sig - sigma_mvp, 0))

# 무위험자산
rf = 0.02

# 접선 포트폴리오: CAL 기울기(샤프비율) 최대 → max (μ - rf) / σ
# d/dσ ((mu - rf)/σ) = 0 → σ * dμ/dσ - (μ - rf) = 0
sigs_fine = np.linspace(0.085, 0.30, 5000)
mus_fine = mu_mvp + 0.30 * np.sqrt(sigs_fine - sigma_mvp)
sharpe = (mus_fine - rf) / sigs_fine
idx_t = np.argmax(sharpe)
sig_t = sigs_fine[idx_t]
mu_t = mus_fine[idx_t]
sharpe_t = sharpe[idx_t]

# CAL 직선
sig_cal = np.linspace(0, 0.30, 100)
mu_cal = rf + sharpe_t * sig_cal

fig, ax = plt.subplots(figsize=(9.5, 6))
ax.plot(sig * 100, mu_front * 100, color="#1f6feb", linewidth=2.4,
        label="효율적 프론티어 (위험자산만)")
ax.plot(sig_cal * 100, mu_cal * 100, color="#d62728", linewidth=2.4,
        label=f"자본배분선 (CAL), 기울기=샤프비율={sharpe_t:.2f}")

ax.scatter(0, rf * 100, c="#444", s=180, marker="s", edgecolors="white",
           linewidths=1.5, zorder=5, label=f"무위험자산 R_f = {rf*100:.0f}%")
ax.scatter(sig_t * 100, mu_t * 100, c="#2ca02c", s=200, marker="*",
           edgecolors="white", linewidths=1.5, zorder=6,
           label=f"접선 포트폴리오 (MVE)")

# 영역 표시
ax.fill_between([0, sig_t * 100], rf * 100,
                rf + sharpe_t * np.array([0, sig_t]) * 100,
                alpha=0.0)  # 빈 영역
ax.annotate("Rf와 MVE 사이:\n무위험자산을 일부 보유\n(저위험 투자자)",
            xy=(sig_t * 50, (rf + sharpe_t * sig_t * 0.5) * 100),
            xytext=(2, 16),
            fontsize=9, ha="left", color="#555",
            arrowprops=dict(arrowstyle="->", color="#888"))
ax.annotate("MVE 너머:\n돈을 빌려 MVE에 추가 투자\n(레버리지 = 공격적 투자자)",
            xy=(0.27 * 100, (rf + sharpe_t * 0.27) * 100),
            xytext=(15, 28),
            fontsize=9, ha="left", color="#555",
            arrowprops=dict(arrowstyle="->", color="#888"))

ax.set_xlabel("표준편차 σ (%)")
ax.set_ylabel("기대수익률 μ (%)")
ax.set_title("자본배분선(CAL) — 무위험자산이 추가되면 곡선 프론티어가 직선이 된다\n"
             "모든 투자자가 동일한 접선 포트폴리오 MVE를 선택 (2기금 분리)")
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim(-1, 32)
ax.set_ylim(0, 32)

plt.tight_layout()
save(fig, "ch04_cal_tangency")
