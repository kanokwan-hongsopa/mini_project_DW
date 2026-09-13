import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="แดชบอร์ดวิเคราะห์ข้อมูลสายการบิน",
    page_icon="✈️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        color: #12355B;
    }

    .stMetric {
        background-color: white;
        border-radius: 16px;
        padding: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e6ecf5;
    }

    .section-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 18px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        border: 1px solid #e7edf6;
        margin-bottom: 1.2rem;
    }

    .small-note {
        color: #5c6b7a;
        font-size: 0.95rem;
    }

    .stSidebar {
        background-color: #eef3f9;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# CONNECT DATABASE
# =========================================================
DB_PATH = Path(__file__).resolve().parent / "dev.duckdb"
con = duckdb.connect(str(DB_PATH), read_only=True)

# =========================================================
# HEADER
# =========================================================
st.title("✈️ แดชบอร์ดวิเคราะห์ข้อมูลสายการบิน")
st.markdown(
    "<p class='small-note'>ใช้สำหรับวิเคราะห์ยอดขายตั๋ว การดำเนินงานเที่ยวบิน และข้อมูลเครื่องบินจาก Data Warehouse</p>",
    unsafe_allow_html=True
)

# =========================================================
# LOAD FILTER VALUES
# =========================================================
date_range = con.execute("""
    SELECT MIN(full_date) AS min_date, MAX(full_date) AS max_date
    FROM dim_date
""").fetchone()

min_date = pd.to_datetime(date_range[0]).date()
max_date = pd.to_datetime(date_range[1]).date()

airports_df = con.execute("""
    SELECT airport_code, airport_name
    FROM dim_airport
    ORDER BY airport_code
""").fetchdf()

fare_df = con.execute("""
    SELECT fare_class
    FROM dim_fare_class
    ORDER BY fare_class
""").fetchdf()

aircraft_df = con.execute("""
    SELECT DISTINCT model
    FROM dim_aircraft
    ORDER BY model
""").fetchdf()

airport_options = ["ทั้งหมด"] + airports_df["airport_code"].tolist()
fare_options = ["ทั้งหมด"] + fare_df["fare_class"].tolist()
aircraft_options = ["ทั้งหมด"] + aircraft_df["model"].tolist()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.header("🔎 ตัวกรองข้อมูล")

start_date = st.sidebar.date_input("วันที่เริ่มต้น", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("วันที่สิ้นสุด", value=max_date, min_value=min_date, max_value=max_date)

departure_airport = st.sidebar.selectbox("สนามบินต้นทาง", airport_options, index=0)
arrival_airport = st.sidebar.selectbox("สนามบินปลายทาง", airport_options, index=0)
fare_class = st.sidebar.selectbox("ชั้นโดยสาร", fare_options, index=0)
aircraft_model = st.sidebar.selectbox("รุ่นเครื่องบิน", aircraft_options, index=0)

if start_date > end_date:
    st.error("วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด")
    st.stop()

if departure_airport != "ทั้งหมด" and arrival_airport != "ทั้งหมด" and departure_airport == arrival_airport:
    st.warning("กรุณาเลือกสนามบินต้นทางและปลายทางต่างกัน หรือเลือก 'ทั้งหมด' อย่างน้อย 1 ช่อง")
    st.stop()

# =========================================================
# BUILD CONDITIONS
# =========================================================
sales_conditions = ["d.full_date BETWEEN ? AND ?"]
sales_params = [start_date, end_date]

if departure_airport != "ทั้งหมด":
    sales_conditions.append("dep.airport_code = ?")
    sales_params.append(departure_airport)

if arrival_airport != "ทั้งหมด":
    sales_conditions.append("arr.airport_code = ?")
    sales_params.append(arrival_airport)

if fare_class != "ทั้งหมด":
    sales_conditions.append("fc.fare_class = ?")
    sales_params.append(fare_class)

if aircraft_model != "ทั้งหมด":
    sales_conditions.append("a.model = ?")
    sales_params.append(aircraft_model)

sales_where = " AND ".join(sales_conditions)

ops_conditions = ["d.full_date BETWEEN ? AND ?"]
ops_params = [start_date, end_date]

if departure_airport != "ทั้งหมด":
    ops_conditions.append("dep.airport_code = ?")
    ops_params.append(departure_airport)

if arrival_airport != "ทั้งหมด":
    ops_conditions.append("arr.airport_code = ?")
    ops_params.append(arrival_airport)

if aircraft_model != "ทั้งหมด":
    ops_conditions.append("a.model = ?")
    ops_params.append(aircraft_model)

ops_where = " AND ".join(ops_conditions)

seat_conditions = []
seat_params = []

if fare_class != "ทั้งหมด":
    seat_conditions.append("fc.fare_class = ?")
    seat_params.append(fare_class)

if aircraft_model != "ทั้งหมด":
    seat_conditions.append("a.model = ?")
    seat_params.append(aircraft_model)

seat_where = ""
if seat_conditions:
    seat_where = "WHERE " + " AND ".join(seat_conditions)

# =========================================================
# KPI SECTION
# =========================================================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.subheader("📌 ภาพรวมข้อมูล")

sales_kpi = con.execute(f"""
    SELECT
        COALESCE(SUM(f.amount), 0) AS total_sales,
        COALESCE(SUM(f.ticket_flight_count), 0) AS total_ticket_flights
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
""", sales_params).fetchone()

ops_kpi = con.execute(f"""
    SELECT
        COALESCE(SUM(f.flight_count), 0) AS total_flights,
        COALESCE(AVG(CASE WHEN f.departure_delay_minutes > 0 THEN f.departure_delay_minutes END), 0) AS avg_delay
    FROM fact_flight_operations f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {ops_where}
""", ops_params).fetchone()

col1, col2, col3, col4 = st.columns(4)
col1.metric("ยอดขายตั๋วรวม", f"{sales_kpi[0]:,.2f}")
col2.metric("จำนวน Ticket Flight", f"{sales_kpi[1]:,.0f}")
col3.metric("จำนวนเที่ยวบินทั้งหมด", f"{ops_kpi[0]:,.0f}")
col4.metric("ดีเลย์ขาออกเฉลี่ย", f"{ops_kpi[1]:,.2f} นาที")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Q9 ROUTE SALES
# =========================================================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.header("การวิเคราะห์ยอดขายตั๋ว")
st.subheader("Q9: เส้นทางที่สร้างยอดขายตั๋วสูงที่สุด")

route_sales = con.execute(f"""
    SELECT
        dep.airport_code || ' → ' || arr.airport_code AS route,
        SUM(f.amount) AS total_ticket_sales
    FROM fact_ticket_sales f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {sales_where}
    GROUP BY route
    ORDER BY total_ticket_sales DESC
    LIMIT 10
""", sales_params).fetchdf()

if route_sales.empty:
    st.warning("ไม่พบข้อมูลยอดขายตามตัวกรองที่เลือก")
else:
    st.bar_chart(route_sales.set_index("route"))
    st.dataframe(route_sales, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# AIRCRAFT ANALYSIS
# =========================================================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.header("การวิเคราะห์เครื่องบิน")

st.subheader("Q10: รุ่นเครื่องบินที่ถูกใช้กับเที่ยวบินมากที่สุด")
aircraft_usage = con.execute(f"""
    SELECT
        a.model,
        SUM(f.flight_count) AS total_flights
    FROM fact_flight_operations f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {ops_where}
    GROUP BY a.model
    ORDER BY total_flights DESC
""", ops_params).fetchdf()

if aircraft_usage.empty:
    st.warning("ไม่พบข้อมูลการใช้งานเครื่องบิน")
else:
    st.bar_chart(aircraft_usage.set_index("model"))

st.subheader("Q11: จำนวนที่นั่งของเครื่องบินแต่ละรุ่น")
aircraft_seat_count = con.execute(f"""
    SELECT
        a.model,
        SUM(f.seat_count) AS total_seats
    FROM fact_seat_inventory f
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
    {seat_where}
    GROUP BY a.model
    ORDER BY total_seats DESC
""", seat_params).fetchdf()

if aircraft_seat_count.empty:
    st.warning("ไม่พบข้อมูลจำนวนที่นั่ง")
else:
    st.bar_chart(aircraft_seat_count.set_index("model"))

st.subheader("Q12: สัดส่วนที่นั่งแต่ละชั้นโดยสารของเครื่องบิน")
seat_share = con.execute(f"""
    WITH seat_summary AS (
        SELECT
            a.model,
            fc.fare_class,
            SUM(f.seat_count) AS seat_count
        FROM fact_seat_inventory f
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        {seat_where}
        GROUP BY a.model, fc.fare_class
    )
    SELECT *
    FROM seat_summary
    ORDER BY model, seat_count DESC
""", seat_params).fetchdf()

if seat_share.empty:
    st.warning("ไม่พบข้อมูลสัดส่วนที่นั่ง")
else:
    st.dataframe(seat_share, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FLIGHT OPERATIONS
# =========================================================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.header("การวิเคราะห์การดำเนินงานเที่ยวบิน")

st.subheader("Q13: จำนวนเที่ยวบินในแต่ละสถานะ")
flight_status = con.execute(f"""
    SELECT
        s.status_name,
        SUM(f.flight_count) AS total_flights
    FROM fact_flight_operations f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    JOIN dim_flight_status s ON f.status_key = s.status_key
    WHERE {ops_where}
    GROUP BY s.status_name
    ORDER BY total_flights DESC
""", ops_params).fetchdf()

if flight_status.empty:
    st.warning("ไม่พบข้อมูลสถานะเที่ยวบิน")
else:
    st.bar_chart(flight_status.set_index("status_name"))
    st.dataframe(flight_status, use_container_width=True, hide_index=True)

st.subheader("Q14: สนามบินต้นทางที่มีเที่ยวบินล่าช้าเฉลี่ยมากที่สุด")
delay_df = con.execute(f"""
    SELECT
        dep.airport_code,
        dep.airport_name,
        ROUND(AVG(f.departure_delay_minutes), 2) AS avg_departure_delay_minutes
    FROM fact_flight_operations f
    JOIN dim_date d ON f.date_key = d.date_key
    JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
    JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
    JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
    WHERE {ops_where}
      AND f.departure_delay_minutes > 0
    GROUP BY dep.airport_code, dep.airport_name
    ORDER BY avg_departure_delay_minutes DESC
    LIMIT 10
""", ops_params).fetchdf()

if delay_df.empty:
    st.warning("ไม่พบข้อมูลเที่ยวบินล่าช้า")
else:
    st.bar_chart(delay_df.set_index("airport_code")[["avg_departure_delay_minutes"]])
    st.dataframe(delay_df, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Q15 MULTI-DIMENSION
# =========================================================
st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.header("การวิเคราะห์ยอดขายแบบหลายมิติ")
st.subheader("Q15: เส้นทางและชั้นโดยสารที่สร้างยอดขายสูงที่สุดในแต่ละเดือน")

monthly_top = con.execute(f"""
    WITH sales_summary AS (
        SELECT
            d.year,
            d.month,
            d.month_name,
            dep.airport_code AS departure_airport,
            arr.airport_code AS arrival_airport,
            fc.fare_class,
            SUM(f.amount) AS total_ticket_sales
        FROM fact_ticket_sales f
        JOIN dim_date d ON f.date_key = d.date_key
        JOIN dim_airport dep ON f.departure_airport_key = dep.airport_key
        JOIN dim_airport arr ON f.arrival_airport_key = arr.airport_key
        JOIN dim_fare_class fc ON f.fare_class_key = fc.fare_class_key
        JOIN dim_aircraft a ON f.aircraft_key = a.aircraft_key
        WHERE {sales_where}
        GROUP BY d.year, d.month, d.month_name,
                 dep.airport_code, arr.airport_code, fc.fare_class
    ),
    ranked AS (
        SELECT *,
               DENSE_RANK() OVER (
                   PARTITION BY year, month
                   ORDER BY total_ticket_sales DESC
               ) AS sales_rank
        FROM sales_summary
    )
    SELECT
        year,
        month_name,
        departure_airport,
        arrival_airport,
        fare_class,
        total_ticket_sales
    FROM ranked
    WHERE sales_rank = 1
    ORDER BY year, month
""", sales_params).fetchdf()

if monthly_top.empty:
    st.warning("ไม่พบข้อมูลยอดขายรายเดือนตามตัวกรองที่เลือก")
else:
    st.dataframe(monthly_top, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.caption("โครงงาน Data Warehouse สายการบิน | Streamlit + DuckDB")

con.close()