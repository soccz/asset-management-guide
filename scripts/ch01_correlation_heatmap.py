"""1단원 보강: 자산 간 상관계수 히트맵 — 분산투자 효과의 정량적 근거.

상관계수가 낮을수록 분산투자 효과가 크다.
6 자산군 (주식 US/EM, 채권, REITs, 원자재, 금)의 historic 상관행렬 (정성적).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

assets = ["주식\n(US)", "주식\n(EM)", "채권", "REITs", "원자재", "금"]
n = len(assets)

# 정성적 historic 상관 (대략적 추정치)
corr = np.array([
    [1.00, 0.78, -0.05, 0.65, 0.30, 0.05],
    [0.78, 1.00, -0.10, 0.55, 0.40, 0.10],
    [-0.05, -0.10, 1.00, 0.20, -0.15, 0.20],
    [0.65, 0.55, 0.20, 1.00, 0.35, 0.15],
    [0.30, 0.40, -0.15, 0.35, 1.00, 0.45],
    [0.05, 0.10, 0.20, 0.15, 0.45, 1.00],
])

fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                         gridspec_kw={"width_ratios": [1.1, 1], "wspace": 0.35})

# (a) 히트맵
ax = axes[0]
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels(assets, fontsize=10)
ax.set_yticklabels(assets, fontsize=10)
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# 셀 안 값
for i in range(n):
    for j in range(n):
        val = corr[i, j]
        color = "white" if abs(val) > 0.55 else "#1c1917"
        ax.text(j, i, f"{val:+.2f}", ha="center", va="center",
                fontsize=10.5, color=color, fontweight="bold")

ax.set_title("(a) 6 자산군 상관계수 행렬\n(가상 historic 추정)", fontsize=12, pad=10)
ax.grid(False)
cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.04)
cbar.set_label("상관계수 ρ", fontsize=10)

# (b) 같은 자산쌍의 분산투자 효과
ax = axes[1]
sigma = 0.18  # 두 자산 동일 σ
rhos = np.linspace(-0.5, 1.0, 100)
# 50/50 포트폴리오 분산: 0.25σ²(1+ρ) + 0.25σ²(1+ρ) = 0.5σ²(1+ρ)
# 잠깐, σ_p² = 0.5²σ² + 0.5²σ² + 2·0.25·ρ·σ² = 0.25σ²(2 + 2ρ) = 0.5σ²(1+ρ)
# σ_p = σ * sqrt((1+ρ)/2)
sd_p = sigma * np.sqrt((1 + rhos) / 2)
sd_indiv = sigma  # 단일 자산 σ

ax.plot(rhos, sd_p * 100, color="#1f6feb", linewidth=2.6,
        label="50/50 포트폴리오 σ_p")
ax.axhline(sd_indiv * 100, color="#888", linestyle="--", linewidth=1.4,
           label=f"단일 자산 σ = {sd_indiv*100:.0f}%")

# 핵심 포인트 마커
for rho_mark, label in [(-0.3, "ρ=-0.3"), (0.0, "ρ=0"), (0.5, "ρ=0.5"), (1.0, "ρ=1")]:
    sd = sigma * np.sqrt((1 + rho_mark) / 2) * 100
    ax.scatter([rho_mark], [sd], s=80, color="#1c1917", zorder=5)
    ax.annotate(f"{label}\n→ σ_p = {sd:.1f}%",
                xy=(rho_mark, sd), xytext=(rho_mark + 0.05, sd + 0.6),
                fontsize=9.5, fontweight="bold")

ax.set_xlabel("두 자산 상관계수 ρ", fontsize=12)
ax.set_ylabel("50/50 포트폴리오 σ_p (%)", fontsize=12)
ax.set_title("(b) ρ가 작을수록 분산투자 효과 큼\n(두 자산 동일 σ=18% 가정)",
             fontsize=12, pad=10)
ax.legend(loc="upper left", fontsize=10.5)
ax.set_xlim(-0.55, 1.05)
ax.set_ylim(0, 22)

# 메시지
ax.text(0.55, 4,
        "ρ=1 (완전 동조): σ_p = σ → 분산 효과 0\n"
        "ρ=0 (무상관): σ_p = σ/√2 ≈ 71%σ\n"
        "ρ<0 (역상관): σ_p < σ/√2 (큰 효과)",
        fontsize=10, color="#1c1917",
        bbox=dict(facecolor="white", edgecolor="#888", boxstyle="round,pad=0.5"))

fig.suptitle("자산 간 상관계수와 분산투자 효과 — 낮은 상관일수록 σ_p 작아짐",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch01_correlation_heatmap")
