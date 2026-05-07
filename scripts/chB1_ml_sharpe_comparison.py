"""B1단원 보강: ML 모형별 OOS 샤프비율 비교.

KNS, IPCA, Conditional Autoencoder, Deng (대규모 최적화) — 4가지 모형의
out-of-sample 샤프비율과 alpha 비교 (정성적 재현).

[Kelly et al. 2019, 2021, Kozak 2020, Gu·Kelly·Xiu 2021, Deng 2024 보고치
정성적 재현]
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 모형별 OOS 샤프비율 + alpha (가상 / 정성적 재현)
models = ["FF6\n(전통 회귀)", "KNS\n(선형 SDF)", "IPCA\n(잠재 팩터)",
          "CAE\n(비선형 노출)", "Deng\n(대규모 MV)"]
sharpe_oos = [0.62, 1.10, 1.45, 1.78, 1.92]
alpha_pct = [0.0, 0.4, 1.1, 1.8, 2.4]
colors = ["#888", "#1f6feb", "#2ca02c", "#9467bd", "#d62728"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5.8),
                         gridspec_kw={"wspace": 0.28})

# (a) OOS Sharpe
ax = axes[0]
bars = ax.bar(models, sharpe_oos, color=colors, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, sharpe_oos):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.04,
            f"{val:.2f}", ha="center", fontsize=11, fontweight="bold")

ax.axhline(sharpe_oos[0], color="#888", linestyle="--", linewidth=1.2, alpha=0.6)
ax.text(4.0, sharpe_oos[0] + 0.04, "FF6 baseline",
        fontsize=9, color="#666", ha="right")

ax.set_title("(a) OOS Sharpe Ratio — 모형 복잡도 ↑ → 성능 ↑\n"
             "선형(KNS) → 잠재(IPCA) → 비선형(CAE) → 대규모(Deng)",
             fontsize=11.5, pad=10)
ax.set_ylabel("Out-of-Sample 샤프비율", fontsize=11)
ax.set_ylim(0, 2.2)
ax.tick_params(axis="x", labelsize=9.5)

# (b) Annualized alpha
ax = axes[1]
bars = ax.bar(models, alpha_pct, color=colors, edgecolor="#1c1917",
              linewidth=0.8, width=0.7)
for bar, val in zip(bars, alpha_pct):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.06,
            f"{val:+.1f}%", ha="center", fontsize=11, fontweight="bold")

ax.axhline(0, color="#1c1917", linewidth=0.7)
ax.set_title("(b) FF6 대비 연간 α (%)\nML 모형이 잡는 추가 수익",
             fontsize=11.5, pad=10)
ax.set_ylabel("연간 α (%)", fontsize=11)
ax.set_ylim(-0.3, 3.0)
ax.tick_params(axis="x", labelsize=9.5)

# 메시지 박스
fig.text(0.5, -0.04,
         "핵심: 모형이 복잡해질수록 OOS 성능이 상승 — 단, transaction cost·overfitting 비용 증가.",
         ha="center", fontsize=10.5, color="#555", style="italic")

fig.suptitle("ML 자산가격결정 — 모형 복잡도와 OOS 성능 (정성적 재현)",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "chB1_ml_sharpe_comparison")
