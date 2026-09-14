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

/* =========================================================
   AIRLINE INTELLIGENCE — PREMIUM UI
   ========================================================= */

:root {
    --ink: #0B1220;
    --muted: #64748B;
    --line: #E6ECF5;
    --panel: rgba(255,255,255,.92);
    --blue: #2563EB;
    --sky: #0EA5E9;
    --cyan: #06B6D4;
}

.stApp {
    background:
        radial-gradient(circle at 6% -5%, rgba(37,99,235,.12), transparent 28%),
        radial-gradient(circle at 96% 0%, rgba(6,182,212,.10), transparent 24%),
        linear-gradient(180deg, #F8FBFF 0%, #F6F8FC 55%, #F8FAFC 100%);
    color: var(--ink);
}

.block-container {
    max-width: 1480px;
    padding-top: 1.05rem;
    padding-bottom: 3.2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 20% 0%, rgba(14,165,233,.18), transparent 26%),
        linear-gradient(180deg, #08111F 0%, #0F1E3C 58%, #172554 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: .9rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #F8FAFC !important;
}

.sidebar-kicker {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(14,165,233,.13);
    border: 1px solid rgba(125,211,252,.24);
    color: #BAE6FD;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 3px 0 10px 0;
}

.sidebar-kicker::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 999px;
    background: #22D3EE;
    box-shadow: 0 0 0 4px rgba(34,211,238,.12);
}

section[data-testid="stSidebar"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    background-color: #FFFFFF !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid rgba(148,163,184,.24) !important;
    border-radius: 13px !important;
    min-height: 44px;
    box-shadow: 0 6px 18px rgba(2,6,23,.10);
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #0F172A !important;
}

.hero {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 90% 18%, rgba(34,211,238,.27), transparent 22%),
        radial-gradient(circle at 70% 130%, rgba(59,130,246,.40), transparent 38%),
        linear-gradient(118deg, #07101F 0%, #12235C 46%, #1D4ED8 76%, #06B6D4 118%);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 28px;
    padding: 34px 38px 32px 38px;
    margin-bottom: 14px;
    box-shadow:
        0 24px 55px rgba(37,99,235,.18),
        inset 0 1px 0 rgba(255,255,255,.08);
}

.hero::after {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    right: -70px;
    top: -92px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,.12);
    box-shadow:
        0 0 0 34px rgba(255,255,255,.035),
        0 0 0 68px rgba(255,255,255,.02);
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #BAE6FD;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.15px;
    margin-bottom: 12px;
}

.hero-kicker-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #22D3EE;
    box-shadow: 0 0 0 5px rgba(34,211,238,.13);
}

.hero-title {
    color: white;
    font-size: clamp(34px, 4vw, 50px);
    font-weight: 860;
    line-height: 1.05;
    letter-spacing: -1.25px;
    margin-bottom: 10px;
}

.hero-title-accent {
    color: #67E8F9;
}

.hero-subtitle {
    color: #DCEBFF;
    font-size: 15px;
    line-height: 1.7;
    max-width: 850px;
}

.hero-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 20px;
}

.hero-chip {
    display: inline-flex;
    align-items: center;
    padding: 7px 11px;
    border-radius: 999px;
    color: #E0F2FE;
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.12);
    font-size: 11px;
    font-weight: 700;
    backdrop-filter: blur(8px);
}

.meta-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 3px 0 20px 0;
}

.meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 11px;
    border-radius: 999px;
    background: rgba(255,255,255,.78);
    border: 1px solid #E3EAF4;
    color: #475569;
    font-size: 11px;
    font-weight: 750;
    box-shadow: 0 6px 18px rgba(15,23,42,.035);
}

.meta-pill strong {
    color: #0F172A;
}

div[data-testid="stMetric"] {
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(248,250,252,.98));
    border: 1px solid #E4EAF3;
    border-radius: 20px;
    padding: 18px 20px 16px 20px;
    box-shadow:
        0 10px 28px rgba(15,23,42,.06),
        inset 0 1px 0 rgba(255,255,255,.8);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}

div[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #2563EB, #06B6D4);
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: #BFDBFE;
    box-shadow: 0 16px 34px rgba(37,99,235,.10);
}

div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 720;
    letter-spacing: .1px;
}

div[data-testid="stMetricValue"] {
    color: #0B1220;
    font-weight: 860;
    letter-spacing: -.7px;
}

.section-title {
    font-size: 29px;
    font-weight: 860;
    letter-spacing: -.45px;
    color: #0B1220;
    margin-top: 8px;
    margin-bottom: 3px;
}

.section-desc {
    color: #64748B;
    font-size: 14px;
    margin-bottom: 18px;
}

.question {
    display: inline-flex;
    align-items: center;
    padding: 5px 9px;
    border-radius: 999px;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    color: #1D4ED8;
    font-size: 10px;
    font-weight: 850;
    letter-spacing: .55px;
    margin-bottom: 5px;
}

.insight {
    position: relative;
    background:
        linear-gradient(120deg, rgba(236,254,255,.95), rgba(239,246,255,.96));
    border: 1px solid #CFFAFE;
    border-radius: 16px;
    padding: 14px 17px 14px 19px;
    margin: 8px 0 18px 0;
    color: #164E63;
    box-shadow: 0 8px 22px rgba(6,182,212,.06);
}

.insight::before {
    content: "";
    position: absolute;
    left: 0;
    top: 14px;
    bottom: 14px;
    width: 4px;
    border-radius: 999px;
    background: linear-gradient(180deg, #06B6D4, #2563EB);
}

div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,.96);
    border: 1px solid #E5EAF2;
    border-radius: 20px;
    padding: 9px;
    box-shadow:
        0 10px 26px rgba(15,23,42,.05),
        inset 0 1px 0 rgba(255,255,255,.8);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(15,23,42,.04);
}

div[data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,.72);
    border: 1px solid #E5EAF2;
    border-radius: 16px;
    padding: 6px;
    box-shadow: 0 8px 24px rgba(15,23,42,.045);
}

button[data-baseweb="tab"] {
    height: 42px;
    border-radius: 11px;
    padding-left: 15px !important;
    padding-right: 15px !important;
    color: #64748B;
    font-size: 13px;
    font-weight: 760;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #EFF6FF, #ECFEFF);
    color: #0F172A !important;
}

div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #2563EB, #06B6D4) !important;
    height: 3px !important;
    border-radius: 999px;
}

.stDownloadButton button,
.stButton button {
    border-radius: 12px;
    border: 1px solid #BFDBFE;
    background: linear-gradient(135deg, #EFF6FF, #ECFEFF);
    color: #155E75;
    font-weight: 760;
    min-height: 42px;
    transition: transform .16s ease, box-shadow .16s ease;
}

.stDownloadButton button:hover,
.stButton button:hover {
    transform: translateY(-1px);
    border-color: #7DD3FC;
    box-shadow: 0 8px 18px rgba(14,165,233,.10);
}

h1, h2, h3 {
    letter-spacing: -.35px;
}

hr {
    border-color: #E8EDF5 !important;
}

@media (max-width: 900px) {
    .hero {
        padding: 28px 24px;
        border-radius: 22px;
    }

    .hero-title {
        font-size: 34px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

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

hero_html = (
    '<div class="hero">'
    '<div class="hero-kicker">'
    '<span class="hero-kicker-dot"></span>'
    'AIRLINE DATA WAREHOUSE • ANALYTICS EXPERIENCE'
    '</div>'
    '<div class="hero-title">'
    'Airline <span class="hero-title-accent">Intelligence</span><br>Dashboard'
    '</div>'
    '<div class="hero-subtitle">'
    'วิเคราะห์ยอดขายตั๋ว เส้นทางบิน เครื่องบิน และประสิทธิภาพการดำเนินงาน '
    'จาก Data Warehouse ในมุมมองเดียว'
    '</div>'
    '<div class="hero-tech">'
    '<span class="hero-chip">DuckDB</span>'
    '<span class="hero-chip">dbt</span>'
    '<span class="hero-chip">Streamlit</span>'
    '<span class="hero-chip">Plotly</span>'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="meta-strip">
        <span class="meta-pill"><strong>15</strong> Business Questions</span>
        <span class="meta-pill"><strong>3</strong> Fact Tables</span>
        <span class="meta-pill"><strong>5</strong> Dimensions</span>
        <span class="meta-pill">Direct <strong>DuckDB</strong> Connection</span>
    </div>
    """,
    unsafe_allow_html=True
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
    '<div class="sidebar-kicker">CONTROL CENTER</div>',
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
# KPI DISPLAY
# ใช้ Native Streamlit → ไม่มี HTML โผล่
# =========================================================

k1, k2, k3, k4 = st.columns(4)


with k1:
    st.metric(
        label="ยอดขายตั๋วรวม • Total Sales",
        value=compact_number(
            sales_kpi[0]
        )
    )


with k2:
    st.metric(
        label="จำนวน Ticket Flight",
        value=f"{sales_kpi[1]:,.0f}"
    )


with k3:
    st.metric(
        label="เที่ยวบินทั้งหมด • Flights",
        value=f"{ops_kpi[0]:,.0f}"
    )


with k4:
    st.metric(
        label="ดีเลย์ขาออกเฉลี่ย • Avg Delay",
        value=f"{ops_kpi[1]:,.1f} นาที"
    )


st.caption(
    "Executive snapshot • KPI จะเปลี่ยนตามตัวกรองที่เลือก"
)

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

st.divider()

st.caption(
    "Airline Intelligence Dashboard  •  Data Warehouse Analytics  •  dbt  •  DuckDB  •  Streamlit  •  Plotly"
)

con.close()