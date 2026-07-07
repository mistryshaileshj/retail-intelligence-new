# retail_intelligence_22
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Retail Intelligence", layout="wide",
                   initial_sidebar_state="expanded")

# ── Palette — Aurora on white ─────────────────────────────────────────────────
BG_PAGE   = "#f4f7fa"
BG_CARD   = "#ffffff"
BG_CARD2  = "#eef3f7"
BG_HEADER = "#eef6f4"

ACCENT    = "#2fb8a3"   # teal
ACCENT2   = "#e0a458"   # amber
ACCENT3   = "#4a90c4"   # blue
ACCENT4   = "#d97b8f"   # rose
ACCENT5   = "#7c6fd4"   # violet
ACCENT6   = "#45c98a"   # green

TEXT_PRI  = "#1f3142"
TEXT_SEC  = "#6b7d8f"
GRID_COL  = "rgba(31,49,66,0.06)"
BORDER    = "#e8edf2"
DIM_GREY  = "rgba(31,49,66,0.13)"   # dimmed (non-selected) bars

SHADOW_3D = "0 1px 2px rgba(31,49,66,0.04), 0 8px 20px rgba(31,49,66,0.08), inset 0 1px 0 rgba(255,255,255,0.9)"
SHADOW_3D_HOVER = "0 2px 4px rgba(31,49,66,0.06), 0 12px 28px rgba(31,49,66,0.12), inset 0 1px 0 rgba(255,255,255,0.9)"

def rgba(hexc, a):
    hexc = hexc.lstrip('#')
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
.stApp{{background:{BG_PAGE};}}

#MainMenu, footer{{visibility:hidden;}}
[data-testid="stDecoration"]{{display:none !important;}}
/* Header is left at Streamlit defaults so the native sidebar collapse/expand
   toggle renders. Sidebar is collapsible; on phones it overlays (won't eat page). */
section[data-testid="stSidebar"]{{min-width:250px;background:{BG_CARD2} !important;
    border-right:1px solid {BORDER};}}
@media (max-width: 640px){{
    section[data-testid="stSidebar"]{{min-width:82vw !important;width:82vw !important;}}
}}
.main .block-container,
[data-testid="stMainBlockContainer"],
.stMainBlockContainer,
.block-container{{padding-top:3rem !important;padding-bottom:1rem;max-width:100%;}}
[data-testid="stVerticalBlock"]{{gap:0.5rem;}}

.main-header{{
    background:linear-gradient(135deg,{BG_HEADER} 0%,#ffffff 100%);
    border:1px solid {BORDER};border-radius:12px;
    padding:7px 18px;margin-bottom:4px;display:flex;align-items:center;
    box-shadow:{SHADOW_3D};
}}
.main-header h1{{color:{TEXT_PRI};font-size:18px;font-weight:700;margin:0;line-height:1.1;}}

[data-testid="stWidgetLabel"] p{{
    font-size:11px !important;font-weight:600 !important;color:{TEXT_SEC} !important;
    text-transform:uppercase;letter-spacing:0.05em;margin:0 0 3px 1px !important;
    white-space:nowrap;overflow:visible;
}}
.ctl-lbl{{font-size:11px;font-weight:600;color:{TEXT_SEC};text-transform:uppercase;
    letter-spacing:0.05em;margin:0 0 4px 1px;white-space:nowrap;height:15px;}}
/* inline label ("From:" / "To:") vertically centred against the controls */
.inl-lbl{{display:flex;align-items:center;justify-content:flex-end;height:34px;
    font-size:12px;font-weight:700;color:{TEXT_SEC};white-space:nowrap;padding-right:1px;}}
/* sidebar filters title */
.side-title{{font-size:14px;font-weight:800;color:{TEXT_PRI};letter-spacing:0.02em;
    margin:2px 0 10px 2px;}}
.stDateInput input{{
    background:{BG_CARD} !important;border:1px solid {BORDER} !important;
    border-radius:8px !important;color:{TEXT_PRI} !important;
    font-size:11px !important;padding:4px 7px !important;
}}
.stDateInput [data-baseweb="input"]{{min-height:32px !important;}}
/* Narrow the Dimension dropdown (was too wide in the Options popover) */
[data-testid="stSelectbox"]{{max-width:180px;}}
[data-testid="stSelectbox"] div[data-baseweb="select"]{{max-width:180px;}}
[data-testid="stNumberInput"] input{{
    font-size:12px !important;color:{TEXT_PRI} !important;
    -webkit-text-fill-color:{TEXT_PRI} !important;padding:3px 6px !important;
    background:{BG_CARD} !important;
}}

/* deploy-proof widget text colors (radio options + any select value) */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] div[role="radiogroup"] label p,
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p{{
    color:{TEXT_PRI} !important;font-size:12px !important;font-weight:500 !important;
    -webkit-text-fill-color:{TEXT_PRI} !important;
}}
[data-testid="stRadio"]>div{{gap:12px !important;}}

/* Clear button */
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button{{
    font-size:11px !important;font-weight:600 !important;padding:5px 12px !important;
    border-radius:8px !important;border:1px solid {BORDER} !important;
    background:{BG_CARD} !important;color:{TEXT_PRI} !important;
}}
[data-testid="stButton"] button:hover{{border-color:{ACCENT4} !important;color:{ACCENT4} !important;}}
[data-testid="stDownloadButton"] button:hover{{border-color:{ACCENT} !important;color:{ACCENT} !important;}}
/* Options (⚙) popover: compact, pinned to the right edge of the card header
   so it sits just past the Plotly zoom-out button in the toolbar below. */
div[data-testid="stPopover"]{{display:flex;justify-content:flex-end;}}
div[data-testid="stPopover"]>button, div[data-testid="stPopover"] button{{
    width:auto !important;min-width:0 !important;padding:4px 9px !important;
    font-size:14px !important;border-radius:8px !important;
    border:1px solid {BORDER} !important;background:{BG_CARD} !important;color:{TEXT_PRI} !important;
}}

/* summary KPI cards */
.kpi-card{{
    background:{BG_CARD};border:1px solid {BORDER};border-radius:14px;
    padding:11px 14px;border-top:4px solid transparent;
    box-shadow:{SHADOW_3D};transition:transform 0.15s, box-shadow 0.2s;
}}
.kpi-card:hover{{transform:translateY(-3px);box-shadow:{SHADOW_3D_HOVER};}}
.kpi-card.k1{{border-top-color:{ACCENT};}}
.kpi-card.k2{{border-top-color:{ACCENT3};}}
.kpi-card.k3{{border-top-color:{ACCENT2};}}
.kpi-card.k4{{border-top-color:{ACCENT4};}}
.kpi-card.k5{{border-top-color:{ACCENT5};}}
.kpi-label{{font-size:10px;font-weight:600;color:{TEXT_SEC};text-transform:uppercase;letter-spacing:0.07em;}}
.kpi-value{{font-size:20px;font-weight:700;color:{TEXT_PRI};margin:3px 0 2px;}}
.kpi-delta{{font-size:11px;font-weight:500;}}
.kpi-delta.up{{color:{ACCENT};}} .kpi-delta.down{{color:{ACCENT4};}} .kpi-delta.neutral{{color:{TEXT_SEC};}}

/* chart card header: "Top" [N input] Name */
.hdr-cell{{display:flex;align-items:center;min-height:38px;}}
.topword{{font-size:13px;font-weight:800;color:{TEXT_SEC};text-transform:uppercase;
    letter-spacing:0.06em;}}
.kpiname{{font-size:14px;font-weight:800;color:{TEXT_PRI};white-space:nowrap;
    overflow:hidden;text-overflow:ellipsis;gap:5px;}}
.chart-title{{
    font-size:12px;font-weight:800;color:{TEXT_PRI};letter-spacing:0.01em;
    margin:2px 0 2px 2px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;
}}
.chart-name{{font-weight:800 !important;color:{TEXT_PRI};font-size:12.5px;}}
.chart-meas{{
    font-size:9px;font-weight:700;color:{ACCENT};
    background:{rgba(ACCENT,0.12)};border:1px solid {rgba(ACCENT,0.30)};
    padding:1px 7px;border-radius:20px;text-transform:uppercase;letter-spacing:0.05em;
}}
.xf-active{{
    font-size:9px;font-weight:700;color:{ACCENT4};
    background:{rgba(ACCENT4,0.12)};border:1px solid {rgba(ACCENT4,0.35)};
    padding:1px 7px;border-radius:20px;
}}

/* cross-filter chips row */
.xf-wrap{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;min-height:34px;}}
.xf-chip{{
    font-size:11px;font-weight:600;color:{TEXT_PRI};
    background:{rgba(ACCENT,0.12)};border:1px solid {rgba(ACCENT,0.35)};
    padding:3px 10px;border-radius:20px;white-space:nowrap;
}}
.xf-chip .k{{color:{TEXT_SEC};font-weight:700;text-transform:uppercase;font-size:9px;letter-spacing:0.05em;margin-right:4px;}}
.xf-none{{font-size:11px;color:{TEXT_SEC};font-style:italic;}}
[data-testid="stVerticalBlockBorderWrapper"]{{border-radius:14px;}}
</style>
""", unsafe_allow_html=True)

# ── Load & cache ──────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Sales_SalesRtn.csv"

@st.cache_data
def load_data():
    df = pd.read_csv("Sales_SalesRtn.csv", low_memory=False)
    df['DOC_DT'] = pd.to_datetime(df['DOC_DT'], errors='coerce')
    df['IS_SALE'] = df['Trj_Type'] == 'Sales'
    df['IS_RTN']  = df['Trj_Type'] == 'Sales Rtn'
    df['REVENUE']  = df['NET_AMT'].where(df['IS_SALE'], 0)
    df['RTN_AMT']  = df['NET_AMT'].abs().where(df['IS_RTN'], 0)
    df['SALE_QTY'] = df['QTY'].where(df['IS_SALE'], 0)
    df['RTN_QTY2'] = df['RTN_QTY'].where(df['IS_RTN'], 0)
    df['NET_VALUE'] = df['REVENUE'] - df['RTN_AMT']
    df['NET_QTY']   = df['SALE_QTY'] - df['RTN_QTY2']
    df['MARGIN']     = df['SALERATE'] - df['PURRATE']
    df['MARGIN_PCT'] = (df['MARGIN'] / df['SALERATE'].replace(0, np.nan) * 100).fillna(0)
    return df

df = load_data()
abs_min = df['DOC_DT'].min().date()
abs_max = df['DOC_DT'].max().date()

# 6 cross-filter dimensions (a→f)
DIM_LABELS = {'SUBGRP':'Sub Group', 'ITEM':'Product', 'BRAND':'Brand',
              'STYLE':'Style', 'SHADE':'Shade', 'SIZE_NAME':'Size'}

# Dimensions the user can plot on a selectable KPI (dropdown order as requested)
DIM_OPTIONS = ['PARTY', 'ITEM', 'STYLE', 'TYPENAME', 'SHADE', 'SIZE_NAME',
               'BRAND', 'QUALITY', 'SEASON', 'OCCASSION', 'SUPPLIER', 'SUBGRP']

if 'xfilters' not in st.session_state:
    st.session_state.xfilters = {}      # dim -> selected value (str)
if 'xnonce' not in st.session_state:
    st.session_state.xnonce = 0         # bumps to give charts a fresh key on change

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header"><h1>🏪 Retail Intelligence</h1></div>',
            unsafe_allow_html=True)

# ── Sidebar filters: From · To · Value/Quantity ───────────────────────────────
with st.sidebar:
    st.markdown('<div class="side-title">🔎 Filters</div>', unsafe_allow_html=True)
    date_from = st.date_input("From", value=abs_min, min_value=abs_min,
                              max_value=abs_max, format="DD/MM/YYYY")
    date_to = st.date_input("To", value=abs_max, min_value=abs_min,
                            max_value=abs_max, format="DD/MM/YYYY")
    measure = st.radio("Measure", ["Value", "Quantity"], horizontal=True,
                       label_visibility="collapsed")

# ── Active cross-filters + Clear (main area) ──────────────────────────────────
xf = st.session_state.xfilters
_spec = [6.4, 1.0]
try:
    cc, cx = st.columns(_spec, vertical_alignment="center")
except TypeError:
    cc, cx = st.columns(_spec)
with cc:
    if xf:
        chips = "".join(
            f'<span class="xf-chip"><span class="k">{DIM_LABELS.get(d, d)}</span>{v}</span>'
            for d, v in xf.items())
    else:
        chips = '<span class="xf-none">Click a bar / point to cross-filter</span>'
    st.markdown(f'<div class="xf-wrap">{chips}</div>', unsafe_allow_html=True)
with cx:
    if st.button("✕ Clear", use_container_width=True, disabled=not xf):
        st.session_state.xfilters = {}
        st.session_state.xnonce += 1
        st.rerun()

# ── Base (date) filter + cross-filter application ─────────────────────────────
mask = (df['DOC_DT'].dt.date >= date_from) & (df['DOC_DT'].dt.date <= date_to)
base = df[mask]
xf = st.session_state.xfilters

def apply_filters(frame, exclude=None):
    out = frame
    for d, v in xf.items():
        if d == exclude:
            continue
        out = out[out[d].astype(str) == str(v)]
    return out

kpi_df = apply_filters(base)   # summary cards honour ALL cross-filters + date

meas_col   = 'NET_VALUE' if measure == "Value" else 'NET_QTY'
meas_label = "Net Value" if measure == "Value" else "Net Quantity"

def fmt(v):
    return f"₹{v:,.0f}" if measure == "Value" else f"{v:,.0f}"

# ── Summary KPI cards (reflect date + all cross-filters) ──────────────────────
sales = kpi_df[kpi_df['IS_SALE']]
gross   = kpi_df['REVENUE'].sum()
rtn_amt = kpi_df['RTN_AMT'].sum()
net     = gross - rtn_amt
units   = kpi_df['SALE_QTY'].sum()
rtn_qty = kpi_df['RTN_QTY2'].sum()
txns    = sales['PDOC_NO'].nunique()
avg_pr  = sales['SALERATE'].mean()    if len(sales) else 0
margin  = sales['MARGIN_PCT'].mean()  if len(sales) else 0
avg_disc= sales['Disc_Perc'].mean()   if len(sales) else 0
tot_disc= sales['ITEMDISC_AMT'].sum()
rtn_rate= (rtn_qty / units * 100)     if units > 0 else 0

def kpi(col, label, value, delta, direction, cls, icon):
    arrow = "▲" if direction == "up" else ("▼" if direction == "down" else "●")
    col.markdown(f"""
    <div class="kpi-card {cls}">
      <div class="kpi-label">{icon} {label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-delta {direction}">{arrow} {delta}</div>
    </div>""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
kpi(m1, "Net Sales",      f"₹{net:,.0f}",    f"Gross ₹{gross:,.0f}",                    "up",      "k1", "💰")
kpi(m2, "Units Sold",     f"{units:,.0f}",   f"{txns} transactions",                    "neutral", "k2", "📦")
kpi(m3, "Avg Sell Price", f"₹{avg_pr:,.0f}", f"Disc: {avg_disc:.1f}%",                  "neutral", "k3", "🏷️")
kpi(m4, "Return Rate",    f"{rtn_rate:.1f}%",f"₹{rtn_amt:,.0f} | {rtn_qty:.0f} units",  "down" if rtn_rate>10 else "up", "k4", "↩️")
kpi(m5, "Gross Margin",   f"{margin:.1f}%",  f"₹{tot_disc:,.0f} discounted",            "up" if margin>30 else "neutral", "k5", "📊")

st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

# ── Plotly helpers ────────────────────────────────────────────────────────────
def light_fig(fig, height=320, axes=True):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=(dict(l=54, r=14, t=28, b=52) if axes else dict(l=12, r=12, t=28, b=12)),
        height=height, showlegend=False,
        font=dict(family="Inter", color=TEXT_SEC, size=10),
        clickmode='event+select',
        hoverlabel=dict(bgcolor="#ffffff", font_color=TEXT_PRI, font_size=11, bordercolor=BORDER),
    )
    if axes:
        fig.update_xaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(color=TEXT_SEC, size=9),
                         title_font=dict(color=TEXT_SEC, size=10), title_standoff=6)
        fig.update_yaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(color=TEXT_SEC, size=9),
                         title_font=dict(color=TEXT_SEC, size=10), title_standoff=6)
    return fig

def top_n_df(frame, dim, n):
    g = frame.groupby(dim, dropna=True)[meas_col].sum().reset_index()
    key = g[dim].astype(str).str.strip()
    g = g[key.ne('') & ~key.str.lower().isin(['nan', 'na', 'none'])]
    return g.sort_values(meas_col, ascending=False).head(n)

def bar_colors(cats, color, active):
    if active is None:
        return color
    return [color if str(c) == str(active) else DIM_GREY for c in cats]

PIE_PALETTE = [ACCENT, ACCENT3, ACCENT5, ACCENT2, ACCENT6, ACCENT4,
               "#6fd0c0", "#7fb3da", "#a59ce3", "#ecc084", "#7fdaa9", "#e6a3b2"]

def build_fig(g, dim, color, ctype, orient, active):
    cats = g[dim].astype(str).tolist()
    vals = g[meas_col].tolist()
    cols = bar_colors(cats, color, active)
    axes = True
    if ctype == "Bar" and orient == 'h':
        fig = go.Figure(go.Bar(y=cats, x=vals, orientation='h', marker_color=cols,
                unselected=dict(marker=dict(opacity=1)),
                hovertemplate="<b>%{y}</b><br>"+meas_label+": %{x:,.0f}<extra></extra>"))
        fig.update_yaxes(autorange='reversed', tickfont=dict(size=9))
        fig.update_xaxes(tickformat=",", title_text=meas_label)
    elif ctype == "Bar":
        fig = go.Figure(go.Bar(x=cats, y=vals, marker_color=cols,
                unselected=dict(marker=dict(opacity=1)),
                hovertemplate="<b>%{x}</b><br>"+meas_label+": %{y:,.0f}<extra></extra>"))
        fig.update_xaxes(tickangle=-35, tickfont=dict(size=8))
        fig.update_yaxes(tickformat=",", title_text=meas_label)
    elif ctype == "Line":
        mcol = cols if active is not None else color
        fig = go.Figure(go.Scatter(x=cats, y=vals, mode='lines+markers',
                line=dict(color=color, width=2.5, shape='spline'),
                marker=dict(size=8, color=mcol),
                fill='tozeroy', fillcolor=rgba(color, 0.12),
                unselected=dict(marker=dict(opacity=1)),
                hovertemplate="<b>%{x}</b><br>"+meas_label+": %{y:,.0f}<extra></extra>"))
        fig.update_xaxes(tickangle=-35, tickfont=dict(size=8))
        fig.update_yaxes(tickformat=",", title_text=meas_label)
    else:  # Pie / Donut (net values clipped at 0 — can't show negatives)
        axes = False
        pvals = [v if v > 0 else 0 for v in vals]
        if active is not None:
            pull = [0.08 if str(c) == str(active) else 0 for c in cats]
            pcolors = [color if str(c) == str(active) else DIM_GREY for c in cats]
        else:
            pull = None
            pcolors = PIE_PALETTE[:max(len(cats), 1)]
        fig = go.Figure(go.Pie(labels=cats, values=pvals, pull=pull, sort=False,
                hole=0.55 if ctype == "Donut" else 0,
                marker=dict(colors=pcolors, line=dict(color="#ffffff", width=1)),
                textinfo="label+percent", textfont=dict(size=10),
                hovertemplate="<b>%{label}</b><br>"+meas_label+": %{value:,.0f}<extra></extra>"))
    if not cats:
        fig.add_annotation(text="No data for this dimension", showarrow=False,
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           font=dict(family="Inter", size=12, color=TEXT_SEC))
    return light_fig(fig, axes=axes)

def clicked_value(event, ctype, orient):
    try:
        pts = event["selection"]["points"]
    except (TypeError, KeyError, AttributeError):
        return None
    if not pts:
        return None
    p = pts[0]
    if ctype in ("Pie", "Donut"):
        val = p.get("label")
    elif ctype == "Bar" and orient == 'h':
        val = p.get("y")
    else:
        val = p.get("x")
    if val is None:
        val = p.get("label")
    return None if val is None else str(val)

# CHART_TYPES = ["Bar", "Line", "Pie", "Donut", "Table"]
# CHART_ICONS = {"Bar": "📊", "Line": "📈", "Pie": "🥧", "Donut": "🍩", "Table": "📋"}
# CHART_ICON_MAP = {
#     "Bar":   ":material/bar_chart:",
#     "Line":  ":material/show_chart:",
#     "Pie":   ":material/pie_chart:",
#     "Donut": ":material/donut_large:",
#     "Table": ":material/table_chart:",
# }


CHART_TYPES = ["Bar", "Line"]
CHART_ICONS = {"Bar": "📊", "Line": "📈"}
CHART_ICON_MAP = {
    "Bar":   ":material/bar_chart:",
    "Line":  ":material/show_chart:"
}


def render(col, slot, dim_default, color, orient, default_type):
    with col.container(border=True):
        hc_name, hc_clr, hc_opt = st.columns([3.0, 0.5, 0.95])
        # All per-chart controls live in one Options popover (keeps header clean)
        with hc_opt.popover("⚙", use_container_width=False):
            n = st.number_input("Top N", min_value=3, max_value=30, value=5, step=1,
                                key=f"n_{slot}")
            dim = st.selectbox("Dimension", DIM_OPTIONS,
                               index=DIM_OPTIONS.index(dim_default), key=f"dim_{slot}")
            if hasattr(st, "segmented_control"):
                ctype = st.segmented_control(
                    "Chart type", CHART_TYPES, default=default_type,
                    format_func=lambda x: CHART_ICON_MAP.get(x, x),
                    key=f"type_{slot}") or default_type
            else:
                ctype = st.radio("Chart type", CHART_TYPES,
                                 index=CHART_TYPES.index(default_type),
                                 horizontal=True, key=f"type_{slot}")
        active = xf.get(dim)
        frame = apply_filters(base, exclude=dim)      # cross-filter by the OTHER dims
        hc_name.markdown(
            f'<div class="hdr-cell kpiname">{CHART_ICONS.get(ctype, "")} Top {n} · {dim}</div>',
            unsafe_allow_html=True)
        if active is not None:
            if hc_clr.button("✕", key=f"x_{slot}", help=f"Clear {dim} filter"):
                st.session_state.xfilters.pop(dim, None)
                st.session_state.xnonce += 1
                st.rerun()
        g = top_n_df(frame, dim, n)
        event = None
        if ctype == "Table":
            if len(g):
                disp = g.copy()
                disp.insert(0, "Rank", range(1, len(disp) + 1))
                disp[meas_col] = disp[meas_col].round(0)
                disp = disp.rename(columns={meas_col: meas_label})
                st.dataframe(disp, hide_index=True, use_container_width=True, height=300)
            else:
                st.caption("No data for this dimension")
        else:
            event = st.plotly_chart(build_fig(g, dim, color, ctype, orient, active),
                                    use_container_width=True,
                                    key=f"chart_{slot}_{st.session_state.xnonce}",
                                    on_select="rerun",
                                    config={
                                        "displayModeBar": True,
                                        "displaylogo": False,
                                        # only Download · Zoom-in · Zoom-out
                                        # (Full screen is Streamlit's own expand button)
                                        "modeBarButtons": [["toImage", "zoomIn2d", "zoomOut2d"]],
                                        "toImageButtonOptions": {
                                            "format": "png",
                                            "filename": f"{dim}_Top{n}",
                                            "scale": 2},
                                    })
    # Only ACT on a real (non-empty) click that changes this dim's selection.
    if event is not None:
        sel = clicked_value(event, ctype, orient)
        if sel is not None and sel != active:
            st.session_state.xfilters[dim] = sel
            st.session_state.xnonce += 1
            st.rerun()

# ── Row 1 ─────────────────────────────────────────────────────────────────────
r1a, r1b, r1c = st.columns(3)
render(r1a, 'kpi1', 'SUBGRP',    ACCENT,  'v', 'Bar')
render(r1b, 'kpi2', 'ITEM',      ACCENT3, 'h', 'Bar')
render(r1c, 'kpi3', 'BRAND',     ACCENT5, 'h', 'Line')

# ── Row 2 ─────────────────────────────────────────────────────────────────────
r2a, r2b, r2c = st.columns(3)
render(r2a, 'kpi4', 'STYLE',     ACCENT2, 'v', 'Bar')
render(r2b, 'kpi5', 'SHADE',     ACCENT6, 'h', 'Bar')
render(r2c, 'kpi6', 'SIZE_NAME', ACCENT4, 'v', 'Line')
