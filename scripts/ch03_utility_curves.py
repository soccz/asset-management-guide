"""3단원 보강: 효용함수 형태 비교 (γ별 CRRA 효용).

효용함수는 위험회피 정도(γ)에 따라 모양이 달라진다.
γ가 클수록 더 보수적 — 같은 손익에 대한 효용 변화가 비대칭적으로 커짐.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 부 (wealth): 0.5 ~ 2.0
W = np.linspace(0.4, 2.0, 200)

def crra(W, gamma):
    """CRRA: U(W) = W^(1-γ) / (1-γ).  γ=1: log."""
    if abs(gamma - 1.0) < 1e-9:
        return np.log(W)
    return (W ** (1 - gamma) - 1) / (1 - gamma)

gammas = [0.5, 1.0, 2.0, 5.0]
colors = ["#2ca02c", "#1f6feb", "#ff9900", "#d62728"]
labels = [f"γ={g}\n(공격적)" if g < 1 else
          (f"γ={g}\n(중립)" if g == 1.0 else
           (f"γ={g}\n(보수적)" if g <= 3 else f"γ={g}\n(매우 보수적)"))
          for g in gammas]

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"wspace": 0.3})

# (a) 효용 곡선
ax = axes[0]
for g, c, l in zip(gammas, colors, labels):
    u = crra(W, g)
    # 정규화: U(1) = 0이 되도록 평행이동
    u = u - crra(np.array([1.0]), g)[0]
    ax.plot(W, u, color=c, linewidth=2.4, label=l)

ax.axvline(1.0, color="#1c1917", linestyle=":", linewidth=1, alpha=0.5)
ax.axhline(0.0, color="#1c1917", linestyle=":", linewidth=1, alpha=0.5)
ax.text(1.02, ax.get_ylim()[1] * 0.85, "기준점\nW=1",
        fontsize=10, color="#666", ha="left")

# 손실 영역 강조
ax.axvspan(0.4, 1.0, alpha=0.07, color="#d62728")
ax.axvspan(1.0, 2.0, alpha=0.07, color="#2ca02c")
ax.text(0.55, ax.get_ylim()[0] * 0.7, "손실 영역",
        fontsize=10, color="#a31515", fontweight="bold")
ax.text(1.55, ax.get_ylim()[0] * 0.7, "이익 영역",
        fontsize=10, color="#1f5e1f", fontweight="bold")

ax.set_xlabel("부 (Wealth, W)", fontsize=12)
ax.set_ylabel("효용 U(W) — W=1 정규화", fontsize=12)
ax.set_title("(a) γ별 CRRA 효용함수 형태\n오목할수록(γ↑) 손실 회피 강함",
             fontsize=12, pad=10)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.95)
ax.set_xlim(0.4, 2.0)

# (b) 같은 ±50% 손익에 대한 효용 변화
ax = axes[1]
gain_pcts = [-0.5, -0.25, 0, 0.25, 0.5]
labels_x = ["-50%", "-25%", "0%", "+25%", "+50%"]
data = {}
for g, c, l in zip(gammas, colors, labels):
    util_changes = []
    for delta in gain_pcts:
        W_new = 1.0 + delta
        u = crra(np.array([W_new]), g)[0] - crra(np.array([1.0]), g)[0]
        util_changes.append(u)
    data[g] = util_changes

x = np.arange(len(gain_pcts))
width = 0.18
for i, g in enumerate(gammas):
    offset = (i - 1.5) * width
    ax.bar(x + offset, data[g], width=width, color=colors[i],
           edgecolor="white", linewidth=0.8, label=f"γ={g}")

ax.axhline(0, color="#1c1917", linewidth=0.7)
ax.set_xticks(x)
ax.set_xticklabels(labels_x, fontsize=10.5)
ax.set_xlabel("부의 변화 (%)", fontsize=12)
ax.set_ylabel("효용 변화 ΔU", fontsize=12)
ax.set_title("(b) ±50% 손익의 효용 변화\nγ↑일수록 손실의 효용 감소가 가파름 (비대칭)",
             fontsize=12, pad=10)
ax.legend(loc="lower right", fontsize=10, framealpha=0.95)

fig.suptitle("위험회피 계수 γ — 효용함수의 모양과 의미",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch03_utility_curves")
