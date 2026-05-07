"""A1단원 Figure: 이차형식 3가지 곡면.

f(x) = (1/2) x^T A x 형태에서 A의 성질에 따라 곡면이 달라진다.
- (a) PD: 컵 모양 (모든 고유값 양수) → 최솟값 유일
- (b) ND: 산 모양 (모든 고유값 음수) → 최댓값 유일
- (c) Indefinite: 안장점 (양·음 혼합) → 안정한 극값 없음
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

x = np.linspace(-2, 2, 60)
y = np.linspace(-2, 2, 60)
X, Y = np.meshgrid(x, y)

A_pd  = np.array([[2.0, 0.5], [0.5, 1.5]])
A_nd  = -A_pd
A_ind = np.array([[1.5, 0.0], [0.0, -1.5]])

def quad(A, X, Y):
    return 0.5 * (A[0, 0] * X**2 + 2 * A[0, 1] * X * Y + A[1, 1] * Y**2)

fig = plt.figure(figsize=(16, 6.5))
titles = [
    "(a) 양정부호 (PD)\n모든 고유값 > 0\n→ 컵 모양, 최솟값 유일",
    "(b) 음정부호 (ND)\n모든 고유값 < 0\n→ 산 모양, 최댓값 유일",
    "(c) 부정부호 (Indefinite)\n양·음 고유값 혼합\n→ 안장점, 극값 없음",
]
mats = [A_pd, A_nd, A_ind]
cmaps = ["viridis", "plasma", "coolwarm"]

for i, (A, title, cmap) in enumerate(zip(mats, titles, cmaps)):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d")
    Z = quad(A, X, Y)
    ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.88,
                    rstride=2, cstride=2, edgecolor="none")
    ax.contour(X, Y, Z, zdir="z",
               offset=Z.min() - 0.3,
               levels=10, cmap=cmap, alpha=0.6, linewidths=0.7)
    ax.set_xlabel("$x_1$", labelpad=2)
    ax.set_ylabel("$x_2$", labelpad=2)
    ax.set_zlabel("$f(x)$", labelpad=2)
    ax.set_title(title, fontsize=11, pad=10)
    eigvals = np.linalg.eigvalsh(A)
    ax.text2D(0.5, -0.05, f"λ₁ = {eigvals[0]:.2f},   λ₂ = {eigvals[1]:.2f}",
              transform=ax.transAxes, ha="center", fontsize=10, color="#333")
    ax.view_init(elev=22, azim=-55)
    ax.tick_params(labelsize=8)

fig.suptitle(r"이차형식 $f(x) = \frac{1}{2}\, x^T A x$ — A의 부호성에 따른 곡면",
             fontsize=14, y=0.99)
fig.subplots_adjust(left=0.02, right=0.98, top=0.85, bottom=0.06,
                    wspace=0.12)
save(fig, "chA1_quadratic_surfaces")
