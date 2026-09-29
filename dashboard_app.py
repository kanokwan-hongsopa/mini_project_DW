import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path
import subprocess
import sys
import shutil

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Airline Intelligence Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# DATABASE
# =========================================================
ROOT_DIR = Path(__file__).resolve().parent
AIRLINE_DIR = ROOT_DIR / "airline_dw"
DB_PATH = AIRLINE_DIR / "dev.duckdb"
PROFILES_PATH = AIRLINE_DIR / "profiles.yml"


def create_profiles_yml():
    """Create a local dbt profile for Streamlit Cloud."""
    PROFILES_PATH.write_text(
        """airline_dw:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
      threads: 4
""",
        encoding="utf-8",
    )


def get_existing_tables():
    if not DB_PATH.exists():
        return set()

    try:
        check_con = duckdb.connect(str(DB_PATH), read_only=True)
        tables = {
            row[0]
            for row in check_con.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'main'
                """
            ).fetchall()
        }
        check_con.close()
        return tables
    except Exception:
        return set()


REQUIRED_DW_TABLES = {
    "dim_date",
    "dim_airport",
    "dim_aircraft",
    "dim_fare_class",
    "dim_flight_status",
    "fact_ticket_sales",
    "fact_flight_operations",
    "fact_seat_utilization",
}


def database_is_ready():
    return REQUIRED_DW_TABLES.issubset(get_existing_tables())


def run_command(command, cwd, label):
    """Run a command and show useful logs if it fails."""
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        st.error(f"{label} ไม่สำเร็จ")

        if result.stdout:
            st.markdown("**STDOUT**")
            st.code(result.stdout[-12000:], language="text")

        if result.stderr:
            st.markdown("**STDERR**")
            st.code(result.stderr[-12000:], language="text")

        raise RuntimeError(
            f"{label} failed with exit code {result.returncode}"
        )

    return result


def rebuild_data_warehouse():
    """Rebuild DuckDB from source CSV files and dbt models."""
    create_profiles_yml()

    dbt_executable = shutil.which("dbt")

    if not dbt_executable:
        st.error("ไม่พบคำสั่ง dbt ใน Streamlit environment")
        st.info(
            "ตรวจสอบ requirements.txt ว่ามี dbt-core และ dbt-duckdb"
        )
        st.stop()

    with st.status(
        "กำลังเตรียม Airline Data Warehouse...",
        expanded=True,
    ) as status:

        st.write("1/3 กำลังโหลด Raw Data...")

        run_command(
            [sys.executable, "scripts/load_raw.py"],
            AIRLINE_DIR,
            "Load Raw Data",
        )

        st.write("2/3 กำลังสร้าง Staging, Dimensions และ Facts...")

        run_command(
            [
                dbt_executable,
                "run",
                "--profiles-dir",
                ".",
            ],
            AIRLINE_DIR,
            "dbt run",
        )

        st.write("3/3 กำลังตรวจสอบ Data Warehouse...")

        run_command(
            [
                dbt_executable,
                "test",
                "--profiles-dir",
                ".",
            ],
            AIRLINE_DIR,
            "dbt test",
        )

        missing_after_build = REQUIRED_DW_TABLES - get_existing_tables()

        if missing_after_build:
            raise RuntimeError(
                "สร้าง Data Warehouse แล้ว แต่ยังขาดตาราง: "
                + ", ".join(sorted(missing_after_build))
            )

        status.update(
            label="Data Warehouse พร้อมใช้งาน",
            state="complete",
            expanded=False,
        )


if not database_is_ready():
    try:
        rebuild_data_warehouse()
    except Exception as exc:
        st.error("ไม่สามารถสร้าง Data Warehouse ได้")
        st.exception(exc)
        st.stop()


con = duckdb.connect(str(DB_PATH), read_only=True)

# =========================================================
# COLORS
# =========================================================
NAVY = "#0F172A"
BLUE = "#2563EB"
CYAN = "#06B6D4"
PURPLE = "#7C3AED"
ORANGE = "#F97316"
GREEN = "#14B8A6"
RED = "#EF4444"
SLATE = "#475569"

MULTI_COLORS = [BLUE, CYAN, PURPLE, ORANGE, GREEN, RED]

# =========================================================
# CSS
# =========================================================
st.markdown(
    """
<style>
:root{
    --ink:#0F172A;
    --muted:#64748B;
    --line:#E2E8F0;
    --blue:#2563EB;
    --cyan:#06B6D4;
    --navy:#071426;
}

*{box-sizing:border-box}

.stApp{
    background:
        radial-gradient(circle at 14% -8%,rgba(37,99,235,.12),transparent 27%),
        radial-gradient(circle at 95% 3%,rgba(6,182,212,.09),transparent 23%),
        linear-gradient(180deg,#F8FBFF 0%,#F4F7FB 100%);
    color:var(--ink);
}

.block-container{
    max-width:1510px;
    padding-top:.8rem;
    padding-bottom:2.8rem;
}

header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}

section[data-testid="stSidebar"]{
    background:
        radial-gradient(circle at 22% 2%,rgba(20,184,166,.14),transparent 21%),
        radial-gradient(circle at 90% 22%,rgba(37,99,235,.22),transparent 34%),
        linear-gradient(180deg,#061223 0%,#0A1D3D 57%,#10285A 100%);
    border-right:1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{
    color:#F8FAFC!important;
}

section[data-testid="stSidebar"] input{
    color:#0F172A!important;
    -webkit-text-fill-color:#0F172A!important;
    background:#fff!important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"],
section[data-testid="stSidebar"] div[data-baseweb="select"]>div{
    background:#fff!important;
    border-radius:13px!important;
}

.hero{
    border-radius:30px;
    padding:38px 42px 34px;
    background:
        radial-gradient(circle at 79% 36%,rgba(34,211,238,.25),transparent 18%),
        radial-gradient(circle at 62% 120%,rgba(37,99,235,.52),transparent 42%),
        linear-gradient(118deg,#071326 0%,#0D2A67 49%,#1156D8 76%,#0EA5E9 125%);
    color:#fff;
    box-shadow:0 28px 64px rgba(37,99,235,.18);
    margin-bottom:16px;
}

.hero-kicker{
    color:#BAE6FD;
    font-size:11px;
    font-weight:850;
    letter-spacing:1.2px;
}

.hero-title{
    font-size:clamp(40px,4.2vw,58px);
    font-weight:900;
    line-height:1;
    margin:14px 0;
}

.hero-sub{
    color:#D9E9FF;
    font-size:15px;
    line-height:1.72;
    max-width:900px;
}

.hero-chip{
    display:inline-block;
    margin:20px 7px 0 0;
    padding:8px 12px;
    border-radius:999px;
    color:#E0F2FE;
    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.13);
    font-size:11px;
    font-weight:750;
}

.kpi-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:14px;
    margin:4px 0 18px;
}

.kpi-card{
    border-radius:22px;
    padding:20px 21px;
    color:#fff;
    min-height:145px;
    box-shadow:0 18px 38px rgba(15,23,42,.11);
}

.kpi-blue{background:linear-gradient(135deg,#2563EB,#0EA5E9 68%,#22D3EE)}
.kpi-teal{background:linear-gradient(135deg,#0F9F95,#14B8A6 56%,#22D3EE)}
.kpi-purple{background:linear-gradient(135deg,#5B4CF0,#7C5CFC 58%,#8B5CF6)}
.kpi-orange{background:linear-gradient(135deg,#EA7000,#F97316 58%,#F59E0B)}

.kpi-label{font-size:12px;font-weight:800;color:#F8FAFC}
.kpi-sub{font-size:10px;color:rgba(255,255,255,.76);margin-top:2px}
.kpi-value{font-size:33px;font-weight:900;letter-spacing:-1px;margin-top:18px}
.kpi-note{font-size:10px;color:rgba(255,255,255,.78);margin-top:5px}

.section-title{
    font-size:29px;
    font-weight:900;
    color:#0B1831;
    margin-top:8px;
    margin-bottom:3px;
}

.section-desc{
    color:#64748B;
    font-size:14px;
    margin-bottom:18px;
}

.question{
    display:inline-flex;
    align-items:center;
    padding:5px 9px;
    border-radius:999px;
    background:linear-gradient(135deg,#EFF6FF,#ECFEFF);
    border:1px solid #CDE8FF;
    color:#1D4ED8;
    font-size:10px;
    font-weight:850;
    letter-spacing:.55px;
    margin-bottom:5px;
}

.insight{
    background:linear-gradient(120deg,#ECFEFF,#EFF6FF);
    border:1px solid #CFFAFE;
    border-radius:16px;
    padding:13px 16px;
    margin:8px 0 16px;
    color:#164E63;
}

div[data-testid="stPlotlyChart"]{
    background:#fff;
    border:1px solid #E5EAF2;
    border-radius:22px;
    padding:9px;
    box-shadow:0 12px 28px rgba(15,23,42,.055);
}

div[data-testid="stDataFrame"]{
    border:1px solid #E2E8F0;
    border-radius:17px;
    overflow:hidden;
}

div[data-baseweb="tab-list"]{
    gap:5px;
    background:rgba(255,255,255,.9);
    border:1px solid #E5EAF2;
    border-radius:18px;
    padding:7px;
}

button[data-baseweb="tab"]{
    height:46px;
    border-radius:13px;
    padding-left:17px!important;
    padding-right:17px!important;
    color:#64748B;
    font-size:13px;
    font-weight:780;
}

button[data-baseweb="tab"][aria-selected="true"]{
    background:linear-gradient(135deg,#2563EB,#0EA5E9);
    color:#fff!important;
}

.footer-premium{
    margin-top:24px;
    padding:15px 18px;
    border-radius:18px;
    background:linear-gradient(135deg,#071426,#0E2A59);
    color:#BFD8FF;
    display:flex;
    justify-content:space-between;
    gap:16px;
    align-items:center;
    flex-wrap:wrap;
    font-size:11px;
}

.footer-premium b{color:#fff}

@media(max-width:1100px){
    .kpi-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:720px){
    .kpi-grid{grid-template-columns:1fr}
    .hero{padding:28px 24px}
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
def query_df(sql, params=None):
    return con.execute(sql, params or []).fetchdf()


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
        margin=dict(l=24, r=24, t=40, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=NAVY, size=13),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            font=dict(color=NAVY, size=12),
            title_font=dict(color=NAVY, size=12),
        ),
        hoverlabel=dict(
            bgcolor=NAVY,
            font_color="white",
            bordercolor="rgba(255,255,255,.2)",
        ),
    )
    fig.update_xaxes(
        title_font=dict(color=NAVY, size=13),
        tickfont=dict(color=SLATE, size=12),
        gridcolor="#E2E8F0",
        linecolor="#CBD5E1",
        zeroline=False,
    )
    fig.update_yaxes(
        title_font=dict(color=NAVY, size=13),
        tickfont=dict(color=SLATE, size=12),
        gridcolor="#E2E8F0",
        linecolor="#CBD5E1",
        zeroline=False,
    )
    return fig


def display_chart(fig, height=420):
    style_chart(fig, height)
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False},
    )


def question_tag(number):
    st.markdown(
        f'<div class="question">Business Question Q{number}</div>',
        unsafe_allow_html=True,
    )


def download_df(df, label, filename):
    st.download_button(
        label,
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
        width="stretch",
    )


def table_columns(table_name):
    try:
        info = con.execute(f"PRAGMA table_info('{table_name}')").fetchdf()
        return set(info["name"].tolist())
    except Exception:
        return set()


def first_existing(table_name, candidates):
    cols = table_columns(table_name)
    for col in candidates:
        if col in cols:
            return col
    return None


# =========================================================
# VALIDATE DW OBJECTS
# =========================================================
required_tables = [
    "dim_date",
    "dim_airport",
    "dim_aircraft",
    "dim_fare_class",
    "dim_flight_status",
    "fact_ticket_sales",
    "fact_flight_operations",
    "fact_seat_utilization",
]

existing_tables = set(
    con.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema','pg_catalog')
        """
    ).fetchdf()["table_name"].tolist()
)

DAYPART_OPS = first_existing(
    "fact_flight_operations",
    ["departure_daypart", "daypart", "scheduled_departure_daypart"],
)
WEEKEND_OPS = first_existing(
    "fact_flight_operations",
    ["departure_is_weekend", "is_weekend", "weekend_flag"],
)
DAYPART_SEAT = first_existing(
    "fact_seat_utilization",
    ["departure_daypart", "daypart", "scheduled_departure_daypart"],
)

if DAYPART_OPS is None or WEEKEND_OPS is None or DAYPART_SEAT is None:
    st.error("ไม่พบคอลัมน์ daypart/weekend ที่ Dashboard Q7, Q8, Q12, Q15 ต้องใช้")
    st.stop()

# =========================================================
# HERO
# =========================================================
st.markdown(
    """
<div class="hero">
  <div class="hero-kicker">AIRLINE DATA WAREHOUSE • DUCKDB • DBT • STREAMLIT • PLOTLY</div>
  <div class="hero-title">Airline Intelligence Dashboard</div>
  <div class="hero-sub">
    Interactive Dashboard สำหรับ Business Questions Q1–Q15
    โดย Query จาก Dimension และ Fact Tables ของ Data Warehouse เท่านั้น
    พร้อม KPI, Filters, Drill-down และ Download CSV
  </div>
  <span class="hero-chip">3 Fact Tables</span>
  <span class="hero-chip">5 Dimensions</span>
  <span class="hero-chip">15 Business Questions</span>
  <span class="hero-chip">Interactive Filters</span>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DATE RANGE
# =========================================================
date_row = con.execute(
    "SELECT MIN(full_date), MAX(full_date) FROM dim_date"
).fetchone()

min_date = pd.to_datetime(date_row[0]).date()
max_date = pd.to_datetime(date_row[1]).date()

# =========================================================
# SIDEBAR CASCADING FILTERS
# =========================================================
st.sidebar.title("ตัวกรองข้อมูล")
st.sidebar.caption("ตัวกรองแบบ Interactive / Cascading Filters")

date_selection = st.sidebar.date_input(
    "ช่วงวันที่",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
    start_date, end_date = date_selection
else:
    start_date, end_date = min_date, max_date

departure_options = query_df(
    """
    SELECT DISTINCT dep.airport_code
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    WHERE d.full_date BETWEEN ? AND ?
    ORDER BY dep.airport_code
    """,
    [start_date, end_date],
)["airport_code"].dropna().tolist()

departure = st.sidebar.selectbox(
    "สนามบินต้นทาง",
    ["ทั้งหมด"] + departure_options,
)

arrival_conditions = ["d.full_date BETWEEN ? AND ?"]
arrival_params = [start_date, end_date]

if departure != "ทั้งหมด":
    arrival_conditions.append("dep.airport_code = ?")
    arrival_params.append(departure)

arrival_options = query_df(
    f"""
    SELECT DISTINCT arr.airport_code
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    WHERE {' AND '.join(arrival_conditions)}
    ORDER BY arr.airport_code
    """,
    arrival_params,
)["airport_code"].dropna().tolist()

arrival = st.sidebar.selectbox(
    "สนามบินปลายทาง",
    ["ทั้งหมด"] + arrival_options,
)

fare_conditions = ["d.full_date BETWEEN ? AND ?"]
fare_params = [start_date, end_date]

if departure != "ทั้งหมด":
    fare_conditions.append("dep.airport_code = ?")
    fare_params.append(departure)
if arrival != "ทั้งหมด":
    fare_conditions.append("arr.airport_code = ?")
    fare_params.append(arrival)

fare_options = query_df(
    f"""
    SELECT DISTINCT fc.fare_class
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    WHERE {' AND '.join(fare_conditions)}
    ORDER BY fc.fare_class
    """,
    fare_params,
)["fare_class"].dropna().tolist()

fare = st.sidebar.selectbox(
    "ชั้นโดยสาร",
    ["ทั้งหมด"] + fare_options,
)

aircraft_conditions = ["d.full_date BETWEEN ? AND ?"]
aircraft_params = [start_date, end_date]

if departure != "ทั้งหมด":
    aircraft_conditions.append("dep.airport_code = ?")
    aircraft_params.append(departure)
if arrival != "ทั้งหมด":
    aircraft_conditions.append("arr.airport_code = ?")
    aircraft_params.append(arrival)
if fare != "ทั้งหมด":
    aircraft_conditions.append("fc.fare_class = ?")
    aircraft_params.append(fare)

aircraft_options = query_df(
    f"""
    SELECT DISTINCT a.model
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {' AND '.join(aircraft_conditions)}
    ORDER BY a.model
    """,
    aircraft_params,
)["model"].dropna().tolist()

aircraft = st.sidebar.selectbox(
    "รุ่นเครื่องบิน",
    ["ทั้งหมด"] + aircraft_options,
)

active_filter_count = sum(
    [
        departure != "ทั้งหมด",
        arrival != "ทั้งหมด",
        fare != "ทั้งหมด",
        aircraft != "ทั้งหมด",
        start_date != min_date or end_date != max_date,
    ]
)

st.sidebar.divider()
st.sidebar.caption(
    f"ข้อมูล {min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')}"
)
st.sidebar.caption(f"Active filters: {active_filter_count}")

# =========================================================
# FILTER BUILDERS
# =========================================================
sales_conditions = ["d.full_date BETWEEN ? AND ?"]
sales_params = [start_date, end_date]

if departure != "ทั้งหมด":
    sales_conditions.append("dep.airport_code = ?")
    sales_params.append(departure)
if arrival != "ทั้งหมด":
    sales_conditions.append("arr.airport_code = ?")
    sales_params.append(arrival)
if fare != "ทั้งหมด":
    sales_conditions.append("fc.fare_class = ?")
    sales_params.append(fare)
if aircraft != "ทั้งหมด":
    sales_conditions.append("a.model = ?")
    sales_params.append(aircraft)

sales_where = " AND ".join(sales_conditions)

ops_conditions = ["d.full_date BETWEEN ? AND ?"]
ops_params = [start_date, end_date]

if departure != "ทั้งหมด":
    ops_conditions.append("dep.airport_code = ?")
    ops_params.append(departure)
if arrival != "ทั้งหมด":
    ops_conditions.append("arr.airport_code = ?")
    ops_params.append(arrival)
if aircraft != "ทั้งหมด":
    ops_conditions.append("a.model = ?")
    ops_params.append(aircraft)

ops_where = " AND ".join(ops_conditions)

seat_conditions = ["d.full_date BETWEEN ? AND ?"]
seat_params = [start_date, end_date]

if departure != "ทั้งหมด":
    seat_conditions.append("dep.airport_code = ?")
    seat_params.append(departure)
if arrival != "ทั้งหมด":
    seat_conditions.append("arr.airport_code = ?")
    seat_params.append(arrival)
if aircraft != "ทั้งหมด":
    seat_conditions.append("a.model = ?")
    seat_params.append(aircraft)

seat_where = " AND ".join(seat_conditions)

# =========================================================
# KPI
# =========================================================
sales_kpi = query_df(
    f"""
    SELECT
        COALESCE(SUM(f.amount),0) AS total_revenue,
        COALESCE(SUM(f.ticket_flight_count),0) AS ticket_flights
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    """,
    sales_params,
).iloc[0]

ops_kpi = query_df(
    f"""
    SELECT
        COALESCE(SUM(f.flight_count),0) AS total_flights,
        COALESCE(AVG(f.departure_delay_minutes),0) AS avg_departure_delay
    FROM fact_flight_operations f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {ops_where}
    """,
    ops_params,
).iloc[0]

seat_kpi = query_df(
    f"""
    SELECT
        COALESCE(SUM(f.boarded_count),0) AS boarded_count,
        COALESCE(
            100.0 * SUM(f.boarded_count) / NULLIF(SUM(f.seat_capacity),0),
            0
        ) AS boarded_load_pct
    FROM fact_seat_utilization f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {seat_where}
    """,
    seat_params,
).iloc[0]

st.markdown(
    f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-blue">
    <div class="kpi-label">TOTAL REVENUE</div>
    <div class="kpi-sub">ยอดขายตั๋วรวม</div>
    <div class="kpi-value">{compact_number(sales_kpi["total_revenue"])}</div>
    <div class="kpi-note">fact_ticket_sales.amount</div>
  </div>

  <div class="kpi-card kpi-teal">
    <div class="kpi-label">TICKET FLIGHTS</div>
    <div class="kpi-sub">จำนวน Ticket × Flight</div>
    <div class="kpi-value">{sales_kpi["ticket_flights"]:,.0f}</div>
    <div class="kpi-note">fact_ticket_sales</div>
  </div>

  <div class="kpi-card kpi-purple">
    <div class="kpi-label">TOTAL FLIGHTS</div>
    <div class="kpi-sub">เที่ยวบินทั้งหมด</div>
    <div class="kpi-value">{ops_kpi["total_flights"]:,.0f}</div>
    <div class="kpi-note">fact_flight_operations</div>
  </div>

  <div class="kpi-card kpi-orange">
    <div class="kpi-label">BOARDED LOAD</div>
    <div class="kpi-sub">อัตราการใช้ที่นั่งจริง</div>
    <div class="kpi-value">{seat_kpi["boarded_load_pct"]:,.1f}%</div>
    <div class="kpi-note">{seat_kpi["boarded_count"]:,.0f} boarded passengers</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================================
# MAIN TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "💰 Revenue & Demand",
        "💺 Capacity",
        "🧭 Travel Pattern",
        "✈️ Fleet & Operations",
        "🔎 Multidimensional",
    ]
)

# =========================================================
# TAB 1 — Q1-Q4
# =========================================================
with tab1:
    st.markdown('<div class="section-title">Revenue & Demand</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Q1–Q4: Route Revenue, Fare Class Share, Monthly Trend และ Region Pair Demand</div>',
        unsafe_allow_html=True,
    )

    # Q1
    question_tag(1)
    st.subheader("เส้นทางใดสร้างรายได้จากการขายตั๋วสูงที่สุด?")

    q1 = query_df(
        f"""
        SELECT
            dep.airport_code || ' → ' || arr.airport_code AS route,
            SUM(f.amount) AS total_revenue,
            SUM(f.ticket_flight_count) AS ticket_flights
        FROM fact_ticket_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {sales_where}
        GROUP BY dep.airport_code, arr.airport_code
        ORDER BY total_revenue DESC
        LIMIT 10
        """,
        sales_params,
    )

    if not q1.empty:
        top = q1.iloc[0]
        st.markdown(
            f'<div class="insight"><b>Insight:</b> {top["route"]} '
            f'มีรายได้สูงสุดในเงื่อนไขที่เลือก ประมาณ <b>{compact_number(top["total_revenue"])}</b></div>',
            unsafe_allow_html=True,
        )

        fig = px.bar(
            q1.sort_values("total_revenue"),
            x="total_revenue",
            y="route",
            orientation="h",
            color="total_revenue",
            color_continuous_scale="Blues",
            hover_data=["ticket_flights"],
        )
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Revenue", yaxis_title="")
        display_chart(fig)

        download_df(q1, "ดาวน์โหลด Q1", "Q1_route_revenue.csv")

    c1, c2 = st.columns(2)

    # Q2
    with c1:
        question_tag(2)
        st.subheader("Fare Class ใดสร้างรายได้สูงที่สุด และมีสัดส่วนเท่าใด?")

        q2 = query_df(
            f"""
            SELECT
                fc.fare_class,
                SUM(f.amount) AS total_revenue
            FROM fact_ticket_sales f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {sales_where}
            GROUP BY fc.fare_class
            ORDER BY total_revenue DESC
            """,
            sales_params,
        )

        if not q2.empty:
            fig = px.pie(
                q2,
                names="fare_class",
                values="total_revenue",
                hole=.58,
                color_discrete_sequence=MULTI_COLORS,
            )
            fig.update_traces(textinfo="percent+label")
            display_chart(fig, 400)

    # Q3
    with c2:
        question_tag(3)
        st.subheader("รายได้จากการขายตั๋วเปลี่ยนแปลงอย่างไรในแต่ละเดือน?")

        q3 = query_df(
            f"""
            SELECT
                d.year,
                d.month,
                SUM(f.amount) AS total_revenue
            FROM fact_ticket_sales f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {sales_where}
            GROUP BY d.year, d.month
            ORDER BY d.year, d.month
            """,
            sales_params,
        )

        if not q3.empty:
            q3["period"] = q3["year"].astype(str) + "-" + q3["month"].astype(str).str.zfill(2)

            fig = px.area(
                q3,
                x="period",
                y="total_revenue",
                markers=True,
            )
            fig.update_traces(line=dict(width=4))
            fig.update_layout(xaxis_title="Month", yaxis_title="Revenue")
            display_chart(fig, 400)

    # Q4
    question_tag(4)
    st.subheader("ภูมิภาคต้นทาง–ปลายทางคู่ใดมีความต้องการเดินทางสูงที่สุด?")

    q4 = query_df(
        f"""
        SELECT
            dep.analysis_region AS departure_region,
            arr.analysis_region AS arrival_region,
            SUM(f.ticket_flight_count) AS ticket_flights,
            SUM(f.amount) AS total_revenue
        FROM fact_ticket_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {sales_where}
          AND dep.analysis_region IS NOT NULL
          AND arr.analysis_region IS NOT NULL
        GROUP BY dep.analysis_region, arr.analysis_region
        ORDER BY ticket_flights DESC
        """,
        sales_params,
    )

    if not q4.empty:
        q4["region_pair"] = q4["departure_region"] + " → " + q4["arrival_region"]

        fig = px.bar(
            q4.sort_values("ticket_flights"),
            x="ticket_flights",
            y="region_pair",
            orientation="h",
            color="ticket_flights",
            color_continuous_scale="Teal",
            hover_data=["total_revenue"],
        )
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Ticket Flight", yaxis_title="")
        display_chart(fig)

        download_df(q4, "ดาวน์โหลด Q4", "Q4_region_pair_demand.csv")

# =========================================================
# TAB 2 — Q5-Q6
# =========================================================
with tab2:
    st.markdown('<div class="section-title">Capacity Utilization</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Q5–Q6: Boarded Load และ Booked-but-not-boarded Gap</div>',
        unsafe_allow_html=True,
    )

    # Q5
    question_tag(5)
    st.subheader("เส้นทางใดมีอัตราการใช้ที่นั่งจริงสูงและต่ำที่สุด?")

    q5 = query_df(
        f"""
        SELECT
            dep.airport_code || ' → ' || arr.airport_code AS route,
            SUM(f.boarded_count) AS boarded_count,
            SUM(f.seat_capacity) AS seat_capacity,
            COUNT(*) AS flight_count,
            ROUND(
                100.0 * SUM(f.boarded_count) / NULLIF(SUM(f.seat_capacity),0),
                2
            ) AS boarded_load_pct
        FROM fact_seat_utilization f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {seat_where}
        GROUP BY dep.airport_code, arr.airport_code
        ORDER BY boarded_load_pct DESC
        """,
        seat_params,
    )

    if not q5.empty:
        q5_display = pd.concat([q5.head(10), q5.tail(10)]).drop_duplicates()

        fig = px.bar(
            q5_display.sort_values("boarded_load_pct"),
            x="boarded_load_pct",
            y="route",
            orientation="h",
            color="boarded_load_pct",
            color_continuous_scale="Teal",
            hover_data=["boarded_count", "seat_capacity", "flight_count"],
        )
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Boarded Load (%)", yaxis_title="")
        display_chart(fig, 520)

        download_df(q5, "ดาวน์โหลด Q5", "Q5_route_boarded_load.csv")

    # Q6
    question_tag(6)
    st.subheader("เที่ยวบินใดมีช่องว่างระหว่างจำนวนตั๋วที่ขายกับผู้โดยสารที่ขึ้นเครื่องจริงมากที่สุด?")

    q6 = query_df(
        f"""
        SELECT
            f.flight_id,
            dep.airport_code || ' → ' || arr.airport_code AS route,
            f.ticket_flight_count,
            f.boarded_count,
            f.booked_not_boarded_count,
            f.seat_capacity,
            f.boarded_load_pct
        FROM fact_seat_utilization f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {seat_where}
        ORDER BY f.booked_not_boarded_count DESC
        LIMIT 20
        """,
        seat_params,
    )

    st.caption(
        "Booked-but-not-boarded เป็น proxy จากข้อมูลตั๋วและ Boarding Pass "
        "ไม่ควรสรุปว่าเป็น no-show ทุกกรณี"
    )

    st.dataframe(q6, width="stretch", hide_index=True)
    download_df(q6, "ดาวน์โหลด Q6", "Q6_booked_not_boarded_gap.csv")

# =========================================================
# TAB 3 — Q7-Q9
# =========================================================
with tab3:
    st.markdown('<div class="section-title">Travel Pattern</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Q7–Q9: Daypart, Weekday vs Weekend และ Booking Lead Time</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    # Q7
    with c1:
        question_tag(7)
        st.subheader("ช่วงเวลาใดของวันมีจำนวนเที่ยวบินและผู้โดยสารสูงที่สุด?")

        q7 = query_df(
            f"""
            SELECT
                f.{DAYPART_OPS} AS departure_daypart,
                SUM(f.flight_count) AS total_flights,
                SUM(f.boarded_count) AS boarded_passengers
            FROM fact_flight_operations f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {ops_where}
              AND f.{DAYPART_OPS} IS NOT NULL
            GROUP BY f.{DAYPART_OPS}
            ORDER BY boarded_passengers DESC
            """,
            ops_params,
        )

        if not q7.empty:
            fig = px.bar(
                q7,
                x="departure_daypart",
                y="boarded_passengers",
                color="total_flights",
                color_continuous_scale="Blues",
                hover_data=["total_flights"],
            )
            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Daypart",
                yaxis_title="Boarded Passengers",
            )
            display_chart(fig, 400)

    # Q8
    with c2:
        question_tag(8)
        st.subheader("วันธรรมดากับวันหยุดสุดสัปดาห์มีความต้องการเดินทางต่างกันอย่างไร?")

        q8 = query_df(
            f"""
            SELECT
                CASE
                    WHEN f.{WEEKEND_OPS} THEN 'Weekend'
                    ELSE 'Weekday'
                END AS day_type,
                SUM(f.flight_count) AS total_flights,
                SUM(f.boarded_count) AS boarded_passengers,
                ROUND(AVG(f.boarded_count),2) AS avg_boarded_per_flight
            FROM fact_flight_operations f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {ops_where}
            GROUP BY f.{WEEKEND_OPS}
            ORDER BY boarded_passengers DESC
            """,
            ops_params,
        )

        if not q8.empty:
            fig = px.bar(
                q8,
                x="day_type",
                y="boarded_passengers",
                color="day_type",
                color_discrete_sequence=[BLUE, CYAN],
                hover_data=["total_flights", "avg_boarded_per_flight"],
            )
            fig.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="Boarded Passengers",
            )
            display_chart(fig, 400)

    # Q9
    question_tag(9)
    st.subheader("ผู้โดยสารมักจองตั๋วล่วงหน้ากี่วัน และแตกต่างกันอย่างไรในแต่ละ Fare Class?")

    q9 = query_df(
        f"""
        SELECT
            fc.fare_class,
            ROUND(AVG(f.booking_lead_days),2) AS avg_booking_lead_days,
            MEDIAN(f.booking_lead_days) AS median_booking_lead_days,
            MIN(f.booking_lead_days) AS min_booking_lead_days,
            MAX(f.booking_lead_days) AS max_booking_lead_days,
            SUM(f.ticket_flight_count) AS ticket_flights
        FROM fact_ticket_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {sales_where}
          AND f.booking_lead_days IS NOT NULL
        GROUP BY fc.fare_class
        ORDER BY avg_booking_lead_days DESC
        """,
        sales_params,
    )

    if not q9.empty:
        fig = px.bar(
            q9,
            x="fare_class",
            y="avg_booking_lead_days",
            color="fare_class",
            color_discrete_sequence=MULTI_COLORS,
            hover_data=[
                "median_booking_lead_days",
                "min_booking_lead_days",
                "max_booking_lead_days",
                "ticket_flights",
            ],
        )
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Average Booking Lead Days")
        display_chart(fig)

        if (q9["min_booking_lead_days"] < 0).any():
            st.warning(
                "พบ booking_lead_days ติดลบบางรายการ "
                "ควรระบุเป็น Data Quality Issue และตรวจสอบก่อนสรุป Q9 ขั้นสุดท้าย"
            )

        download_df(q9, "ดาวน์โหลด Q9", "Q9_booking_lead_by_fare_class.csv")

# =========================================================
# TAB 4 — Q10-Q12
# =========================================================
with tab4:
    st.markdown('<div class="section-title">Fleet & Operations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Q10–Q12: Aircraft Usage, Route Delay และ Region × Daypart Delay</div>',
        unsafe_allow_html=True,
    )

    # Q10
    question_tag(10)
    st.subheader("Aircraft Manufacturer และ Model ใดถูกใช้งานกับเที่ยวบินมากที่สุด?")

    q10 = query_df(
        f"""
        SELECT
            a.manufacturer,
            a.model AS aircraft_model,
            SUM(f.flight_count) AS total_flights
        FROM fact_flight_operations f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {ops_where}
        GROUP BY a.manufacturer, a.model
        ORDER BY total_flights DESC
        """,
        ops_params,
    )

    if not q10.empty:
        q10["aircraft"] = (
            q10["manufacturer"].fillna("Unknown")
            + " — "
            + q10["aircraft_model"].fillna("Unknown")
        )

        fig = px.bar(
            q10.sort_values("total_flights"),
            x="total_flights",
            y="aircraft",
            orientation="h",
            color="total_flights",
            color_continuous_scale="Purples",
        )
        fig.update_layout(coloraxis_showscale=False, xaxis_title="Flights", yaxis_title="")
        display_chart(fig)

        download_df(q10, "ดาวน์โหลด Q10", "Q10_aircraft_usage.csv")

    # Q11
    question_tag(11)
    st.subheader("เส้นทางใดมีความล่าช้าในการออกเดินทางและถึงปลายทางเฉลี่ยสูงที่สุด?")

    q11 = query_df(
        f"""
        SELECT
            dep.airport_code || ' → ' || arr.airport_code AS route,
            ROUND(AVG(f.departure_delay_minutes),2) AS avg_departure_delay,
            ROUND(AVG(f.arrival_delay_minutes),2) AS avg_arrival_delay,
            SUM(f.flight_count) AS total_flights
        FROM fact_flight_operations f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {ops_where}
          AND (
              f.departure_delay_minutes IS NOT NULL
              OR f.arrival_delay_minutes IS NOT NULL
          )
        GROUP BY dep.airport_code, arr.airport_code
        ORDER BY avg_departure_delay DESC
        LIMIT 15
        """,
        ops_params,
    )

    if not q11.empty:
        fig = px.bar(
            q11.sort_values("avg_departure_delay"),
            x="avg_departure_delay",
            y="route",
            orientation="h",
            color="avg_departure_delay",
            color_continuous_scale="Oranges",
            hover_data=["avg_arrival_delay", "total_flights"],
        )
        fig.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Avg Departure Delay (minutes)",
            yaxis_title="",
        )
        display_chart(fig)

        st.caption(
            "ควรดู total_flights ร่วมด้วย เพราะเส้นทางที่มีค่า delay สูงบางเส้นทางอาจมีจำนวนเที่ยวบินน้อย"
        )

        download_df(q11, "ดาวน์โหลด Q11", "Q11_route_delay.csv")

    # Q12
    question_tag(12)
    st.subheader("ในแต่ละภูมิภาคและช่วงเวลาของวัน ช่วงใดมี Departure Delay เฉลี่ยสูงที่สุด?")

    q12 = query_df(
        f"""
        SELECT
            dep.analysis_region AS departure_region,
            f.{DAYPART_OPS} AS departure_daypart,
            ROUND(AVG(f.departure_delay_minutes),2) AS avg_departure_delay,
            SUM(f.flight_count) AS total_flights
        FROM fact_flight_operations f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {ops_where}
          AND f.departure_delay_minutes IS NOT NULL
          AND dep.analysis_region IS NOT NULL
          AND f.{DAYPART_OPS} IS NOT NULL
        GROUP BY dep.analysis_region, f.{DAYPART_OPS}
        ORDER BY avg_departure_delay DESC
        """,
        ops_params,
    )

    if not q12.empty:
        fig = px.bar(
            q12,
            x="departure_region",
            y="avg_departure_delay",
            color="departure_daypart",
            barmode="group",
            color_discrete_sequence=MULTI_COLORS,
            hover_data=["total_flights"],
        )
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Avg Departure Delay (minutes)",
            legend_title="Daypart",
        )
        display_chart(fig)

        download_df(q12, "ดาวน์โหลด Q12", "Q12_region_daypart_delay.csv")

# =========================================================
# TAB 5 — Q13-Q15
# =========================================================
with tab5:
    st.markdown('<div class="section-title">Multidimensional Decision Support</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-desc">Q13–Q15: Route × Fare, Region × Aircraft และ Route × Daypart</div>',
        unsafe_allow_html=True,
    )

    # Q13
    question_tag(13)
    st.subheader("ในแต่ละเส้นทาง Fare Class ใดสร้างรายได้สูงเมื่อเทียบกับจำนวนตั๋วที่ขาย?")

    q13 = query_df(
        f"""
        WITH route_fare AS (
            SELECT
                dep.airport_code || ' → ' || arr.airport_code AS route,
                fc.fare_class,
                SUM(f.amount) AS total_revenue,
                SUM(f.ticket_flight_count) AS ticket_count,
                ROUND(
                    SUM(f.amount)
                    / NULLIF(SUM(f.ticket_flight_count),0),
                    2
                ) AS revenue_per_ticket
            FROM fact_ticket_sales f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {sales_where}
            GROUP BY dep.airport_code, arr.airport_code, fc.fare_class
            HAVING SUM(f.ticket_flight_count) > 0
        ),
        thresholds AS (
            SELECT
                MEDIAN(total_revenue) AS median_revenue,
                MEDIAN(ticket_count) AS median_ticket_count
            FROM route_fare
        )
        SELECT
            rf.route,
            rf.fare_class,
            rf.total_revenue,
            rf.ticket_count,
            rf.revenue_per_ticket
        FROM route_fare rf
        CROSS JOIN thresholds t
        WHERE
            rf.total_revenue >= t.median_revenue
            AND rf.ticket_count <= t.median_ticket_count
        ORDER BY
            rf.total_revenue DESC,
            rf.revenue_per_ticket DESC
        LIMIT 20
        """,
        sales_params,
    )

    if not q13.empty:
        q13["route_fare"] = q13["route"] + " • " + q13["fare_class"]

        fig = px.bar(
            q13.sort_values("revenue_per_ticket"),
            x="revenue_per_ticket",
            y="route_fare",
            orientation="h",
            color="fare_class",
            color_discrete_sequence=MULTI_COLORS,
            hover_data=["total_revenue", "ticket_count"],
        )
        fig.update_layout(
            xaxis_title="Revenue per Ticket",
            yaxis_title="Route × Fare Class",
            legend_title="Fare Class",
        )
        display_chart(fig, 520)

        st.caption(
            "Q13 คัดเลือก Route × Fare Class ที่มี total_revenue ไม่น้อยกว่าค่ามัธยฐาน "
            "และ ticket_count ไม่เกินค่ามัธยฐานของกลุ่มทั้งหมด แล้วใช้ Revenue per Ticket ประกอบการตีความ"
        )

        download_df(q13, "ดาวน์โหลด Q13", "Q13_route_fare_efficiency.csv")

    # Q14
    question_tag(14)
    st.subheader("ในแต่ละภูมิภาค Aircraft Manufacturer/Model ใดมีอัตราการใช้ที่นั่งจริงสูงที่สุด?")

    q14 = query_df(
        f"""
        SELECT
            dep.analysis_region AS departure_region,
            a.manufacturer,
            a.model AS aircraft_model,
            SUM(f.boarded_count) AS boarded_count,
            SUM(f.seat_capacity) AS seat_capacity,
            COUNT(*) AS flight_count,
            ROUND(
                100.0 * SUM(f.boarded_count) / NULLIF(SUM(f.seat_capacity),0),
                2
            ) AS boarded_load_pct
        FROM fact_seat_utilization f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {seat_where}
          AND dep.analysis_region IS NOT NULL
          AND a.model IS NOT NULL
        GROUP BY dep.analysis_region, a.manufacturer, a.model
        ORDER BY departure_region, boarded_load_pct DESC
        """,
        seat_params,
    )

    if not q14.empty:
        fig = px.bar(
            q14,
            x="departure_region",
            y="boarded_load_pct",
            color="aircraft_model",
            barmode="group",
            hover_data=[
                "manufacturer",
                "boarded_count",
                "seat_capacity",
                "flight_count",
            ],
        )
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Boarded Load (%)",
            legend_title="Aircraft Model",
        )
        display_chart(fig, 500)

        download_df(q14, "ดาวน์โหลด Q14", "Q14_region_aircraft_load.csv")

    # Q15
    question_tag(15)
    st.subheader("เส้นทางและช่วงเวลาใดมี Demand สูงและ Boarded Load สูงเมื่อเทียบกับข้อมูลชุดนี้?")

    q15 = query_df(
        f"""
        WITH monthly_route_daypart AS (
            SELECT
                d.year,
                d.month,
                dep.airport_code || ' → ' || arr.airport_code AS route,
                f.{DAYPART_SEAT} AS departure_daypart,
                SUM(f.ticket_flight_count) AS ticket_flight_count,
                SUM(f.boarded_count) AS boarded_count,
                SUM(f.seat_capacity) AS seat_capacity,
                COUNT(*) AS flight_count,
                ROUND(
                    100.0 * SUM(f.boarded_count) / NULLIF(SUM(f.seat_capacity),0),
                    2
                ) AS boarded_load_pct
            FROM fact_seat_utilization f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {seat_where}
              AND f.{DAYPART_SEAT} IS NOT NULL
            GROUP BY
                d.year,
                d.month,
                dep.airport_code,
                arr.airport_code,
                f.{DAYPART_SEAT}
        ),
        ranked AS (
            SELECT
                *,
                AVG(boarded_count) OVER () AS avg_demand,
                AVG(boarded_load_pct) OVER () AS avg_load
            FROM monthly_route_daypart
        )
        SELECT
            route,
            departure_daypart,
            COUNT(*) AS active_months,
            SUM(ticket_flight_count) AS ticket_flight_count,
            SUM(boarded_count) AS boarded_count,
            SUM(seat_capacity) AS seat_capacity,
            SUM(flight_count) AS flight_count,
            ROUND(AVG(boarded_load_pct),2) AS avg_boarded_load_pct
        FROM ranked
        WHERE
            boarded_count >= avg_demand
            AND boarded_load_pct >= avg_load
        GROUP BY route, departure_daypart
        HAVING COUNT(*) >= 2
        ORDER BY
            avg_boarded_load_pct DESC,
            boarded_count DESC
        LIMIT 30
        """,
        seat_params,
    )

    if not q15.empty:
        fig = px.scatter(
            q15,
            x="boarded_count",
            y="avg_boarded_load_pct",
            size="ticket_flight_count",
            color="departure_daypart",
            hover_name="route",
            hover_data=["active_months", "flight_count", "seat_capacity"],
            color_discrete_sequence=MULTI_COLORS,
        )
        fig.update_layout(
            xaxis_title="Boarded Passengers (Demand)",
            yaxis_title="Average Boarded Load (%)",
            legend_title="Daypart",
        )
        display_chart(fig, 520)

        st.caption(
            "Q15 เลือก Route × Daypart ที่มีทั้ง Demand และ Boarded Load สูงกว่าค่าเฉลี่ยของแต่ละเดือน "
            "และเกิดซ้ำอย่างน้อย 2 เดือน เพื่อสะท้อนความต่อเนื่องมากกว่าการดูค่า Aggregate เพียงครั้งเดียว"
        )

        download_df(q15, "ดาวน์โหลด Q15", "Q15_route_daypart_demand_load.csv")

    # Drill-down
    st.divider()
    st.subheader("Drill-down: Route Detail")

    route_options = query_df(
        f"""
        SELECT DISTINCT
            dep.airport_code || ' → ' || arr.airport_code AS route
        FROM fact_ticket_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {sales_where}
        ORDER BY route
        """,
        sales_params,
    )

    if not route_options.empty:
        selected_route = st.selectbox(
            "เลือกเส้นทางเพื่อ Drill-down",
            route_options["route"].tolist(),
        )

        selected_dep, selected_arr = selected_route.split(" → ")

        drill_conditions = list(sales_conditions)
        drill_params = list(sales_params)

        drill_conditions.extend(
            [
                "dep.airport_code = ?",
                "arr.airport_code = ?",
            ]
        )
        drill_params.extend([selected_dep, selected_arr])

        drill_where = " AND ".join(drill_conditions)

        drill_df = query_df(
            f"""
            SELECT
                fc.fare_class,
                SUM(f.amount) AS total_revenue,
                SUM(f.ticket_flight_count) AS ticket_flights,
                ROUND(
                    SUM(f.amount) / NULLIF(SUM(f.ticket_flight_count),0),
                    2
                ) AS revenue_per_ticket
            FROM fact_ticket_sales f
            JOIN dim_date d ON f.date_key = d.date_key
            JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
            JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
            JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
            JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
            WHERE {drill_where}
            GROUP BY fc.fare_class
            ORDER BY total_revenue DESC
            """,
            drill_params,
        )

        d1, d2 = st.columns([2, 1])

        with d1:
            if not drill_df.empty:
                fig = px.bar(
                    drill_df,
                    x="fare_class",
                    y="total_revenue",
                    color="fare_class",
                    color_discrete_sequence=MULTI_COLORS,
                    hover_data=["ticket_flights", "revenue_per_ticket"],
                )
                fig.update_layout(
                    showlegend=False,
                    xaxis_title="Fare Class",
                    yaxis_title="Revenue",
                )
                display_chart(fig, 360)

        with d2:
            st.dataframe(drill_df, width="stretch", hide_index=True)
            download_df(
                drill_df,
                "ดาวน์โหลด Route Detail",
                f"{selected_dep}_{selected_arr}_route_detail.csv",
            )

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="footer-premium">
  <div>
    <b>✈ Airline Data Warehouse</b><br>
    DuckDB • dbt • Streamlit • Plotly • Q1–Q15 • Interactive Dashboard
  </div>
  <div>Analytics Ready</div>
</div>
""",
    unsafe_allow_html=True,
)

con.close()
