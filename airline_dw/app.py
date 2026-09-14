import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Airline Intelligence Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLORS
# =========================================================

NAVY = "#0B1220"
BLUE = "#2563EB"
CYAN = "#06B6D4"
PURPLE = "#6366F1"
ORANGE = "#F59E0B"
GREEN = "#14B8A6"
RED = "#EF4444"
YELLOW = "#F59E0B"

MULTI_COLORS = [
    BLUE,
    CYAN,
    PURPLE,
    ORANGE,
    GREEN,
    RED
]


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

:root {
    --ink:#081225;
    --muted:#64748B;
    --line:#E6ECF5;
    --blue:#2563EB;
    --sky:#0EA5E9;
    --cyan:#06B6D4;
    --navy:#071426;
    --navy2:#102B5A;
    --purple:#6D5DFB;
    --teal:#14B8A6;
    --orange:#F97316;
}

* { box-sizing: border-box; }

.stApp {
    background:
        radial-gradient(circle at 14% -8%, rgba(37,99,235,.13), transparent 27%),
        radial-gradient(circle at 95% 3%, rgba(6,182,212,.10), transparent 23%),
        linear-gradient(180deg,#F5F9FF 0%,#F8FBFF 46%,#F4F7FB 100%);
    color:var(--ink);
}

.stApp::before {
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    opacity:.20;
    background-image:radial-gradient(rgba(37,99,235,.12) 1px, transparent 1px);
    background-size:28px 28px;
    mask-image:linear-gradient(to bottom,black,transparent 76%);
}

.block-container {
    max-width:1510px;
    padding-top:.8rem;
    padding-bottom:2.8rem;
}
header[data-testid="stHeader"] { background:transparent; }
#MainMenu, footer { visibility:hidden; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 22% 2%,rgba(20,184,166,.14),transparent 21%),
        radial-gradient(circle at 90% 22%,rgba(37,99,235,.22),transparent 34%),
        linear-gradient(180deg,#061223 0%,#0A1D3D 57%,#10285A 100%);
    border-right:1px solid rgba(255,255,255,.08);
    box-shadow:16px 0 40px rgba(8,18,37,.08);
}
section[data-testid="stSidebar"] > div { padding-top:.65rem; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#F8FAFC!important; }

.side-brand {
    display:flex;align-items:center;gap:12px;
    padding:7px 3px 16px 3px;
    border-bottom:1px solid rgba(255,255,255,.09);
    margin-bottom:14px;
}
.side-logo {
    width:44px;height:44px;border-radius:15px;
    display:grid;place-items:center;font-size:24px;
    background:linear-gradient(145deg,#0EA5E9,#2563EB 55%,#06B6D4);
    box-shadow:0 12px 30px rgba(14,165,233,.28),inset 0 1px 0 rgba(255,255,255,.3);
}
.side-brand-title { color:white;font-weight:900;letter-spacing:.4px;font-size:18px;line-height:1.05; }
.side-brand-sub { color:#93C5FD;font-size:11px;margin-top:4px; }

.sidebar-kicker {
    display:inline-flex;align-items:center;gap:7px;
    padding:7px 11px;border-radius:999px;
    background:rgba(6,182,212,.12);border:1px solid rgba(103,232,249,.24);
    color:#A5F3FC;font-size:10px;font-weight:850;letter-spacing:1.15px;margin:0 0 8px 0;
}
.sidebar-kicker::before {
    content:"";width:7px;height:7px;border-radius:50%;background:#22D3EE;
    box-shadow:0 0 0 5px rgba(34,211,238,.12),0 0 18px rgba(34,211,238,.8);
}
section[data-testid="stSidebar"] input {
    color:#0F172A!important;-webkit-text-fill-color:#0F172A!important;background:#fff!important;
}
section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background:#fff!important;border:1px solid rgba(148,163,184,.25)!important;border-radius:13px!important;
    min-height:44px;box-shadow:0 8px 20px rgba(2,6,23,.16);
}
section[data-testid="stSidebar"] div[data-baseweb="select"] span { color:#0F172A!important; }

/* HERO */
.hero {
    position:relative;overflow:hidden;
    min-height:335px;
    border-radius:30px;
    padding:39px 42px 34px 42px;
    background:
      radial-gradient(circle at 79% 36%,rgba(34,211,238,.26),transparent 18%),
      radial-gradient(circle at 62% 120%,rgba(37,99,235,.55),transparent 42%),
      linear-gradient(118deg,#071326 0%,#0D2A67 49%,#1156D8 76%,#0EA5E9 125%);
    box-shadow:0 28px 64px rgba(37,99,235,.20),inset 0 1px 0 rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.13);
    margin-bottom:14px;
}
.hero::before {
    content:"";position:absolute;right:-20px;top:-80px;width:520px;height:420px;opacity:.42;
    background-image:
      radial-gradient(circle at 12% 24%,rgba(255,255,255,.95) 0 3px,transparent 4px),
      radial-gradient(circle at 34% 61%,rgba(103,232,249,.95) 0 4px,transparent 5px),
      radial-gradient(circle at 59% 35%,rgba(255,255,255,.92) 0 3px,transparent 4px),
      radial-gradient(circle at 80% 68%,rgba(103,232,249,.95) 0 4px,transparent 5px);
}
.hero::after {
    content:"";position:absolute;right:-62px;top:-92px;width:305px;height:305px;border-radius:50%;
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 0 0 38px rgba(255,255,255,.035),0 0 0 78px rgba(255,255,255,.018);
}
.hero-grid { display:grid;grid-template-columns:1.18fr .82fr;gap:18px;position:relative;z-index:2; }
.hero-kicker { display:flex;align-items:center;gap:9px;color:#BAE6FD;font-size:11px;font-weight:850;letter-spacing:1.22px;margin-bottom:13px; }
.hero-dot { width:9px;height:9px;border-radius:50%;background:#22D3EE;box-shadow:0 0 0 5px rgba(34,211,238,.13),0 0 20px rgba(34,211,238,.75); }
.hero-title { color:#fff;font-size:clamp(40px,4.2vw,58px);font-weight:900;line-height:1.0;letter-spacing:-1.8px;margin-bottom:14px; }
.hero-accent { background:linear-gradient(90deg,#67E8F9,#7DD3FC);-webkit-background-clip:text;background-clip:text;color:transparent; }
.hero-sub { color:#D9E9FF;font-size:15px;line-height:1.75;max-width:740px; }
.hero-tech { display:flex;flex-wrap:wrap;gap:8px;margin-top:21px; }
.hero-chip { padding:8px 12px;border-radius:999px;color:#E0F2FE;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.13);font-size:11px;font-weight:750;backdrop-filter:blur(8px); }
.hero-art { position:relative;min-height:245px;display:flex;align-items:center;justify-content:center;overflow:visible; }
.hero-map { position:absolute;inset:7% 1% 8% 1%;opacity:.48;z-index:0; }
.hero-map svg { width:100%;height:100%;display:block; }
.hero-plane {
    position:relative;z-index:4;width:min(95%,560px);
    filter:drop-shadow(0 24px 22px rgba(2,6,23,.28)) drop-shadow(0 0 18px rgba(56,189,248,.20));
    animation:floatPlane 5s ease-in-out infinite;transform-origin:center;
}
.hero-plane svg { width:100%;height:auto;display:block;overflow:visible; }
@keyframes floatPlane {
    0%,100%{transform:translate3d(0,0,0) rotate(-2deg)}
    50%{transform:translate3d(0,-8px,0) rotate(0deg)}
}
.route-line { position:absolute;width:88%;height:56%;border:1.8px solid rgba(103,232,249,.58);border-color:rgba(103,232,249,.68) transparent transparent transparent;border-radius:50%;transform:rotate(-12deg);z-index:1;filter:drop-shadow(0 0 4px rgba(34,211,238,.42)); }
.route-line.r2 { width:72%;height:42%;transform:rotate(15deg);top:36%;left:13%;opacity:.72; }
.route-line.r3 { width:58%;height:30%;transform:rotate(-27deg);top:26%;left:23%;opacity:.5; }
.route-dot { position:absolute;width:8px;height:8px;border-radius:50%;background:#fff;z-index:2;box-shadow:0 0 0 5px rgba(103,232,249,.14),0 0 19px rgba(103,232,249,1); }
.route-dot.d1{left:8%;top:60%}.route-dot.d2{right:7%;top:25%}.route-dot.d3{right:15%;bottom:17%}.route-dot.d4{left:38%;top:18%}
.hero-mini {
    position:absolute;right:5%;bottom:3%;padding:12px 14px;border-radius:16px;
    background:rgba(6,24,60,.44);border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(9px);
    color:#DFF6FF;font-size:11px;line-height:1.55;box-shadow:0 12px 32px rgba(0,0,0,.12);
}
.hero-mini b { color:white;font-size:17px; }

.status-strip { display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin:7px 0 18px 0; }
.status-left,.status-right { display:flex;gap:8px;flex-wrap:wrap; }
.status-pill { display:inline-flex;align-items:center;gap:7px;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.85);border:1px solid #E2E8F0;color:#475569;font-size:11px;font-weight:750;box-shadow:0 8px 20px rgba(15,23,42,.045); }
.status-live::before { content:"";width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 0 5px rgba(34,197,94,.11); }

/* KPI CARDS */
.kpi-grid { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:2px 0 12px 0; }
.kpi-card { position:relative;overflow:hidden;border-radius:22px;padding:20px 21px 18px;color:white;min-height:154px;box-shadow:0 18px 38px rgba(15,23,42,.12);transition:.2s ease; }
.kpi-card:hover { transform:translateY(-4px);box-shadow:0 24px 48px rgba(37,99,235,.18); }
.kpi-blue{background:linear-gradient(135deg,#2563EB,#0EA5E9 68%,#22D3EE)}
.kpi-teal{background:linear-gradient(135deg,#0F9F95,#14B8A6 56%,#22D3EE)}
.kpi-purple{background:linear-gradient(135deg,#5B4CF0,#7C5CFC 58%,#8B5CF6)}
.kpi-orange{background:linear-gradient(135deg,#EA7000,#F97316 58%,#F59E0B)}
.kpi-icon { width:43px;height:43px;border-radius:15px;display:grid;place-items:center;font-size:21px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);box-shadow:inset 0 1px 0 rgba(255,255,255,.18); }
.kpi-label { position:absolute;left:77px;top:20px;font-size:13px;font-weight:800;color:#F8FAFC; }
.kpi-sub { position:absolute;left:77px;top:40px;font-size:10px;color:rgba(255,255,255,.78); }
.kpi-value { font-size:34px;font-weight:900;letter-spacing:-1px;margin-top:19px; }
.kpi-note { margin-top:7px;font-size:10px;color:rgba(255,255,255,.78); }
.kpi-wave { position:absolute;right:-5px;bottom:10px;font-size:34px;opacity:.68;letter-spacing:-10px;transform:rotate(-8deg); }

/* INSIGHTS */
.insight-panel { background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(248,251,255,.96));border:1px solid #E4EAF3;border-radius:22px;padding:17px 17px 15px;margin:14px 0 18px;box-shadow:0 12px 30px rgba(15,23,42,.055); }
.insight-head { display:flex;align-items:center;gap:9px;font-size:18px;font-weight:900;color:#0F2A62;margin-bottom:12px; }
.insight-head small { font-size:11px;color:#64748B;font-weight:650; }
.insight-grid { display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:11px; }
.insight-mini { background:#fff;border:1px solid #E6EDF7;border-radius:17px;padding:14px;min-height:110px;transition:.18s ease;position:relative;overflow:hidden; }
.insight-mini:hover { transform:translateY(-2px);border-color:#BFDBFE;box-shadow:0 12px 24px rgba(37,99,235,.08); }
.insight-mini::after { content:"";position:absolute;width:70px;height:70px;right:-25px;top:-30px;border-radius:50%;background:rgba(37,99,235,.055); }
.insight-icon { font-size:20px;margin-bottom:6px; }
.insight-label { color:#64748B;font-size:10px;font-weight:750; }
.insight-value { color:#102A66;font-size:20px;font-weight:900;margin-top:5px;letter-spacing:-.35px; }
.insight-detail { color:#2563EB;font-size:11px;font-weight:800;margin-top:4px; }

/* CHART / TABS / GENERAL */
.section-title { font-size:30px;font-weight:900;letter-spacing:-.7px;color:#0B1831;margin-top:8px;margin-bottom:3px; }
.section-desc { color:#64748B;font-size:14px;margin-bottom:18px; }
.question { display:inline-flex;align-items:center;padding:5px 9px;border-radius:999px;background:linear-gradient(135deg,#EFF6FF,#ECFEFF);border:1px solid #CDE8FF;color:#1D4ED8;font-size:10px;font-weight:850;letter-spacing:.55px;margin-bottom:5px; }
.insight { position:relative;background:linear-gradient(120deg,#ECFEFF,#EFF6FF);border:1px solid #CFFAFE;border-radius:16px;padding:14px 17px 14px 20px;margin:8px 0 18px;color:#164E63;box-shadow:0 8px 22px rgba(6,182,212,.06); }
.insight::before { content:"";position:absolute;left:0;top:13px;bottom:13px;width:4px;border-radius:999px;background:linear-gradient(180deg,#06B6D4,#2563EB); }
div[data-testid="stPlotlyChart"] { background:rgba(255,255,255,.97);border:1px solid #E5EAF2;border-radius:22px;padding:9px;box-shadow:0 12px 28px rgba(15,23,42,.055);transition:.18s ease; }
div[data-testid="stPlotlyChart"]:hover { box-shadow:0 16px 34px rgba(37,99,235,.08); }
div[data-testid="stDataFrame"] { border:1px solid #E2E8F0;border-radius:17px;overflow:hidden;box-shadow:0 8px 20px rgba(15,23,42,.04); }
div[data-baseweb="tab-list"] { gap:5px;background:rgba(255,255,255,.88);border:1px solid #E5EAF2;border-radius:18px;padding:7px;box-shadow:0 10px 26px rgba(15,23,42,.05); }
button[data-baseweb="tab"] { height:46px;border-radius:13px;padding-left:17px!important;padding-right:17px!important;color:#64748B;font-size:13px;font-weight:780; }
button[data-baseweb="tab"][aria-selected="true"] { background:linear-gradient(135deg,#2563EB,#0EA5E9);color:#fff!important;box-shadow:0 8px 20px rgba(37,99,235,.19); }
div[data-baseweb="tab-highlight"] { display:none; }
.stDownloadButton button,.stButton button { border-radius:12px;border:1px solid #BFDBFE;background:linear-gradient(135deg,#EFF6FF,#ECFEFF);color:#155E75;font-weight:780;min-height:42px;transition:.16s ease; }
.stDownloadButton button:hover,.stButton button:hover { transform:translateY(-1px);border-color:#7DD3FC;box-shadow:0 8px 18px rgba(14,165,233,.10); }

.footer-premium { margin-top:24px;padding:15px 18px;border-radius:18px;background:linear-gradient(135deg,#071426,#0E2A59);color:#BFD8FF;display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap;font-size:11px;box-shadow:0 14px 30px rgba(15,23,42,.08); }
.footer-premium b { color:#fff; }
.footer-ready { display:flex;align-items:center;gap:7px;color:#D1FAE5;font-weight:800; }
.footer-ready::before { content:"";width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 0 5px rgba(34,197,94,.11); }

@media(max-width:1100px){ .kpi-grid,.insight-grid{grid-template-columns:repeat(2,1fr)} .hero-grid{grid-template-columns:1fr}.hero-art{display:none}.hero{min-height:auto} }
@media(max-width:720px){ .kpi-grid,.insight-grid{grid-template-columns:1fr}.hero{padding:28px 24px;border-radius:23px}.hero-title{font-size:39px}.block-container{padding-left:1rem;padding-right:1rem} }
</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

DB_PATH = Path(__file__).resolve().parent / "dev.duckdb"

con = duckdb.connect(
    str(DB_PATH),
    read_only=True
)


def query_df(sql, params=None):
    if params is None:
        params = []

    return con.execute(
        sql,
        params
    ).fetchdf()


def compact_number(value):
    value = float(value or 0)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f} B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.2f} M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:,.2f} K"

    return f"{value:,.2f}"


def style_chart(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(
            l=22,
            r=22,
            t=34,
            b=22
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            color="#334155",
            size=12,
            family="Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_color="white",
            bordercolor="rgba(255,255,255,.14)"
        ),
        hovermode="closest"
    )

    fig.update_xaxes(
        gridcolor="#EDF2F7",
        linecolor="#DCE4EE",
        tickcolor="#DCE4EE",
        zeroline=False,
        showline=False
    )

    fig.update_yaxes(
        gridcolor="#EDF2F7",
        linecolor="#DCE4EE",
        tickcolor="#DCE4EE",
        zeroline=False,
        showline=False
    )

    return fig


def display_chart(fig):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# HERO
# =========================================================

hero_html = """
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="hero-kicker"><span class="hero-dot"></span>AIRLINE DATA WAREHOUSE • ANALYTICS EXPERIENCE</div>
      <div class="hero-title">Airline <span class="hero-accent">Intelligence</span><br>Dashboard</div>
      <div class="hero-sub">วิเคราะห์ยอดขายตั๋ว เส้นทางบิน เครื่องบิน และประสิทธิภาพการดำเนินงาน จาก Data Warehouse ในมุมมองเดียว พร้อมตัวกรองแบบ Interactive</div>
      <div class="hero-tech">
        <span class="hero-chip">◉ DuckDB</span>
        <span class="hero-chip">◆ dbt</span>
        <span class="hero-chip">▦ Streamlit</span>
        <span class="hero-chip">◈ Plotly</span>
      </div>
    </div>
    <div class="hero-art">
      <div class="hero-map" aria-hidden="true">
        <svg viewBox="0 0 620 280" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g fill="#7DD3FC" opacity=".55">
            <circle cx="70" cy="72" r="2"/><circle cx="88" cy="66" r="2"/><circle cx="103" cy="80" r="2"/><circle cx="124" cy="74" r="2"/><circle cx="142" cy="89" r="2"/>
            <circle cx="170" cy="66" r="2"/><circle cx="190" cy="77" r="2"/><circle cx="210" cy="70" r="2"/><circle cx="235" cy="85" r="2"/><circle cx="255" cy="72" r="2"/>
            <circle cx="287" cy="83" r="2"/><circle cx="310" cy="70" r="2"/><circle cx="332" cy="90" r="2"/><circle cx="360" cy="79" r="2"/><circle cx="386" cy="92" r="2"/>
            <circle cx="414" cy="79" r="2"/><circle cx="442" cy="92" r="2"/><circle cx="470" cy="82" r="2"/><circle cx="500" cy="101" r="2"/><circle cx="530" cy="92" r="2"/>
            <circle cx="105" cy="118" r="2"/><circle cx="132" cy="128" r="2"/><circle cx="155" cy="115" r="2"/><circle cx="181" cy="135" r="2"/><circle cx="208" cy="123" r="2"/>
            <circle cx="250" cy="133" r="2"/><circle cx="282" cy="118" r="2"/><circle cx="315" cy="138" r="2"/><circle cx="350" cy="125" r="2"/><circle cx="385" cy="141" r="2"/>
            <circle cx="420" cy="126" r="2"/><circle cx="455" cy="145" r="2"/><circle cx="492" cy="130" r="2"/><circle cx="525" cy="148" r="2"/>
            <circle cx="150" cy="170" r="2"/><circle cx="185" cy="182" r="2"/><circle cx="220" cy="168" r="2"/><circle cx="255" cy="190" r="2"/><circle cx="295" cy="175" r="2"/>
            <circle cx="340" cy="188" r="2"/><circle cx="380" cy="172" r="2"/><circle cx="420" cy="194" r="2"/><circle cx="463" cy="178" r="2"/>
          </g>
        </svg>
      </div>
      <div class="route-line"></div><div class="route-line r2"></div><div class="route-line r3"></div>
      <span class="route-dot d1"></span><span class="route-dot d2"></span><span class="route-dot d3"></span><span class="route-dot d4"></span>
      <div class="hero-plane" aria-label="airliner illustration">
        <svg viewBox="0 0 760 360" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="bodyG" x1="110" y1="140" x2="650" y2="240" gradientUnits="userSpaceOnUse">
              <stop offset="0" stop-color="#EAF7FF"/><stop offset=".48" stop-color="#FFFFFF"/><stop offset=".72" stop-color="#D9EAF7"/><stop offset="1" stop-color="#BFD5E8"/>
            </linearGradient>
            <linearGradient id="wingG" x1="250" y1="120" x2="470" y2="310" gradientUnits="userSpaceOnUse">
              <stop stop-color="#DCEEFF"/><stop offset="1" stop-color="#8DB8D7"/>
            </linearGradient>
            <linearGradient id="blueG" x1="280" y1="120" x2="610" y2="240" gradientUnits="userSpaceOnUse">
              <stop stop-color="#0EA5E9"/><stop offset="1" stop-color="#1D4ED8"/>
            </linearGradient>
            <radialGradient id="engineG" cx="50%" cy="45%" r="55%">
              <stop offset="0" stop-color="#0B1220"/><stop offset=".55" stop-color="#1F3B5B"/><stop offset="1" stop-color="#A7C7DE"/>
            </radialGradient>
          </defs>
          <g transform="translate(8 0) rotate(-7 380 180)">
            <path d="M108 195 C190 178 300 164 520 150 C594 145 656 153 692 168 C709 175 709 188 692 194 C646 211 570 218 481 220 L168 220 C130 220 102 211 90 203 C85 199 91 197 108 195Z" fill="url(#bodyG)" stroke="#D5E8F6" stroke-width="2"/>
            <path d="M541 151 C590 150 635 156 684 169 C665 172 643 177 621 182 C594 176 568 170 535 167Z" fill="#E9F6FF" opacity=".95"/>
            <path d="M187 186 L360 74 C375 64 389 64 398 69 L316 181Z" fill="url(#wingG)" stroke="#C7DDEA" stroke-width="2"/>
            <path d="M305 220 L470 304 C485 312 496 311 506 305 L388 216Z" fill="url(#wingG)" stroke="#C7DDEA" stroke-width="2"/>
            <path d="M142 195 L84 153 C77 148 73 149 69 152 L91 198Z" fill="#C9E2F3"/>
            <path d="M151 199 L101 234 C95 239 91 239 87 236 L103 204Z" fill="#BDD8EC"/>
            <path d="M168 197 C286 181 432 170 608 164" fill="none" stroke="url(#blueG)" stroke-width="8" stroke-linecap="round" opacity=".95"/>
            <path d="M640 165 C654 167 671 171 685 177" fill="none" stroke="#0B4C9C" stroke-width="5" stroke-linecap="round"/>
            <g fill="#17466E" opacity=".95">
              <rect x="282" y="176" width="14" height="6" rx="3"/><rect x="303" y="173" width="14" height="6" rx="3"/><rect x="324" y="171" width="14" height="6" rx="3"/>
              <rect x="345" y="169" width="14" height="6" rx="3"/><rect x="366" y="167" width="14" height="6" rx="3"/><rect x="387" y="165" width="14" height="6" rx="3"/>
              <rect x="408" y="163" width="14" height="6" rx="3"/><rect x="429" y="161" width="14" height="6" rx="3"/><rect x="450" y="160" width="14" height="6" rx="3"/>
              <rect x="471" y="158" width="14" height="6" rx="3"/><rect x="492" y="157" width="14" height="6" rx="3"/>
            </g>
            <path d="M612 160 C635 158 657 160 673 166 C659 167 645 171 631 177 C622 173 614 168 612 160Z" fill="#0A2945"/>
            <g transform="translate(298 187)">
              <ellipse cx="0" cy="0" rx="31" ry="24" fill="#D7EAF6" stroke="#C2DCEB" stroke-width="2"/>
              <ellipse cx="3" cy="1" rx="21" ry="17" fill="url(#engineG)"/>
              <ellipse cx="6" cy="1" rx="8" ry="8" fill="#0B1220"/>
            </g>
            <g transform="translate(424 217) scale(.95)">
              <ellipse cx="0" cy="0" rx="31" ry="24" fill="#D7EAF6" stroke="#C2DCEB" stroke-width="2"/>
              <ellipse cx="3" cy="1" rx="21" ry="17" fill="url(#engineG)"/>
              <ellipse cx="6" cy="1" rx="8" ry="8" fill="#0B1220"/>
            </g>
            <path d="M175 185 L207 107 C212 96 220 92 228 93 L246 179Z" fill="#BFD8EC" stroke="#AFCDE2" stroke-width="2"/>
            <path d="M201 106 L222 100 L238 177 L216 180Z" fill="#1D4ED8" opacity=".9"/>
            <path d="M119 199 C183 206 243 207 305 204" fill="none" stroke="#FFFFFF" stroke-width="3" opacity=".75"/>
          </g>
        </svg>
      </div>
      <div class="hero-mini"><b>15</b> Business Questions<br><b>3</b> Fact Tables &nbsp; • &nbsp; <b>5</b> Dimensions</div>
    </div>
  </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

st.markdown(
    """
    <div class="status-strip">
      <div class="status-left">
        <span class="status-pill">🗄️ Direct <b>DuckDB</b> Connection</span>
        <span class="status-pill">⚙️ Built with dbt + Streamlit + Plotly</span>
      </div>
      <div class="status-right">
        <span class="status-pill status-live">Warehouse Ready</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATE RANGE
# =========================================================

date_row = con.execute(
    """
    SELECT
        MIN(full_date),
        MAX(full_date)
    FROM dim_date
    """
).fetchone()

min_date = pd.to_datetime(
    date_row[0]
).date()

max_date = pd.to_datetime(
    date_row[1]
).date()


# =========================================================
# SIDEBAR — CASCADING FILTERS
# =========================================================

st.sidebar.markdown(
    """
    <div class="side-brand">
      <div class="side-logo">✈</div>
      <div><div class="side-brand-title">AIRLINE DW</div><div class="side-brand-sub">Flight Data Analytics</div></div>
    </div>
    <div class="sidebar-kicker">CONTROL CENTER</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title(
    "ตัวกรองข้อมูล"
)

st.sidebar.caption(
    "เลือกเงื่อนไขเพื่อสำรวจข้อมูลแบบ Interactive — ตัวเลือกจะปรับตามข้อมูลที่มีอยู่จริง"
)


# DATE

date_selection = st.sidebar.date_input(
    "ช่วงวันที่",
    value=(
        min_date,
        max_date
    ),
    min_value=min_date,
    max_value=max_date
)


if (
    isinstance(
        date_selection,
        (tuple, list)
    )
    and len(date_selection) == 2
):
    start_date = date_selection[0]
    end_date = date_selection[1]

else:
    start_date = min_date
    end_date = max_date


# =========================================================
# DEPARTURE
# =========================================================

departure_options = query_df(
    """
    SELECT DISTINCT
        dep.airport_code

    FROM fact_ticket_sales f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    WHERE
        d.full_date BETWEEN ? AND ?

    ORDER BY
        dep.airport_code
    """,
    [
        start_date,
        end_date
    ]
)["airport_code"].tolist()


departure = st.sidebar.selectbox(
    "สนามบินต้นทาง",
    ["ทั้งหมด"] + departure_options
)


# =========================================================
# ARRIVAL
# =========================================================

arrival_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

arrival_params = [
    start_date,
    end_date
]


if departure != "ทั้งหมด":
    arrival_conditions.append(
        "dep.airport_code = ?"
    )

    arrival_params.append(
        departure
    )


arrival_where = " AND ".join(
    arrival_conditions
)


arrival_options = query_df(
    f"""
    SELECT DISTINCT
        arr.airport_code

    FROM fact_ticket_sales f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    WHERE
        {arrival_where}

    ORDER BY
        arr.airport_code
    """,
    arrival_params
)["airport_code"].tolist()


arrival = st.sidebar.selectbox(
    "สนามบินปลายทาง",
    ["ทั้งหมด"] + arrival_options
)


# =========================================================
# FARE CLASS
# =========================================================

fare_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

fare_params = [
    start_date,
    end_date
]


if departure != "ทั้งหมด":
    fare_conditions.append(
        "dep.airport_code = ?"
    )
    fare_params.append(
        departure
    )


if arrival != "ทั้งหมด":
    fare_conditions.append(
        "arr.airport_code = ?"
    )
    fare_params.append(
        arrival
    )


fare_where = " AND ".join(
    fare_conditions
)


fare_options = query_df(
    f"""
    SELECT DISTINCT
        fc.fare_class

    FROM fact_ticket_sales f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    JOIN dim_fare_class fc
        ON f.fare_class_key = fc.fare_class_key

    WHERE
        {fare_where}

    ORDER BY
        fc.fare_class
    """,
    fare_params
)["fare_class"].tolist()


fare = st.sidebar.selectbox(
    "ชั้นโดยสาร",
    ["ทั้งหมด"] + fare_options
)


# =========================================================
# AIRCRAFT
# =========================================================

aircraft_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

aircraft_params = [
    start_date,
    end_date
]


if departure != "ทั้งหมด":
    aircraft_conditions.append(
        "dep.airport_code = ?"
    )
    aircraft_params.append(
        departure
    )


if arrival != "ทั้งหมด":
    aircraft_conditions.append(
        "arr.airport_code = ?"
    )
    aircraft_params.append(
        arrival
    )


if fare != "ทั้งหมด":
    aircraft_conditions.append(
        "fc.fare_class = ?"
    )
    aircraft_params.append(
        fare
    )


aircraft_where = " AND ".join(
    aircraft_conditions
)


aircraft_options = query_df(
    f"""
    SELECT DISTINCT
        a.model

    FROM fact_ticket_sales f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    JOIN dim_fare_class fc
        ON f.fare_class_key = fc.fare_class_key

    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key

    WHERE
        {aircraft_where}

    ORDER BY
        a.model
    """,
    aircraft_params
)["model"].tolist()


aircraft = st.sidebar.selectbox(
    "รุ่นเครื่องบิน",
    ["ทั้งหมด"] + aircraft_options
)


st.sidebar.divider()

st.sidebar.caption(
    f"ข้อมูลตั้งแต่ "
    f"{min_date.strftime('%d/%m/%Y')} "
    f"ถึง "
    f"{max_date.strftime('%d/%m/%Y')}"
)




active_filter_count = sum([
    departure != "ทั้งหมด",
    arrival != "ทั้งหมด",
    fare != "ทั้งหมด",
    aircraft != "ทั้งหมด",
    start_date != min_date or end_date != max_date,
])

st.sidebar.markdown(
    f"""
    <div style="margin-top:12px;padding:13px 14px;border-radius:16px;
                background:rgba(6,182,212,.10);border:1px solid rgba(103,232,249,.20);
                box-shadow:0 10px 25px rgba(2,6,23,.12);">
      <div style="display:flex;align-items:center;gap:8px;color:#D1FAE5;font-weight:850;font-size:12px;">
        <span style="width:9px;height:9px;border-radius:50%;background:#22C55E;box-shadow:0 0 0 5px rgba(34,197,94,.12);"></span> Filters Active
      </div>
      <div style="color:#BAE6FD;font-size:11px;margin-top:7px;">{active_filter_count} filter(s) applied</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SALES FILTER
# =========================================================

sales_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

sales_params = [
    start_date,
    end_date
]


if departure != "ทั้งหมด":
    sales_conditions.append(
        "dep.airport_code = ?"
    )
    sales_params.append(
        departure
    )


if arrival != "ทั้งหมด":
    sales_conditions.append(
        "arr.airport_code = ?"
    )
    sales_params.append(
        arrival
    )


if fare != "ทั้งหมด":
    sales_conditions.append(
        "fc.fare_class = ?"
    )
    sales_params.append(
        fare
    )


if aircraft != "ทั้งหมด":
    sales_conditions.append(
        "a.model = ?"
    )
    sales_params.append(
        aircraft
    )


sales_where = " AND ".join(
    sales_conditions
)


# =========================================================
# OPERATIONS FILTER
# =========================================================

ops_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

ops_params = [
    start_date,
    end_date
]


if departure != "ทั้งหมด":
    ops_conditions.append(
        "dep.airport_code = ?"
    )
    ops_params.append(
        departure
    )


if arrival != "ทั้งหมด":
    ops_conditions.append(
        "arr.airport_code = ?"
    )
    ops_params.append(
        arrival
    )


if aircraft != "ทั้งหมด":
    ops_conditions.append(
        "a.model = ?"
    )
    ops_params.append(
        aircraft
    )


ops_where = " AND ".join(
    ops_conditions
)


# =========================================================
# SEAT FILTER
# =========================================================

seat_conditions = []
seat_params = []


if fare != "ทั้งหมด":
    seat_conditions.append(
        "fc.fare_class = ?"
    )
    seat_params.append(
        fare
    )


if aircraft != "ทั้งหมด":
    seat_conditions.append(
        "a.model = ?"
    )
    seat_params.append(
        aircraft
    )


seat_where = ""


if seat_conditions:
    seat_where = (
        "WHERE "
        + " AND ".join(
            seat_conditions
        )
    )


# =========================================================
# KPI DATA — Q1 / Q2
# =========================================================

sales_kpi = con.execute(
    f"""
    SELECT
        COALESCE(
            SUM(f.amount),
            0
        ) AS total_sales,

        COALESCE(
            SUM(f.ticket_flight_count),
            0
        ) AS total_ticket_flights

    FROM fact_ticket_sales f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    JOIN dim_fare_class fc
        ON f.fare_class_key = fc.fare_class_key

    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key

    WHERE
        {sales_where}
    """,
    sales_params
).fetchone()


ops_kpi = con.execute(
    f"""
    SELECT
        COALESCE(
            SUM(f.flight_count),
            0
        ) AS total_flights,

        COALESCE(
            AVG(
                CASE
                    WHEN
                        f.departure_delay_minutes > 0
                    THEN
                        f.departure_delay_minutes
                END
            ),
            0
        ) AS avg_delay

    FROM fact_flight_operations f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key

    WHERE
        {ops_where}
    """,
    ops_params
).fetchone()


# =========================================================
# KPI DISPLAY — PREMIUM CARDS
# =========================================================

# Small executive insight queries that reuse the active filters
_top_route = query_df(
    f"""
    SELECT dep.airport_code || ' → ' || arr.airport_code AS route,
           SUM(f.ticket_flight_count) AS ticket_flights,
           SUM(f.amount) AS total_sales
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    GROUP BY dep.airport_code, arr.airport_code
    ORDER BY ticket_flights DESC
    LIMIT 1
    """,
    sales_params,
)

_top_sales_route = query_df(
    f"""
    SELECT dep.airport_code || ' → ' || arr.airport_code AS route,
           SUM(f.amount) AS total_sales
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    GROUP BY dep.airport_code, arr.airport_code
    ORDER BY total_sales DESC
    LIMIT 1
    """,
    sales_params,
)

_top_fare = query_df(
    f"""
    SELECT fc.fare_class, SUM(f.amount) AS total_sales
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    GROUP BY fc.fare_class
    ORDER BY total_sales DESC
    LIMIT 1
    """,
    sales_params,
)

_top_airport = query_df(
    f"""
    SELECT dep.airport_code, SUM(f.ticket_flight_count) AS ticket_flights
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    GROUP BY dep.airport_code
    ORDER BY ticket_flights DESC
    LIMIT 1
    """,
    sales_params,
)

kpi_html = f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-blue">
    <div class="kpi-icon">◉</div><div class="kpi-label">ยอดขายตั๋วรวม</div><div class="kpi-sub">TOTAL SALES</div>
    <div class="kpi-value">{compact_number(sales_kpi[0])}</div><div class="kpi-note">Filtered executive revenue</div><div class="kpi-wave">⌁⌁⌁</div>
  </div>
  <div class="kpi-card kpi-teal">
    <div class="kpi-icon">🎫</div><div class="kpi-label">จำนวน Ticket Flight</div><div class="kpi-sub">TICKET FLIGHT COUNT</div>
    <div class="kpi-value">{sales_kpi[1]:,.0f}</div><div class="kpi-note">Ticket × flight segments</div><div class="kpi-wave">⌁⌁⌁</div>
  </div>
  <div class="kpi-card kpi-purple">
    <div class="kpi-icon">✈</div><div class="kpi-label">เที่ยวบินทั้งหมด</div><div class="kpi-sub">TOTAL FLIGHTS</div>
    <div class="kpi-value">{ops_kpi[0]:,.0f}</div><div class="kpi-note">Operational flight records</div><div class="kpi-wave">⌁⌁⌁</div>
  </div>
  <div class="kpi-card kpi-orange">
    <div class="kpi-icon">◷</div><div class="kpi-label">ดีเลย์ขาออกเฉลี่ย</div><div class="kpi-sub">AVG. DEPARTURE DELAY</div>
    <div class="kpi-value">{ops_kpi[1]:,.1f} นาที</div><div class="kpi-note">Positive departure delays</div><div class="kpi-wave">⌁⌁⌁</div>
  </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

route_name = _top_route.iloc[0]['route'] if not _top_route.empty else '-'
route_count = _top_route.iloc[0]['ticket_flights'] if not _top_route.empty else 0
sales_route_name = _top_sales_route.iloc[0]['route'] if not _top_sales_route.empty else '-'
sales_route_value = _top_sales_route.iloc[0]['total_sales'] if not _top_sales_route.empty else 0
fare_name = _top_fare.iloc[0]['fare_class'] if not _top_fare.empty else '-'
fare_value = _top_fare.iloc[0]['total_sales'] if not _top_fare.empty else 0
airport_name = _top_airport.iloc[0]['airport_code'] if not _top_airport.empty else '-'
airport_count = _top_airport.iloc[0]['ticket_flights'] if not _top_airport.empty else 0

insight_html = f"""
<div class="insight-panel">
  <div class="insight-head">★ Key Insights <small>ข้อมูลสำคัญจากตัวกรองที่เลือก</small></div>
  <div class="insight-grid">
    <div class="insight-mini"><div class="insight-icon">📍</div><div class="insight-label">MOST TICKET FLIGHTS</div><div class="insight-value">{route_name}</div><div class="insight-detail">{route_count:,.0f} รายการ</div></div>
    <div class="insight-mini"><div class="insight-icon">💰</div><div class="insight-label">HIGHEST ROUTE SALES</div><div class="insight-value">{sales_route_name}</div><div class="insight-detail">{compact_number(sales_route_value)}</div></div>
    <div class="insight-mini"><div class="insight-icon">💺</div><div class="insight-label">TOP FARE CLASS</div><div class="insight-value">{fare_name}</div><div class="insight-detail">{compact_number(fare_value)}</div></div>
    <div class="insight-mini"><div class="insight-icon">🛫</div><div class="insight-label">BUSIEST DEPARTURE AIRPORT</div><div class="insight-value">{airport_name}</div><div class="insight-detail">{airport_count:,.0f} รายการ</div></div>
  </div>
</div>
"""
st.markdown(insight_html, unsafe_allow_html=True)

st.caption("Executive snapshot • KPI และ Key Insights จะเปลี่ยนตามตัวกรองที่เลือก")
st.write("")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 ภาพรวม",
    "🌐 เส้นทาง",
    "✈️ เครื่องบิน",
    "⏱️ การดำเนินงาน",
    "🔎 วิเคราะห์หลายมิติ"
])


# =========================================================
# TAB 1 — Q3 Q4 Q5
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        'ภาพรวมยอดขาย'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์รายได้ จำนวน Ticket Flight และแนวโน้มยอดขายตามเวลา'
        '</div>',
        unsafe_allow_html=True
    )


    fare_sales = query_df(
        f"""
        SELECT
            fc.fare_class,

            SUM(f.amount)
                AS total_sales,

            SUM(f.ticket_flight_count)
                AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            fc.fare_class

        ORDER BY
            total_sales DESC
        """,
        sales_params
    )


    if fare_sales.empty:

        st.info(
            "ไม่พบข้อมูลตามตัวกรองที่เลือก"
        )

    else:

        top_fare = fare_sales.iloc[0]

        insight_html = (
            '<div class="insight">'
            '<b>Insight:</b> '
            f'ชั้นโดยสารที่สร้างยอดขายสูงที่สุดคือ '
            f'<b>{top_fare["fare_class"]}</b> '
            f'ด้วยยอดขายประมาณ '
            f'<b>{compact_number(top_fare["total_sales"])}</b>'
            '</div>'
        )

        st.markdown(
            insight_html,
            unsafe_allow_html=True
        )


        c1, c2 = st.columns(2)


        # Q3
        with c1:

            st.markdown(
                '<div class="question">'
                'Business Question Q3'
                '</div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "ยอดขายตามชั้นโดยสาร"
            )

            fig = px.pie(
                fare_sales,
                values="total_sales",
                names="fare_class",
                hole=.62,
                color_discrete_sequence=
                MULTI_COLORS
            )

            fig.update_traces(
                textinfo="percent+label"
            )

            style_chart(
                fig,
                410
            )

            display_chart(
                fig
            )


        # Q4
        with c2:

            st.markdown(
                '<div class="question">'
                'Business Question Q4'
                '</div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "จำนวน Ticket Flight ตามชั้นโดยสาร"
            )

            fig = px.bar(
                fare_sales.sort_values(
                    "ticket_flights"
                ),

                x="ticket_flights",
                y="fare_class",

                orientation="h",

                color="ticket_flights",

                color_continuous_scale=[
                    "#CFFAFE",
                    CYAN,
                    "#155E75"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_chart(
                fig,
                410
            )

            display_chart(
                fig
            )


    # Q5
    monthly_sales = query_df(
        f"""
        SELECT
            d.year,
            d.month,

            SUM(f.amount)
                AS total_sales

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            d.year,
            d.month

        ORDER BY
            d.year,
            d.month
        """,
        sales_params
    )


    if not monthly_sales.empty:

        monthly_sales["period"] = (
            monthly_sales["year"]
            .astype(str)
            + "-"
            + monthly_sales["month"]
            .astype(str)
            .str.zfill(2)
        )


        st.markdown(
            '<div class="question">'
            'Business Question Q5'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "แนวโน้มยอดขายตามช่วงเวลา"
        )


        fig = px.area(
            monthly_sales,
            x="period",
            y="total_sales"
        )

        fig.update_traces(
            line=dict(
                color=ORANGE,
                width=4
            ),

            fillcolor=
            "rgba(249,115,22,.16)"
        )

        fig.update_layout(
            xaxis_title="ช่วงเวลา",
            yaxis_title="ยอดขาย"
        )

        style_chart(
            fig,
            430
        )

        display_chart(
            fig
        )


# =========================================================
# TAB 2 — Q6 Q7 Q8 Q9
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        'สนามบินและเส้นทาง'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์สนามบินต้นทาง สนามบินปลายทาง และประสิทธิภาพของเส้นทางบิน'
        '</div>',
        unsafe_allow_html=True
    )


    departure_df = query_df(
        f"""
        SELECT
            dep.airport_code,

            SUM(f.ticket_flight_count)
                AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            dep.airport_code

        ORDER BY
            ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    arrival_df = query_df(
        f"""
        SELECT
            arr.airport_code,

            SUM(f.ticket_flight_count)
                AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            arr.airport_code

        ORDER BY
            ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            '<div class="question">'
            'Business Question Q6'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สนามบินต้นทางยอดนิยม"
        )

        if not departure_df.empty:

            fig = px.bar(
                departure_df.sort_values(
                    "ticket_flights"
                ),

                x="ticket_flights",
                y="airport_code",

                orientation="h",

                color="ticket_flights",

                color_continuous_scale=[
                    "#CFFAFE",
                    CYAN,
                    "#155E75"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    with c2:

        st.markdown(
            '<div class="question">'
            'Business Question Q7'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สนามบินปลายทางยอดนิยม"
        )

        if not arrival_df.empty:

            fig = px.bar(
                arrival_df.sort_values(
                    "ticket_flights"
                ),

                x="ticket_flights",
                y="airport_code",

                orientation="h",

                color="ticket_flights",

                color_continuous_scale=[
                    "#EDE9FE",
                    PURPLE,
                    "#5B21B6"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    route_ticket_df = query_df(
        f"""
        SELECT
            dep.airport_code
            || ' → ' ||
            arr.airport_code
                AS route,

            SUM(f.ticket_flight_count)
                AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            dep.airport_code,
            arr.airport_code

        ORDER BY
            ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    route_sales_df = query_df(
        f"""
        SELECT
            dep.airport_code
            || ' → ' ||
            arr.airport_code
                AS route,

            SUM(f.amount)
                AS total_sales

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        GROUP BY
            dep.airport_code,
            arr.airport_code

        ORDER BY
            total_sales DESC

        LIMIT 10
        """,
        sales_params
    )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            '<div class="question">'
            'Business Question Q8'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "เส้นทางที่มี Ticket Flight สูงสุด"
        )

        if not route_ticket_df.empty:

            fig = px.bar(
                route_ticket_df.sort_values(
                    "ticket_flights"
                ),

                x="ticket_flights",
                y="route",

                orientation="h",

                color="ticket_flights",

                color_continuous_scale=[
                    "#D1FAE5",
                    GREEN,
                    "#065F46"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    with c2:

        st.markdown(
            '<div class="question">'
            'Business Question Q9'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "เส้นทางที่สร้างยอดขายสูงสุด"
        )

        if not route_sales_df.empty:

            fig = px.bar(
                route_sales_df.sort_values(
                    "total_sales"
                ),

                x="total_sales",
                y="route",

                orientation="h",

                color="total_sales",

                color_continuous_scale=[
                    "#FFEDD5",
                    ORANGE,
                    "#C2410C"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="ยอดขาย",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    # =====================================================
    # DRILL DOWN
    # =====================================================

    st.divider()

    st.subheader(
        "Drill-down รายละเอียดเส้นทาง"
    )

    st.caption(
        "เลือกเส้นทางเพื่อดูยอดขายและ Ticket Flight แยกตามชั้นโดยสาร"
    )


    route_options = query_df(
        f"""
        SELECT DISTINCT
            dep.airport_code
            || ' → ' ||
            arr.airport_code
                AS route

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {sales_where}

        ORDER BY
            route
        """,
        sales_params
    )


    if not route_options.empty:

        selected_route = st.selectbox(
            "เลือกเส้นทาง",

            route_options[
                "route"
            ].tolist()
        )


        selected_dep, selected_arr = (
            selected_route
            .split(" → ")
        )


        drill_conditions = list(
            sales_conditions
        )

        drill_params = list(
            sales_params
        )


        drill_conditions.extend([
            "dep.airport_code = ?",
            "arr.airport_code = ?"
        ])

        drill_params.extend([
            selected_dep,
            selected_arr
        ])


        drill_where = " AND ".join(
            drill_conditions
        )


        route_detail = query_df(
            f"""
            SELECT
                fc.fare_class,

                SUM(f.amount)
                    AS total_sales,

                SUM(f.ticket_flight_count)
                    AS ticket_flights

            FROM fact_ticket_sales f

            JOIN dim_date d
                ON f.date_key = d.date_key

            JOIN dim_airport dep
                ON f.departure_airport_key = dep.airport_key

            JOIN dim_airport arr
                ON f.arrival_airport_key = arr.airport_key

            JOIN dim_fare_class fc
                ON f.fare_class_key = fc.fare_class_key

            JOIN dim_aircraft a
                ON f.aircraft_key = a.aircraft_key

            WHERE
                {drill_where}

            GROUP BY
                fc.fare_class

            ORDER BY
                total_sales DESC
            """,
            drill_params
        )


        if not route_detail.empty:

            c1, c2 = st.columns(
                [2, 1]
            )


            with c1:

                fig = px.bar(
                    route_detail,

                    x="fare_class",
                    y="total_sales",

                    color="fare_class",

                    color_discrete_sequence=
                    MULTI_COLORS
                )

                fig.update_layout(
                    showlegend=False,
                    xaxis_title="ชั้นโดยสาร",
                    yaxis_title="ยอดขาย"
                )

                style_chart(
                    fig,
                    340
                )

                display_chart(
                    fig
                )


            with c2:

                st.dataframe(
                    route_detail,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "ดาวน์โหลด Route Detail",

                    data=
                    route_detail
                    .to_csv(
                        index=False
                    )
                    .encode(
                        "utf-8-sig"
                    ),

                    file_name=
                    f"{selected_dep}_{selected_arr}_detail.csv",

                    mime="text/csv"
                )


# =========================================================
# TAB 3 — Q10 Q11 Q12
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">'
        'วิเคราะห์เครื่องบิน'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์การใช้งานเครื่องบิน ความจุ และโครงสร้างที่นั่ง'
        '</div>',
        unsafe_allow_html=True
    )


    usage = query_df(
        f"""
        SELECT
            a.model,

            SUM(f.flight_count)
                AS total_flights

        FROM fact_flight_operations f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {ops_where}

        GROUP BY
            a.model

        ORDER BY
            total_flights DESC
        """,
        ops_params
    )


    seat_df = query_df(
        f"""
        SELECT
            a.model,

            fc.fare_class,

            SUM(f.seat_count)
                AS seats,

            ROUND(
                100.0
                * SUM(f.seat_count)
                /
                SUM(
                    SUM(f.seat_count)
                ) OVER (
                    PARTITION BY a.model
                ),
                2
            ) AS seat_percentage

        FROM fact_seat_inventory f

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        JOIN dim_fare_class fc
            ON f.fare_class_key = fc.fare_class_key

        {seat_where}

        GROUP BY
            a.model,
            fc.fare_class
        """,
        seat_params
    )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            '<div class="question">'
            'Business Question Q10'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "รุ่นเครื่องบินที่ถูกใช้มากที่สุด"
        )

        if not usage.empty:

            fig = px.bar(
                usage.sort_values(
                    "total_flights"
                ),

                x="total_flights",
                y="model",

                orientation="h",

                color="total_flights",

                color_continuous_scale=[
                    "#EDE9FE",
                    PURPLE,
                    "#5B21B6"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="จำนวนเที่ยวบิน",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    total_seats = (
        seat_df
        .groupby(
            "model",
            as_index=False
        )["seats"]
        .sum()
    )


    with c2:

        st.markdown(
            '<div class="question">'
            'Business Question Q11'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "จำนวนที่นั่งของเครื่องบินแต่ละรุ่น"
        )

        if not total_seats.empty:

            fig = px.bar(
                total_seats.sort_values(
                    "seats"
                ),

                x="seats",
                y="model",

                orientation="h",

                color="seats",

                color_continuous_scale=[
                    "#D1FAE5",
                    GREEN,
                    "#065F46"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="จำนวนที่นั่ง",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    st.markdown(
        '<div class="question">'
        'Business Question Q12'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "สัดส่วนที่นั่งตามชั้นโดยสาร"
    )

    st.caption(
        "Seat Inventory เป็นข้อมูลโครงสร้างที่นั่ง จึงไม่เปลี่ยนตามช่วงวันที่"
    )


    if not seat_df.empty:

        fig = px.bar(
            seat_df,

            x="model",

            y="seat_percentage",

            color="fare_class",

            barmode="stack",

            color_discrete_sequence=
            MULTI_COLORS,

            hover_data=[
                "seats"
            ]
        )

        fig.update_layout(
            xaxis_title="รุ่นเครื่องบิน",
            yaxis_title="สัดส่วนที่นั่ง (%)",
            legend_title="ชั้นโดยสาร"
        )

        style_chart(
            fig,
            460
        )

        display_chart(
            fig
        )


# =========================================================
# TAB 4 — Q13 Q14
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">'
        'การดำเนินงานเที่ยวบิน'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์สถานะเที่ยวบินและความล่าช้าของสนามบิน'
        '</div>',
        unsafe_allow_html=True
    )


    status_df = query_df(
        f"""
        SELECT
            s.status_name,

            SUM(f.flight_count)
                AS total_flights

        FROM fact_flight_operations f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        JOIN dim_flight_status s
            ON f.status_key = s.status_key

        WHERE
            {ops_where}

        GROUP BY
            s.status_name

        ORDER BY
            total_flights DESC
        """,
        ops_params
    )


    delay_df = query_df(
        f"""
        SELECT
            dep.airport_code,

            ROUND(
                AVG(
                    f.departure_delay_minutes
                ),
                2
            ) AS avg_delay,

            COUNT(*)
                AS delayed_flights

        FROM fact_flight_operations f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE
            {ops_where}

        AND
            f.departure_delay_minutes > 0

        GROUP BY
            dep.airport_code

        ORDER BY
            avg_delay DESC

        LIMIT 10
        """,
        ops_params
    )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            '<div class="question">'
            'Business Question Q13'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สัดส่วนสถานะเที่ยวบิน"
        )

        if not status_df.empty:

            fig = px.pie(
                status_df,

                values="total_flights",

                names="status_name",

                hole=.62,

                color_discrete_sequence=
                MULTI_COLORS
            )

            fig.update_traces(
                textinfo=
                "percent+label"
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


    with c2:

        st.markdown(
            '<div class="question">'
            'Business Question Q14'
            '</div>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สนามบินที่มีดีเลย์เฉลี่ยสูงสุด"
        )

        if not delay_df.empty:

            fig = px.bar(
                delay_df.sort_values(
                    "avg_delay"
                ),

                x="avg_delay",

                y="airport_code",

                orientation="h",

                color="avg_delay",

                color_continuous_scale=[
                    "#FFEDD5",
                    YELLOW,
                    "#EA580C"
                ],

                hover_data=[
                    "delayed_flights"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="ดีเลย์เฉลี่ย (นาที)",
                yaxis_title=""
            )

            style_chart(
                fig,
                420
            )

            display_chart(
                fig
            )


# =========================================================
# TAB 5 — Q15
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">'
        'การวิเคราะห์ข้อมูลแบบหลายมิติ'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'Date × Route × Fare Class × Revenue'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="question">'
        'Business Question Q15'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "เส้นทางและชั้นโดยสารที่สร้างยอดขายสูงสุดในแต่ละเดือน"
    )


    monthly_top = query_df(
        f"""
        WITH sales_summary AS (

            SELECT
                d.year,
                d.month,
                d.month_name,

                dep.airport_code
                    AS departure_airport,

                arr.airport_code
                    AS arrival_airport,

                fc.fare_class,

                SUM(f.amount)
                    AS total_sales

            FROM fact_ticket_sales f

            JOIN dim_date d
                ON f.date_key = d.date_key

            JOIN dim_airport dep
                ON f.departure_airport_key = dep.airport_key

            JOIN dim_airport arr
                ON f.arrival_airport_key = arr.airport_key

            JOIN dim_fare_class fc
                ON f.fare_class_key = fc.fare_class_key

            JOIN dim_aircraft a
                ON f.aircraft_key = a.aircraft_key

            WHERE
                {sales_where}

            GROUP BY
                d.year,
                d.month,
                d.month_name,
                dep.airport_code,
                arr.airport_code,
                fc.fare_class
        ),

        ranked AS (

            SELECT
                *,

                DENSE_RANK() OVER (
                    PARTITION BY
                        year,
                        month

                    ORDER BY
                        total_sales DESC
                ) AS sales_rank

            FROM sales_summary
        )

        SELECT
            year,
            month,
            month_name,
            departure_airport,
            arrival_airport,
            fare_class,
            total_sales

        FROM ranked

        WHERE
            sales_rank = 1

        ORDER BY
            year,
            month
        """,
        sales_params
    )


    if monthly_top.empty:

        st.info(
            "ไม่พบข้อมูลตามตัวกรองที่เลือก"
        )

    else:

        monthly_top["period"] = (
            monthly_top["year"]
            .astype(str)

            + "-"

            + monthly_top["month"]
            .astype(str)
            .str.zfill(2)
        )


        best_row = monthly_top.loc[
            monthly_top[
                "total_sales"
            ].idxmax()
        ]


        insight_html = (
            '<div class="insight">'
            '<b>Top Insight:</b> '
            f'ช่วงที่มียอดขายสูงที่สุดคือ '
            f'<b>{best_row["period"]}</b> '
            f'เส้นทาง '
            f'<b>{best_row["departure_airport"]} → '
            f'{best_row["arrival_airport"]}</b> '
            f'ชั้นโดยสาร '
            f'<b>{best_row["fare_class"]}</b> '
            f'ยอดขายประมาณ '
            f'<b>{compact_number(best_row["total_sales"])}</b>'
            '</div>'
        )

        st.markdown(
            insight_html,
            unsafe_allow_html=True
        )


        fig = px.bar(
            monthly_top,

            x="period",

            y="total_sales",

            color="fare_class",

            color_discrete_sequence=
            MULTI_COLORS,

            hover_data=[
                "departure_airport",
                "arrival_airport",
                "month_name"
            ]
        )

        fig.update_layout(
            xaxis_title="ช่วงเวลา",
            yaxis_title="ยอดขาย",
            legend_title="ชั้นโดยสาร"
        )

        style_chart(
            fig,
            480
        )

        display_chart(
            fig
        )


        st.subheader(
            "รายละเอียดผลการวิเคราะห์"
        )


        display_df = monthly_top[
            [
                "year",
                "month_name",
                "departure_airport",
                "arrival_airport",
                "fare_class",
                "total_sales"
            ]
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        st.download_button(
            "ดาวน์โหลดผลการวิเคราะห์ Q15",

            data=
            display_df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            ),

            file_name=
            "Q15_multidimensional_analysis.csv",

            mime="text/csv"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer-premium">
      <div><b>✈ Airline Data Warehouse</b><br>Built with DuckDB • dbt • Streamlit • Plotly • 15 Business Questions</div>
      <div class="footer-ready">Analytics Ready</div>
    </div>
    """,
    unsafe_allow_html=True,
)

con.close()