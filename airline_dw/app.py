import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
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
# THEME
# =========================================================

COLORS = [
    "#2563EB",
    "#7C3AED",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
]


st.markdown("""
<style>

/* ---------------- MAIN ---------------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #eff6ff 0, transparent 26%),
        radial-gradient(circle at 90% 5%, #eef2ff 0, transparent 25%),
        #f8fafc;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}


/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b1120 0%,
            #111c3f 45%,
            #172554 100%
        );
    border-right: 1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #ffffff !important;
}

/* ทำให้ช่องวันที่อ่านได้ */
section[data-testid="stSidebar"] input {
    color: #0f172a !important;
    background: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background: #ffffff !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #0f172a !important;
}


/* ---------------- HERO ---------------- */

.hero {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            120deg,
            #0f172a 0%,
            #172554 35%,
            #1d4ed8 72%,
            #2563eb 100%
        );

    border-radius: 26px;
    padding: 34px 38px;
    margin-bottom: 24px;

    box-shadow:
        0 20px 55px rgba(30, 64, 175, .20);
}

.hero::after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -70px;
    top: -110px;
    border-radius: 50%;
    background: rgba(255,255,255,.08);
}

.hero-badge {
    display: inline-block;
    padding: 5px 12px;

    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.20);

    border-radius: 999px;

    color: #dbeafe;
    font-size: 12px;
    font-weight: 700;

    margin-bottom: 12px;
}

.hero-title {
    color: white;
    font-size: 39px;
    font-weight: 850;
    line-height: 1.15;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #dbeafe;
    font-size: 16px;
    margin: 0;
}


/* ---------------- METRICS ---------------- */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,1),
            rgba(248,250,252,1)
        );

    border: 1px solid #e2e8f0;
    border-radius: 20px;

    padding: 18px 20px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, .06);

    min-height: 118px;
}

div[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 650;
}

div[data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 850;
    font-size: 1.85rem;
}


/* ---------------- HEADINGS ---------------- */

.section-title {
    font-size: 27px;
    font-weight: 850;
    color: #0f172a;

    margin-top: 8px;
    margin-bottom: 3px;
}

.section-desc {
    color: #64748b;
    font-size: 14px;

    margin-bottom: 18px;
}


/* ---------------- BUSINESS QUESTION ---------------- */

.bq {
    display: inline-block;

    padding: 5px 11px;
    margin-bottom: 7px;

    border-radius: 999px;

    background: #dbeafe;
    color: #1d4ed8;

    font-size: 12px;
    font-weight: 800;
}


/* ---------------- INSIGHT ---------------- */

.insight-card {

    background:
        linear-gradient(
            135deg,
            #eff6ff,
            #eef2ff
        );

    border: 1px solid #dbeafe;

    border-radius: 16px;

    padding: 15px 18px;

    color: #1e3a8a;

    margin: 8px 0 16px 0;
}


/* ---------------- CHART ---------------- */

div[data-testid="stPlotlyChart"] {

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 19px;

    padding: 7px;

    box-shadow:
        0 5px 20px rgba(15, 23, 42, .05);
}


/* ---------------- TABS ---------------- */

button[data-baseweb="tab"] {
    font-size: 14px;
    font-weight: 700;
}


/* ---------------- DATAFRAME ---------------- */

div[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    overflow: hidden;
}


/* ---------------- DOWNLOAD ---------------- */

.stDownloadButton button {

    border-radius: 12px;

    border: 1px solid #bfdbfe;

    background: #eff6ff;

    color: #1d4ed8;

    font-weight: 700;
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

    return con.execute(
        sql,
        params
    ).fetchdf()


def style_fig(fig, height=410):

    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=35,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(
            color="#0f172a",
            size=13
        ),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_color="white"
        )
    )

    return fig


def compact_amount(value):

    value = float(value or 0)

    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f} B"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.2f} M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:,.2f} K"

    return f"{value:,.2f}"


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ● LIVE DATA FROM DUCKDB
    </div>

    <div class="hero-title">
        ✈ การวิเคราะห์ข้อมูลสายการบิน
    </div>

    <p class="hero-subtitle">
        Data Warehouse Dashboard • ยอดขายตั๋ว • เส้นทางบิน •
        เครื่องบิน • การดำเนินงานเที่ยวบิน
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# MASTER DATA FOR FILTERS
# =========================================================

date_row = con.execute("""
    SELECT
        MIN(full_date),
        MAX(full_date)
    FROM dim_date
""").fetchone()


min_date = pd.to_datetime(
    date_row[0]
).date()

max_date = pd.to_datetime(
    date_row[1]
).date()


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
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 ตัวกรองข้อมูล")

st.sidebar.caption(
    "เลือกเงื่อนไขเพื่อวิเคราะห์ข้อมูลแบบ Interactive"
)


date_selection = st.sidebar.date_input(
    "ช่วงวันที่",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if len(date_selection) == 2:

    start_date = date_selection[0]
    end_date = date_selection[1]

else:

    start_date = min_date
    end_date = max_date


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


st.sidebar.divider()

st.sidebar.caption(
    f"ข้อมูลตั้งแต่ {min_date.strftime('%d/%m/%Y')} "
    f"ถึง {max_date.strftime('%d/%m/%Y')}"
)


if (
    departure != "ทั้งหมด"
    and arrival != "ทั้งหมด"
    and departure == arrival
):

    st.sidebar.warning(
        "ต้นทางและปลายทางเป็นสนามบินเดียวกัน "
        "จึงอาจไม่พบข้อมูลเส้นทาง"
    )


# =========================================================
# BUILD SALES FILTER
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
# BUILD OPERATIONS FILTER
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
# BUILD SEAT FILTER
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
# KPI
# Q1 + Q2
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
        ON f.departure_airport_key
        = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key
        = arr.airport_key

    JOIN dim_fare_class fc
        ON f.fare_class_key
        = fc.fare_class_key

    JOIN dim_aircraft a
        ON f.aircraft_key
        = a.aircraft_key

    WHERE {sales_where}
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
        ON f.date_key
        = d.date_key

    JOIN dim_airport dep
        ON f.departure_airport_key
        = dep.airport_key

    JOIN dim_airport arr
        ON f.arrival_airport_key
        = arr.airport_key

    JOIN dim_aircraft a
        ON f.aircraft_key
        = a.aircraft_key

    WHERE {ops_where}
    """,
    ops_params
).fetchone()


k1, k2, k3, k4 = st.columns(4)


k1.metric(
    "💰 ยอดขายตั๋วรวม",
    compact_amount(
        sales_kpi[0]
    )
)


k2.metric(
    "🎫 Ticket Flight",
    f"{sales_kpi[1]:,.0f}"
)


k3.metric(
    "✈️ เที่ยวบินทั้งหมด",
    f"{ops_kpi[0]:,.0f}"
)


k4.metric(
    "⏱️ ดีเลย์ขาออกเฉลี่ย",
    f"{ops_kpi[1]:,.1f} นาที"
)


st.caption(
    "Q1–Q2 แสดงเป็น KPI และปรับตามตัวกรองแบบ Real-time"
)


st.write("")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 ภาพรวมยอดขาย",
    "🌍 สนามบินและเส้นทาง",
    "✈️ เครื่องบิน",
    "⏱️ การดำเนินงานเที่ยวบิน",
    "📊 วิเคราะห์หลายมิติ"
])


# =========================================================
# TAB 1
# Q3 Q4 Q5
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
        'วิเคราะห์รายได้ จำนวน Ticket Flight '
        'และแนวโน้มยอดขายตามช่วงเวลา'
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
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {sales_where}

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

        st.markdown(
            f"""
            <div class="insight-card">
            💡 <b>Insight:</b>
            ชั้นโดยสารที่สร้างยอดขายสูงที่สุดคือ
            <b>{top_fare['fare_class']}</b>
            ด้วยยอดขายประมาณ
            <b>{compact_amount(top_fare['total_sales'])}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


        c1, c2 = st.columns(2)


        with c1:

            st.markdown(
                '<span class="bq">'
                'Business Question Q3'
                '</span>',
                unsafe_allow_html=True
            )

            st.subheader(
                "ยอดขายตามชั้นโดยสาร"
            )

            fig = px.pie(
                fare_sales,
                values="total_sales",
                names="fare_class",
                hole=0.63,
                color_discrete_sequence=COLORS
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            style_fig(
                fig,
                420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with c2:

            st.markdown(
                '<span class="bq">'
                'Business Question Q4'
                '</span>',
                unsafe_allow_html=True
            )

            st.subheader(
                "จำนวน Ticket Flight ตามชั้นโดยสาร"
            )

            fare_count = fare_sales.sort_values(
                "ticket_flights",
                ascending=True
            )

            fig = px.bar(
                fare_count,
                x="ticket_flights",
                y="fare_class",
                orientation="h",
                color="ticket_flights",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="จำนวน Ticket Flight",
                yaxis_title=""
            )

            style_fig(
                fig,
                420
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

            SUM(f.amount)
                AS total_sales

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

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
            monthly_sales["year"]
            .astype(str)
            + "-"
            + monthly_sales["month"]
            .astype(str)
            .str.zfill(2)
        )


        st.markdown(
            '<span class="bq">'
            'Business Question Q5'
            '</span>',
            unsafe_allow_html=True
        )

        st.subheader(
            "แนวโน้มยอดขายตามช่วงเวลา"
        )


        fig = px.line(
            monthly_sales,
            x="period",
            y="total_sales",
            markers=True
        )

        fig.update_traces(
            line=dict(
                width=4
            ),
            marker=dict(
                size=9
            )
        )

        fig.update_layout(
            xaxis_title="ช่วงเวลา",
            yaxis_title="ยอดขาย"
        )

        style_fig(
            fig,
            440
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 2
# Q6 Q7 Q8 Q9 + DRILL DOWN
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
        'เปรียบเทียบสนามบินต้นทาง สนามบินปลายทาง '
        'และเส้นทางที่สำคัญ'
        '</div>',
        unsafe_allow_html=True
    )


    departure_df = query_df(
        f"""
        SELECT
            dep.airport_code,

            SUM(
                f.ticket_flight_count
            ) AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {sales_where}

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

            SUM(
                f.ticket_flight_count
            ) AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {sales_where}

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
            '<span class="bq">'
            'Business Question Q6'
            '</span>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สนามบินต้นทางยอดนิยม"
        )


        if not departure_df.empty:

            plot_df = departure_df.sort_values(
                "ticket_flights"
            )

            fig = px.bar(
                plot_df,
                x="ticket_flights",
                y="airport_code",
                orientation="h",
                color="ticket_flights",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_fig(
                fig,
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    with c2:

        st.markdown(
            '<span class="bq">'
            'Business Question Q7'
            '</span>',
            unsafe_allow_html=True
        )

        st.subheader(
            "สนามบินปลายทางยอดนิยม"
        )


        if not arrival_df.empty:

            plot_df = arrival_df.sort_values(
                "ticket_flights"
            )

            fig = px.bar(
                plot_df,
                x="ticket_flights",
                y="airport_code",
                orientation="h",
                color="ticket_flights",
                color_continuous_scale="Purples"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_fig(
                fig,
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    route_ticket_df = query_df(
        f"""
        SELECT
            dep.airport_code
            || ' → ' ||
            arr.airport_code
                AS route,

            SUM(
                f.ticket_flight_count
            ) AS ticket_flights

        FROM fact_ticket_sales f

        JOIN dim_date d
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {sales_where}

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
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {sales_where}

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
            '<span class="bq">'
            'Business Question Q8'
            '</span>',
            unsafe_allow_html=True
        )

        st.subheader(
            "เส้นทางที่มี Ticket Flight สูงที่สุด"
        )


        if not route_ticket_df.empty:

            plot_df = route_ticket_df.sort_values(
                "ticket_flights"
            )

            fig = px.bar(
                plot_df,
                x="ticket_flights",
                y="route",
                orientation="h",
                color="ticket_flights",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Ticket Flight",
                yaxis_title=""
            )

            style_fig(
                fig,
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    with c2:

        st.markdown(
            '<span class="bq">'
            'Business Question Q9'
            '</span>',
            unsafe_allow_html=True
        )

        st.subheader(
            "เส้นทางที่สร้างยอดขายสูงสุด"
        )


        if not route_sales_df.empty:

            plot_df = route_sales_df.sort_values(
                "total_sales"
            )

            fig = px.bar(
                plot_df,
                x="total_sales",
                y="route",
                orientation="h",
                color="total_sales",
                color_continuous_scale="Purples"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="ยอดขาย",
                yaxis_title=""
            )

            style_fig(
                fig,
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # -----------------------------------------------------
    # DRILL DOWN
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "🔎 Drill-down รายละเอียดเส้นทาง"
    )


    if not route_sales_df.empty:

        selected_route = st.selectbox(
            "เลือกเส้นทางเพื่อดูรายละเอียด",
            route_sales_df["route"].tolist()
        )


        selected_dep, selected_arr = [
            x.strip()
            for x
            in selected_route.split("→")
        ]


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

                SUM(
                    f.ticket_flight_count
                ) AS ticket_flights

            FROM fact_ticket_sales f

            JOIN dim_date d
                ON f.date_key
                = d.date_key

            JOIN dim_airport dep
                ON f.departure_airport_key
                = dep.airport_key

            JOIN dim_airport arr
                ON f.arrival_airport_key
                = arr.airport_key

            JOIN dim_fare_class fc
                ON f.fare_class_key
                = fc.fare_class_key

            JOIN dim_aircraft a
                ON f.aircraft_key
                = a.aircraft_key

            WHERE {drill_where}

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
                    color_discrete_sequence=COLORS
                )

                fig.update_layout(
                    showlegend=False,
                    xaxis_title="ชั้นโดยสาร",
                    yaxis_title="ยอดขาย"
                )

                style_fig(
                    fig,
                    360
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            with c2:

                st.dataframe(
                    route_detail,
                    use_container_width=True,
                    hide_index=True
                )


                st.download_button(
                    "⬇️ ดาวน์โหลดข้อมูล Route",
                    data=route_detail.to_csv(
                        index=False
                    ).encode("utf-8-sig"),
                    file_name=(
                        selected_dep
                        + "_"
                        + selected_arr
                        + "_detail.csv"
                    ),
                    mime="text/csv"
                )


# =========================================================
# TAB 3
# Q10 Q11 Q12
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
        'วิเคราะห์การใช้งานเครื่องบิน '
        'ความจุที่นั่ง และโครงสร้างชั้นโดยสาร'
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
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        WHERE {ops_where}

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
                / SUM(
                    SUM(f.seat_count)
                  ) OVER (
                    PARTITION BY a.model
                  ),
                2
            ) AS seat_percentage

        FROM fact_seat_inventory f

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        JOIN dim_fare_class fc
            ON f.fare_class_key
            = fc.fare_class_key

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
            '<span class="bq">'
            'Business Question Q10'
            '</span>',
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
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="จำนวนเที่ยวบิน",
                yaxis_title=""
            )

            style_fig(
                fig,
                420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
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
            '<span class="bq">'
            'Business Question Q11'
            '</span>',
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
                color_continuous_scale="Purples"
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="จำนวนที่นั่ง",
                yaxis_title=""
            )

            style_fig(
                fig,
                420
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    st.markdown(
        '<span class="bq">'
        'Business Question Q12'
        '</span>',
        unsafe_allow_html=True
    )

    st.subheader(
        "สัดส่วนที่นั่งตามชั้นโดยสาร"
    )

    st.caption(
        "หมายเหตุ: Seat Inventory เป็นข้อมูลโครงสร้างที่นั่ง "
        "จึงไม่เปลี่ยนตามช่วงวันที่"
    )


    if not seat_df.empty:

        fig = px.bar(
            seat_df,
            x="model",
            y="seat_percentage",
            color="fare_class",
            barmode="stack",
            color_discrete_sequence=COLORS,
            hover_data=[
                "seats"
            ]
        )

        fig.update_layout(
            xaxis_title="รุ่นเครื่องบิน",
            yaxis_title="สัดส่วนที่นั่ง (%)",
            legend_title="ชั้นโดยสาร"
        )

        style_fig(
            fig,
            470
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
        '<div class="section-title">'
        'การดำเนินงานเที่ยวบิน'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์สถานะเที่ยวบิน '
        'และความล่าช้าของสนามบินต้นทาง'
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
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

        JOIN dim_flight_status s
            ON f.status_key
            = s.status_key

        WHERE {ops_where}

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
            ON f.date_key
            = d.date_key

        JOIN dim_airport dep
            ON f.departure_airport_key
            = dep.airport_key

        JOIN dim_airport arr
            ON f.arrival_airport_key
            = arr.airport_key

        JOIN dim_aircraft a
            ON f.aircraft_key
            = a.aircraft_key

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
            '<span class="bq">'
            'Business Question Q13'
            '</span>',
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
                color_discrete_sequence=COLORS
            )

            fig.update_traces(
                textinfo="percent+label"
            )

            style_fig(
                fig,
                430
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    with c2:

        st.markdown(
            '<span class="bq">'
            'Business Question Q14'
            '</span>',
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
                color_continuous_scale="Reds",
                hover_data=[
                    "delayed_flights"
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="ดีเลย์เฉลี่ย (นาที)",
                yaxis_title=""
            )

            style_fig(
                fig,
                430
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
        '<div class="section-title">'
        'การวิเคราะห์ข้อมูลแบบหลายมิติ'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-desc">'
        'วิเคราะห์ Date × Route × Fare Class × Sales'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<span class="bq">'
        'Business Question Q15'
        '</span>',
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

                dep.airport_code
                    AS departure_airport,

                arr.airport_code
                    AS arrival_airport,

                fc.fare_class,

                SUM(f.amount)
                    AS total_sales

            FROM fact_ticket_sales f

            JOIN dim_date d
                ON f.date_key
                = d.date_key

            JOIN dim_airport dep
                ON f.departure_airport_key
                = dep.airport_key

            JOIN dim_airport arr
                ON f.arrival_airport_key
                = arr.airport_key

            JOIN dim_fare_class fc
                ON f.fare_class_key
                = fc.fare_class_key

            JOIN dim_aircraft a
                ON f.aircraft_key
                = a.aircraft_key

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


        fig = px.bar(
            monthly_top,
            x="period",
            y="total_sales",
            color="fare_class",
            color_discrete_sequence=COLORS,

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


        style_fig(
            fig,
            500
        )


        st.plotly_chart(
            fig,
            use_container_width=True
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
            "⬇️ ดาวน์โหลดผลการวิเคราะห์ Q15",
            data=display_df.to_csv(
                index=False
            ).encode(
                "utf-8-sig"
            ),
            file_name="Q15_multidimensional_analysis.csv",
            mime="text/csv"
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
        Airline Data Warehouse Project
        &nbsp;•&nbsp;
        dbt
        &nbsp;•&nbsp;
        DuckDB
        &nbsp;•&nbsp;
        Streamlit
        &nbsp;•&nbsp;
        Plotly
    </div>
    """,
    unsafe_allow_html=True
)


con.close()