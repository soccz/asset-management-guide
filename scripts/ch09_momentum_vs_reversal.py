"""9단원 보강: 모멘텀과 반전의 시간 구조 (정성적 패턴).

같은 자산 가격에서 lookback 기간에 따라 정반대 시그널이 나온다:
- 1개월 (단기): 반전 — 안정적 작은 alpha
- 12개월 (중기): 모멘텀 — 강한 alpha + 가끔 크래시
- 60개월 (장기): 반전 — 약한 alpha + 변동 큼

[Lewellen 2002 RFS, Daniel & Moskowitz 2016 JFE 패턴 정성적 재현 — 시뮬레이션]
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _setup import plt, np, save

rng = np.random.default_rng(2026)
T = 600  # 50년 월별
months = np.arange(T)
years = months / 12

# 단기반전 — 안정적 작은 alpha
reversal_short = rng.normal(0.0045, 0.022, T)
# 중기모멘텀 — 강한 alpha + 두 번 크래시 (1932/2009 정성적 재현)
momentum_mid = rng.normal(0.010, 0.040, T)
crash_1 = slice(195, 200)  # 약 16년차
crash_2 = slice(485, 490)  # 약 40년차
momentum_mid[crash_1] = [-0.08, -0.18, -0.10, -0.04, -0.02]
momentum_mid[crash_2] = [-0.10, -0.20, -0.08, -0.03, -0.01]
# 장기반전 — 약한 alpha + 변동 큼
reversal_long = rng.normal(0.005, 0.034, T)

cum_rev_s = np.cumprod(1 + reversal_short)
cum_mom_m = np.cumprod(1 + momentum_mid)
cum_rev_l = np.cumprod(1 + reversal_long)

fig, ax = plt.subplots(figsize=(13, 6.8))

ax.plot(years, cum_rev_s, color="#d62728", linewidth=2.0,
        label="단기 반전 (1개월 lookback) — 지난달 패자 매수 [안정적]")
ax.plot(years, cum_mom_m, color="#1f6feb", linewidth=2.6,
        label="중기 모멘텀 (12개월 lookback) — 지난해 승자 매수 [강하나 크래시]")
ax.plot(years, cum_rev_l, color="#2ca02c", linewidth=2.0, linestyle="--",
        label="장기 반전 (60개월 lookback) — 5년 패자 매수 [변동 큼]")

ax.set_yscale("log")
ax.axhline(1.0, color="#bbb", linestyle=":", linewidth=1)

# 크래시 강조
ax.fill_between(years[crash_1], 0.1, 1000, alpha=0.18, color="#a31515")
ax.fill_between(years[crash_2], 0.1, 1000, alpha=0.18, color="#a31515")
ax.text(years[crash_1][2], cum_mom_m[crash_1][2] * 0.5, "크래시\n(1932 패턴)",
        ha="center", fontsize=10, color="#a31515", fontweight="bold")
ax.text(years[crash_2][2], cum_mom_m[crash_2][2] * 0.5, "크래시\n(2009 패턴)",
        ha="center", fontsize=10, color="#a31515", fontweight="bold")

# 최종값
for series, color, name in [(cum_rev_s, "#d62728", "단기반전"),
                             (cum_mom_m, "#1f6feb", "중기모멘텀"),
                             (cum_rev_l, "#2ca02c", "장기반전")]:
    final = series[-1]
    ax.text(years[-1] + 0.5, final, f" ${final:.1f}",
            color=color, fontsize=11, va="center", fontweight="bold")

ax.set_title("같은 자산, 다른 lookback — 모멘텀과 반전의 시간 구조\n"
             "1개월: 반전(안정) / 12개월: 모멘텀(강+크래시) / 60개월: 반전(변동)",
             fontsize=13, pad=14)
ax.set_xlabel("연도", fontsize=12)
ax.set_ylabel("누적수익 ($1 시작, 로그 스케일)", fontsize=12)
ax.legend(loc="upper left", fontsize=10.5, framealpha=0.95)
ax.set_xlim(0, T / 12 + 4)
ax.set_ylim(0.3, max(cum_mom_m.max(), cum_rev_l.max(), cum_rev_s.max()) * 2)

# 메시지 박스
ax.text(28, 0.5,
        "핵심: lookback이 자산의 '시간 주기'를 결정한다.\n"
        "모멘텀과 반전은 별개 현상이 아니라\n"
        "같은 가격 시계열의 다른 시간대를 본 결과\n"
        "(Lewellen 2002).",
        fontsize=10.5, color="#1c1917",
        bbox=dict(facecolor="white", edgecolor="#888", boxstyle="round,pad=0.6"))

save(fig, "ch09_momentum_vs_reversal")
