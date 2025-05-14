# playground.py  --------------------------------------------------------
"""
Vector‑rebuild of the IML DISC Insights™ “Personality System Graph Page”.
This version **removes**:
  • the “Organization” and “Position” rows in the header
  • the grey "Note:" rectangle at the bottom‑right of the page

Run → open **DISC_Draft.pdf** → adjust coordinates if you like.

pip install reportlab pillow
python playground.py
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import date
from pathlib import Path
from reportlab.lib.utils import ImageReader

PAGE_W, PAGE_H = letter                       # 612 × 792 pt
MARGIN_X = 36                                  # 0.5‑inch side margin
LINE_W_THIN = 0.6                              # default stroke width

# ----------------------------------------------------------------------
# 1 ─── STATIC LAYOUT ───────────────────────────────────────────────────
# ----------------------------------------------------------------------

def draw_static_page(c: canvas.Canvas) -> None:
    """Elements that never change (boxes, rules, labels, etc.)."""

    # helpers ----------------------------------------------------------
    def h(y, x1=MARGIN_X, x2=PAGE_W - MARGIN_X, w=LINE_W_THIN):
        c.setLineWidth(w)
        c.line(x1, y, x2, y)

    def v(x, y1, y2, w=LINE_W_THIN):
        c.setLineWidth(w)
        c.line(x, y1, x, y2)

    def txt(x, y, text, *, size=9, bold=False):
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        c.drawString(x, y, text)

    # ── Title ---------------------------------------------------------
    txt(MARGIN_X, PAGE_H - 40, "IML DISC Insights™ Personality System Graph Page", size=13, bold=True)

    # ── Header form fields  (Organization & Position REMOVED) ---------
    header_top = PAGE_H - 60
    gap_y = 16                               # vertical gap between rows
    underline_len = 192                      # uniform underline length

    left_fields  = ["Name:", "Email:"] 
    right_fields = ["Date of Birth:", "Gender:"]         

    # draw left‑hand labels & underlines
    for idx, label in enumerate(left_fields):
        y = header_top - idx * gap_y
        txt(MARGIN_X, y, label)
        h(y - 3, MARGIN_X + 65, MARGIN_X + 65 + underline_len)

    # draw right‑hand labels & underlines (except Gender)
    for idx, label in enumerate(right_fields):
        y = header_top - idx * gap_y
        xlbl = PAGE_W / 2 + 10
        txt(xlbl, y, label)
        if label != "Gender:":
            h(y - 3, xlbl + 55, xlbl + 55 + underline_len - 30)

    # gender boxes (row index = 1 now)
    gender_row_idx = right_fields.index("Gender:")       # 1
    gender_y = header_top - gender_row_idx * gap_y
    box = 11
    male_x = PAGE_W / 2 + 85
    female_x = male_x + 85
    for x in (male_x, female_x):
        v(x, gender_y - 2, gender_y - 2 + box)
        v(x + box, gender_y - 2, gender_y - 2 + box)
        h(gender_y - 2, x, x + box)
        h(gender_y - 2 + box, x, x + box)
    txt(male_x   + box + 6, gender_y, "Male")
    txt(female_x + box + 6, gender_y, "Female")

    # ── 3‑row score table -------------------------------------------
    table_top = PAGE_H - 150
    row_h = 36
    col_w = 46
    table_left = MARGIN_X + 110
    cols = ["D", "I", "S", "C", "★", "Total Score"]

    for i, col in enumerate(cols):
        txt(table_left + i * col_w + 15, table_top + 20, col, size=8, bold=True)
    for i in range(len(cols) + 1):
        v(table_left + i * col_w, table_top - 3 * row_h, table_top)
    for i in range(4):
        h(table_top - i * row_h, table_left, table_left + len(cols) * col_w)

    # grey row labels
    label_w = 66
    for i, lbl in enumerate(["Most", "Least", "Change"]):
        y_top = table_top - i * row_h
        c.setFillColor(colors.grey if i % 2 == 0 else colors.lightgrey)
        c.rect(MARGIN_X, y_top - row_h, label_w, row_h, fill=1, stroke=0)
        c.setFillColor(colors.white)
        txt(MARGIN_X + 6,  y_top - 14, "Row", size=7,  bold=True)
        txt(MARGIN_X + 6,  y_top - 26, str(i + 1), size=8, bold=True)
        txt(MARGIN_X + 28, y_top - 20, lbl,          size=9, bold=True)
        c.setFillColor(colors.black)

    # right‑side "Must equal 24" & star note
    note_x = table_left + len(cols) * col_w + 12
    for row in (0, 1):
        y = table_top - row * row_h - 10
        txt(note_x,     y,       "Must Equal", size=7)
        txt(note_x + 4, y - 14, "24",         size=12, bold=True)

    # explanatory note under table
    small = " "
    txt(MARGIN_X, table_top - 3 * row_h - 14, small, size=6)

    # ── Graph rectangles --------------------------------------------
    g_w, g_h = 150, 200
    g_gap = 16
    g_y = PAGE_H - 500  # lowered from previous value to shift graphs downward
    g_x = [MARGIN_X, 
           MARGIN_X + g_w + g_gap,
           MARGIN_X + 2 * (g_w + g_gap)]

    # graph headings + DISC blocks
    heads = [
        ("Graph 1  MOST",   "Mask, Public Self"),
        ("Graph 2  LEAST",  "Core, Private Self"),
        ("Graph 3  CHANGE", "Mirror, Perceived Self"),
    ]
    for (title, sub), gx in zip(heads, g_x):
        txt(gx, g_y + g_h + 10, title, size=8, bold=True)
        txt(gx, g_y + g_h - 4,  sub,   size=7)
    # footer -----------------------------------------------------------
    txt(MARGIN_X, 60, "© Copyright 2000 -- 2024, The Institute for Motivational Living, Inc.  All rights reserved.  Reproduction prohibited.", size=6)

# ----------------------------------------------------------------------
# 2 ─── DYNAMIC CONTENT (user data + real graphs) ----------------------
# ----------------------------------------------------------------------

# ---------- helpers ---------------------------------------------------
def _draw_score_row(c, values, y0, table_left, col_w):
    for i, val in enumerate(values):
        x = table_left + i * col_w + col_w / 2
        c.drawCentredString(x, y0, str(val))

def draw_client_layer(c: canvas.Canvas,
                      *,
                      user: dict,
                      graphs: dict | None = None,
                      scores: dict | None = None):

    ## --- text fields -------------------------------------------------
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN_X + 68, PAGE_H - 60,  user.get("name", ""))
    c.drawString(MARGIN_X + 68, PAGE_H - 76,  user.get("email", ""))
    # date
    date_str = (user.get("date") or date.today()).strftime("%d-%b-%Y")
    c.drawString(PAGE_W / 2 + 65, PAGE_H - 60, date_str)

    ## --- gender tick -------------------------------------------------
    gender = user.get("gender", "").lower()
    if gender in {"male", "female"}:
        c.setFont("Helvetica-Bold", 12)
        box = 11
        male_x   = PAGE_W / 2 + 85
        female_x = male_x + 85
        tick_x = male_x + 3 if gender == "male" else female_x + 3
        c.drawString(tick_x, PAGE_H - 76, "X")

    # fill-in score table ----------------
    if scores:
        table_top = PAGE_H - 150
        row_h = 36
        col_w = 46
        table_left = MARGIN_X + 110
        
        rows = ("most", "least", "change")
        for idx, key in enumerate(rows):
            y_mid = table_top - idx * row_h - row_h / 2 - 3
            row   = scores[key]
            vals = [
                row["D"], row["I"], row["S"], row["C"],
                row["*"],
                "" if key=="change" else row["Total"]   
            ]
            _draw_score_row(c, vals, y_mid, table_left, col_w)
    ## --- embed PNG graphs -------------------------------------------
    g_w, g_h = 150, 200
    g_gap = 16
    g_y = PAGE_H - 500
    g_x = [MARGIN_X, 
           MARGIN_X + g_w + g_gap, 
           MARGIN_X + 2 * (g_w + g_gap)]

    order = ["most", "least", "change"]

    if graphs:
        for key, x in zip(order, g_x):
            path = graphs.get(key)
            if path:
                c.drawImage(ImageReader(path), x, g_y, g_w, g_h, mask="auto")
    else:
        c.setFillColor(colors.whitesmoke)
        for x in g_x:
            c.rect(x+1, g_y+1, g_w-2, g_h-2, fill=1, stroke=0)
        c.setFillColor(colors.black)
# ----------------------------------------------------------------------
# 3 ─── BUILD PDF ------------------------------------------------------
# ----------------------------------------------------------------------

def build_pdf(*, 
              user: dict,
              graphs: dict | None = None,
              scores: dict | None = None,
              out_path: str = "DISC_Draft.pdf") -> str:
    """
    Parameters
    ----------
    user   : dict  – required keys: name, profile, date, gender
    graphs : dict  – keys 'most' 'least' 'change' → PNG paths (optional)
    out_path : str – where to write the PDF

    Returns
    -------
    str – absolute path to the written PDF (so Streamlit can attach it)
    """
    c = canvas.Canvas(out_path, pagesize=letter)
    draw_static_page(c)
    draw_client_layer(c, user=user, graphs=graphs, scores=scores)
    c.showPage()
    c.save()
    abs_path = str(Path(out_path).resolve())
    print("PDF created →", abs_path)
    return abs_path
