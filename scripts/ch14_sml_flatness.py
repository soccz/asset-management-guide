"""14단원 Figure 1: SML 평탄성 (BAB의 수익원).

CAPM이 예측하는 가파른 SML(점선) vs 실제 평탄한 SML(실선)을 비교.
실제 SML이 더 평탄한 만큼 저베타가 CAPM 예측보다 높은 알파를 갖고
고베타가 낮은 알파를 갖는다 → BAB의 수익원.
출처: Frazzini & Pedersen (2014), Fig.1 개념적 재현.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

betas = np.linspace(0.4, 1.8, 11)

# CAPM 예측 (가파른 직선): rf=2%, MRP=8%
rf = 0.02
mrp_capm = 0.08
expected_capm = rf + betas * mrp_capm

# 실제 SML (평탄): MRP_actual = 0.04 (절반)
mrp_actual = 0.04
intercept_actual = rf + 0.04
expected_actual = intercept_actual + betas * mrp_actual

# 십분위 점 (실제 데이터 패턴)
deciles = np.array([0.45, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.7])
returns = intercept_actual + deciles * mrp_actual + np.array([
    0.012, 0.008, 0.005, 0.003, 0.001, -0.001, -0.002, -0.005, -0.010, -0.015
])

fig, ax = plt.subplots(figsize=(9, 5.8))

ax.plot(betas, expected_capm * 100, "--", color="#888", linewidth=1.8,
        label=r"CAPM 예측 SML (가파름, MRP=8%)")
ax.plot(betas, expected_actual * 100, "-", color="#d62728", linewidth=2.2,
        label="실제 SML (평탄, MRP≈4%)")
ax.scatter(deciles, returns * 100, s=80, c="#1f6feb",
           edgecolors="white", linewidths=1.2, zorder=5,
           label="베타 십분위 평균 수익률 (실측)")

# 알파 표시 (저베타 P1, 고베타 P10)
ax.annotate("", xy=(deciles[0], returns[0] * 100),
            xytext=(deciles[0], (rf + deciles[0] * mrp_capm) * 100),
            arrowprops=dict(arrowstyle="<->", color="#2ca02c", lw=1.5))
ax.text(deciles[0] + 0.05, returns[0] * 100 - 0.5,
        "저베타 양의 α\n(BAB의 long 측)", fontsize=9, color="#2ca02c")

ax.annotate("", xy=(deciles[-1], returns[-1] * 100),
            xytext=(deciles[-1], (rf + deciles[-1] * mrp_capm) * 100),
            arrowprops=dict(arrowstyle="<->", color="#9467bd", lw=1.5))
ax.text(deciles[-1] - 0.55, returns[-1] * 100 + 1.5,
        "고베타 음의 α\n(BAB의 short 측)", fontsize=9, color="#9467bd")

ax.axhline(rf * 100, color="grey", linewidth=0.6, linestyle=":", alpha=0.7)
ax.text(0.42, rf * 100 + 0.2, "$R_f$", fontsize=10, color="grey")

ax.set_xlabel("시장 베타 (β)")
ax.set_ylabel("연환산 기대수익률 (%)")
ax.set_title("SML 평탄성 — BAB의 수익원\n"
             "[Frazzini & Pedersen 2014, Fig.1 개념적 재현]")
ax.legend(loc="upper left", fontsize=9)
ax.set_xlim(0.3, 1.9)
ax.set_ylim(0, 18)

plt.tight_layout()
save(fig, "ch14_sml_flatness")
