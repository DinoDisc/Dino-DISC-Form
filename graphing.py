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

from matplotlib.patches import Rectangle
import itertools

# fill these in with exactly the y-positions you want for each v in 0..24
GRAPHLABELS_MOST = {
    'D': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,21],   # length-25 list of pt-positions
    'I': [0,1,2,3,4,5,6,7,8,9,11,19],
    'S': [0,1,2,3,4,5,6,7,8,9,10,12,14,20],
    'C': [0,1,2,3,4,5,6,7,8,9,11,13,17],
}
GRAPHLABELS_LEAST = {
    'D': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,20],
    'I': [0,1,2,3,4,5,6,7,8,9,10,11,12,19],
    'S': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,16,19],
    'C': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,17],
}
GRAPHLABELS_CHANGE = {
    'D': [-20,-16,-12,-11,-10,-9,-7,-6,-4,-3,-2,0,+1,+3,+5,+7,+8,+9,+10,+12,+13,+14,+15,+18,+21],
    'I': [-18,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,+1,+2,+3,+4,+5,+6,+7,+8,+10,+18],
    'S': [-18,-15,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,+1,+2,+3,+4,+5,+7,+8,+9,+10,+11,+15,+20],
    'C': [-22,-19,-15,-13,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,+1,+2,+3,+4,+5,+6,+10,+17],
}

# ------------------------------------------------------------------
# small helpers for grid annotations
# ------------------------------------------------------------------
_LABEL_FSIZE   = 4         # tiny font
_LABEL_X_SHIFT = 0.20      # shift to the right of the column centre

def _annotate_column_numbers(ax, x_pos, mapping_rowlist, label_list):
    """
    Draw the small grid numbers for one column.

    Parameters
    ----------
    ax               : matplotlib Axes
    x_pos            : float      – column x (0,1,2,3)
    mapping_rowlist  : list[float] length-25, y-positions for score 0..24
    label_list       : list[int]  the *scores* you want printed in this column
    """
    for v in label_list:               # v is a score (0-24 or –24..+24 for change)
        try:
            y = mapping_rowlist[v]     # where that score lives on this graph
        except IndexError:             # e.g. negative indices in CHANGE graph
            continue
        ax.text(x_pos + _LABEL_X_SHIFT, y,
                str(v),
                ha="left", va="center",
                fontsize=_LABEL_FSIZE,
                color="black",
                zorder=3)
        
def _annotate_column_numbers_change(ax, x_pos, mapping_rowlist, label_list):
    """
    Plot the tiny guideline numbers for one DISC column.

    mapping_rowlist : list of 50 y-values  (index 0 … 48)
    label_list      : list of scores (–24 … +24) you want to show
    """
    for v in label_list:
        idx = v + 24                     # <- always shift (stage b)

        if 0 <= idx < len(mapping_rowlist):
            y = mapping_rowlist[idx]     # stage c  (same as dots)

            ax.text(x_pos + _LABEL_X_SHIFT, y,      # stage d
                    str(v),                          # keep sign
                    ha="left", va="center",
                    fontsize=_LABEL_FSIZE,
                    color="black",
                    zorder=3)


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

TXT   = 0

def _style_ax(ax, *, invert=False, show_vals=False):
    """Apply paper-like styling and optional numeric row labels."""
    # clear frame
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.set_xlim(-0.5, 3.5)               # D,I,S,C
    ax.set_ylim((80, 0) if invert else (0, 80))

    # ------------------------------------------------------------------
    # draw 3 evenly-spaced dotted lines above and below the centre-line
    # ------------------------------------------------------------------
    mid = 40                 # heavy centre line
    band_step = 80 / 8       # 8 equal rows  ⇒  step = 10 units
    band_lines = [mid + i * band_step for i in (-3, -2, -1, 1, 2, 3)]

    for y in band_lines:
        ax.axhline(y,
                   lw=0.7,
                   ls=(0, (2, 2)),   # dotted
                   color="grey",
                   zorder=0)

    # central thick line
    ax.axhline(mid, lw=1.2, color="black", zorder=0)

    for xcol in range(4):                      # 0,1,2,3  (D,I,S,C)
        ax.axvline(xcol,
                   lw=0.3,
                   color="lightgrey",
                   zorder=0)                  # keep under dots / line

    # outer rectangle
    rect = Rectangle((-0.5, 0), 4, 80,
                     fill=False, lw=0.8, color="black", zorder=1)
    ax.add_patch(rect)

    # remove ticks/labels
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("none"); ax.figure.set_facecolor("none")

    # DISC column headers
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(range(4))
    ax2.set_xticklabels(list("DISC"), fontsize=7, weight="bold")
    ax2.tick_params(axis="x", length=0, pad=1)
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
    ax.plot(x, y, "o-", color="#1C80BC", lw=0.8, markersize=4, zorder=1)
    # --- NEW: tiny grid numbers ------------------------------------
    for col, L in enumerate(labels):           # D I S C
        _annotate_column_numbers(
            ax,
            x_pos      = col,
            mapping_rowlist = mappings[L],
            label_list      = GRAPHLABELS_MOST[L],
        )

    return ax

# ---------------------------------------------------------------------
# 2. LEAST -------------------------------------------------------------
# ---------------------------------------------------------------------

def plot_disc_graph_least(values, ax):
    """Plot GRAPH 2 – LEAST (values 0‑24, inverted axis)."""
    labels = "DISC"
    mappings = {
        'D': [3, 7, 18, 27, 33, 37, 42, 46, 47, 53, 55, 58, 62, 66, 68, 71, 73, 74, 75, 76, 77, 78, 79, 79, 80],
        'I': [5, 10, 21, 27, 37, 42, 50, 58, 63, 66, 71, 73, 75, 77, 77, 78, 78, 78, 79,79, 79, 80, 80, 80, 80],
        'S': [3, 5, 10, 21, 27, 33, 37, 46, 50, 55, 63, 66, 71, 73, 74, 75, 76, 77, 78, 79, 80, 80, 80, 80, 80],
        'C': [3, 5, 13, 21, 27, 33, 37, 42, 46, 53, 57, 66, 68, 71, 73, 75, 76, 77, 78, 79, 79, 80, 80, 80, 80]
    }
    y = [mappings[L][v] for L, v in zip(labels, values)]
    x = np.arange(4)

    _style_ax(ax, invert=True)                      # <- was invert=False
    ax.plot(x, y, "o-", color="#A00100",
            lw=0.8, markersize=4, zorder=1)
    for col, L in enumerate(labels):
        _annotate_column_numbers(
            ax,
            x_pos      = col,
            mapping_rowlist = mappings[L],
            label_list      = GRAPHLABELS_LEAST[L],
        )

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
    ax.plot(x, y, "o-", color="#278D8D", lw=0.8, markersize=4, zorder=1)
    for col, L in enumerate(labels):
        _annotate_column_numbers_change(
            ax,
            x_pos      = col,
            mapping_rowlist = mappings[L],
            label_list      = GRAPHLABELS_CHANGE[L],
        )

    return ax
