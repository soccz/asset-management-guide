"""12단원 보강: '이 전략이 좋아 보일 때' 사고 체크리스트 인포그래픽.

12단원 본문의 핵심 메시지 — 시각적 결정 트리 형태.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 11)
ax.axis("off")

# 큰 제목
ax.text(7, 10.5, "이 전략이 좋아 보일 때 — 8단계 사고 체크리스트",
        ha="center", fontsize=15, fontweight="bold", color="#1c1917")
ax.text(7, 10.0, "(12단원 사고 프레임워크 — 결정 전 자문해야 할 질문들)",
        ha="center", fontsize=10, color="#666", style="italic")

# 각 박스: (x, y, width, height, num, title, question, color, decision)
items = [
    (1.0, 8.5, 5.5, 1.1, "1", "데이터의 기간",
     "이 결과는 얼마나 긴 기간의 데이터에서 나왔나?\n10년 이하 → 의심", "#1f6feb"),
    (7.5, 8.5, 5.5, 1.1, "2", "시장의 다양성",
     "한 국가만? 글로벌·신흥시장에서도 작동하나?\n단일 시장 → 우연일 수 있음", "#1f6feb"),

    (1.0, 7.0, 5.5, 1.1, "3", "transaction cost",
     "거래비용·세금·임팩트 반영했나?\n이론값-실제값 차이 큼 (Novy-Marx 2022)", "#9467bd"),
    (7.5, 7.0, 5.5, 1.1, "4", "샤프 vs α",
     "FF3/FF6 같은 표준 모형 통제 후에도 α > 0?\n시장·사이즈·가치 노출 차감해야", "#9467bd"),

    (1.0, 5.5, 5.5, 1.1, "5", "크래시 위험",
     "최악의 1개월/1년 손실은? 변동성 평균 뒤에 숨은 꼬리 위험?\n예: 모멘텀 -78%/월", "#d62728"),
    (7.5, 5.5, 5.5, 1.1, "6", "용량 (capacity)",
     "$10M에서 작동 → $10B에서도?\n알파는 거의 항상 자본 규모로 줄어듦", "#d62728"),

    (1.0, 4.0, 5.5, 1.1, "7", "이론적 메커니즘",
     "왜 작동하는가? 위험 보상? 행동편향?\n메커니즘 설명 못하면 우연일 가능성", "#2ca02c"),
    (7.5, 4.0, 5.5, 1.1, "8", "발표 후 효과",
     "논문 발표 후 alpha가 줄었나? (post-publication decay)\n계속 유지된다면 진짜 alpha", "#2ca02c"),
]

for x, y, w, h, num, title, q, color in items:
    # 박스
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.05",
                          facecolor="white", edgecolor=color, linewidth=2)
    ax.add_patch(box)
    # 번호 원
    circle_x = x + 0.4
    circle_y = y + h - 0.3
    ax.add_patch(plt.Circle((circle_x, circle_y), 0.22,
                             facecolor=color, edgecolor="white", linewidth=1.5,
                             zorder=5))
    ax.text(circle_x, circle_y, num, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=6)
    # 제목
    ax.text(x + 0.85, circle_y, title, ha="left", va="center",
            fontsize=11.5, fontweight="bold", color=color)
    # 질문
    ax.text(x + 0.4, y + 0.3, q, ha="left", va="center",
            fontsize=9.5, color="#1c1917")

# 4 그룹 라벨
group_labels = [
    (8.0, "데이터 검증",       "#1f6feb"),
    (7.0 - 0.3, "비용·정확성", "#9467bd"),  # 다시 짚기
]
ax.text(0.4, 8.0, "①②\n데이터·\n시장 검증", ha="center", va="center",
        fontsize=9, fontweight="bold", color="#1f6feb")
ax.text(0.4, 6.5, "③④\n비용·\n모형 통제", ha="center", va="center",
        fontsize=9, fontweight="bold", color="#9467bd")
ax.text(0.4, 5.0, "⑤⑥\n위험·\n용량", ha="center", va="center",
        fontsize=9, fontweight="bold", color="#d62728")
ax.text(0.4, 3.5, "⑦⑧\n이론·\n지속성", ha="center", va="center",
        fontsize=9, fontweight="bold", color="#2ca02c")

# 결론 박스
conclusion = FancyBboxPatch((1.5, 1.5), 11, 1.7,
                             boxstyle="round,pad=0.1",
                             facecolor="#fef3c7", edgecolor="#d97706",
                             linewidth=2)
ax.add_patch(conclusion)
ax.text(7, 2.7, "8개 질문 모두 통과 → 진지하게 검토할 가치",
        ha="center", fontsize=12.5, fontweight="bold", color="#92400e")
ax.text(7, 2.1, "하나라도 막히면 → 더 검증할 것이 있다는 신호.\n"
        "유망한 전략은 흔하지만 위 8개를 모두 통과하는 건 드물다.",
        ha="center", fontsize=10.5, color="#1c1917")

# 출처
ax.text(7, 0.6,
        "12단원: 사고 프레임워크 — 5층 '왜?' 다음에 오는 실전 의사결정 도구",
        ha="center", fontsize=10, color="#666", style="italic")

save(fig, "ch12_thinking_checklist")
