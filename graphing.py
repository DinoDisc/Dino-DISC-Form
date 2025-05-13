# disc_graphs.py --------------------------------------------------------
"""
Drop‑in replacements for plot_disc_graph_most / least / change that
match the look of the *printed* DISC form:
  • exact 18‑row grid (235 pt tall) with a heavy mid‑line at score 40
  • dotted grey lines every 10 points (10,30,50,70)
  • thin light lines between (every ~4.4 pt) to mimic the paper holes
  • transparent background, no frame spines, no matplotlib tick labels
  • plotted value labels sit just above/below the dot like the form

Call pattern (example):
------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(178/72, 235/72), dpi=72)  # 1 px = 1 pt
plot_disc_graph_most([3,2,10,3], ax)
fig.savefig("/tmp/most.png", bbox_inches="tight", transparent=True)
plt.close(fig)
------------------------------------------------------------------
The PNG will drop perfectly into the 178×235 pt rectangle we reserved
in *playground.py*.
"""

import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    "plot_disc_graph_most",
    "plot_disc_graph_least",
    "plot_disc_graph_change",
]

# ---------------------------------------------------------------------
# shared helpers -------------------------------------------------------
# ---------------------------------------------------------------------
GRID_Y = np.linspace(0, 80, 19)      # 0,4.44,…,80  ==> 18 equal bands

MAJOR_Y = {10, 20, 30, 50, 60, 70}  # dotted grey
MID_Y   = 40                        # heavy solid

TXT_OFFSET_UP   = 1.5
TXT_OFFSET_DOWN = 1.5

COLORS = {
    "most":   "#1C80BC",
    "least":  "#A00100",
    "change": "#278D8D",
}


def _style_ax(ax, invert=False):
    """Apply paper‑like styling to *ax* (assumes y in 0..80)."""

    # frame -----------------------------------------------------------------
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlim(-0.5, 3.5)              # four columns D,I,S,C
    if invert:
        ax.set_ylim(80, 0)              # LEAST graph counts downward
    else:
        ax.set_ylim(0, 80)

    # grid ------------------------------------------------------------------
    for y in GRID_Y:
        if y == MID_Y:                  # heavy centre line
            ax.axhline(y, lw=1.4, color="black", zorder=0)
        elif y in MAJOR_Y:
            ax.axhline(y, lw=0.8, ls=(0, (2, 2)), color="grey", zorder=0)
        else:
            ax.axhline(y, lw=0.35, ls="-", color="lightgrey", zorder=0)

    # ticks/spines ----------------------------------------------------------
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("none")
    ax.figure.set_facecolor("none")

    # top DISC labels -------------------------------------------------------
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(list("DISC"), fontsize=8)
    ax2.tick_params(axis="x", length=0, pad=2)
    ax2.spines["top"].set_visible(False)

# ---------------------------------------------------------------------
# 1. MOST --------------------------------------------------------------
# ---------------------------------------------------------------------

def plot_disc_graph_most(values, ax):
    """Plot GRAPH 1 – MOST (values 0‑24)."""
    labels = "DISC"
    mappings = {
        'D': [9, 14, 20, 28, 32, 35, 39, 43, 45, 50, 55, 57, 59, 64, 66, 73, 75, 76, 76, 76, 76, 77, 78, 79, 80],
        'I': [4, 16, 28, 35, 45, 55, 57, 66, 68, 70, 73, 75, 76, 76, 76, 76, 76, 76, 76, 77, 77, 78, 78, 79, 80],
        'S': [12, 18, 22, 32, 37, 43, 45, 53, 55, 59, 64, 66, 68, 70, 73, 73, 74, 74, 75, 76, 77, 78, 79, 80, 80],
        'C': [9, 16, 22, 32, 43, 50, 55, 66, 68, 70, 71, 73, 74, 75, 75, 76, 76, 77, 77, 78, 78, 79, 79, 80, 80]
    }
    y = [mappings[L][v] for L, v in zip(labels, values)]
    x = np.arange(4)

    _style_ax(ax, invert=False)
    ax.plot(x, y, "o-", color=COLORS["most"], lw=1.2, zorder=1)
    for xx, yy, vv in zip(x, y, values):
        ax.text(xx, yy + TXT_OFFSET_UP, str(vv), ha="center", va="bottom", fontsize=8, color=COLORS["most"])

    return ax

# ---------------------------------------------------------------------
# 2. LEAST -------------------------------------------------------------
# ---------------------------------------------------------------------

def plot_disc_graph_least(values, ax):
    """Plot GRAPH 2 – LEAST (values 0‑24, inverted axis)."""
    labels = "DISC"
    mappings = {
        'D': [3, 7, 18, 27, 33, 37, 42, 46, 47, 53, 55, 58, 62, 66, 68, 71, 73, 74, 75, 76, 77, 78, 79, 79, 80],
        'I': [5, 10, 21, 27, 37, 42, 50, 58, 63, 66, 71, 73, 75, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80, 80, 80],
        'S': [3, 5, 10, 21, 27, 33, 37, 46, 50, 55, 63, 66, 71, 73, 74, 75, 76, 77, 78, 79, 80, 80, 80, 80, 80],
        'C': [3, 5, 13, 21, 27, 33, 37, 42, 46, 53, 57, 66, 68, 71, 73, 75, 76, 77, 78, 79, 79, 80, 80, 80, 80]
    }
    y = [mappings[L][v] for L, v in zip(labels, values)]
    x = np.arange(4)

    _style_ax(ax, invert=True)
    ax.plot(x, y, "o-", color=COLORS["least"], lw=1.2, zorder=1)
    for xx, yy, vv in zip(x, y, values):
        ax.text(xx, yy - TXT_OFFSET_DOWN, str(vv), ha="center", va="top", fontsize=8, color=COLORS["least"])

    return ax

# ---------------------------------------------------------------------
# 3. CHANGE ------------------------------------------------------------
# ---------------------------------------------------------------------

def plot_disc_graph_change(values, ax):
    """Plot GRAPH 3 – CHANGE (values -24…+24)."""
    labels = "DISC"
    values24 = [v + 24 for v in values]   # shift into 0…48 index space
    mappings = {
        'D': [0, 1, 2, 3, 4, 4, 5, 5, 6, 8, 10, 11, 12, 18, 23, 24, 25, 27, 30, 32, 34, 36, 37, 38, 38, 43, 44, 45, 46, 47, 50, 53, 56, 59, 64, 65, 66, 68, 70, 72, 73, 73, 74, 75, 76, 77, 78, 78, 79, 80 ],
        'I': [0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 9, 12, 16, 18, 23, 25, 30, 32, 38, 41, 43, 45, 47, 55, 59, 62, 66, 68, 72, 73, 75, 75, 75, 75, 76, 76, 76, 76, 77, 77, 77, 78, 78, 79, 79, 80],
        'S': [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 5, 6, 7, 8, 9, 16, 18, 23, 25, 30, 32, 34, 36, 38, 45, 48, 50, 55, 57, 59, 62, 64, 66, 68, 70, 72, 73, 74, 75, 75, 76, 76, 76, 77, 77, 77, 77, 78, 79, 80],
        'C': [0, 1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 9, 10, 11, 12, 16, 18, 23, 25, 27, 36, 38, 43, 45, 48, 55, 59, 62, 68, 69, 70, 71, 72, 72, 73, 74, 75, 75, 76, 76, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80]
    }

    y = [mappings[L][v] for L, v in zip(labels, values24)]
    x = np.arange(4)

    _style_ax(ax, invert=False)
    ax.plot(x, y, "o-", color=COLORS["change"], lw=1.2, zorder=1)
    for xx, yy, vv in zip(x, y, values):
        ax.text(xx, yy + TXT_OFFSET_UP, str(vv), ha="center", va="bottom", fontsize=8, color=COLORS["change"])

    return ax
