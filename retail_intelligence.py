import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Retail Intelligence", layout="wide",
                   initial_sidebar_state="collapsed")

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

SHADOW_3D = "0 1px 2px rgba(31,49,66,0.04), 0 8px 20px rgba(31,49,66,0.08), inset 0 1px 0 rgba(255,255,255,0.9)"
SHADOW_3D_HOVER = "0 2px 4px rgba(31,49,66,0.06), 0 12px 28px rgba(31,49,66,0.12), inset 0 1px 0 rgba(255,255,255,0.9)"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
.stApp{{background:{BG_PAGE};}}

/* move the page up: drop the Streamlit header + shrink top padding */
#MainMenu, footer{{visibility:hidden;}}
[data-testid="stHeader"]{{display:none !important;height:0 !important;}}
[data-testid="stToolbar"]{{display:none !important;}}
[data-testid="stDecoration"]{{display:none !important;}}
[data-testid="stAppViewContainer"]>.main{{padding-top:0 !important;}}
.main .block-container,
[data-testid="stMainBlockContainer"],
.stMainBlockContainer,
.block-container{{padding-top:0.35rem !important;padding-bottom:1rem;max-width:100%;}}
[data-testid="stVerticalBlock"]{{gap:0.5rem;}}

/* compact header band */
.main-header{{
    background:linear-gradient(135deg,{BG_HEADER} 0%,#ffffff 100%);
    border:1px solid {BORDER};border-radius:12px;
    padding:7px 18px;margin-bottom:4px;
    display:flex;align-items:center;
    box-shadow:{SHADOW_3D};
}}
.main-header h1{{color:{TEXT_PRI};font-size:18px;font-weight:700;margin:0;line-height:1.1;}}

/* native widget labels — visible, compact, never clipped */
[data-testid="stWidgetLabel"] p{{
    font-size:11px !important;font-weight:600 !important;color:{TEXT_SEC} !important;
    text-transform:uppercase;letter-spacing:0.05em;margin:0 0 3px 1px !important;
    white-space:nowrap;overflow:visible;
}}
.stDateInput input{{
    background:{BG_CARD} !important;border:1px solid {BORDER} !important;
    border-radius:8px !important;color:{TEXT_PRI} !important;
    font-size:12px !important;padding:5px 9px !important;
}}
div[data-baseweb="select"]>div{{
    background:{BG_CARD} !important;border:1px solid {BORDER} !important;
    border-radius:8px !important;font-size:12px !important;min-height:32px !important;
    cursor:pointer !important;
}}
/* Sub Group: plain dropdown feel — no text caret, no I-beam, no typing */
div[data-baseweb="select"] input{{
    caret-color:transparent !important;cursor:pointer !important;
}}
div[data-baseweb="select"] *{{cursor:pointer !important;}}
[data-testid="stRadio"]>div{{gap:12px !important;}}

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

/* chart card title */
.chart-title{{
    font-size:11px;font-weight:700;color:{TEXT_PRI};letter-spacing:0.02em;
    margin:2px 0 4px 2px;display:flex;align-items:center;gap:7px;flex-wrap:wrap;
}}
.chart-meas{{
    font-size:9px;font-weight:700;color:{ACCENT};
    background:rgba(47,184,163,0.12);border:1px solid rgba(47,184,163,0.30);
    padding:1px 7px;border-radius:20px;text-transform:uppercase;letter-spacing:0.05em;
}}
[data-testid="stVerticalBlockBorderWrapper"]{{border-radius:14px;}}
</style>
""", unsafe_allow_html=True)

# ── Load & cache ──────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Sales_SalesRtn.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    df['DOC_DT'] = pd.to_datetime(df['DOC_DT'], errors='coerce')

    df['IS_SALE'] = df['Trj_Type'] == 'Sales'
    df['IS_RTN']  = df['Trj_Type'] == 'Sales Rtn'

    df['REVENUE']  = df['NET_AMT'].where(df['IS_SALE'], 0)
    df['RTN_AMT']  = df['NET_AMT'].abs().where(df['IS_RTN'], 0)
    df['SALE_QTY'] = df['QTY'].where(df['IS_SALE'], 0)
    df['RTN_QTY2'] = df['RTN_QTY'].where(df['IS_RTN'], 0)

    # per-row net contributions (sales positive, returns negative)
    df['NET_VALUE'] = df['REVENUE'] - df['RTN_AMT']
    df['NET_QTY']   = df['SALE_QTY'] - df['RTN_QTY2']

    df['MARGIN']     = df['SALERATE'] - df['PURRATE']
    df['MARGIN_PCT'] = (df['MARGIN'] / df['SALERATE'].replace(0, np.nan) * 100).fillna(0)
    return df

df = load_data()

abs_min = df['DOC_DT'].min().date()
abs_max = df['DOC_DT'].max().date()

# ── Header title ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-header"><h1>🏪 Retail Intelligence</h1></div>',
            unsafe_allow_html=True)

# ── Control strip (native labels so they never get cut) ───────────────────────
c_from, c_to, c_meas, c_sub, c_topn = st.columns([1.1, 1.1, 1.4, 1.3, 2.0])
with c_from:
    date_from = st.date_input("From Date", value=abs_min, min_value=abs_min,
                              max_value=abs_max, format="DD/MM/YYYY")
with c_to:
    date_to = st.date_input("To Date", value=abs_max, min_value=abs_min,
                            max_value=abs_max, format="DD/MM/YYYY")
with c_meas:
    measure = st.radio("Measure", ["Value", "Quantity"], horizontal=True)
with c_sub:
    subgrps = ["All"] + sorted(df['SUBGRP'].dropna().unique().tolist())
    subgrp = st.selectbox("Sub Group", subgrps)
with c_topn:
    top_n = st.slider("Top N", 3, 20, 5)

# ── Filter: date + sub group ──────────────────────────────────────────────────
mask = (df['DOC_DT'].dt.date >= date_from) & (df['DOC_DT'].dt.date <= date_to)
if subgrp != "All":
    mask &= (df['SUBGRP'] == subgrp)
fdf = df[mask]

meas_col   = 'NET_VALUE' if measure == "Value" else 'NET_QTY'
meas_label = "Net Value" if measure == "Value" else "Net Quantity"

def fmt(v):
    return f"₹{v:,.0f}" if measure == "Value" else f"{v:,.0f}"

# ── Summary KPI cards (restored from the first version) ───────────────────────
sales = fdf[fdf['IS_SALE']]
gross   = fdf['REVENUE'].sum()
rtn_amt = fdf['RTN_AMT'].sum()
net     = gross - rtn_amt
units   = fdf['SALE_QTY'].sum()
rtn_qty = fdf['RTN_QTY2'].sum()
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

# ── Plotly light theme helper ─────────────────────────────────────────────────
def light_fig(fig, height=215):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=14, t=14, b=44), height=height, showlegend=False,
        font=dict(family="Inter", color=TEXT_SEC, size=10),
        hoverlabel=dict(bgcolor="#ffffff", font_color=TEXT_PRI, font_size=11, bordercolor=BORDER),
    )
    fig.update_xaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(color=TEXT_SEC, size=9))
    fig.update_yaxes(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(color=TEXT_SEC, size=9))
    return fig

def top_n_df(dim, n):
    g = fdf.groupby(dim, dropna=True)[meas_col].sum().reset_index()
    key = g[dim].astype(str).str.strip()
    g = g[key.ne('') & ~key.str.lower().isin(['nan', 'na', 'none'])]
    return g.sort_values(meas_col, ascending=False).head(n)

def card_title(icon, title):
    st.markdown(
        f'<div class="chart-title">{icon} Top {top_n} {title}'
        f'<span class="chart-meas">{meas_label}</span></div>',
        unsafe_allow_html=True)

def vbar(col, dim, title, icon, color, key):
    g = top_n_df(dim, top_n)
    fig = go.Figure(go.Bar(
        x=g[dim], y=g[meas_col], marker_color=color,
        hovertemplate="<b>%{x}</b><br>"+meas_label+": %{y:,.0f}<extra></extra>"))
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=8))
    fig.update_yaxes(tickformat=",")
    with col.container(border=True):
        card_title(icon, title)
        st.plotly_chart(light_fig(fig), use_container_width=True, key=key)

def hbar(col, dim, title, icon, color, key):
    g = top_n_df(dim, top_n)
    fig = go.Figure(go.Bar(
        y=g[dim], x=g[meas_col], orientation='h', marker_color=color,
        hovertemplate="<b>%{y}</b><br>"+meas_label+": %{x:,.0f}<extra></extra>"))
    fig.update_yaxes(autorange='reversed', tickfont=dict(size=9))
    fig.update_xaxes(tickformat=",")
    with col.container(border=True):
        card_title(icon, title)
        st.plotly_chart(light_fig(fig), use_container_width=True, key=key)

def lchart(col, dim, title, icon, color, key):
    g = top_n_df(dim, top_n)
    fig = go.Figure(go.Scatter(
        x=g[dim], y=g[meas_col], mode='lines+markers',
        line=dict(color=color, width=2.5, shape='spline'),
        marker=dict(size=6, color=color),
        fill='tozeroy', fillcolor='rgba(124,111,212,0.12)',
        hovertemplate="<b>%{x}</b><br>"+meas_label+": %{y:,.0f}<extra></extra>"))
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=8))
    fig.update_yaxes(tickformat=",")
    with col.container(border=True):
        card_title(icon, title)
        st.plotly_chart(light_fig(fig), use_container_width=True, key=key)

# ── Row 1: vertical bar · horizontal bar · line ───────────────────────────────
r1a, r1b, r1c = st.columns(3)
vbar(r1a,  'ITEM',  'Products', '📦', ACCENT,  'c_prod')
hbar(r1b,  'BRAND', 'Brands',   '🏷️', ACCENT3, 'c_brand')
lchart(r1c,'STYLE', 'Styles',   '✂️', ACCENT5, 'c_style')

# ── Row 2: vertical bar · horizontal bar · line ───────────────────────────────
r2a, r2b, r2c = st.columns(3)
vbar(r2a,  'SHADE',     'Shades',    '🎨', ACCENT2, 'c_shade')
hbar(r2b,  'SIZE_NAME', 'Sizes',     '📐', ACCENT6, 'c_size')
lchart(r2c,'SUPPLIER',  'Suppliers', '🚚', ACCENT4, 'c_supp')
