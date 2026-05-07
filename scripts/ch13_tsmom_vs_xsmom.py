"""13단원 보강: TSMOM vs XSMOM 누적수익 비교.

TSMOM (시계열): 같은 자산의 과거 12개월 부호로 long/short
XSMOM (횡단면): 자산들 중 상위 매수 + 하위 매도

둘 다 양 alpha지만 메커니즘 다름.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(13)
T = 600
months = np.arange(T)
years = months / 12

# TSMOM: 안정적이며 시장 전체 추세 따라감
# 평균 월 0.85%, 변동성 작음
tsmom = rng.normal(0.0085, 0.030, T)
# 추세 변화 시점 일부 손실
tsmom[200:204] = [-0.04, -0.03, -0.02, -0.02]

# XSMOM: 더 강한 alpha + 더 변동성 (크래시 포함)
xsmom = rng.normal(0.011, 0.040, T)
xsmom[195:200] = [-0.08, -0.18, -0.10, -0.04, -0.02]
xsmom[485:490] = [-0.10, -0.20, -0.08, -0.03, -0.01]

cum_ts = np.cumprod(1 + tsmom)
cum_xs = np.cumprod(1 + xsmom)

fig, axes = plt.subplots(1, 2, figsize=(15, 6),
                         gridspec_kw={"width_ratios": [1.5, 1], "wspace": 0.28})

# (a) 누적수익
ax = axes[0]
ax.plot(years, cum_ts, color="#1f6feb", linewidth=2.4,
        label="TSMOM (시계열) — 자기 시계열 부호 long/short")
ax.plot(years, cum_xs, color="#d62728", linewidth=2.4,
        label="XSMOM (횡단면) — 자산 정렬 winner-loser")
ax.set_yscale("log")
ax.axhline(1.0, color="#bbb", linestyle=":", linewidth=1)

# 크래시 영역
ax.fill_between(years[195:200], 0.1, 1000, alpha=0.18, color="#a31515")
ax.fill_between(years[485:490], 0.1, 1000, alpha=0.18, color="#a31515")

# 최종값
ax.text(years[-1] + 0.5, cum_ts[-1], f" ${cum_ts[-1]:.1f}",
        color="#1f6feb", fontsize=11, va="center", fontweight="bold")
ax.text(years[-1] + 0.5, cum_xs[-1], f" ${cum_xs[-1]:.1f}",
        color="#d62728", fontsize=11, va="center", fontweight="bold")

ax.set_title("(a) TSMOM vs XSMOM 50년 누적수익\nXSMOM 더 높지만 크래시 동반 / TSMOM 안정적",
             fontsize=12, pad=10)
ax.set_xlabel("연도", fontsize=11)
ax.set_ylabel("누적수익 ($1 시작, 로그 스케일)", fontsize=11)
ax.legend(loc="upper left", fontsize=10.5)
ax.set_xlim(0, T/12 + 4)
ax.set_ylim(0.7, max(cum_xs.max(), cum_ts.max()) * 2)

# (b) 핵심 차이 요약 표
ax = axes[1]
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

ax.text(5, 9.5, "TSMOM vs XSMOM 핵심 차이",
        ha="center", fontsize=12.5, fontweight="bold")
ax.plot([0.3, 9.7], [9.0, 9.0], color="#888", linewidth=1)

rows = [
    ("",            "TSMOM",                          "XSMOM"),
    ("신호 단위",   "각 자산별 자기 부호",             "자산 간 상대 순위"),
    ("롱숏",        "Long(+) / Short(-) 직접 결정",   "상위 long + 하위 short"),
    ("적용 자산",   "선물·통화·채권 등 다양",          "주식 위주"),
    ("크래시",      "약함 (자산별 독립)",             "강함 (반등 시 동시)"),
    ("Moskowitz12", "TS 평균 +14%/yr (가상)",         "XS 평균 +12%/yr (가상)"),
]

y_start = 8.0
# 짧은 형태로 정리 (셀 길이 단축)
rows_short = [
    ("",            "TSMOM",                "XSMOM"),
    ("신호 단위",   "자기 시계열 부호",      "자산 간 상대 순위"),
    ("롱숏",        "Long(+) / Short(-)",   "상위 long + 하위 short"),
    ("적용 자산",   "선물·통화·채권 등",    "주식 위주"),
    ("크래시",      "약함 (자산별 독립)",    "강함 (반등 시 동시)"),
    ("Moskowitz12", "TS +14%/yr (가상)",    "XS +12%/yr (가상)"),
]
for i, (col1, col2, col3) in enumerate(rows_short):
    y = y_start - i * 1.1
    weight = "bold" if i == 0 else "normal"
    ax.text(0.3, y, col1, fontsize=10, fontweight="bold", color="#444")
    ax.text(3.4, y, col2, fontsize=9.5, fontweight=weight,
            color="#1f6feb" if i > 0 else "#444")
    ax.text(6.7, y, col3, fontsize=9.5, fontweight=weight,
            color="#d62728" if i > 0 else "#444")
    if i < len(rows_short) - 1:
        ax.plot([0.3, 9.7], [y - 0.55, y - 0.55], color="#e7e5e4", linewidth=0.5)

fig.suptitle("두 가지 모멘텀의 시간 구조 — TSMOM(자기) vs XSMOM(상대)",
             fontsize=13.5, y=1.02, fontweight="bold")

save(fig, "ch13_tsmom_vs_xsmom")
