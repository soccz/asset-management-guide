"""B1단원 보강: Conditional Autoencoder 신경망 구조 도식.

Gu, Kelly & Xiu 2021 — 자산 특성 z를 비선형으로 변환해 잠재 팩터 노출 β를 추정.
좌측: 특성 인코더 (z → β), 우측: 수익률 인코더 (R → f),
   합쳐서 R̂ = β'·f 예측.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

# 큰 제목
ax.text(7, 8.5, "Conditional Autoencoder (Gu·Kelly·Xiu 2021)",
        ha="center", fontsize=14.5, fontweight="bold", color="#1c1917")
ax.text(7, 8.05, "자산 특성 z → 비선형 신경망 → 잠재 팩터 노출 β",
        ha="center", fontsize=10.5, color="#666", style="italic")

# 좌측 인코더 (Beta network) ──────────────
ax.text(2.5, 7.4, "특성 인코더 (β network)",
        ha="center", fontsize=12, fontweight="bold", color="#1f6feb")

# 입력 특성
def draw_layer(x, y, n, label, color, w=0.5, h=0.42, gap=0.55):
    """세로 노드 n개"""
    total_h = (n - 1) * gap
    y_start = y - total_h / 2
    nodes = []
    for i in range(n):
        ny = y_start + i * gap
        rect = Rectangle((x - w/2, ny - h/2), w, h,
                          facecolor=color, edgecolor="#1c1917", linewidth=0.8)
        ax.add_patch(rect)
        nodes.append((x, ny))
    ax.text(x, y - total_h / 2 - 0.6, label, ha="center", fontsize=9.5,
            color=color, fontweight="bold")
    return nodes

# β network: 5 (특성) → 3 (hidden) → 2 (β)
in_nodes = draw_layer(0.8, 5.5, 5, "z (특성)\nB/M, mom, ...", "#dbeafe")
h1_nodes = draw_layer(2.5, 5.5, 4, "ReLU\nhidden", "#93c5fd")
beta_nodes = draw_layer(4.2, 5.5, 2, "β (잠재 노출)", "#1f6feb")

# 화살표 (전체 연결)
for n1 in in_nodes:
    for n2 in h1_nodes:
        ax.add_patch(FancyArrowPatch(n1, n2, arrowstyle="-",
                                      color="#bfdbfe", linewidth=0.4))
for n1 in h1_nodes:
    for n2 in beta_nodes:
        ax.add_patch(FancyArrowPatch(n1, n2, arrowstyle="-",
                                      color="#bfdbfe", linewidth=0.4))

# 우측 인코더 (Factor network) ──────────────
ax.text(11.5, 7.4, "수익률 인코더 (factor network)",
        ha="center", fontsize=12, fontweight="bold", color="#d62728")

# Factor network: N (자산수익률) → 4 hidden → K (factors)
in_R_nodes = draw_layer(13.2, 5.5, 6, "R (수익률)\nN×1", "#fee2e2")
h2_nodes = draw_layer(11.5, 5.5, 4, "ReLU\nhidden", "#fca5a5")
f_nodes = draw_layer(9.8, 5.5, 2, "f (잠재 팩터)", "#d62728")

for n1 in in_R_nodes:
    for n2 in h2_nodes:
        ax.add_patch(FancyArrowPatch(n1, n2, arrowstyle="-",
                                      color="#fecaca", linewidth=0.4))
for n1 in h2_nodes:
    for n2 in f_nodes:
        ax.add_patch(FancyArrowPatch(n1, n2, arrowstyle="-",
                                      color="#fecaca", linewidth=0.4))

# 가운데 결합 — R̂ = β'·f
combine_box = FancyBboxPatch((5.7, 4.7), 2.6, 1.6,
                              boxstyle="round,pad=0.1",
                              facecolor="#fef3c7", edgecolor="#d97706",
                              linewidth=2)
ax.add_patch(combine_box)
ax.text(7, 5.8, r"$\hat{R} = \beta^T \cdot f$",
        ha="center", fontsize=15, fontweight="bold", color="#92400e")
ax.text(7, 5.2, "예측 수익률\n(β와 f의 내적)",
        ha="center", fontsize=9.5, color="#92400e")

# β와 f를 결합 박스로 화살표
for n in beta_nodes:
    ax.add_patch(FancyArrowPatch(n, (5.7, 5.5),
                                  arrowstyle="->", color="#1f6feb",
                                  linewidth=1.4, mutation_scale=12))
for n in f_nodes:
    ax.add_patch(FancyArrowPatch(n, (8.3, 5.5),
                                  arrowstyle="->", color="#d62728",
                                  linewidth=1.4, mutation_scale=12))

# 학습 — Loss
loss_box = FancyBboxPatch((5.0, 2.5), 4.0, 1.2,
                          boxstyle="round,pad=0.1",
                          facecolor="white", edgecolor="#1c1917", linewidth=1.5)
ax.add_patch(loss_box)
ax.text(7, 3.3, "학습 손실 (Loss)",
        ha="center", fontsize=11, fontweight="bold")
ax.text(7, 2.9, r"$\min \sum_t \| R_t - \hat{R}_t \|^2$",
        ha="center", fontsize=12, color="#1c1917")

# 결합 → 손실 화살표
ax.add_patch(FancyArrowPatch((7, 4.7), (7, 3.7),
                              arrowstyle="->", color="#1c1917",
                              linewidth=1.6, mutation_scale=14))

# 핵심 메시지 박스
msg_box = FancyBboxPatch((1.0, 0.3), 12.0, 1.6,
                          boxstyle="round,pad=0.1",
                          facecolor="#f3e8ff", edgecolor="#7c3aed",
                          linewidth=1.5)
ax.add_patch(msg_box)
ax.text(7, 1.4,
        "★ 핵심: 전통 IPCA(B1 §6)는 β = z'·Γ로 선형 매핑.\n"
        "Conditional Autoencoder는 β = NN(z)로 비선형 매핑 → 더 풍성한 노출 표현.\n"
        "두 인코더(특성↔수익률)를 같은 손실로 동시 학습 → 양변이 자연스러운 잠재 팩터.",
        ha="center", fontsize=10.5, color="#1c1917")

save(fig, "chB1_autoencoder")
