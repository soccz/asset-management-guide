"""10단원 Figure: 변동성 스케일링 효과.

(a) 변동성 클러스터링
(b) 같은 모멘텀 신호로 만든 누적수익 — 원래 vs 스케일 버전

[Barroso & Santa-Clara 2015 Fig.1·6] 정성적 패턴 재현 (시뮬레이션).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(7)

T = 1200  # 100년 월별
months = np.arange(T)

# === 변동성 시계열 (클러스터링) ===
sigma_t = np.full(T, 0.05)
for t in range(1, T):
    sigma_t[t] = 0.92 * sigma_t[t - 1] + 0.08 * 0.05 + abs(rng.normal(0, 0.003))

# 두 차례 위기 (1932 / 2009)
def crisis(start, peak_idx, end, peak_vol):
    rise = np.linspace(sigma_t[start - 1], peak_vol, peak_idx - start)
    fall = np.linspace(peak_vol, 0.06, end - peak_idx)
    sigma_t[start:peak_idx] = rise
    sigma_t[peak_idx:end] = fall

crisis(290, 308, 335, 0.20)
crisis(990, 1008, 1035, 0.22)
sigma_t = np.clip(sigma_t, 0.025, 0.25)

# === 모멘텀 수익률 (평균 양수, 변동성 비례) ===
# 평균: 월 0.7% → 연 ~8.4% (실제 WML 평균과 유사)
mu_mom = 0.007
mom = mu_mom + sigma_t * rng.normal(0, 1, T)

# 위기 직후 크래시 (모멘텀 뒤집힘)
mom[315:320] = [-0.10, -0.15, -0.08, -0.05, -0.04]
mom[1015:1020] = [-0.12, -0.18, -0.10, -0.06, -0.04]

# === 변동성 스케일 ===
sigma_hat = np.zeros(T)
window = 6
for t in range(T):
    if t < 2:
        sigma_hat[t] = 0.05
    else:
        sigma_hat[t] = max(0.025, np.std(mom[max(0, t - window):t]))

target = 0.05
scale = np.minimum(target / sigma_hat, 2.5)
mom_scaled = scale * mom

# === 누적 수익 ===
cum_orig = np.cumprod(1 + mom)
cum_scaled = np.cumprod(1 + mom_scaled)

# === 그림 ===
fig, axes = plt.subplots(2, 1, figsize=(14, 10),
                         gridspec_kw={"hspace": 0.45, "height_ratios": [1, 1.2]})

# (a) 변동성 클러스터링
ax = axes[0]
ax.plot(months, sigma_t * 100, color="#333", linewidth=1.0)
ax.fill_between(months, 0, sigma_t * 100, alpha=0.30, color="#888")
ax.axhline(5, color="#1f6feb", linestyle="--", linewidth=1.4,
           label="평상시 변동성 ≈ 5%")
ax.axvspan(290, 335, alpha=0.22, color="#d62728")
ax.axvspan(990, 1035, alpha=0.22, color="#d62728")
ax.text(312, 23.5, "1932\n대공황", ha="center", fontsize=11,
        color="#a31515", fontweight="bold")
ax.text(1012, 23.5, "2009\n금융위기", ha="center", fontsize=11,
        color="#a31515", fontweight="bold")
ax.set_title("(a) 변동성 클러스터링 — 변동성은 시기마다 크게 다르다\n"
             "한번 폭증하면 한동안 큰 채로 유지된다 → 다음 달을 어느 정도 예측 가능 (스케일링의 토대)",
             fontsize=12)
ax.set_xlabel("월 (가상 기간 1900~2010, 약 100년)")
ax.set_ylabel("월별 변동성 σ (%)")
ax.set_ylim(0, 27)
ax.legend(loc="upper right", fontsize=10.5)

# (b) 누적수익 비교
ax = axes[1]
ax.plot(months, cum_orig, color="#d62728", linewidth=1.7,
        label="원래 WML  (변동성 스케일링 없음)")
ax.plot(months, cum_scaled, color="#1f6feb", linewidth=2.0,
        label=f"변동성 스케일 WML  (target σ = {target*100:.0f}%)")
ax.set_yscale("log")
ax.axvspan(290, 335, alpha=0.22, color="#d62728")
ax.axvspan(990, 1035, alpha=0.22, color="#d62728")

final_orig = cum_orig[-1]
final_scaled = cum_scaled[-1]
ax.text(T + 5, final_orig, f"  최종\n  $1 → ${final_orig:,.1f}",
        fontsize=10, color="#a31515", va="center", fontweight="bold")
ax.text(T + 5, final_scaled, f"  최종\n  $1 → ${final_scaled:,.1f}",
        fontsize=10, color="#1f6feb", va="center", fontweight="bold")

# 샤프비율 비교 (연환산)
sharpe_orig = np.mean(mom) / np.std(mom) * np.sqrt(12)
sharpe_scaled = np.mean(mom_scaled) / np.std(mom_scaled) * np.sqrt(12)
sharpe_box = (
    f"연환산 샤프비율 비교\n"
    f"   원래 WML        : {sharpe_orig:.2f}\n"
    f"   스케일 WML      : {sharpe_scaled:.2f}\n"
    f"   향상 배율         : {sharpe_scaled/sharpe_orig:.2f}×\n"
    "(Barroso 2015 실측: 0.53 → 0.97, ≈ 1.83×)"
)
ax.text(0.02, 0.98, sharpe_box, transform=ax.transAxes,
        fontsize=9.5, va="top", ha="left", family="monospace",
        bbox=dict(boxstyle="round,pad=0.5", fc="#fffde7", ec="#888"))

# 크래시 직후 강조
ax.annotate("크래시 직후 큰 손실",
            xy=(322, cum_orig[322]), xytext=(420, cum_orig[322] * 0.35),
            fontsize=10, color="#a31515",
            arrowprops=dict(arrowstyle="->", color="#a31515", lw=1.2))
ax.annotate("스케일링이\n크래시 직전 σ̂ 급증을 감지\n→ 자동으로 비중 축소\n→ 손실 완화",
            xy=(322, cum_scaled[322]), xytext=(390, cum_scaled[322] * 1.8),
            fontsize=10, color="#1f6feb",
            arrowprops=dict(arrowstyle="->", color="#1f6feb", lw=1.2))

ax.set_title("(b) 누적수익 비교 — 같은 모멘텀 신호, 다른 위험 관리\n"
             "원래 WML은 위기 직후 크래시로 큰 손실. 스케일 버전은 σ̂ 급증을 감지해 자동 비중 축소.",
             fontsize=12)
ax.set_xlabel("월")
ax.set_ylabel("누적수익 (로그 스케일, 시작 = $1)")
ax.set_xlim(0, T + 130)
ax.legend(loc="upper left", fontsize=10.5)

fig.suptitle("변동성 스케일링이 모멘텀 크래시를 어떻게 방어하는가\n"
             "[Barroso & Santa-Clara 2015 Fig.1·6 정성적 재현 — 시뮬레이션]",
             fontsize=14, y=0.995, fontweight="bold")

save(fig, "ch10_volatility_scaling")
