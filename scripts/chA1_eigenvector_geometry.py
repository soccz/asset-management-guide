"""A1단원 Figure: 고유벡터 기하학.

행렬 M이 일반 벡터들과 고유벡터들을 어떻게 변환하는지 비교.
- 일반 벡터 (점선): 방향이 변한다
- 고유벡터 (굵은 선): 방향 유지, 길이만 λ배
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

# 실대칭 행렬 M (양정부호)
M = np.array([[2.0, 1.0],
              [1.0, 3.0]])
eigvals, eigvecs = np.linalg.eigh(M)  # 실대칭이므로 정확
print("eigvals:", eigvals)
print("eigvecs:\n", eigvecs)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

# ── 좌측: 일반 벡터의 변환 (방향 바뀜) ─────────────────────
ax = axes[0]
angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
for theta in angles:
    v = np.array([np.cos(theta), np.sin(theta)]) * 1.5
    Mv = M @ v
    # 원본 벡터 (옅게)
    ax.arrow(0, 0, v[0], v[1], head_width=0.10, head_length=0.13,
             fc="#999", ec="#999", alpha=0.55, linewidth=1.0,
             length_includes_head=True)
    # 변환된 벡터 (진하게, 점선)
    ax.arrow(0, 0, Mv[0], Mv[1], head_width=0.13, head_length=0.16,
             fc="#1f6feb", ec="#1f6feb", alpha=0.8, linewidth=1.2,
             length_includes_head=True, linestyle="--")

ax.set_xlim(-7, 7); ax.set_ylim(-7, 7)
ax.set_aspect("equal")
ax.axhline(0, color="k", linewidth=0.5)
ax.axvline(0, color="k", linewidth=0.5)
ax.set_title("일반 벡터: M에 의해 방향이 바뀐다\n"
             "(회색 = 원본, 파랑 점선 = M·v)", fontsize=11)
ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")

# ── 우측: 고유벡터 (방향 유지) ─────────────────────────────
ax = axes[1]
colors = ["#d62728", "#2ca02c"]
for k in range(2):
    v = eigvecs[:, k] * 1.5
    Mv = M @ v
    ax.arrow(0, 0, v[0], v[1], head_width=0.10, head_length=0.13,
             fc=colors[k], ec=colors[k], alpha=0.6, linewidth=1.6,
             length_includes_head=True,
             label=f"고유벡터 $x_{k+1}$ (λ={eigvals[k]:.2f})")
    ax.arrow(0, 0, Mv[0], Mv[1], head_width=0.13, head_length=0.16,
             fc=colors[k], ec=colors[k], alpha=1.0, linewidth=2.4,
             length_includes_head=True)

# 비교용 일반 벡터 한두 개도 그려넣기
for theta in [np.pi / 6, 2 * np.pi / 3]:
    v = np.array([np.cos(theta), np.sin(theta)]) * 1.5
    Mv = M @ v
    ax.arrow(0, 0, v[0], v[1], head_width=0.08, head_length=0.10,
             fc="#bbb", ec="#bbb", alpha=0.5, linewidth=0.8,
             length_includes_head=True)
    ax.arrow(0, 0, Mv[0], Mv[1], head_width=0.10, head_length=0.13,
             fc="#888", ec="#888", alpha=0.6, linewidth=1.0,
             length_includes_head=True, linestyle=":")

ax.set_xlim(-7, 7); ax.set_ylim(-7, 7)
ax.set_aspect("equal")
ax.axhline(0, color="k", linewidth=0.5)
ax.axvline(0, color="k", linewidth=0.5)
ax.set_title("고유벡터: 방향은 유지, 크기만 λ배\n"
             "(연한 색 = 원본, 진한 색 = M·v)", fontsize=11)
ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
ax.legend(loc="lower right", fontsize=9)

fig.suptitle("고유벡터의 기하학 — 행렬 M = [[2, 1], [1, 3]]",
             fontsize=13, y=1.02)
plt.tight_layout()
save(fig, "chA1_eigenvector_geometry")
