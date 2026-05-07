"""11단원 보강: 16편 논문의 분야별 분포 + 단원 매핑.

좌: 분야별 도넛 (모멘텀 6 / BAB 3 / ML 3 / 가치 2 / 리스크패리티 1 / 효율시장 1)
우: 분야 → 단원 매핑 테이블 (시각적 박스)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 카테고리별 논문 수 + 색
categories = [
    ("모멘텀 (TS·XS·크래시)", 6, "#1f6feb"),
    ("BAB / 저베타",           3, "#d62728"),
    ("ML 자산가격결정",        3, "#9467bd"),
    ("가치·사이즈 (FF3)",      2, "#2ca02c"),
    ("리스크패리티",           1, "#ff9900"),
    ("효율적 시장 비판",        1, "#8c564b"),
]

# 분야 → 단원 매핑
mapping = [
    ("모멘텀",         "9, 10, 13",   "Lewellen, Barroso, Daniel,\nMoskowitz, Blitz, Beckmeyer"),
    ("BAB / 저베타",   "14",           "Frazzini, Novy-Marx, Xu"),
    ("ML",             "B1, 11",       "Kelly, Beckmeyer, Xu"),
    ("가치·사이즈",    "8",             "Fama-French, Novy-Marx"),
    ("리스크패리티",    "5",             "Qian"),
    ("효율적 시장 비판","6, 11",         "Blitz"),
]

fig, axes = plt.subplots(1, 2, figsize=(15, 7),
                         gridspec_kw={"width_ratios": [1, 1.3], "wspace": 0.05})

# (a) 도넛
ax = axes[0]
labels = [c[0] for c in categories]
sizes = [c[1] for c in categories]
colors = [c[2] for c in categories]
total = sum(sizes)

wedges, texts = ax.pie(sizes, labels=None, colors=colors,
                        startangle=90, counterclock=False,
                        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2.5))

# 가운데 텍스트
ax.text(0, 0.08, f"{total}", ha="center", va="center",
        fontsize=42, fontweight="bold", color="#1c1917",
        fontfamily="serif")
ax.text(0, -0.16, "P A P E R S", ha="center", va="center",
        fontsize=10, color="#666")

# 외곽 라벨 (도넛 안 침범 방지 — radius 1.45)
for i, (label, size, color) in enumerate(categories):
    ang = (sum(sizes[:i]) + size / 2) / total * 360
    rad = np.radians(90 - ang)
    x, y = 1.45 * np.cos(rad), 1.45 * np.sin(rad)
    ha = "left" if x > 0.05 else ("right" if x < -0.05 else "center")
    ax.text(x, y,
            f"{label}\n{size}편",
            ha=ha, va="center", fontsize=10,
            color=color, fontweight="bold")

ax.set_title("(a) 16편 논문의 분야별 분포",
             fontsize=12.5, pad=18)
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.7, 1.7)
ax.axis("off")

# (b) 분야 → 단원 매핑 테이블
ax = axes[1]
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, len(mapping) + 1)

# 헤더
ax.text(0.3, len(mapping) + 0.5, "분야",
        fontsize=11, fontweight="bold", color="#1c1917")
ax.text(3.2, len(mapping) + 0.5, "관련 단원",
        fontsize=11, fontweight="bold", color="#1c1917")
ax.text(5.0, len(mapping) + 0.5, "주요 저자",
        fontsize=11, fontweight="bold", color="#1c1917")

ax.plot([0, 10], [len(mapping) + 0.3, len(mapping) + 0.3],
        color="#888", linewidth=1)

for i, (cat, ch, authors) in enumerate(mapping):
    y = len(mapping) - i - 0.4
    color = categories[i][2]
    # 컬러 박스
    ax.add_patch(plt.Rectangle((0.05, y - 0.15), 0.18, 0.5,
                                facecolor=color, edgecolor="none"))
    ax.text(0.4, y + 0.1, cat, fontsize=10.5, color="#1c1917", fontweight="500")
    ax.text(3.2, y + 0.1, ch, fontsize=10.5, color="#1f6feb",
            fontfamily="monospace", fontweight="bold")
    ax.text(5.0, y + 0.1, authors, fontsize=9.5, color="#444",
            fontstyle="italic")
    if i < len(mapping) - 1:
        ax.plot([0, 10], [y - 0.3, y - 0.3], color="#e7e5e4", linewidth=0.5)

ax.set_title("(b) 분야 → 단원 → 저자 매핑",
             fontsize=12.5, pad=18, loc="left")

fig.suptitle("16편 논문 풍경 — 분야 분포와 단원 연결",
             fontsize=14, y=1.0, fontweight="bold")

save(fig, "ch11_paper_landscape")
