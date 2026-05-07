"""공통 setup — 한국어 폰트 + matplotlib 기본 설정.

모든 차트 스크립트는 가장 먼저 `from _setup import *`를 호출한다.
"""

import matplotlib
matplotlib.use("Agg")  # GUI 없이 PNG로만 저장
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# macOS 한국어 폰트 우선순위
_KO_CANDIDATES = [
    "Apple SD Gothic Neo",
    "AppleGothic",
    "Nanum Gothic",
    "NanumGothic",
    "Malgun Gothic",
]
_avail = {f.name for f in fm.fontManager.ttflist}
for _name in _KO_CANDIDATES:
    if _name in _avail:
        plt.rcParams["font.family"] = _name
        break

plt.rcParams["axes.unicode_minus"] = False  # 한글 폰트의 음수 부호 깨짐 방지
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.25
plt.rcParams["grid.linewidth"] = 0.5
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

import numpy as np

FIG_DIR = "/Users/hong/main/자산운용/figures"


def save(fig, name: str, dpi: int = 150) -> str:
    """fig를 figures/{name}.png로 저장."""
    path = f"{FIG_DIR}/{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"saved → {path}")
    return path


__all__ = ["plt", "fm", "np", "save", "FIG_DIR"]
