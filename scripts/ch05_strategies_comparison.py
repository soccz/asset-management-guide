"""5단원 Figure: 4가지 포트폴리오 전략 비교.

(a) 가중치 비교 막대 — EW, MV, RP, MD
(b) 60/40 vs 25/75의 위험 기여도
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# (a) 5개 자산에 대한 4전략 가중치 (가상 결과)
assets = ["주식 A", "주식 B", "주식 C", "채권 D", "원자재 E"]
ew = np.full(5, 0.20)
mv = np.array([0.12, 0.08, 0.05, 0.65, 0.10])  # 저변동성 채권에 집중
rp = np.array([0.18, 0.15, 0.12, 0.45, 0.10])  # 채권 비중 크지만 MV보다 분산
md = np.array([0.22, 0.18, 0.20, 0.30, 0.10])

fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

ax = axes[0]
x = np.arange(len(assets))
w = 0.20
ax.bar(x - 1.5*w, ew * 100, w, label="EW (동일가중)", color="#1f6feb")
ax.bar(x - 0.5*w, mv * 100, w, label="MV (최소분산)", color="#d62728")
ax.bar(x + 0.5*w, rp * 100, w, label="RP (리스크패리티)", color="#2ca02c")
ax.bar(x + 1.5*w, md * 100, w, label="MD (최대분산)", color="#9467bd")
ax.set_xticks(x)
ax.set_xticklabels(assets, fontsize=9)
ax.set_ylabel("가중치 (%)")
ax.set_title("(a) 4가지 전략의 자산별 가중치 비교\n"
             "MV는 저변동성 자산에 집중 / EW는 무관히 균등")
ax.legend(loc="upper right", fontsize=9)
ax.set_ylim(0, 75)

# (b) 60/40 vs 25/75 위험 기여
# 60/40: 주식 60%, 채권 40%, σ_s=0.15, σ_b=0.05, ρ=0.2
# 25/75: 주식 25%, 채권 75%
ax = axes[1]
sig_s, sig_b, rho = 0.15, 0.05, 0.2

def risk_contribs(w_s, w_b):
    Sigma = np.array([[sig_s**2, rho*sig_s*sig_b],
                      [rho*sig_s*sig_b, sig_b**2]])
    w = np.array([w_s, w_b])
    var_p = w @ Sigma @ w
    sigma_p = np.sqrt(var_p)
    rc_s = w[0] * (Sigma @ w)[0] / sigma_p
    rc_b = w[1] * (Sigma @ w)[1] / sigma_p
    return rc_s, rc_b, sigma_p

rc_s_60, rc_b_60, vp_60 = risk_contribs(0.6, 0.4)
rc_s_25, rc_b_25, vp_25 = risk_contribs(0.25, 0.75)

# 정규화 (위험 기여 비율로)
total_60 = rc_s_60 + rc_b_60
total_25 = rc_s_25 + rc_b_25

categories = ["60/40 포트폴리오", "25/75 (Risk Parity)"]
stock_share = [rc_s_60 / total_60 * 100, rc_s_25 / total_25 * 100]
bond_share = [rc_b_60 / total_60 * 100, rc_b_25 / total_25 * 100]

bottom_pct = np.array(stock_share)
ax.bar(categories, stock_share, color="#d62728", label="주식의 위험 기여",
       edgecolor="white", linewidth=2)
ax.bar(categories, bond_share, bottom=bottom_pct, color="#1f6feb",
       label="채권의 위험 기여", edgecolor="white", linewidth=2)

for i, (s, b) in enumerate(zip(stock_share, bond_share)):
    ax.text(i, s / 2, f"{s:.0f}%", ha="center", color="white",
            fontsize=11, fontweight="bold")
    ax.text(i, s + b / 2, f"{b:.0f}%", ha="center", color="white",
            fontsize=11, fontweight="bold")

ax.set_ylabel("위험 기여 비율 (%)")
ax.set_title("(b) 자본 비중 vs 위험 비중\n"
             "60/40: 자본은 60/40이지만 위험은 ~92/8 → 사실상 주식 단일 노출")
ax.set_ylim(0, 105)
ax.legend(loc="upper right", fontsize=9)

plt.tight_layout()
save(fig, "ch05_strategies_comparison")
