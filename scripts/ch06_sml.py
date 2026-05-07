"""6단원 보강: Security Market Line — CAPM의 시각적 핵심.

E[R_i] = R_f + β_i·(E[R_m] − R_f)
SML 위 = 양의 알파(과소가격), 아래 = 음의 알파(과대가격).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(11)

Rf = 0.04   # 무위험 수익률
ERP = 0.06  # 시장 위험 프리미엄

betas_range = np.linspace(0, 2.0, 100)
sml = Rf + betas_range * ERP

# 가상 자산 12개
n = 12
asset_betas = np.linspace(0.3, 1.8, n)
# CAPM 예측에 잡음 + 의도적 알파 (저베타 +α, 고베타 −α 패턴)
alphas = -0.025 * (asset_betas - 1.0) + rng.normal(0, 0.008, n)
asset_returns = Rf + asset_betas * ERP + alphas

fig, ax = plt.subplots(figsize=(11, 7))

# SML
ax.plot(betas_range, sml * 100, color="#1f6feb", linewidth=2.5,
        label="Security Market Line (CAPM 예측)")

# 자산 점
for b, r, a in zip(asset_betas, asset_returns, alphas):
    color = "#2ca02c" if a > 0 else "#d62728"
    ax.scatter([b], [r * 100], s=110, color=color, zorder=5,
               edgecolor="#1c1917", linewidth=0.9)
    # 알파 화살표
    expected = Rf + b * ERP
    ax.annotate("", xy=(b, r * 100), xytext=(b, expected * 100),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.4, alpha=0.7))

# Rf 마커
ax.scatter([0], [Rf * 100], s=120, color="#1c1917", marker="D", zorder=6)
ax.annotate(f"R_f = {Rf*100:.0f}%", xy=(0, Rf * 100), xytext=(0.1, Rf * 100 - 0.6),
            fontsize=11)

# 시장 포트폴리오
mkt_r = (Rf + ERP) * 100
ax.scatter([1.0], [mkt_r], s=180, color="#1f6feb", marker="*", zorder=6,
           edgecolor="white", linewidth=1.5)
ax.annotate(f"시장 포트폴리오 M\n(β=1, E[R]={mkt_r:.0f}%)",
            xy=(1.0, mkt_r), xytext=(1.05, mkt_r - 1.5),
            fontsize=10.5)

# 라벨 박스
ax.text(0.4, 12,
        "SML 위\n→ 양의 α\n(과소평가, BUY)",
        fontsize=10.5, color="#1f5e1f",
        bbox=dict(facecolor="white", edgecolor="#2ca02c", boxstyle="round,pad=0.5"))
ax.text(1.55, 8,
        "SML 아래\n→ 음의 α\n(과대평가, SELL)",
        fontsize=10.5, color="#a31515",
        bbox=dict(facecolor="white", edgecolor="#d62728", boxstyle="round,pad=0.5"))

ax.set_xlabel("베타 β (시장 노출도)", fontsize=12)
ax.set_ylabel("기대 수익률 E[R] (%)", fontsize=12)
ax.set_title("Security Market Line — CAPM 예측과 알파의 의미\n"
             f"E[R_i] = R_f + β_i · ERP   (R_f={Rf*100:.0f}%, ERP={ERP*100:.0f}%)",
             fontsize=13, pad=14)
ax.legend(loc="upper left", fontsize=11)
ax.set_xlim(-0.05, 2.05)
ax.set_ylim(2, 18)

save(fig, "ch06_sml")
