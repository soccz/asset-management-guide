"""11단원 보강: 16편 논문 timeline (1981~2025).

x: 발표 연도, y: 분야 카테고리, 점 크기 = 본 학습서 기여도(주관 등급).
시간을 따라 자산운용 학문이 어떻게 발전했는지 한눈에 보임.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# (year, author, title_short, category, weight, single_chapter)
papers = [
    (1981, "Banz",                  "Size effect (사이즈 효과)",            "value-size",    3, "8 (참조)"),
    (1992, "Fama-French",            "FF3 모형",                              "value-size",    4, "8 (참조)"),
    (2002, "Lewellen",               "모멘텀 메커니즘",                       "momentum",      4, "9"),
    (2011, "Blitz·Van Vliet",        "잔차 모멘텀·변동성 효과",                "momentum",      3, "9"),
    (2011, "Qian",                   "Risk Parity",                          "risk-parity",   3, "5"),
    (2012, "Moskowitz·Ooi·Pedersen", "TSMOM",                                "momentum",      5, "13"),
    (2014, "Frazzini·Pedersen",      "BAB / 워렌버핏",                        "BAB",           5, "14"),
    (2015, "Barroso·Santa-Clara",    "모멘텀 크래시 + Vol scaling",            "momentum",      5, "10"),
    (2019, "Kelly·Pruitt·Su",        "IPCA",                                  "ML",            5, "B1"),
    (2020, "Kozak·Nagel·Santosh",    "KNS — 특성 SDF",                        "ML",            5, "B1"),
    (2021, "Kelly·Pruitt·Su",        "Conditional FE",                        "momentum",      4, "9"),
    (2021, "Gu·Kelly·Xiu",           "Conditional Autoencoder",                "ML",            5, "B1"),
    (2021, "Saejoon Kim",            "한국 주식 모멘텀",                       "korea",         3, "9 (참조)"),
    (2022, "Novy-Marx·Velikov",      "팩터 transaction costs",                 "BAB",           4, "14"),
    (2023, "Saejoon Kim",            "한국 BAB / Smart beta",                  "korea",         3, "14 (참조)"),
    (2024, "Deng et al.",            "Deep Portfolio (대규모 MV)",              "ML",            4, "B1"),
    (2025, "Beckmeyer·Moerke",       "CMM (Characteristic-Managed Mom)",       "momentum",      4, "9"),
    (2025, "Xu",                     "한국 BAB",                                "BAB",           3, "14"),
]

cat_y = {
    "momentum":   3,
    "ML":         4,
    "BAB":        2,
    "value-size": 5,
    "risk-parity":1,
    "korea":      0,
}
cat_color = {
    "momentum":   "#1f6feb",
    "ML":         "#9467bd",
    "BAB":        "#d62728",
    "value-size": "#2ca02c",
    "risk-parity":"#ff9900",
    "korea":      "#8c564b",
}
cat_label = {
    "momentum":   "모멘텀 (TS·XS·잔차·CMM)",
    "ML":         "ML 자산가격결정",
    "BAB":        "BAB / 저베타",
    "value-size": "가치·사이즈 (참조)",
    "risk-parity":"리스크패리티",
    "korea":      "한국 시장",
}

fig, ax = plt.subplots(figsize=(15, 7.5))

# 가로축: 연도
year_min, year_max = 1980, 2027

# 각 카테고리 가로 라인
for cat, y in cat_y.items():
    ax.plot([year_min, year_max], [y, y], color=cat_color[cat],
            linewidth=0.8, alpha=0.25, zorder=1)
    ax.text(year_min - 0.5, y, cat_label[cat], ha="right", va="center",
            fontsize=10.5, color=cat_color[cat], fontweight="bold")

# 학습서 본문 단원 16편(참조 제외) — sizes
# weight 클수록 큰 점
for (year, author, title, cat, w, ch) in papers:
    y = cat_y[cat]
    color = cat_color[cat]
    s = 80 + w * 80
    ax.scatter([year], [y], s=s, color=color, alpha=0.85,
               edgecolor="white", linewidth=1.5, zorder=5)

# 핵심 논문 라벨 (수동 위치 — 겹침 방지)
labels_manual = [
    (1981, 5,  +0.4, "Banz '81\nSize"),
    (1992, 5,  -0.55, "Fama-French '92\nFF3"),
    (2002, 3,  +0.4, "Lewellen '02"),
    (2011, 1,  -0.5, "Qian '11\nRP"),
    (2012, 3,  +0.4, "Moskowitz '12\nTSMOM"),
    (2014, 2,  +0.4, "Frazzini-Pedersen '14\nBAB"),
    (2015, 3,  -0.55, "Barroso '15\n모멘텀 크래시"),
    (2019, 4,  +0.45, "Kelly '19  IPCA"),
    (2020, 4,  -0.55, "Kozak '20  KNS"),
    (2021, 4,  +1.05, "Gu-Kelly-Xiu '21\nAutoencoder"),
    (2024, 4,  -0.55, "Deng '24"),
    (2022, 2,  -0.55, "Novy-Marx '22"),
    (2025, 3,  +0.4, "Beckmeyer '25\nCMM"),
]
for year, y, dy, label in labels_manual:
    cat_for_color = next((c for c, yval in cat_y.items() if yval == y), "momentum")
    ax.annotate(label,
                xy=(year, y), xytext=(year, y + dy),
                fontsize=8.5, color=cat_color[cat_for_color],
                fontweight="bold", ha="center")

# x축
ax.set_xlim(year_min - 6, year_max + 1)
ax.set_ylim(-0.7, 6)
ax.set_xticks([1981, 1992, 2002, 2011, 2014, 2019, 2021, 2024, 2025])
ax.set_xticklabels(["1981", "1992", "2002", "2011", "2014", "2019", "2021", "2024", "2025"],
                   fontsize=10)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("발표 연도", fontsize=12)

# Phase 배경 (선택적)
phases = [
    (1980, 2000, "고전 팩터 시대",    "#fef3c7"),
    (2000, 2015, "행동·모멘텀 시대",  "#dbeafe"),
    (2015, 2027, "ML 시대",            "#f3e8ff"),
]
for s, e, name, c in phases:
    ax.axvspan(s, e, alpha=0.20, color=c, zorder=0)
    ax.text((s + e) / 2, 5.5, name, ha="center", fontsize=10.5,
            color="#666", fontweight="bold")

# legend
from matplotlib.lines import Line2D
legend_items = [Line2D([0], [0], marker='o', color='w',
                       markerfacecolor=c, markersize=10, label=cat_label[cat])
                for cat, c in cat_color.items()]
ax.legend(handles=legend_items, loc="lower right", ncol=3,
          fontsize=9.5, framealpha=0.95)

ax.set_title("16편 논문의 시간순 풍경 (1981~2025) — 자산운용 학문의 진화",
             fontsize=14, pad=15, fontweight="bold")

# 메시지 박스
ax.text(1981, -0.4,
        "★ 점 크기 = 본 학습서 기여도",
        fontsize=9, color="#666", style="italic")

save(fig, "ch11_paper_timeline")
