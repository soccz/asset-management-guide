"""6단원 보강: SDF와 payoff 매트릭스 — 자산가격결정의 만능 열쇠.

p = E[m · x]  =  Σ π_s · m_s · x_s

3개 상태(호황/평상/불황) × 2 자산(주식/채권)의 payoff와 SDF로
각 자산의 가격이 결정되는 도식.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 상태 (호황/평상/불황)
states = ["호황 (s₁)", "평상 (s₂)", "불황 (s₃)"]
probs = np.array([0.30, 0.50, 0.20])

# 자산별 payoff
payoff_stock = np.array([1.40, 1.05, 0.60])
payoff_bond  = np.array([1.04, 1.04, 1.04])

# SDF (불황에 클수록 = 위험회피 + 한계효용 큼)
sdf = np.array([0.85, 0.95, 1.30])

# 가격 = E[m·x]
price_stock = np.sum(probs * sdf * payoff_stock)
price_bond  = np.sum(probs * sdf * payoff_bond)

fig, ax = plt.subplots(figsize=(13, 6.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8.5)
ax.axis("off")

# 표 헤더
ax.text(2.0, 7.7, "상태 s", ha="center", fontsize=11, fontweight="bold")
ax.text(3.6, 7.7, "확률 π_s", ha="center", fontsize=11, fontweight="bold")
ax.text(5.2, 7.7, "SDF m_s", ha="center", fontsize=11, fontweight="bold",
        color="#1f6feb")
ax.text(7.0, 7.7, "주식 payoff x_s", ha="center", fontsize=11, fontweight="bold",
        color="#d62728")
ax.text(9.2, 7.7, "채권 payoff x_s", ha="center", fontsize=11, fontweight="bold",
        color="#2ca02c")
ax.text(11.0, 7.7, "기여도\nπ_s·m_s·x_s", ha="center", fontsize=10, fontweight="bold")

# 가로선
ax.plot([1.0, 11.8], [7.4, 7.4], color="#1c1917", linewidth=1.2)

# 행 (각 상태)
y_rows = [6.5, 5.5, 4.5]
for i, (state, p, m, xs, xb, y) in enumerate(zip(states, probs, sdf,
                                                  payoff_stock, payoff_bond, y_rows)):
    ax.text(2.0, y, state, ha="center", fontsize=11)
    ax.text(3.6, y, f"{p:.2f}", ha="center", fontsize=11, fontfamily="monospace")
    ax.text(5.2, y, f"{m:.2f}", ha="center", fontsize=11, fontfamily="monospace",
            color="#1f6feb", fontweight="bold")
    ax.text(7.0, y, f"{xs:.2f}", ha="center", fontsize=11, fontfamily="monospace",
            color="#a31515")
    ax.text(9.2, y, f"{xb:.2f}", ha="center", fontsize=11, fontfamily="monospace",
            color="#1f5e1f")
    contrib_s = p * m * xs
    contrib_b = p * m * xb
    ax.text(10.7, y, f"S: {contrib_s:.3f}", ha="left", fontsize=9.5, fontfamily="monospace")
    ax.text(10.7, y - 0.25, f"B: {contrib_b:.3f}", ha="left", fontsize=9.5, fontfamily="monospace")

# 합계 영역
ax.plot([1.0, 11.8], [3.9, 3.9], color="#888", linewidth=0.8)
ax.text(2.0, 3.4, "합계 (가격)", ha="center", fontsize=11, fontweight="bold")
ax.text(7.0, 3.4, f"$p_S = {price_stock:.3f}$", ha="center", fontsize=12,
        color="#a31515", fontweight="bold")
ax.text(9.2, 3.4, f"$p_B = {price_bond:.3f}$", ha="center", fontsize=12,
        color="#1f5e1f", fontweight="bold")

# 핵심 공식 박스
ax.text(6.0, 2.3,
        r"$\bf{p = E[m \cdot x] = \sum_s \pi_s \cdot m_s \cdot x_s}$",
        ha="center", fontsize=15,
        bbox=dict(facecolor="#fef3c7", edgecolor="#d97706",
                  boxstyle="round,pad=0.7", linewidth=1.5))

# 해설
ax.text(6.0, 1.2,
        "SDF m_s가 '불황에 클수록' = 그 상태의 payoff가 더 비싸다.\n"
        "주식은 호황 payoff 큰데 SDF 작음 → 평균적으로 가격이 낮아짐 (= 기대수익률 ↑).\n"
        "채권은 모든 상태 payoff 동일 → SDF 평균이 곧 가격 (R_f를 결정).",
        ha="center", fontsize=10.5, color="#444",
        bbox=dict(facecolor="white", edgecolor="#bbb",
                  boxstyle="round,pad=0.5"))

ax.set_title("SDF와 payoff — 자산가격은 '상태별 SDF×payoff의 가중평균'",
             fontsize=13.5, y=0.98, fontweight="bold")

save(fig, "ch06_sdf_payoff")
