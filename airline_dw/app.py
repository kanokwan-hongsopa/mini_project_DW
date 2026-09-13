import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Airline Analytics Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f6f8fc;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #172554 100%);
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    section[data-testid="stSidebar"] input {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0f172a !important;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            120deg,
            #0f172a 0%,
            #1e3a8a 45%,
            #2563eb 100%
        );
        border-radius: 24px;
        padding: 32px 36px;
        margin-bottom: 25px;
        box-shadow: 0 14px 40px rgba(30, 64, 175, 0.20);
    }

    .hero-title {
        color: white;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #dbeafe;
        font-size: 16px;
        margin: 0;
    }

    /* Section headings */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .section-desc {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 16px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 19px 20px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 800;
    }

    /* Chart containers */
    div[data-testid="stPlotlyChart"] {
        background: white;
        border: 1px solid #e5e7eb;
        padding: 10px;
        border-radius: 18px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 650;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* Small badge */
    .bq {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #dbeafe;
        color: #1d4ed8;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }

</style>
""", unsafe_allow_html=True)


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
    return con.execute(sql, params).fetchdf()


# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">✈ Airline Analytics</div>
    <p class="hero-subtitle">
        Data Warehouse Dashboard • Ticket Sales • Routes • Aircraft • Flight Operations
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTER DATA
# =========================================================

date_row = con.execute("""
    SELECT
        MIN(full_date),
        MAX(full_date)
    FROM dim_date
""").fetchone()

min_date = pd.to_datetime(date_row[0]).date()
max_date = pd.to_datetime(date_row[1]).date()


airports = query_df("""
    SELECT airport_code
    FROM dim_airport
    ORDER BY airport_code
""")["airport_code"].tolist()


fare_classes = query_df("""
    SELECT fare_class
    FROM dim_fare_class
    ORDER BY fare_class
""")["fare_class"].tolist()


aircraft_models = query_df("""
    SELECT DISTINCT model
    FROM dim_aircraft
    ORDER BY model
""")["model"].tolist()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("ตัวกรองข้อมูล")
st.sidebar.caption("เลือกเงื่อนไขเพื่อวิเคราะห์ข้อมูลแบบ Interactive")

start_date = st.sidebar.date_input(
    "วันที่เริ่มต้น",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "วันที่สิ้นสุด",
    max_date,
    min_value=min_date,
    max_value=max_date
)

departure = st.sidebar.selectbox(
    "สนามบินต้นทาง",
    ["ทั้งหมด"] + airports
)

arrival = st.sidebar.selectbox(
    "สนามบินปลายทาง",
    ["ทั้งหมด"] + airports
)

fare = st.sidebar.selectbox(
    "ชั้นโดยสาร",
    ["ทั้งหมด"] + fare_classes
)

aircraft = st.sidebar.selectbox(
    "รุ่นเครื่องบิน",
    ["ทั้งหมด"] + aircraft_models
)


if start_date > end_date:
    st.error("วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด")
    st.stop()


if (
    departure != "ทั้งหมด"
    and arrival != "ทั้งหมด"
    and departure == arrival
):
    st.sidebar.warning(
        "สนามบินต้นทางและปลายทางเป็นสนามบินเดียวกัน"
    )


# =========================================================
# FILTER BUILDERS
# =========================================================

sales_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

sales_params = [
    start_date,
    end_date
]

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


ops_conditions = [
    "d.full_date BETWEEN ? AND ?"
]

ops_params = [
    start_date,
    end_date
]

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


seat_conditions = []
seat_params = []

if fare != "ทั้งหมด":
    seat_conditions.append("fc.fare_class = ?")
    seat_params.append(fare)

if aircraft != "ทั้งหมด":
    seat_conditions.append("a.model = ?")
    seat_params.append(aircraft)

seat_where = ""

if seat_conditions:
    seat_where = "WHERE " + " AND ".join(seat_conditions)


# =========================================================
# KPI - Q1 / Q2
# =========================================================

sales_kpi = con.execute(
    f"""
    SELECT
        COALESCE(SUM(f.amount), 0),
        COALESCE(SUM(f.ticket_flight_count), 0)

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

    WHERE {sales_where}
    """,
    sales_params
).fetchone()


ops_kpi = con.execute(
    f"""
    SELECT
        COALESCE(SUM(f.flight_count), 0),

        COALESCE(
            AVG(
                CASE
                    WHEN f.departure_delay_minutes > 0
                    THEN f.departure_delay_minutes
                END
            ),
            0
        )

    FROM fact_flight_operations f

    JOIN dim_date d
        ON f.date_key = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key = arr.airport_key

    JOIN dim_aircraft a
        ON f.aircraft_key = a.aircraft_key

    WHERE {ops_where}
    """,
    ops_params
).fetchone()


k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "ยอดขายตั๋วรวม",
    f"{sales_kpi[0]:,.0f}"
)

k2.metric(
    "Ticket Flight",
    f"{sales_kpi[1]:,.0f}"
)

k3.metric(
    "เที่ยวบินทั้งหมด",
    f"{ops_kpi[0]:,.0f}"
)

k4.metric(
    "ดีเลย์เฉลี่ย",
    f"{ops_kpi[1]:,.1f} นาที"
)


st.write("")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "ภาพรวมยอดขาย",
    "สนามบินและเส้นทาง",
    "เครื่องบิน",
    "การดำเนินงานเที่ยวบิน",
    "วิเคราะห์หลายมิติ"
])


# =========================================================
# TAB 1
# Q3 Q4 Q5
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-title">ภาพรวมยอดขาย</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">วิเคราะห์รายได้ จำนวนตั๋ว และแนวโน้มตามช่วงเวลา</div>',
        unsafe_allow_html=True
    )


    fare_sales = query_df(
        f"""
        SELECT
            fc.fare_class,
            SUM(f.amount) AS total_sales,
            SUM(f.ticket_flight_count) AS ticket_flights

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

        WHERE {sales_where}

        GROUP BY fc.fare_class

        ORDER BY total_sales DESC
        """,
        sales_params
    )


    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<span class="bq">Business Question Q3</span>',
            unsafe_allow_html=True
        )

        st.subheader("ยอดขายตามชั้นโดยสาร")

        fig = px.pie(
            fare_sales,
            values="total_sales",
            names="fare_class",
            hole=0.58
        )

        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend_title="ชั้นโดยสาร"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        st.markdown(
            '<span class="bq">Business Question Q4</span>',
            unsafe_allow_html=True
        )

        st.subheader("จำนวน Ticket Flight ตามชั้นโดยสาร")

        fig = px.bar(
            fare_sales.sort_values("ticket_flights"),
            x="ticket_flights",
            y="fare_class",
            orientation="h"
        )

        fig.update_layout(
            xaxis_title="จำนวน Ticket Flight",
            yaxis_title="",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    monthly_sales = query_df(
        f"""
        SELECT
            d.year,
            d.month,
            d.month_name,
            SUM(f.amount) AS total_sales

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

        WHERE {sales_where}

        GROUP BY
            d.year,
            d.month,
            d.month_name

        ORDER BY
            d.year,
            d.month
        """,
        sales_params
    )


    if not monthly_sales.empty:

        monthly_sales["period"] = (
            monthly_sales["year"].astype(str)
            + "-"
            + monthly_sales["month"].astype(str).str.zfill(2)
        )


        st.markdown(
            '<span class="bq">Business Question Q5</span>',
            unsafe_allow_html=True
        )

        st.subheader("แนวโน้มยอดขายตามช่วงเวลา")

        fig = px.line(
            monthly_sales,
            x="period",
            y="total_sales",
            markers=True
        )

        fig.update_layout(
            xaxis_title="ช่วงเวลา",
            yaxis_title="ยอดขาย",
            margin=dict(l=20, r=20, t=30, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 2
# Q6 Q7 Q8 Q9
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-title">สนามบินและเส้นทาง</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">เปรียบเทียบสนามบินต้นทาง ปลายทาง และเส้นทางสำคัญ</div>',
        unsafe_allow_html=True
    )


    departure_df = query_df(
        f"""
        SELECT
            dep.airport_code,
            SUM(f.ticket_flight_count) AS ticket_flights

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

        WHERE {sales_where}

        GROUP BY dep.airport_code

        ORDER BY ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    arrival_df = query_df(
        f"""
        SELECT
            arr.airport_code,
            SUM(f.ticket_flight_count) AS ticket_flights

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

        WHERE {sales_where}

        GROUP BY arr.airport_code

        ORDER BY ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<span class="bq">Business Question Q6</span>',
            unsafe_allow_html=True
        )

        st.subheader("สนามบินต้นทางที่มี Ticket Flight สูงสุด")

        fig = px.bar(
            departure_df.sort_values("ticket_flights"),
            x="ticket_flights",
            y="airport_code",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        st.markdown(
            '<span class="bq">Business Question Q7</span>',
            unsafe_allow_html=True
        )

        st.subheader("สนามบินปลายทางที่มี Ticket Flight สูงสุด")

        fig = px.bar(
            arrival_df.sort_values("ticket_flights"),
            x="ticket_flights",
            y="airport_code",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    route_df = query_df(
        f"""
        SELECT
            dep.airport_code || ' → ' ||
            arr.airport_code AS route,

            SUM(f.ticket_flight_count) AS ticket_flights,

            SUM(f.amount) AS total_sales

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

        WHERE {sales_where}

        GROUP BY
            dep.airport_code,
            arr.airport_code

        ORDER BY ticket_flights DESC

        LIMIT 10
        """,
        sales_params
    )


    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<span class="bq">Business Question Q8</span>',
            unsafe_allow_html=True
        )

        st.subheader("เส้นทางที่มี Ticket Flight สูงสุด")

        fig = px.bar(
            route_df.sort_values("ticket_flights"),
            x="ticket_flights",
            y="route",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    route_sales = route_df.sort_values(
        "total_sales",
        ascending=False
    )


    with c2:

        st.markdown(
            '<span class="bq">Business Question Q9</span>',
            unsafe_allow_html=True
        )

        st.subheader("เส้นทางที่สร้างยอดขายสูงสุด")

        fig = px.bar(
            route_sales.sort_values("total_sales"),
            x="total_sales",
            y="route",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 3
# Q10 Q11 Q12
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-title">วิเคราะห์เครื่องบิน</div>',
        unsafe_allow_html=True
    )


    usage = query_df(
        f"""
        SELECT
            a.model,
            SUM(f.flight_count) AS total_flights

        FROM fact_flight_operations f

        JOIN dim_date d
            ON f.date_key = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key = a.aircraft_key

        WHERE {ops_where}

        GROUP BY a.model

        ORDER BY total_flights DESC
        """,
        ops_params
    )


    seat_df = query_df(
        f"""
        SELECT
            a.model,
            fc.fare_class,
            SUM(f.seat_count) AS seats

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
            '<span class="bq">Business Question Q10</span>',
            unsafe_allow_html=True
        )

        st.subheader("รุ่นเครื่องบินที่ถูกใช้มากที่สุด")

        fig = px.bar(
            usage.sort_values("total_flights"),
            x="total_flights",
            y="model",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    total_seats = (
        seat_df
        .groupby("model", as_index=False)["seats"]
        .sum()
    )


    with c2:

        st.markdown(
            '<span class="bq">Business Question Q11</span>',
            unsafe_allow_html=True
        )

        st.subheader("จำนวนที่นั่งของเครื่องบินแต่ละรุ่น")

        fig = px.bar(
            total_seats.sort_values("seats"),
            x="seats",
            y="model",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown(
        '<span class="bq">Business Question Q12</span>',
        unsafe_allow_html=True
    )

    st.subheader("โครงสร้างที่นั่งตามชั้นโดยสาร")

    fig = px.bar(
        seat_df,
        x="model",
        y="seats",
        color="fare_class",
        barmode="stack"
    )

    fig.update_layout(
        legend_title="ชั้นโดยสาร"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TAB 4
# Q13 Q14
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-title">การดำเนินงานเที่ยวบิน</div>',
        unsafe_allow_html=True
    )


    status_df = query_df(
        f"""
        SELECT
            s.status_name,
            SUM(f.flight_count) AS total_flights

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

        WHERE {ops_where}

        GROUP BY s.status_name
        """,
        ops_params
    )


    delay_df = query_df(
        f"""
        SELECT
            dep.airport_code,

            ROUND(
                AVG(f.departure_delay_minutes),
                2
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
            AND f.departure_delay_minutes > 0

        GROUP BY dep.airport_code

        ORDER BY avg_delay DESC

        LIMIT 10
        """,
        ops_params
    )


    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            '<span class="bq">Business Question Q13</span>',
            unsafe_allow_html=True
        )

        st.subheader("สัดส่วนสถานะเที่ยวบิน")

        fig = px.pie(
            status_df,
            values="total_flights",
            names="status_name",
            hole=0.55
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with c2:

        st.markdown(
            '<span class="bq">Business Question Q14</span>',
            unsafe_allow_html=True
        )

        st.subheader("สนามบินที่มีความล่าช้าเฉลี่ยสูงสุด")

        fig = px.bar(
            delay_df.sort_values("avg_delay"),
            x="avg_delay",
            y="airport_code",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 5
# Q15
# =========================================================

with tab5:

    st.markdown(
        '<div class="section-title">Multidimensional Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<span class="bq">Business Question Q15</span>',
        unsafe_allow_html=True
    )

    st.subheader(
        "เส้นทางและชั้นโดยสารที่สร้างยอดขายสูงที่สุดในแต่ละเดือน"
    )


    monthly_top = query_df(
        f"""
        WITH sales_summary AS (

            SELECT
                d.year,
                d.month,
                d.month_name,

                dep.airport_code AS departure_airport,
                arr.airport_code AS arrival_airport,

                fc.fare_class,

                SUM(f.amount) AS total_sales

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

            WHERE {sales_where}

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
                    PARTITION BY year, month
                    ORDER BY total_sales DESC
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

        WHERE sales_rank = 1

        ORDER BY
            year,
            month
        """,
        sales_params
    )


    if not monthly_top.empty:

        monthly_top["period"] = (
            monthly_top["year"].astype(str)
            + "-"
            + monthly_top["month"].astype(str).str.zfill(2)
        )


        fig = px.bar(
            monthly_top,
            x="period",
            y="total_sales",
            color="fare_class",
            hover_data=[
                "departure_airport",
                "arrival_airport"
            ]
        )

        fig.update_layout(
            xaxis_title="ช่วงเวลา",
            yaxis_title="ยอดขาย",
            legend_title="ชั้นโดยสาร"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.dataframe(
            monthly_top[
                [
                    "year",
                    "month_name",
                    "departure_airport",
                    "arrival_airport",
                    "fare_class",
                    "total_sales"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "ไม่พบข้อมูลตามตัวกรองที่เลือก"
        )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:13px;
        padding:25px 0 10px 0;
    ">
        Airline Data Warehouse Project • Streamlit + DuckDB + dbt
    </div>
    """,
    unsafe_allow_html=True
)

con.close()