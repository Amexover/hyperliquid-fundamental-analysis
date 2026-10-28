"""Shared chart styling, matching the Aave research project's rounded theme."""
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/hyperliquid-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path as DrawPath

BACKGROUND = "#000000"
TEXT = "#f2f5f7"
MUTED = "#b4bdc7"
GRID = "#303740"
BORDER = "#414952"
BLUE = "#7894ff"
MINT = "#86e0b0"
AMBER = "#e6bf7a"


def research_chart(title, subtitle, *, left=0.12):
    """Create a consistent title, plot and source-note hierarchy."""
    plt.rcParams.update({
        "font.family": "DejaVu Sans Mono",
        "font.size": 10,
        "axes.axisbelow": True,
        "axes.labelcolor": "#c4c9d0",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": TEXT,
        "axes.prop_cycle": plt.cycler(color=[BLUE, MINT, AMBER]),
    })
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    fig.set_facecolor(BACKGROUND)
    fig.add_artist(Rectangle(
        (0.015, 0.02), 0.97, 0.96, transform=fig.transFigure,
        facecolor=BACKGROUND, edgecolor=BORDER, linewidth=0.8, zorder=-10,
    ))
    ax.set_facecolor("none")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, pad=7)
    ax.grid(axis="y", color=GRID, linewidth=0.7)
    fig.text(0.045, 0.94, title, fontsize=15, weight="bold", va="top")
    fig.text(0.045, 0.89, subtitle, fontsize=9, color=MUTED, va="top")
    fig.subplots_adjust(left=left, right=0.93, top=0.79, bottom=0.23)
    return fig, ax


def rounded_bars(fig, ax):
    """Round in display coordinates so short bars retain their true values."""
    fig.canvas.draw()
    inverse = ax.transData.inverted()
    origin = inverse.transform((0, 0))
    radius = inverse.transform((4, 4)) - origin
    for bar in list(ax.patches):
        if not isinstance(bar, Rectangle):
            continue
        x, y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        if w <= 0 or h <= 0:
            continue
        rx, ry = min(abs(radius[0]), w / 2), min(abs(radius[1]), h / 2)
        vertices = [
            (x + rx, y), (x + w - rx, y), (x + w, y), (x + w, y + ry),
            (x + w, y + h - ry), (x + w, y + h), (x + w - rx, y + h),
            (x + rx, y + h), (x, y + h), (x, y + h - ry),
            (x, y + ry), (x, y), (x + rx, y), (x + rx, y),
        ]
        codes = [
            DrawPath.MOVETO, DrawPath.LINETO, DrawPath.CURVE3, DrawPath.CURVE3,
            DrawPath.LINETO, DrawPath.CURVE3, DrawPath.CURVE3,
            DrawPath.LINETO, DrawPath.CURVE3, DrawPath.CURVE3,
            DrawPath.LINETO, DrawPath.CURVE3, DrawPath.CURVE3, DrawPath.CLOSEPOLY,
        ]
        ax.add_patch(PathPatch(
            DrawPath(vertices, codes), facecolor=bar.get_facecolor(),
            edgecolor="none", zorder=bar.get_zorder(), antialiased=True,
        ))
        bar.remove()


def save_chart(fig, ax, path, source, note):
    fig.text(0.045, 0.085, source, fontsize=7.5, color=MUTED, va="bottom")
    fig.text(0.045, 0.052, note, fontsize=7.5, color=MUTED, va="bottom")
    for line in ax.lines:
        line.set_solid_capstyle("round")
        line.set_solid_joinstyle("round")
        line.set_antialiased(True)
    rounded_bars(fig, ax)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, facecolor=BACKGROUND)
    plt.close(fig)
