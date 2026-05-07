"""14단원 Figure 2: Buffett의 알파 감소.

팩터를 추가할 때마다 워렌 버핏의 미설명 알파(α)가 어떻게 감소하는지를 막대로.
출처: l4.pdf p.8, Table 1 (13F Portfolio, 1980~2017).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

models = ["MKT만\n(1팩터)", "MKT+SMB+HML+UMD\n(4팩터)",
          "+ BAB\n(5팩터)", "+ QMJ\n(6팩터)"]
alphas = [5.8, 4.5, 3.0, 0.3]
significant = [True, True, True, False]

colors = ["#d62728" if s else "#bbbbbb" for s in significant]

fig, ax = plt.subplots(figsize=(9.5, 5.5))
bars = ax.bar(models, alphas, color=colors, edgecolor="white", linewidth=2)

for bar, val, sig in zip(bars, alphas, significant):
    h = bar.get_height()
    label = f"{val}%"
    if not sig:
        label += "\n(통계적으로 비유의)"
    ax.text(bar.get_x() + bar.get_width() / 2, h + 0.15, label,
            ha="center", va="bottom", fontsize=10, fontweight="bold",
            color="#333" if sig else "#666")

ax.set_ylabel("워렌 버핏의 미설명 알파 α (%/연)", fontsize=11)
ax.set_title("팩터 모형이 정교해질수록 버핏의 '천재 알파'는 사라진다\n"
             "[Frazzini, Kabiller & Pedersen 2018; l4.pdf p.8 Table 1]")
ax.set_ylim(0, 7.0)

# 화살표로 감소 흐름 표시
for i in range(3):
    ax.annotate("", xy=(i + 1, alphas[i + 1] + 0.4),
                xytext=(i, alphas[i] + 0.4),
                arrowprops=dict(arrowstyle="->", color="#444", lw=1.4))

ax.text(2.0, 5.5,
        "BAB와 QMJ를 추가하면 알파가 0.3%로 떨어지고\n"
        "통계적 유의성도 사라진다.\n"
        "→ 버핏은 마법사가 아니라 6팩터 투자자였다.",
        fontsize=10, color="#1f6feb", ha="center",
        bbox=dict(boxstyle="round,pad=0.5", fc="#e3f2fd", ec="#1f6feb"))

ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
save(fig, "ch14_buffett_alpha")
